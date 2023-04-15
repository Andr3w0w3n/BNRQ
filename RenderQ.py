import sys
import os
import nuke
from PyQt import QtWidgets, QtGui
from PyQt.QtWidgets import QApplication, QMainWindow
class MainWindow(QMainWindow):
    """This creates the primary window for the render queue


    
    """

    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())