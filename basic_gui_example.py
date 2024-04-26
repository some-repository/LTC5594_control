#from PySide6.QtWidgets import QApplication
import os.path as op
import sys
from PySide6.QtWidgets import QApplication
from PySide6 import uic

def res_path (fname):
    return op.join (op.dirname (__file__), fname)

MainFormUI, MainForm = uic.loadUiType (res_path ('main_form.ui'))

class MainWindow (MainForm):
    def __init__ (self):
        super ().__init__ ()
        # Create UI instance
        self.ui = MainFormUI ()
        self.ui.setupUi (self)
        # Attach event handlers
        self.ui.pushButton.clicked.connect (self.__button_handler)

    def __button_handler (self):
        print (self.ui.lineEdit.text ())
        self.ui.lineEdit.setText ('')

def main ():
    app = QApplication (sys.argv)
    w = MainWindow ()
    w.show ()
    sys.exit (app.exec_ ())

if __name__ == '__main__':
    main ()
