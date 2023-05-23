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
        self.settings_filepath = r".\settings.json"
        self.load_settings_from_json()
        if self.nuke_exe is None:
            self.nuke_exe = self.get_default_nuke_path()
        self.save_settings()


    def load_settings_from_json(self):
        try:
            base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            json_filepath = os.path.join(base_path, "settings.json")
            with open(json_filepath, "r") as settings_file:
                json_settings = json.load(settings_file)
                self.nuke_exe = json_settings.get("exe", self.nuke_exe)
                self.folder_search_start = json_settings.get("search_start", self.folder_search_start)
                self.write_node_name = json_settings.get("write_name", self.write_node_name)

        except (AttributeError, FileNotFoundError):
            try:
                with open(self.settings_filepath, "r") as settings_file:
                    json_settings = json.load(settings_file)
                    self.nuke_exe = json_settings.get("exe", self.nuke_exe)
                    self.folder_search_start = json_settings.get("search_start", self.folder_search_start)
                    self.write_node_name = json_settings.get("write_name", self.write_node_name)

            except (AttributeError, FileNotFoundError):
                pass


    def save_settings_to_json(self):
        self.settings_dict = {
            "exe": self.nuke_exe,
            "search_start": self.folder_search_start,
            "write_name": self.write_node_name
        }

        try:
            base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            json_filepath = os.path.join(base_path, "settings.json")
            with open(json_filepath, "w") as settings_file:
                json.dump(self.settings_dict, settings_file)

        except (AttributeError, FileNotFoundError):
            with open(self.settings_filepath, "w") as settings_file:
                json.dump(self.settings_dict, settings_file)


    def load_settings(self):
        settings = QtCore.QSettings()
        settings.beginGroup("Paths")
        self.nuke_exe = settings.value("Nuke executable", self.nuke_exe)
        self.folder_search_start = settings.value("Search start", self.folder_search_start)
        settings.endGroup()

        settings.beginGroup("Write Node")
        self.write_node_name = settings.value("write_node_name", self.write_node_name)
        settings.endGroup()


    def save_settings(self):
        settings = QtCore.QSettings()
        settings.beginGroup("Paths")
        settings.setValue("Nuke executable", self.nuke_exe)
        settings.setValue("Search start", self.folder_search_start)
        settings.endGroup()

        settings.beginGroup("Write Node")
        settings.setValue("write_node_name", self.write_node_name)
        settings.endGroup()

        self.save_settings_to_json()


    def get_default_nuke_path(self):
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