import sys
import os
import subprocess
import time
import threading

from PreferencesTab import PreferencesTab
from Settings import Settings
from MainWindowTab import MainWindowTab
from SeparateThread import SeparateThread
from SplashScreen import SplashScreen


from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QHBoxLayout,
    QLabel, QLineEdit, QVBoxLayout, QGridLayout, QFileDialog,
    QMainWindow, QListWidget, QMessageBox, QTabWidget, QToolBar,
    QDialog, QSplashScreen
)
from PySide6.QtCore import(
    QSettings, Qt, QUrl, QEventLoop, QThread, 
    QCoreApplication, QEventLoop
)

class Application(QMainWindow):
    """
        The main application class that sets up the application window and handles the loading of settings.

        This class inherits from QMainWindow and constructs the main window with tabs. It also displays a splash screen
        during the loading process and handles the completion of settings loading.

        Attributes:
            splash_screen (SplashScreen): The splash screen widget.
            threads (QThread): The thread for loading settings.
            launch_worker (Settings): The settings loading worker object.
            settings (Settings): The settings object.

        Methods:
            __init__(): Initializes the Application object and sets up the application window.
            continue_construction(): Continues the construction of the application after settings loading is finished.
            closeEvent(event): Overrides the closeEvent method to handle the event of the application window being closed.
            open_readme(): Opens the README file in the default browser under the use section.
            open_pref_dialog(): Opens the preferences dialog.
    """

    def __init__(self):
        """
        This method sets up the application window, loads settings in a separate thread,
        and constructs the main window with tabs.

        The splash screen is displayed during the loading process and is automatically closed
        when the settings are loaded. It has a slight pause (sleep) so the user can see which nuke version was loaded

        """
        
        super(Application, self).__init__()

        #load logo splashscreen
        self.splash_screen = SplashScreen()
        self.splash_screen.setWindowModality(Qt.ApplicationModal)
        #self.splash_screen.setDisabled(True)
        self.splash_screen.show()
        self.hide()
        QtWidgets.QApplication.processEvents() 

        #load settings in separate thread
        self.threads = QThread(self)

        self.launch_worker = Settings()
        self.launch_worker.moveToThread(self.threads)
        self.launch_worker.root_being_explored.connect(self.splash_screen.set_root_description_text)
        self.launch_worker.latest_nuke.connect(self.splash_screen.set_nuke_version_description)
        self.launch_worker.finished_launch.connect(self.continue_construction)
        self.threads.started.connect(self.launch_worker.launch)
        self.threads.start()

    
    def continue_construction(self):
        """
        Continues the construction of the application after the settings loading is finished.

        This method performs various tasks to finalize the construction of the application window and user interface.
        It hides the splash screen, sets window properties such as size and title, constructs the main window with tabs
        and adds toolbar buttons for Help and Preferences.
        """
        self.splash_screen.deal_with_end()
        QtWidgets.QApplication.processEvents() 
        time.sleep(1.5)
        self.show()
        self.threads.quit()
        self.settings = Settings()
        self.settings.load_settings()
        
        #hide logo once settings are done loading
        self.splash_screen.hide()
        QtWidgets.QApplication.processEvents() 

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


    def closeEvent(self, event):
        """This method overrides the closeEvent method to handle the event of the application window being closed.
        It clears internal settings and performs slight clean-up before closing the application.

        Args:
            event: The event passed into the method.
        """
        user = self.settings.get_user()
        pyside_settings = QtCore.QSettings(user, "BNRQ")
        pyside_settings.clear()
        self.settings.clear()

        #self.settings.remove_appdata_contents()
        super().closeEvent(event)
        
    
    def open_readme(self):
        """
        Open the README file under the use section, in the default browser.
        """
        url = QUrl("https://github.com/Andr3w0w3n/BNRQ/blob/main/README.md#use")
        QtGui.QDesktopServices.openUrl(url)

        
    def open_pref_dialog(self):
        """
        Open up the preferences dialog.
        """
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