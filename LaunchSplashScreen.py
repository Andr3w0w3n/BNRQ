import os
import sys

from Settings import Settings
from SplashScreen import SplashScreen

from PySide6 import QtGui, QtWidgets, QtCore
from PySide6.QtWidgets import QWidget, QSplashScreen, QVBoxLayout, QFrame, QLabel
from PySide6.QtGui import QGuiApplication, QPixmap, QColor, QFont
from PySide6.QtCore import Qt, QThread, Signal


class LaunchSplashScreen(QSplashScreen):
    finished_launching = Signal()

    def __init__(self):
        super().__init__()

        #load logo splashscreen
        self.splash_screen = SplashScreen()
        
        
    def launch(self):
        self.splash_screen.show()
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
        self.threads.quit()
        #hide logo once settings are done loading
        self.splash_screen.hide()
        QtWidgets.QApplication.processEvents()
        self.finished_launching.emit()
