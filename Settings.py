import sys
import os
from PySide2 import QtCore
from PySide2.QtCore import(QSettings)

class settings(QtCore.QSettings):

    def __init__(self):
        super().__init__()
        self.applicationName = "Nuke Render Queue"
        self.nuke_exe = None
        self.folder_search_start = "C:/"
        self.write_node_name = "Write1"


    def load_settings(self):
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

    
    def save_settings(self):
        settings = QtCore.QSettings()
        settings.beginGroup("Paths")
        settings.setValue("Nuke executable", self.nuke_exe)
        settings.setValue("Search start", self.folder_search_start)
        settings.endGroup()

        settings.beginGroup("Write Node")
        settings.setValue("write_node_name", self.write_node_name)
        settings.endGroup()

    def get_default_nuke_path(self):
        nuke_path = None
        max_ver = -1

        for root, dirs, files in os.walk("C:/Program Files/"):
            for file in files:
                if "Nuke" in file and file.endswith(".exe"):
                    ver = float(file.split("Nuke")[1].split(".exe")[0])
                    if ver > max_ver:
                        max_ver = ver
                        nuke_path = os.path.join(root, file)

        return nuke_path
