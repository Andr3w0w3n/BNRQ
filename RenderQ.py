import sys
import os
import subprocess

from PreferencesTab import preferences_tab
from Settings import settings
from MainWindowTab import main_window_tab

from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QHBoxLayout,
    QLabel, QLineEdit, QVBoxLayout, QGridLayout, QFileDialog,
    QMainWindow, QListWidget, QMessageBox, QTabWidget
)
from PySide2.QtCore import(QSettings)



class MainWindow(QMainWindow):
    """
        This creates the primary window for the render queue
    
        Attributes:
            settings (Settings): An instance of the `Settings` class that loads and stores application settings.

        Methods:
            __init__(): Initializes a `MainWindow` instance by setting window size, title, and layout. Also creates a
                    QTabWidget with two tabs, one for the main render queue window and one for the preferences window.
            closeEvent(event): Saves the application settings when the user closes the main window.
    """

    def __init__(self):
        super(MainWindow, self).__init__()

        #load settings
        self.settings = settings()
        self.settings.load_settings()
        
        #Window set
        self.resize(900, 450)
        self.setMaximumSize(1920, 1080)
        self.setMinimumSize(100, 50)
        #self.setWindowIcon(QIcon("ICON PATH GOES HERE"))
        self.setWindowTitle("Nuke Render Queue")
        self.setContentsMargins(20, 20, 10, 10)
        
        #elements
        central_widget = QWidget()
        tab = QTabWidget()
        pref_tab = preferences_tab(self.settings)
        mw_tab = main_window_tab(self.settings)
        tab.addTab(mw_tab, "Render Queue")
        tab.addTab(pref_tab, "Preferences")
        main_layout = QVBoxLayout()
        main_layout.addWidget(tab)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        


    def closeEvent(self, event):
        """This method saves the settings and then ends whatever event is passed into it

        Args:
            event: The event passed into the method
        """
        self.settings.save_settings()
        super().closeEvent(event)


if __name__ == "__main__":
    """Program start. This creates an insance of the MainWindow and shows
        it to the user. 
    """
    app = QApplication(sys.argv)
    main_window = MainWindow()
    #pdb.run('main_window.show()', globals(), locals())
    main_window.show()
    sys.exit(app.exec_())