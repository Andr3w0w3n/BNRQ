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
    """
        This class manages application settings.

        This class extends the QtCore.QSettings class and provides methods for loading, saving, and accessing application settings.
        It also emits signals to indicate the progress and status of certain operations.

        Signals:
            root_being_explored (str): Signal emitted when exploring a directory during the search for the Nuke executable.
                It provides the path of the directory being explored.
            latest_nuke (str): Signal emitted when the latest Nuke executable path is found.
                It provides the filename of the latest Nuke executable (without the extension).
            finished_launch: Signal emitted when the application launch is finished.
            loaded_nuke (str): Signal emitted when a Nuke script is loaded.
                It provides the path of the loaded Nuke script.
            json_created: Signal emitted when the JSON settings file is created.

        Attributes:
            applicationName (str): The name of the application.
            username (str): The username of the current user.
            json_settings_filepath (str): The path to the JSON settings file.
            render_queue_folder (str): The path to the render queue folder.
            temp_folder (str): The path to the temporary folder.
            xml_filepath (str): The path to the XML file containing current render script information.
            nuke_exe (str): The path to the Nuke executable.
            folder_search_start (str): The starting folder for searching Nuke executables.
            write_node_name (str): The name of the Write node.
            full_filepath_name (bool): Flag indicating whether to use the full filepath as the output filename.
            render_nuke_open (bool): Flag indicating whether to keep Nuke open after rendering.

        Methods:
            __init__(): Initializes the Settings object.
            load_settings_from_json(): Loads settings from the JSON settings file.
            save_settings_to_json(): Saves settings to the JSON settings file.
            load_settings(): Loads settings from the QSettings object and the JSON settings file.
            save_settings(): Saves settings to the QSettings object and the JSON settings file.
            launch(): Launches the application and performs necessary initialization.
            get_default_nuke_path(): Finds the latest version of the Nuke executable.
            handle_nuke_path_search_result(nuke_path): Handles the result of the Nuke executable path search.
            remove_appdata_contents(): Removes the application data folder.
            remove_temp_files(): Removes temporary files.
            get_user(): Returns the username of the current user.
            assign_json_paths(): Assigns paths for the JSON settings file and the render queue folder.
    """
    #The QtCore.QSettings is wonky, I have made it so the application clears them on exit. 
    #For now, it is working as the settings are being taken from self. , unsure how this will affect if 
    #   you create a new instance of settings

    root_being_explored = Signal(str)
    latest_nuke = Signal(str)
    finished_launch = Signal()
    loaded_nuke = Signal(str)
    json_created = Signal()


    def __init__(self):
        """
        Initializes the Basic Nuke Render Queue application.

        This method sets up the initial state and configuration of the application.
        It assigns values to various instance variables, such as the application name, username,
        file paths for JSON settings, render queue folder, temporary folder, XML file path,
        Nuke executable, folder search start path, write node name, full file path flag, and
        render Nuke open flag. It also loads the application settings.
        """

        super().__init__()
        self.applicationName = "Basic Nuke Render Queue"
        #This is to use for the QSettings object
        self.username = getpass.getuser()
        self.json_settings_filepath = None
        self.render_queue_folder = None

        self.assign_json_paths()

        self.temp_folder = os.path.join(self.render_queue_folder, "Temp")
        self.xml_filepath = os.path.join(self.temp_folder, "CurrentRenderScriptInfo.xml")

        self.nuke_exe = None
        self.folder_search_start = "C:\\Users\\"
        self.write_node_name = "Write1"
        self.full_filepath_name = True
        self.render_nuke_open = False

        self.load_settings()


    def load_settings_from_json(self):
        """
        Loads application settings from a JSON file.

        This method reads the JSON settings file specified by `json_settings_filepath`.
        It retrieves the values for various settings, such as the Nuke executable, folder search start path,
        write node name, full file path flag, and render Nuke open flag, from the JSON file and assigns them
        to the corresponding instance variables.

        If the JSON file is not found or an attribute error occurs, an error message is printed.
        """
        try:
            with open(self.json_settings_filepath, "r") as settings_file:
                json_settings = json.load(settings_file)
                self.nuke_exe = json_settings.get("exe", self.nuke_exe)
                self.folder_search_start = json_settings.get("search_start", self.folder_search_start)
                self.write_node_name = json_settings.get("write_name", self.write_node_name)
                self.full_filepath_name = json_settings.get("full_filepath_name", self.full_filepath_name)
                self.render_nuke_open = json_settings.get("render_nuke_open", self.render_nuke_open)
            
            #catch any true/false coming back as strings
            if isinstance(self.full_filepath_name, str) and self.full_filepath_name.lower() == "true":
                self.full_filepath_name = True
            elif isinstance(self.full_filepath_name, str) and self.full_filepath_name.lower() == "false":
                self.full_filepath_name = False
            elif isinstance(self.full_filepath_name, str):
                self.full_filepath_name = False

            if isinstance(self.render_nuke_open, str) and self.render_nuke_open.lower() == "true":
                self.render_nuke_open = True
            elif isinstance(self.render_nuke_open, str) and self.render_nuke_open.lower() == "false":
                self.render_nuke_open = False
            elif isinstance(self.render_nuke_open, str):
                self.render_nuke_open = False

        except (AttributeError, FileNotFoundError):
            print("Unable to load settings file")


    def save_settings_to_json(self):
        """
        Saves application settings to a JSON file.

        This method constructs a dictionary `settings_dict` with the current values of various application settings,
        such as the Nuke executable, folder search start path, write node name, full file path flag, and render Nuke open flag.

        It then attempts to write the `settings_dict` dictionary to the JSON settings file specified by `json_settings_filepath`.

        If the write operation is successful, the `json_created` signal is emitted.

        If the JSON file cannot be created or an attribute error occurs, an error message is printed.
        """

        self.settings_dict = {
            "exe": self.nuke_exe,
            "search_start": self.folder_search_start,
            "write_name": self.write_node_name,
            "full_filepath_name": self.full_filepath_name,
            "render_nuke_open": self.render_nuke_open
        }

        try:
            with open(self.json_settings_filepath, "w") as settings_file:
                json.dump(self.settings_dict, settings_file)

            self.json_created.emit()
        except (AttributeError, FileNotFoundError):
            print("Unable to save settings file")    


    def load_settings(self, skip_json = False):
        """
        Loads application settings from the QSettings object and optionally from a JSON file.

        This method retrieves various application settings from the QSettings object, such as the Nuke executable,
        folder search start path, write node name, full file path flag, and render Nuke open flag.

        If `skip_json` is False (default), it also attempts to load additional settings from a JSON file by calling
        the `load_settings_from_json` method.

        The retrieved settings are assigned to their respective instance variables. The `full_filepath_name` and
        `render_nuke_open` settings are converted to boolean values if they are in string format.
        """
        
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

        settings.beginGroup("Performance")
        self.render_nuke_open = settings.value("render_nuke_open", self.render_nuke_open)
        settings.endGroup()

        if isinstance(self.full_filepath_name, str) and self.full_filepath_name.lower() == "true":
            self.full_filepath_name = True
        elif isinstance(self.full_filepath_name, str) and self.full_filepath_name.lower() == "false":
            self.full_filepath_name = False
        elif isinstance(self.full_filepath_name, str):
            self.full_filepath_name = False

        if isinstance(self.render_nuke_open, str) and self.render_nuke_open.lower() == "true":
            self.render_nuke_open = True
        elif isinstance(self.render_nuke_open, str) and self.render_nuke_open.lower() == "false":
            self.render_nuke_open = False
        elif isinstance(self.render_nuke_open, str):
            self.render_nuke_open = False


    def save_settings(self):
        """
            Saves application settings to the QSettings object and a JSON file.

            This method retrieves the current application settings and saves them to the QSettings object, including the
            Nuke executable, folder search start path, write node name, full file path flag, and render Nuke open flag.

            The settings are stored in their respective groups within the QSettings object.

            Afterwards, the `save_settings_to_json` method is called to save the settings to a JSON file.
        """

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

        settings.beginGroup("Performance")
        settings.setValue("render_nuke_open", self.render_nuke_open)
        settings.endGroup()
        
        self.save_settings_to_json()


    def launch(self):
        """
        Launches the application and performs necessary initialization steps.

        This method is responsible for launching the application and performing various initialization steps.

        If the render queue folder and the JSON settings file do not exist, it creates the render queue folder
        and sets the `skip_json` flag to True.

        If `skip_json` is False, it calls the `load_settings_from_json` method to load settings from the JSON file.

        It then retrieves the default Nuke path or uses the previously set Nuke executable. The basename of the
        Nuke executable is emitted through the `latest_nuke` signal.

        The current settings are saved by calling the `save_settings` method.

        Finally, the `finished_launch` signal is emitted to indicate the completion of the launch process.
        """

        skip_json = False #Switch this to True if you want to skip the json no matter what

        if not os.path.exists(self.render_queue_folder) and not os.path.exists(self.json_settings_filepath):
            os.makedirs(self.render_queue_folder, exist_ok=True)
            skip_json = True

        if not skip_json:
            self.load_settings_from_json()
        
        if self.nuke_exe is None:
            self.get_default_nuke_path()
        else:
            self.latest_nuke.emit(os.path.splitext(os.path.basename(self.nuke_exe))[0])
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
            This method removes the folder contianing files 
            for the application from the appdata folder. This acts as an "uninstall"
            of sorts. It does not remove the executable however and if the executable re-launches
            then the application will make the folder again.
        """
        shutil.rmtree(self.render_queue_folder)

    
    def remove_temp_files(self):
        files = os.listdir(self.temp_folder)
        for file in files:
            file_path = os.path.join(self.temp_folder, file)
            if os.path.isfile(file_path):
                os.remove(file_path)


    def get_user(self):
        """
        Returns the username of the current user.
        """

        return self.username
    

    def assign_json_paths(self):
        """
        Assigns the necessary file paths for JSON files and creates the render queue folder if it doesn't exist.

        The method determines the data directory based on the operating system environment or the application path.
        It sets the render queue folder and the JSON settings file path using the determined data directory.
        If the render queue folder does not exist, it creates the folder.
        """
        #data_dir = os.getenv('APPDATA')
        try:
            data_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        except FileNotFoundError:
            app = QCoreApplication.instance()
            data_dir = app.applicationFilePath()

        self.render_queue_folder = os.path.join(data_dir, "BNRQ")
        #self.render_queue_folder = r"C:\Users\User\Desktop\BNRQ"
        
        self.json_settings_filepath = os.path.join(self.render_queue_folder, "settings.json")
        if not os.path.exists(self.render_queue_folder):
            os.mkdir(self.render_queue_folder)
