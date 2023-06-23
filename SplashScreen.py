import os
import sys

from PySide6 import QtGui, QtWidgets, QtCore
from PySide6.QtWidgets import QWidget, QSplashScreen, QVBoxLayout, QFrame, QLabel, QApplication
from PySide6.QtGui import QGuiApplication, QPixmap, QColor, QFont
from PySide6.QtCore import Qt


class SplashScreen(QSplashScreen):
    """
        A splash screen widget for displaying logo and loading information.

        Attributes:
            root_path (str): The root path for the search.
            latested_found_nuke_version (str): The latest found Nuke version.
            logo_filepath (str): The file path for the logo image.

        Methods:
            __init__(): Initializes the SplashScreen object.
            set_root_description_text(root_dir_text): Sets the description text to the current folder being searched.
            set_nuke_version_description(nuke_v_text): Sets text to indicate that Nuke has been found and displays its version.
            deal_with_end(): Performs any necessary tasks at the end of the splash screen.
            mousePressEvent(event): Handles the mouse press event on the splash screen.
    """


    def __init__(self):
        """
        Initializes the splash screen.

        It sets up the window size, position, and appearance. Loads the logo image, sets up the layout, and initializes
        various labels. Finally, it sets the layout for the splash screen.
        """
        super().__init__()
    
        #screen size
        primary_screen_resolution = QGuiApplication.screens()[0].size()

        self.root_path = "None"
        self.latested_found_nuke_version = "None"


        self.logo_filepath = None
        try:
            base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            self.logo_filepath = os.path.join(base_path, "Logo.png")
            if not os.path.exists(self.logo_filepath):
                raise FileNotFoundError
        except FileNotFoundError:           
            self.logo_filepath = "./Assets/Logo/Logo.png"
            
        if not os.path.exists(self.logo_filepath):
            print("No logo image filepath exists", self.logo_filepath)

        self.setFixedSize(primary_screen_resolution.width()/2, 
                          primary_screen_resolution.height()/2)

        primary_screen_resolution = QApplication.primaryScreen().size()
        screen_center = QApplication.primaryScreen().geometry().center()
        
        # Set the size and position of the splash screen
        splash_width = primary_screen_resolution.width() / 2
        splash_height = primary_screen_resolution.height() / 2
        self.setGeometry(
            screen_center.x() - splash_width / 2,
            screen_center.y() - splash_height / 2,
            splash_width,
            splash_height,
        )

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        #self.setAttribute(Qt.WA_TranslucentBackground)
        
        
        self.splash_layout = QVBoxLayout()
        self.frame = QFrame()
        #self.splash_layout.addWidget(self.frame)
        self.frame.setStyleSheet("background-color: #fefefe")
        self.splash_layout.setContentsMargins(0, 10, 0, 0)
        self.frame.setFrameStyle(QFrame.NoFrame)

        self.logo_image = QPixmap(self.logo_filepath)
        self.logo_label = QLabel(self.frame)
        self.logo_label.setAlignment(Qt.AlignCenter)
        #self.logo_label.setPixmap(self.logo_image)

        
        self.version = QLabel(self.frame)
        self.details = QLabel(self.frame)
        self.nuke_v_found = QLabel(self.frame)

        self.version_font = QFont()
        self.version_font.setPointSize(16)
        self.detail_font = QFont()
        self.detail_font.setPointSize(10)
        self.nuke_v_font = QFont()
        self.nuke_v_font.setPointSize(12)

        self.version.setText("BNRQ_v2.0")
        self.version.setFont(self.version_font)
        self.version.setAlignment(Qt.AlignCenter)
        self.details.setText("Looking through\nC:\\Program Files\\ for nuke")
        self.details.setFont(self.detail_font)
        self.details.setAlignment(Qt.AlignCenter)
        self.nuke_v_found.setText("No nuke found")
        self.nuke_v_found.setFont(self.nuke_v_font)
        self.nuke_v_found.setAlignment(Qt.AlignCenter)

        self.splash_layout.addWidget(self.logo_label, 0)
        self.splash_layout.addWidget(self.version, 0)
        self.splash_layout.addWidget(self.nuke_v_found, 0)
        self.splash_layout.addWidget(self.details, 0)
        
        self.logo_label.setPixmap(self.logo_image.scaledToWidth(self.width() * 0.8))
        
        self.setLayout(self.splash_layout)



    def set_root_description_text(self, root_dir_text):
        """
            Sets the description text to the current folder being searched.
        """
        self.details.setText(f"Looking through\n{root_dir_text}")
        QtWidgets.QApplication.processEvents()

    
    def set_nuke_version_description(self, nuke_v_text):
        """
            Set text to say that nuke has been found and what version
        """
        self.nuke_v_found.setText(f"Using Nuke version {nuke_v_text}")
        QtWidgets.QApplication.processEvents()

    
    def deal_with_end(self):
        """
            Function to do any tasks at the end of the splash screen
        """
        self.details.hide()
    

    def mousePressEvent(self, event):
        """
            Removes the ability for the user to click so nothing breaks
        """
        # disable default "click-to-dismiss" behaviour
        pass
