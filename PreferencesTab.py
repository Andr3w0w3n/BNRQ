import sys
import os

from functools import partial

from SeparateThread import SeparateThread
from Settings import Settings

from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import QMovie, QColor, QIcon, QPalette
from PySide6.QtWidgets import (
    QWidget, QPushButton, QHBoxLayout, QLabel, QLineEdit, QVBoxLayout, QFileDialog,
    QMessageBox, QApplication, QDialog, QCheckBox
)
from PySide6.QtCore import(QSettings, Qt, QUrl, QThread, QCoreApplication)


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
            close_prefs(event): UNUSED. A method that prompts the user if they would really like to close with unsaved changes
            update_file_start_path(): A method that updates the starting folder for the file search based on the user's selection.
            save_button_clicked(): Actions taken once the user clicks the save button
            settings_changed(): enables the save and cancel buttons if not already done so
            get_nuke_path(): Runs a separate thread to get the nuke path and apply it to the settings
            handle_nuke_path_search_result(nuke_path): Applies the result of the nuke search to the settings
            cancel_setting_chagnes(): Called when the user clicks the save button
            enable_save_Buttons(): Enables the save and cancel buttons as well as displays the warning text
            disable_save_buttons(): Disables the save and cancel buttons as well as hides the warning text
            show_warning_label(on): shows warning text, on is defaulted to False
            prompt_user_save_file_del(): Confirms that the user would like to delete the save file
            prompt_user_temp_file_del(): UNUSED. Confirms that the user would like to delete the temporary files and folders
            enable_del_button(): Re-enables the delete button if settings were to be saved again
    """

    def __init__(self, settings):
        """
            Initialization method.

            It initializes the Settings object and sets up the user interface for the preferences tab.
            The method creates various widgets, connects signals and slots, and sets the layout for the preferences tab.

            Args:
                settings (Settings): The settings object containing the initial settings values.
        """
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
        
        self.loading_dialog = QDialog(None, Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.loading_label = QLabel("Loading...", self.loading_dialog)
        #self.loading_dialog.setStyleSheet("background-color: transparent;")
        self.loading_dialog.setAutoFillBackground(True)
        self.loading_dialog.setBackgroundRole(QPalette.Base)
        self.loading_dialog.setPalette(QPalette(QColor(256, 256, 256, 0)))
        self.loading_label.setAlignment(Qt.AlignCenter)
        color = "black"
        self.loading_label.setStyleSheet("color: {};".format(color))
        
        
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

        #have to use isinstance as sometimes the settings return as a string from the json
        self.file_name_checkbox = QCheckBox("Full Path Filenames")
        self.file_name_checkbox.setChecked(
            True if (isinstance(self.settings.full_filepath_name, str) and self.settings.full_filepath_name == "true") 
                or 
                self.settings.full_filepath_name == True 
            else False
        ) 
        #self.file_name_checkbox.setChecked(self.settings.full_filepath_name.lower())

        self.render_nuke_open_checkbox = QCheckBox("Render without closing Nuke (Beta)")
        self.render_nuke_open_checkbox.setChecked(
            True if (isinstance(self.settings.render_nuke_open, str) and self.settings.render_nuke_open == "true") 
                or 
                self.settings.render_nuke_open == True 
            else False
        )
        
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_button_clicked)
        #self.save_button.clicked.connect(self.figure_bs_out)
        self.cancel_changes_button = QPushButton("Cancel")
        self.cancel_changes_button.clicked.connect(self.cancel_setting_changes)
        self.del_json_file_button = QPushButton("Delete Save File")
        self.del_json_file_button.clicked.connect(self.prompt_user_save_file_del)
        self.del_json_file_button.setStyleSheet("background-color: red;")
        
        self.warning_label = QLabel("")
        self.warning_label.setStyleSheet("color: red; font-weight: bold;")
        
        self.disable_save_buttons()

        #if the settings have changed
        self.write_node_edit.textChanged.connect(self.settings_changed)
        self.nuke_exe_edit.textChanged.connect(self.settings_changed)
        self.search_start_edit.textChanged.connect(self.settings_changed)
        self.file_name_checkbox.stateChanged.connect(self.settings_changed)
        self.render_nuke_open_checkbox.stateChanged.connect(self.settings_changed)

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
        button_layout.addWidget(self.warning_label)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_changes_button)
        
        list_name_layout = QVBoxLayout
        #list_name_layout.addWidget(self.file_name_checkbox)
        
        danger_zone_text = QLabel("DANGER ZONE")
        danger_zone_text.setStyleSheet("color: red; font-weight: bold;")
        danger_zone_text.setAlignment(Qt.AlignHCenter)
        danger_zone_layout = QVBoxLayout()
        danger_zone_layout.addWidget(self.del_json_file_button)
        danger_zone_layout.setAlignment(Qt.AlignHCenter)

        # Add the layouts to the preferences tab
        vbox = QVBoxLayout()
        vbox.addLayout(nuke_exe_layout)
        vbox.addLayout(search_start_layout)
        vbox.addLayout(write_node_layout)
        vbox.addWidget(self.file_name_checkbox)
        vbox.addWidget(self.render_nuke_open_checkbox)
        vbox.addLayout(button_layout)
        vbox.addWidget(danger_zone_text)
        vbox.addLayout(danger_zone_layout)
        vbox.addStretch(0)
        self.setLayout(vbox)

        self.dialog = QDialog(self)
        self.dialog.setWindowTitle("Preferences") 
        self.dialog.setLayout(vbox)
        self.dialog.setModal(True)
        self.dialog.setWindowFlags(self.dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.dialog.setWindowFlags(self.dialog.windowFlags() | Qt.WindowCloseButtonHint)
        self.dialog.setFixedSize(750, 300)

        self.settings.json_created.connect(self.enable_del_button)
    
    
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
        

    def close_prefs(self, event):
        """
            UNUSED. Meant to stop the user if the user attempts to exit the preferences panel without saving.
            This is not implemented yet.
        """
        if self.save_button.isEnabled():
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
        self.settings.full_filepath_name = self.file_name_checkbox.isChecked()
        self.settings.render_nuke_open = self.render_nuke_open_checkbox.isChecked()
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
        self.loading_label.raise_()
        self.loading_dialog.show()
        
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
            error_box.setIcon(QMessageBox.critical)
            error_box.setText("No Nuke path found!")
            error_box.exec()
            self.nuke_exe_edit.setText("")
        self.threads.quit()
        self.loading_dialog.hide()
        self.loading_label.hide()
        QCoreApplication.processEvents()
       
        
    def cancel_setting_changes(self):
        """
            Prompts user to make sure they would like to discard all of their changes. If so, all changes are removed and values 
            of the text boxes and buttons reset to their original values before the changes. This is not a reset to default.
        """
        self.confirmation_box = QMessageBox.question(self, 'Warning', 'Do you wish to discard all your changes?',
                                                     QMessageBox.Yes | QMessageBox.No,
                                                     QMessageBox.No)
        if self.confirmation_box == QMessageBox.Yes:
            self.search_start_edit.setText(self.settings.folder_search_start)
            self.nuke_exe_edit.setText(self.settings.nuke_exe)
            self.write_node_edit.setText(self.settings.write_node_name)
            self.file_name_checkbox.setChecked(True if (isinstance(self.settings.full_filepath_name, str) and self.settings.full_filepath_name == "true") or self.settings.full_filepath_name == True else False)
            self.render_nuke_open_checkbox.setChecked(
                True if (isinstance(self.settings.render_nuke_open, str) and self.settings.render_nuke_open == "true") 
                    or 
                    self.settings.render_nuke_open == True 
                else False
            )
            self.disable_save_buttons()
            
            
    def enable_save_buttons(self):
        """
            Enables the save and cancel buttons and shows the warning label.
        """
        self.save_button.setEnabled(True)
        self.cancel_changes_button.setEnabled(True)
        self.show_warning_label(True)
    
    
    def disable_save_buttons(self):
        """
            Disables the save and cancel buttons and hides the warning label.
        """
        self.save_button.setEnabled(False)
        self.cancel_changes_button.setEnabled(False)
        self.show_warning_label(False)
    

    def show_warning_label(self, on = False):
        """
            Sets the warning label when the user has not saved settings.
        """
        if on:
            self.warning_label.setText("You have not saved any changes!")
        else:
            self.warning_label.setText("")


    def prompt_user_save_file_del(self):
        """
            Prompts user to make sure they want to remove the save file. Deletes the save file if confirmed
        """
        self.confirmation_box = QMessageBox.question(self, 'Warning', 'Do you wish to delete the save file? \n(a new one will be created when you relaunch but no settings will be saved for relaunch)',
                                                     QMessageBox.Yes | QMessageBox.No,
                                                     QMessageBox.No)
        if self.confirmation_box == QMessageBox.Yes:
            self.settings.remove_appdata_contents()
            self.del_json_file_button.setEnabled(False)
            self.del_json_file_button.setStyleSheet("background-color: grey;")


    def prompt_user_temp_file_del(self):
        #TODO, finish this method to allow user to delete temp data files
        self.confirmation_box = QMessageBox.question(self, 'Warning', 'Do you wish to delete the temp files?',
                                                     QMessageBox.Yes | QMessageBox.No,
                                                     QMessageBox.No)
        if self.confirmation_box == QMessageBox.Yes:
            self.settings.remove_appdata_contents()
            self.del_json_file_button.setEnabled(False)
            self.del_json_file_button.setStyleSheet("background-color: grey;")
    

    def enable_del_button(self):
        """
            Re-enables the del json file button.
        """
        self.del_json_file_button.setEnabled(True)

        