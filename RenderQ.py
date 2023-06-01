import sys
import os
import subprocess

from PreferencesTab import PreferencesTab
from Settings import Settings
from MainWindowTab import MainWindowTab

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QHBoxLayout,
    QLabel, QLineEdit, QVBoxLayout, QGridLayout, QFileDialog,
    QMainWindow, QListWidget, QMessageBox, QTabWidget, QToolBar,
    QDialog
)
from PySide6.QtCore import(QSettings, Qt, QUrl, QEventLoop)



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
        self.settings = Settings()
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

        """
        self.dialog = QDialog(self)
        self.dialog.setWindowTitle("Preferences")             
        self.pref_widget = PreferencesTab(self.settings)
        layout = QVBoxLayout()
        layout.addWidget(self.pref_widget)
        self.dialog.setLayout(layout)
        self.dialog.setModal(True)
        self.dialog.setWindowFlags(self.dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.dialog.setWindowFlags(self.dialog.windowFlags() | Qt.WindowCloseButtonHint)      
        """
        

    def closeEvent(self, event):
        """This method ends the events, it does not save any settings

        Args:
            event: The event passed into the method
        """
        pyside_settings = QtCore.QSettings("Andrew Owen", "BNRQ")
        pyside_settings.clear()

        #self.settings.remove_appdata_contents()
        super().closeEvent(event)
        
    
    def open_readme(self):
        url = QUrl("https://github.com/Andr3w0w3n/BNRQ/blob/main/README.md#use")
        QtGui.QDesktopServices.openUrl(url)

        
    def open_pref_dialog(self):
        prefs = PreferencesTab(self.settings)
        prefs.finished.connect(prefs.close_prefs)
        prefs.dialog.exec()

        #self.dialog.finished.connect(self.not_saved_warning)

    """
    def not_saved_warning(self):
        if self.pref_widget.save_button.isEnabled():
            warning_box = QMessageBox()
            warning_box.setIcon(QMessageBox.Warning)
            warning_box.setWindowTitle("Warning")
            warning_box.setText("No settings were saved")
            warning_box.setStandardButtons(QMessageBox.Ok)
            warning_box.finished.connect(warning_box.accept)


    def handle_dialog_close(self):
        if self.pref_widget.save_button.isEnabled():
            reply = QMessageBox.question(self.dialog, "Unsaved Changes",
                                         "Are you sure you want to close without saving your changes?",
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.dialog.reject()
        else:
            self.dialog.reject()
    """
        
if __name__ == "__main__":
    """Program start. This creates an insance of the MainWindow and shows
        it to the user. 
    """
    app = QApplication(sys.argv)
    main_window = Application()
    #pdb.run('main_window.show()', globals(), locals())
    main_window.show()
    sys.exit(app.exec())