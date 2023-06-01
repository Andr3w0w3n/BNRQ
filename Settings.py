import sys
import os
import json
import shutil
import getpass

from PySide6 import QtCore
from PySide6.QtCore import(QSettings, QStandardPaths)


class Settings(QtCore.QSettings):


    #The QtCore.QSettings is wonky, I have made it so the application clears them on exit. 
    #For now, it is working as the settings are being taken from self. , unsure how this will affect if 
    #   you create a new instance of settings

    def __init__(self, skip_json = False):
        super().__init__()
        self.applicationName = "Basic Nuke Render Queue"
        #This is to use for the QSettings object
        self.username = getpass.getuser()
        

        #Defaults
        self.nuke_exe = None
        self.folder_search_start = "C:\\Users\\"
        self.write_node_name = "Write1"
        self.full_filepath_name = True

        self.json_settings_filepath = None

        data_dir = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
        self.render_queue_folder = data_dir + r"/BNRQ"
        self.json_settings_filepath = self.render_queue_folder + r"/settings.json"
        if not os.path.exists(self.render_queue_folder) and not os.path.exists(self.json_settings_filepath):
            print(f"making a folder at {self.render_queue_folder}")
            os.makedirs(self.render_queue_folder, exist_ok=True)
            skip_json = True

        if not skip_json:
            self.load_settings_from_json()
            
        self.load_settings()
        if self.nuke_exe is None:
            self.nuke_exe = self.get_default_nuke_path()
        self.save_settings()


    def load_settings_from_json(self):
        print("Loading settings from json")
        try:
            with open(self.json_settings_filepath, "r") as settings_file:
                json_settings = json.load(settings_file)
                self.nuke_exe = json_settings.get("exe", self.nuke_exe)
                self.folder_search_start = json_settings.get("search_start", self.folder_search_start)
                self.write_node_name = json_settings.get("write_name", self.write_node_name)
                self.full_filepath_name = json_settings["full_filepath_name"]
                
        except (AttributeError, FileNotFoundError):
            print("Unable to load settings from json")
            pass


    def save_settings_to_json(self):
        self.settings_dict = {
            "exe": self.nuke_exe,
            "search_start": self.folder_search_start,
            "write_name": self.write_node_name,
            "full_filepath_name": self.full_filepath_name
        }

        try:
            json.dump(self.settings_dict, open(self.json_settings_filepath, "w"))

        except (AttributeError, FileNotFoundError):
            print("Unable to save to json")
            pass
        


    def load_settings(self):
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


    def get_default_nuke_path(self):
        """
            This method finds nuke without opening up a different thread. 
            It is for the initial launch of the application.

            Find the latest version of Nuke executable installed. This is limited in it only searches the default
                and common spot of C:/ProgramFiles

            Returns:
                nuke_path (str): Signal emitted when the latest Nuke executable path is found.
                    It provides the path in it so the path can be useable by the UI.

            Steps:
                - The method searches for Nuke executable (by OS walking) in the "C:\Program Files\" directory and its subdirectories.
                - It identifies Nuke executables by looking for files with "Nuke" in their name and ending with ".exe".
        """

        print("Finding nuke")
        nuke_path = None
        max_ver = -1

        for root, dirs, files in os.walk("C:\\Program Files\\"):
            for file in files:
                if "Nuke" in file and file.endswith(".exe"):
                    ver = float(file.split("Nuke")[1].split(".exe")[0])
                    if ver > max_ver:
                        max_ver = ver
                        nuke_path = os.path.join(root, file)

        return nuke_path
    

    def remove_appdata_contents(self):
        """
            This method removes the folder continaing files 
            for the application from the appdata folder. This acts as an "uninstall"
            of sorts. It does not remove the executable however and if the executable re-launches
            then the application will make the folder again.
        """
        shutil.rmtree(self.render_queue_folder)