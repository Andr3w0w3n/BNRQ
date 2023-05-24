import sys
import os
import subprocess

from PreferencesTab import PreferencesTab
from Settings import Settings
from MainWindowTab import MainWindowTab

from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QHBoxLayout,
    QLabel, QLineEdit, QVBoxLayout, QGridLayout, QFileDialog,
    QMainWindow, QListWidget, QMessageBox, QTabWidget, QToolBar,
    QDialog
)
from PySide2.QtCore import(QSettings, Qt, QUrl)



class Application(QMainWindow):
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
        super(Application, self).__init__()

        #load settings
        self.settings = Settings(False)
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
        tabs = QTabWidget()
        #pref_tab = PreferencesTab(self.settings)
        mw_tab = MainWindowTab(self.settings)
        tabs.addTab(mw_tab, "Render Queue")
        #tabs.addTab(pref_tab, "Preferences")
        main_layout = QVBoxLayout()
        main_layout.addWidget(tabs)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        help_button = QPushButton("Help", self)
        help_button.clicked.connect(self.open_readme)
        preferences_button = QPushButton("Preferences", self)
        preferences_button.clicked.connect(self.open_pref_dialog)
        
        toolbar = QToolBar(self)
        toolbar.addWidget(preferences_button)
        toolbar.addWidget(help_button)
        toolbar.setMovable(False)
        self.addToolBar(Qt.TopToolBarArea, toolbar)
        


    def close_event(self, event):
        """This method saves the settings and then ends whatever event is passed into it

        Args:
            event: The event passed into the method
        """
        self.settings.save_settings()
        super().close_event(event)
        
    
    def open_readme(self):
        url = QUrl("https://github.com/Andr3w0w3n/BNRQ/blob/main/README.md")
        QtGui.QDesktopServices.openUrl(url)
        
        
    def open_pref_dialog(self):     
        dialog = QDialog(self)
        dialog.setWindowTitle("Preferences")
        if self.settings is None:
            print("self.settings = None")
        
        
        pref_widget = PreferencesTab(self.settings)
        layout = QVBoxLayout()
        layout.addWidget(pref_widget)
        dialog.setLayout(layout)
        dialog.setModal(True)
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        dialog.show()
        
        
        
if __name__ == "__main__":
    """Program start. This creates an insance of the MainWindow and shows
        it to the user. 
    """
    app = QApplication(sys.argv)
    main_window = Application()
    #pdb.run('main_window.show()', globals(), locals())
    main_window.show()
    sys.exit(app.exec_())