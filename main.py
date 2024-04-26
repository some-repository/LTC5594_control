#!/usr/bin/env python3

import os.path as op
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6 import uic
from ctypes import BigEndianStructure, c_uint8
import usb.core

def res_path (fname):
    return op.join (op.dirname (__file__), fname)

MainFormUI, MainForm = uic.loadUiType (res_path ('main_form.ui'))

class LTC5594_control (BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('RW_address', c_uint8), # bits 0...6 - address, bit 7 - RW (1 for read mode, 0 for write mode)
        ('IM3QY', c_uint8),
        ('IM3QX', c_uint8),
        ('IM3IY', c_uint8),
        ('IM3IX', c_uint8),
        ('IM2QX', c_uint8),
        ('IM2IX', c_uint8),
        ('HD3QY', c_uint8),
        ('HD3QX', c_uint8),
        ('HD3IY', c_uint8),
        ('HD3IX', c_uint8),
        ('HD2QY', c_uint8),
        ('HD2QX', c_uint8),
        ('HD2IY', c_uint8),
        ('HD2IX', c_uint8),
        ('DCOI', c_uint8),
        ('DCOQ', c_uint8),
        ('IP3IC', c_uint8), # bits [2:0] - IP3IC, bits [7:3] - do not change
        ('GERR_IP3CC', c_uint8), # bits [7:2] - GERR, bits [1:0] - IP3CC
        ('LVCM_CF1', c_uint8), # bits [7:5] - LVCM, bits [4:0] - CF1
        ('BAND_LF1_CF2', c_uint8), # bit 7 - BAND, bits [6:5] - LF1, bits [4:0] - CF2
        ('PHA', c_uint8), # PHA [8:1]
        ('PHA_AMPG_AMPCC_AMPIC', c_uint8), # bit 7 - PHA [0], bits [6:4] - AMPG, bits [3:2] - AMPCC, bits [0:1] - AMPIC
        ('EDEM_EDC_EADJ_EAMP_SRST_SDO', c_uint8), # bit 7 - EDEM, 6 - EDC, 5 - EADJ, 4 - EAMP, 3 - SRST, 2 - SDO, [1:0] - do not change
        ('CHIPID', c_uint8), # bits [7:6] - CHIPID, bits [5:0] - do not change (LSB should always be set to 1)
    ]
    def __init__ (self):
        self.CHIPID = 1 # LSB should always be set to 
        
control_structure = LTC5594_control ()

class MainWindow (MainForm):
    def __init__ (self):
        super ().__init__ ()
        # Create UI instance
        self.ui = MainFormUI ()
        self.ui.setupUi (self)
        # Attach event handlers
        self.ui.write_button.clicked.connect (self.write_button_handler)

    def write_button_handler (self):
        if self.ui.EDEM.isChecked ():
            control_structure.EDEM_EDC_EADJ_EAMP_SRST_SDO |= 0b10000000
            self.ui.console_output.appendPlainText ('Demodulator enabled')
        else:
            control_structure.EDEM_EDC_EADJ_EAMP_SRST_SDO &= ~0b10000000
            self.ui.console_output.appendPlainText ('Demodulator disabled')
        #------------------------------------------------------------------------
        if self.ui.EDC.isChecked ():
            control_structure.EDEM_EDC_EADJ_EAMP_SRST_SDO |= 0b01000000
            #self.ui.console_output.appendPlainText ('DC offset adjust enabled')
        else:
            control_structure.EDEM_EDC_EADJ_EAMP_SRST_SDO &= ~0b01000000
            #self.ui.console_output.appendPlainText ('DC offset adjust disabled')
        #------------------------------------------------------------------------
        if self.ui.EADJ.isChecked ():
            control_structure.EDEM_EDC_EADJ_EAMP_SRST_SDO |= 0b00100000
            #self.ui.console_output.appendPlainText ('Nonlinearity adjust enabled')
        else:
            control_structure.EDEM_EDC_EADJ_EAMP_SRST_SDO &= ~0b00100000
            #self.ui.console_output.appendPlainText ('Nonlinearity adjust disabled')
        #------------------------------------------------------------------------
        if self.ui.EAMP.isChecked ():
            control_structure.EDEM_EDC_EADJ_EAMP_SRST_SDO |= 0b00010000
            #self.ui.console_output.appendPlainText ('IF amplifiers enabled')
        else:
            control_structure.EDEM_EDC_EADJ_EAMP_SRST_SDO &= ~0b00010000
            #self.ui.console_output.appendPlainText ('IF amplifiers disabled')
        #------------------------------------------------------------------------
        if self.ui.SRST.isChecked ():
            control_structure.EDEM_EDC_EADJ_EAMP_SRST_SDO |= 0b00001000
            #self.ui.console_output.appendPlainText ('SRST bit set')
        else:
            control_structure.EDEM_EDC_EADJ_EAMP_SRST_SDO &= ~0b00001000
            #self.ui.console_output.appendPlainText ('SRST bit reset')
        #------------------------------------------------------------------------
        if self.ui.SDO_MODE.isChecked ():
            control_structure.EDEM_EDC_EADJ_EAMP_SRST_SDO |= 0b00000100
            #self.ui.console_output.appendPlainText ('SDO enabled')
        else:
            control_structure.EDEM_EDC_EADJ_EAMP_SRST_SDO &= ~0b00000100
            #self.ui.console_output.appendPlainText ('SDO disabled')
        #------------------------------------------------------------------------
        #print (control_structure.EDEM_EDC_EADJ_EAMP_SRST_SDO)
        #------------------------------------------------------------------------
        #------------------------------------------------------------------------
        control_structure.PHA_AMPG_AMPCC_AMPIC &= ~(0b111 << 4)
        control_structure.PHA_AMPG_AMPCC_AMPIC |= ((self.ui.IF_gain.value () - 8) << 4)
        #------------------------------------------------------------------------
        #print (control_structure.PHA_AMPG_AMPCC_AMPIC)
        #------------------------------------------------------------------------
        #------------------------------------------------------------------------
        control_array = bytes (control_structure)
        #------------------------------------------------------------------------
        #------------------------------------------------------------------------
        dev = usb.core.find (idVendor = 0x1209, idProduct = 0x0001)
        dev.write (1, control_array)
        read_buf = bytes (dev.read (0x81, 64))
        print (read_buf.hex (" ", 1))
        dev.finalize ()

def main ():
    app = QApplication (sys.argv)
    w = MainWindow ()
    w.show ()
    sys.exit (app.exec ())

if __name__ == '__main__':
    main ()
