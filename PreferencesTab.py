import sys
import os

from functools import partial

from SeparateThread import SeparateThread
from Settings import Settings

from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import QThread, QCoreApplication
from PySide6.QtGui import QMovie
from PySide6.QtWidgets import (
    QWidget, QPushButton, QHBoxLayout, QLabel, QLineEdit, QVBoxLayout, QFileDialog,
    QMessageBox, QApplication, QDialog
)
from PySide6.QtCore import(QSettings, Qt, QUrl)

class PreferencesTab(QDialog):
    """
        The preferences tab for Nuke Render Queue.

        Attributes:
            settings: An instance of the `settings` class used to store the user's preferences.
            nuke_exe_edit: A QLineEdit widget used to display and edit the path to the Nuke executable.
            search_start_edit: A QLineEdit widget used to display and edit the starting folder for the file search.
            write_node_edit: A QLineEdit widget used to display and edit the name of the write node.
        
        Methods:
            update_nuke_path(): A method that updates the Nuke executable path based on the user's selection.
            update_file_start_path(): A method that updates the starting folder for the file search based on the user's selection.
    """

    def __init__(self, settings):
        super().__init__()

        # Store a reference to the settings object
        self.settings = settings

        #loading GIF
        self.loading_label = QLabel()
        self.loading_gif = QMovie("./Assets/FolderLoading.gif")
        self.loading_label.setMovie(self.loading_gif)
        self.loading_label.setFixedSize(250, 250)
        self.loading_label.setStyleSheet("background-color: transparent;")
        self.loading_label.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.loading_label.setScaledContents(True)
        self.loading_label.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.loading_label.setAlignment(QtCore.Qt.AlignCenter)

        # Create the widgets for the preferences tab
        nuke_exe_label = QLabel("Nuke Executable Path:")
        self.nuke_exe_edit = QLineEdit(self.settings.nuke_exe)
        nuke_exe_file_finder = QPushButton("File Explorer")
        nuke_exe_file_finder.clicked.connect(self.update_nuke_path)
        nuke_exe_default_search = QPushButton("Find Nuke")
        nuke_exe_default_search.clicked.connect(self.get_nuke_path)
        
        search_start_label = QLabel("File Search Start:")
        self.search_start_edit = QLineEdit(self.settings.folder_search_start)
        file_path_start_finder = QPushButton("File Explorer")
        file_path_start_finder.clicked.connect(self.update_file_start_path)
        
        write_node_label = QLabel("Write Node Name:")
        self.write_node_edit = QLineEdit(self.settings.write_node_name)
        
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_button_clicked)
        #self.save_button.clicked.connect(self.figure_bs_out)
        self.cancel_changes_button = QPushButton("Cancel")
        self.cancel_changes_button.clicked.connect(self.cancel_setting_changes)
        self.disable_save_buttons()

        #if the settings have changed
        self.write_node_edit.textChanged.connect(self.settings_changed)
        self.nuke_exe_edit.textChanged.connect(self.settings_changed)
        self.search_start_edit.textChanged.connect(self.settings_changed)

        # Add the widgets to layouts
        nuke_exe_layout = QHBoxLayout()
        nuke_exe_layout.addWidget(nuke_exe_label)
        nuke_exe_layout.addWidget(self.nuke_exe_edit)
        nuke_exe_layout.addWidget(nuke_exe_file_finder)
        nuke_exe_layout.addWidget(nuke_exe_default_search)
        search_start_layout = QHBoxLayout()
        search_start_layout.addWidget(search_start_label)
        search_start_layout.addWidget(self.search_start_edit)
        search_start_layout.addWidget(file_path_start_finder)
        write_node_layout = QHBoxLayout()
        write_node_layout.addWidget(write_node_label)
        write_node_layout.addWidget(self.write_node_edit)
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_changes_button)

        # Add the layouts to the preferences tab
        vbox = QVBoxLayout()
        vbox.addLayout(nuke_exe_layout)
        vbox.addLayout(search_start_layout)
        vbox.addLayout(write_node_layout)
        vbox.addLayout(button_layout)
        self.setLayout(vbox)

        self.dialog = QDialog(self)
        self.dialog.setWindowTitle("Preferences") 
        self.dialog.setLayout(vbox)
        self.dialog.setModal(True)
        self.dialog.setWindowFlags(self.dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.dialog.setWindowFlags(self.dialog.windowFlags() | Qt.WindowCloseButtonHint)  
    
    
    def update_nuke_path(self):
        """A visual way to find and update the nuke executable path
        """

        folder_dialog = QFileDialog()
        folder_dialog.setFileMode(QFileDialog.ExistingFile)
        folder_dialog.setFilter(QtCore.QDir.Executable)
        path, _ = folder_dialog.getOpenFileName(self, 
                                                "Select File", 
                                                self.search_start_edit.text(), 
                                                "Executables (*.exe)")
        
        if path:
            self.nuke_exe_edit.setText(path)
        

    def closeEvent(self, event):
        if self.pref_widget.save_button.isEnabled():
            reply = QMessageBox.question(self.dialog, "Unsaved Changes",
                                         "Are you sure you want to close without saving your changes?",
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


    def update_file_start_path(self):
        """A visual way to find and update the file finder start folder path
        """
        folder_dialog = QFileDialog()
        folder_dialog.setFileMode(QFileDialog.ExistingFile)
        folder_dialog.setFilter(QtCore.QDir.Executable)
        path = folder_dialog.getExistingDirectory(self, 
                                             "Select File", 
                                             self.settings.folder_search_start)
        if path:
            self.search_start_edit.setText(path)


    def save_button_clicked(self):
        """Saves the settings if the save button is clicked and then disables the save button.
        """
        self.settings.write_node_name = self.write_node_edit.text()
        self.settings.nuke_exe = self.nuke_exe_edit.text()
        self.settings.folder_search_start = self.search_start_edit.text()
        self.settings.save_settings()

        self.disable_save_buttons()


    def settings_changed(self):
        """Turns on the save button when a setting has been changed.
        """
        if not self.save_button.isEnabled():
            self.enable_save_buttons()


    def get_nuke_path(self):
        """Sets up a loading icon and then starts the task of finding the Nuke executable in 
            a separate thread.
        """
        
        self.loading_gif.start()
        self.loading_label.show()
        QCoreApplication.processEvents()

        #Thread creator
        self.threads = QThread(self)

        self.nuke_finder_worker = SeparateThread()
        self.nuke_finder_worker.moveToThread(self.threads)
        self.nuke_finder_worker.nuke_path_ready.connect(self.handle_nuke_path_search_result)
        self.nuke_finder_worker.nuke_path_ready.connect(self.loading_label.hide)
        self.threads.started.connect(self.nuke_finder_worker.get_latest_nuke_path)
        self.threads.start()


    def handle_nuke_path_search_result(self, nuke_path):
        """Handles the signal emited once the nuke path is found by the separate thread. Sets text to the nuke path

        Args:
            nuke_path (str): The nuke path emited by the signal. Either str or None
        """
        if nuke_path:
            self.nuke_exe_edit.setText(nuke_path)
        else:
            error_box = QMessageBox()
            error_box.setIcon(QMessageBox.Critical)
            error_box.setText("No Nuke path found!")
            error_box.exec_()
        self.threads.quit()
        QCoreApplication.processEvents()
       
        
    def cancel_setting_changes(self):
        self.confirmation_box = QMessageBox.question(self, 'Warning', 'Do you wish to discard all your changes?',
                                                     QMessageBox.Yes | QMessageBox.No,
                                                     QMessageBox.No)
        if self.confirmation_box == QMessageBox.Yes:
            self.search_start_edit.setText(self.settings.folder_search_start)
            self.nuke_exe_edit.setText(self.settings.nuke_exe)
            self.write_node_edit.setText(self.settings.write_node_name)
            self.disable_save_buttons()
            
            
    def enable_save_buttons(self):
        self.save_button.setEnabled(True)
        self.cancel_changes_button.setEnabled(True)
    
    
    def disable_save_buttons(self):
        self.save_button.setEnabled(False)
        self.cancel_changes_button.setEnabled(False) 
    

    def figure_bs_out(self):
        print("Nuke exe" + self.settings.nuke_exe)
        print(f"filepath: {self.settings.folder_search_start}")
        print(f"write node name: {self.settings.write_node_name}")
        