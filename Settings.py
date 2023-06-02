import sys
import os
import json
import shutil
import getpass
import time

#from SeparateBootupThread import SeparateBootupThread

from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import(QSettings, QStandardPaths, Signal, QThread, QCoreApplication)
from PySide6.QtWidgets import QMessageBox


class Settings(QtCore.QSettings):

    #The QtCore.QSettings is wonky, I have made it so the application clears them on exit. 
    #For now, it is working as the settings are being taken from self. , unsure how this will affect if 
    #   you create a new instance of settings

    root_being_explored = Signal(str)
    latest_nuke = Signal(str)
    finished_launch = Signal()


    def __init__(self):
        super().__init__()
        self.applicationName = "Basic Nuke Render Queue"
        #This is to use for the QSettings object
        self.username = getpass.getuser()
        self.json_settings_filepath = None
        self.render_queue_folder = None

        self.assign_json_paths()

        self.nuke_exe = None
        self.folder_search_start = "C:\\Users\\"
        self.write_node_name = "Write1"
        self.full_filepath_name = True

        self.load_settings()


    def load_settings_from_json(self):
        try:
            with open(self.json_settings_filepath, "r") as settings_file:
                json_settings = json.load(settings_file)
                self.nuke_exe = json_settings.get("exe", self.nuke_exe)
                self.folder_search_start = json_settings.get("search_start", self.folder_search_start)
                self.write_node_name = json_settings.get("write_name", self.write_node_name)
                self.full_filepath_name = json_settings["full_filepath_name"]
                
        except (AttributeError, FileNotFoundError):
            print("Unable to load settings file")


    def save_settings_to_json(self):
        self.settings_dict = {
            "exe": self.nuke_exe,
            "search_start": self.folder_search_start,
            "write_name": self.write_node_name,
            "full_filepath_name": self.full_filepath_name
        }

        try:
            with open(self.json_settings_filepath, "w") as settings_file:
                json.dump(self.settings_dict, settings_file)
        except (AttributeError, FileNotFoundError):
            print("Unable to save settings file")    


    def load_settings(self, skip_json = False):
        
        settings = QtCore.QSettings(self.username, "BNRQ")
        settings.beginGroup("Paths")
        self.nuke_exe = settings.value("Nuke executable", self.nuke_exe)
        self.folder_search_start = settings.value("Search start", self.folder_search_start)
        settings.endGroup()

        settings.beginGroup("Write Node")
        self.write_node_name = settings.value("write_node_name", self.write_node_name)
        settings.endGroup()

        settings.beginGroup("UI Look")
        self.full_filepath_name = settings.value("full_filepath_name", self.full_filepath_name)
        settings.endGroup()


    def save_settings(self):

        settings = QtCore.QSettings(self.username, "BNRQ")
        settings.beginGroup("Paths")
        settings.setValue("Nuke executable", self.nuke_exe)
        settings.setValue("Search start", self.folder_search_start)
        settings.endGroup()

        settings.beginGroup("Write Node")
        settings.setValue("write_node_name", self.write_node_name)
        settings.endGroup()

        settings.beginGroup("UI Look")
        settings.setValue("full_filepath_name", self.full_filepath_name)
        settings.endGroup()
        
        self.save_settings_to_json()


    def launch(self):
        skip_json = True

        if not os.path.exists(self.render_queue_folder) and not os.path.exists(self.json_settings_filepath):
            os.makedirs(self.render_queue_folder, exist_ok=True)
            skip_json = True

        if not skip_json:
            self.load_settings_from_json()
        
        if self.nuke_exe is None:
            self.get_default_nuke_path()
        self.save_settings()
        self.finished_launch.emit()


    #this should only be called on launch
    def get_default_nuke_path(self):
        """ Find the latest version of Nuke executable installed. This is limited in it only searches the default
                and common spot of C:/ProgramFiles

        Emits:
            nuke_path_ready (str): Signal emitted when the latest Nuke executable path is found.
                It provides the path in it so the path can be useable by the UI.

        Steps:
            - The method searches for Nuke executable (by OS walking) in the "C:\Program Files\" directory and its subdirectories.
            - It identifies Nuke executables by looking for files with "Nuke" in their name and ending with ".exe".
            - The method determines the version of each found executable and keeps track of the latest version.
            - Once the latest Nuke executable path is found, it is emitted via the `nuke_path_ready` signal.

        """
        nuke_path = None
        max_ver = -1

        for root, dirs, files in os.walk("C:\\Program Files\\"):
            #time.sleep(0.0000005) #I HATE THAT I NEED THIS, I CANNOT FIND WHY IT IS BEING OVERLOADED
            #QtWidgets.QApplication.processEvents() 
            self.root_being_explored.emit(root)
            for file in files:
                if "Nuke" in file and file.endswith(".exe"):
                    ver = float(file.split("Nuke")[1].split(".exe")[0])
                    if ver > max_ver:
                        max_ver = ver
                        nuke_path = os.path.join(root, file)
                        self.latest_nuke.emit(os.path.splitext(os.path.basename(nuke_path))[0])

        self.handle_nuke_path_search_result(nuke_path)


    def handle_nuke_path_search_result(self, nuke_path):
        """Sets the nuke_exe setting to the found nuke path or shows an error message saying
            that no nuke path was found, and then sets the nuke path to empty

        Args:
            nuke_path (str): The nuke path emited by the signal. Either str or None
        """
        if nuke_path:
            self.nuke_exe = nuke_path
        else:
            error_box = QMessageBox()
            error_box.setIcon(QMessageBox.critical)
            error_box.setText("No Nuke path found!")
            error_box.exec()
            self.nuke_exe = ""


    def remove_appdata_contents(self):
        """
            This method removes the folder continaing files 
            for the application from the appdata folder. This acts as an "uninstall"
            of sorts. It does not remove the executable however and if the executable re-launches
            then the application will make the folder again.
        """
        shutil.rmtree(self.render_queue_folder)

    
    def get_user(self):
        return self.username
    

    def assign_json_paths(self):
        data_dir = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
        self.render_queue_folder = os.path.join(data_dir, "BNRQ")
        self.json_settings_filepath = os.path.join(self.render_queue_folder, "settings.json")
