import os
import sys

from Settings import Settings
from SplashScreen import SplashScreen

from PySide6 import QtGui, QtWidgets, QtCore
from PySide6.QtWidgets import QWidget, QSplashScreen, QVBoxLayout, QFrame, QLabel
from PySide6.QtGui import QGuiApplication, QPixmap, QColor, QFont
from PySide6.QtCore import Qt, QThread, Signal


class LaunchSplashScreen(QSplashScreen):
    """
    A class that represents a launch splash screen.

    Attributes:
        finished_launching (Signal): A signal emitted when the launch process is finished.
        splash_screen (SplashScreen): The SplashScreen object.

    Methods:
        __init__(): Initializes the LaunchSplashScreen object.
        launch(): Launches the splash screen and starts loading settings in a separate thread.
        continue_construction(): Continues the construction process after the settings are done loading.

    """

    finished_launching = Signal()

    def __init__(self):
        """
        Initialization method.

        It initializes the LaunchSplashScreen object and loads the SplashScreen object.

        """
        super().__init__()

        # Load logo splash screen
        self.splash_screen = SplashScreen()

    def launch(self):
        """
        Launches the splash screen and starts loading settings in a separate thread.

        This method shows the splash screen, initializes a separate thread, and connects the necessary signals and slots
        between the thread and the splash screen. Then, it starts the thread to load the settings.

        """
        self.splash_screen.show()
        QtWidgets.QApplication.processEvents()

        # Load settings in a separate thread
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
        Continues the construction process after the settings are done loading.

        This method is called when the loading of settings is finished. It stops the thread, hides the splash screen,
        and emits the finished_launching signal to indicate that the launch process is finished.

        """
        self.threads.quit()
        # Hide logo once settings are done loading
        self.splash_screen.hide()
        QtWidgets.QApplication.processEvents()
        self.finished_launching.emit()
