import sys
from PyQt5.QtWidgets import (QApplication, QWidget)

class MainWindow (QWidget):
    pass

def main ():
    app = QApplication (sys.argv)
    w = MainWindow ()
    w.show ()
    sys.exit (app.exec_ ())

if __name__ == '__main__':
    main ()
