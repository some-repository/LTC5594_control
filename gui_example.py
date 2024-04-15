import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QPushButton)

class MainWindow (QWidget):
    def __init__ (self):
        # Call original Qwidget constructor
        super ().__init__ ()
        self.setWindowTitle ("GUI example") # Set custom window title
        grid = QGridLayout ()
        self.setLayout (grid) # Create grid for widgets placing
        button_1 = QPushButton ("Button name") # Create button and put it on grid
        grid.addWidget (button_1, 0, 0)
        button_1.clicked.connect (self.__button_1_handler) # Connect handler to "clicked" event
    def __button_1_handler (self): # Create handler for "clicked" event
        print ("Button pushed")

def main ():
    app = QApplication (sys.argv)
    w = MainWindow ()
    w.show ()
    sys.exit (app.exec_ ())

if __name__ == '__main__':
    main ()
