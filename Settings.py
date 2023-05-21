import sys
import os
import json

from PySide2 import QtCore
from PySide2.QtCore import(QSettings)


class Settings(QtCore.QSettings):

    def __init__(self):
        super().__init__()
        
        self.applicationName = "Nuke Render Queue"
        self.nuke_exe = None
        self.folder_search_start = "C:\\"
        self.write_node_name = "Write1"
        
        self.settings_filepath = r"./settings.json"
        
        try:
            base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            json_filepath = os.path.join(base_path, "settings.json")
            if os.path.exists(json_filepath):
                with open(self.settings_filepath, "r") as settings_file:
                    json_settings = json.load(settings_file)
                    self.nuke_exe = json_settings["exe"]
                    self.folder_search_start = json_settings["search_start"]
                    self.write_node_name = json_settings["write_name"]
        
        except AttributeError:        
            if os.path.exists(self.settings_filepath):
                with open(self.settings_filepath, "r") as settings_file:
                    json_settings = json.load(settings_file)
                    self.nuke_exe = json_settings["exe"]
                    self.folder_search_start = json_settings["search_start"]
                    self.write_node_name = json_settings["write_name"]
                
        self.settings_dict = {
            "exe": self.nuke_exe,
            "search_start": self.folder_search_start,
            "write_name": self.write_node_name
        }
        print("setting up settings")
        settings = QtCore.QSettings()
        settings.beginGroup("Paths")
        settings.setValue("Nuke executable", self.nuke_exe)
        settings.setValue("Search start", self.folder_search_start)
        settings.endGroup()

        settings.beginGroup("Write Node")
        settings.setValue("write_node_name", self.write_node_name)
        settings.endGroup()


    def load_settings(self):
        print("in load settings")
        settings = QtCore.QSettings()
        settings.beginGroup("Paths")
        nuke_exe_path = settings.value("Nuke executable")
        settings.endGroup()

        if not nuke_exe_path:
            nuke_exe_path = self.get_default_nuke_path()
            settings.beginGroup("Paths")
            settings.setValue("Nuke executable", nuke_exe_path)
            settings.endGroup()

        self.nuke_exe = nuke_exe_path

        settings.beginGroup("Write Node")
        self.write_node_name = settings.value("write_node_name", self.write_node_name)
        settings.endGroup()
        
        self.update_settings_file()

    
    def save_settings(self):
        print("in save settings")
        settings = QtCore.QSettings()
        settings.beginGroup("Paths")
        settings.setValue("Nuke executable", self.nuke_exe)
        settings.setValue("Search start", self.folder_search_start)
        settings.endGroup()

        settings.beginGroup("Write Node")
        settings.setValue("write_node_name", self.write_node_name)
        settings.endGroup()
        
        self.update_settings_file()

    def get_default_nuke_path(self):
        """ Find the latest version of Nuke executable installed. This is limited in it only searches the default
                and common spot of C:/ProgramFiles. It is run as soon as the program is launched. It throws no errors
                and does not do much in the case Nuke is not found.

        returns:
            nuke_path_ready (str): Path to the nuke executable or None if there isn't a path to the executable found.

        Steps:
            - The method searches for Nuke executable (by OS walking) in the "C:\Program Files\" directory and its subdirectories.
            - It identifies Nuke executables by looking for files with "Nuke" in their name and ending with ".exe".
            - The method determines the version of each found executable and keeps track of the latest version.
            - Once the latest Nuke executable path is found, it is emitted via the `nuke_path_ready` signal.

        """
        print("finding the nuke path for some reason")
        
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
    
    
    def update_settings_file(self):
        self.settings_dict["exe"] = self.nuke_exe
        self.settings_dict["search_start"] = self.folder_search_start
        self.settings_dict["write_name"] = self.write_node_name

        with open(self.settings_filepath, "w") as settings_file:
            json.dump(self.settings_dict, settings_file)
