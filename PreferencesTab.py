import sys
import os
from PySide2 import QtWidgets, QtCore

from PySide2.QtWidgets import (
    QWidget, QPushButton, QHBoxLayout, QLabel, QLineEdit, QVBoxLayout, QFileDialog
)


class preferences_tab(QWidget):
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

        # Create the widgets for the preferences tab
        nuke_exe_label = QLabel("Nuke Executable Path:")
        self.nuke_exe_edit = QLineEdit(self.settings.nuke_exe)
        nuke_exe_file_finder = QPushButton("File Explorer")
        nuke_exe_file_finder.clicked.connect(self.update_nuke_path)
        search_start_label = QLabel("File Search Start:")
        self.search_start_edit = QLineEdit(self.settings.folder_search_start)
        file_path_start_finder = QPushButton("File Explorer")
        file_path_start_finder.clicked.connect(self.update_file_start_path)
        write_node_label = QLabel("Write Node Name:")
        self.write_node_edit = QLineEdit(self.settings.write_node_name)
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.settings.save_settings)
        

        # Add the widgets to layouts
        nuke_exe_layout = QHBoxLayout()
        nuke_exe_layout.addWidget(nuke_exe_label)
        nuke_exe_layout.addWidget(self.nuke_exe_edit)
        nuke_exe_layout.addWidget(nuke_exe_file_finder)
        search_start_layout = QHBoxLayout()
        search_start_layout.addWidget(search_start_label)
        search_start_layout.addWidget(self.search_start_edit)
        search_start_layout.addWidget(file_path_start_finder)
        write_node_layout = QHBoxLayout()
        write_node_layout.addWidget(write_node_label)
        write_node_layout.addWidget(self.write_node_edit)
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(save_button)

        # Add the layouts to the preferences tab
        vbox = QVBoxLayout()
        vbox.addLayout(nuke_exe_layout)
        vbox.addLayout(search_start_layout)
        vbox.addLayout(write_node_layout)
        vbox.addLayout(button_layout)
        self.setLayout(vbox)
    
    def update_nuke_path(self):
        """A visual way to find and update the nuke executable path
        """
        folder_dialog = QFileDialog()
        folder_dialog.setFileMode(QFileDialog.ExistingFile)
        folder_dialog.setFilter(QtCore.QDir.Executable)
        tempPath = folder_dialog.getOpenFileName(self, 
                                             "Select File", 
                                             self.settings.folder_search_start, 
                                             "Executables (*.exe) ;; All Files(*)")[0]
        if tempPath:
            self.settings.nuke_exe = tempPath
        self.nuke_exe_edit.setText(self.settings.nuke_exe)

    def update_file_start_path(self):
        """A visual way to find and update the file finder start folder path
        """
        folder_dialog = QFileDialog()
        folder_dialog.setFileMode(QFileDialog.ExistingFile)
        folder_dialog.setFilter(QtCore.QDir.Executable)
        tempPath = folder_dialog.getExistingDirectory(self, 
                                             "Select File", 
                                             self.settings.folder_search_start)
        if tempPath:
            self.settings.folder_search_start = tempPath
        self.search_start_edit.setText(self.settings.folder_search_start)