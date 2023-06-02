import os
import sys
import subprocess
import time
from typing import Optional

from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import QThread, Signal, QObject
from PySide6.QtWidgets import QMessageBox

class SeparateBootupThread(QObject):
    """A class to handle single thread tasks. This was created to help keep the GUI active while some tasks
        are run such as finding the nuke executable path.

    Args:
        QObject (_type_)
        
    Signals:
        nuke_path_ready (str): This emits the nuke path once it is found, or none if it is not.
        render_script_update (str, int, float): This signal emits the information needed for the GUI to present
            the render info to the user. The Script, the exit code of the render, and the time it took to render it
        render_done (): This just sends a signal once the render is done so the GUI can handle everything.
    """
    done = Signal()
    root_being_explored = Signal(str)
    nuke_path_stored = Signal(str)
    
            
    def __init__(self):
        super().__init__()
        self.stop_flag = False


    def get_latest_nuke_path(self):
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
            self.root_being_explored.emit(root)
            for file in files:
                if "Nuke" in file and file.endswith(".exe"):
                    ver = float(file.split("Nuke")[1].split(".exe")[0])
                    if ver > max_ver:
                        max_ver = ver
                        nuke_path = os.path.join(root, file)
                        self.nuke_path_stored.emit(nuke_path)

        self.nuke_path_ready.emit(nuke_path)

    
    def stop(self):
        self.stop_flag = True