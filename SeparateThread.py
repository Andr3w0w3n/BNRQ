import os
import sys
import subprocess
import time
from typing import Optional

from Settings import Settings
from ErrorCodes import ErrorCodes

from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import (
    QThread, Signal, QObject, QFileSystemWatcher, QDir, QStandardPaths, QFileInfo,
    QFile, QXmlStreamReader, QFileSystemWatcher, QTimer, QProcess
)
from PySide6.QtWidgets import QMessageBox

class SeparateThread(QObject):
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
    nuke_path_ready = Signal(str)
    render_script_update = Signal(str, int, float)
    render_stopped = Signal(int)
    render_done = Signal()
    update_gui = Signal()
    render_cancelled = Signal()

            
    def __init__(self):
        super().__init__()
        self.settings = Settings()
        self.settings.load_settings()
        self.error_obj = ErrorCodes()
        self.stop_flag = False

        self.external_error_code = None

        data_dir = os.getenv('APPDATA')
        self.render_queue_folder = os.path.join(data_dir, "BNRQ")
        self.render_queue_folder = self.settings.render_queue_folder
        self.temp_folder = os.path.join(self.render_queue_folder, "Temp")
        self.xml_filepath = os.path.join(self.temp_folder, "CurrentRenderScriptInfo.xml")
        
        
        if not QDir(self.temp_folder).exists():
            QDir().mkpath(self.temp_folder)
        elif os.path.exists(self.xml_filepath):
            os.remove(self.xml_filepath)

        self.timer = QTimer()
        self.timer.timeout.connect(self.emit_update)
        self.timer.start(50)


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
            for file in files:
                if "Nuke" in file and file.endswith(".exe"):
                    ver = float(file.split("Nuke")[1].split(".exe")[0])
                    if ver > max_ver:
                        max_ver = ver
                        nuke_path = os.path.join(root, file)

        self.nuke_path_ready.emit(nuke_path)
    

    def render_list(self, file_paths):
        """Render the list of Nuke scripts provided from the GUI. This method itterates through the 
            filepaths provided in the file_paths() argument and renders them out. After each script rendered
            out (or stopped due to error), the method emits a signal with the nessesary information to 
            give back to the user.

        Args:
            file_paths (list): List of file paths containing the Nuke scripts to render.

        Emits:
            render_script_update (str, int, float): Signal emitted after each script is rendered.
                It provides the script path, exit code, and elapsed time for the GUI to use.
            render_done: Signal emitted when rendering of all scripts is complete.

        Notes:
            - A delay of 1 second is added between rendering each script to allow for GUI
            interaction and possible thread interruption.

        """

        temp_file_paths = file_paths.copy()

        for script in temp_file_paths:
            if self.stop_flag:
                return        
            start_time = time.time()
            self.external_error_code = self.render_nuke_script(script)
            self.render_script_update.emit(script, self.external_error_code, time.time()-start_time)
            time.sleep(1) #this is to give time for the GUI to tell the thread to stop

        self.render_done.emit()
        

    def render_nuke_script(self, nuke_script_path):
        """This method calls for nuke to render the project passed into it. It will render it by running the render script in 
            the instance of nuke

        Args:
            nuke_script_path (str): This is the path where the script will

        Returns:
            str: it returns the exit code as a string (not bit) so that it can be read and interpreted 
        """
        #this line is to make sure the packaged executable is able to keep RenderScript.py for use

        """self.external_render_process = QProcess()
        self.external_render_process.readyReadStandardOutput.connect(self.handle_external_output)
        self.external_render_process.finished.connect(self.handle_external_finish)
        self.external_render_process.errorOccurred.connect(self.handle_error)""" 
        
        try:
            self.py_render_script = os.path.join(sys._MEIPASS, "RenderScript.py")
        except AttributeError:
            self.py_render_script = "./RenderScript.py"

        cmd = [self.settings.nuke_exe,
                '-ti',
                "-V", "2", #this is verbose mode, level 2, https://learn.foundry.com/nuke/content/comp_environment/configuring_nuke/command_line_operations.html
                self.py_render_script,
                nuke_script_path,
                self.settings.write_node_name,
                ]
        print(cmd)
        #self.external_render_process.start(cmd[0], cmd[1:])
        proc = subprocess.Popen(cmd, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        exit_code = proc.returncode
        #stderr = proc.communicate()[1]
        #output = str(stderr.decode("utf-8"))
        return exit_code


    #opening 1 instance of nuke and open scripts from there render method
    def render_script_list(self, file_paths):
        try:
            self.py_render_script = os.path.join(sys._MEIPASS, "RenderScriptList.py")
        except AttributeError:
            self.py_render_script = "./RenderScriptList.py"

        self.internal_render_process = QProcess()
        self.internal_render_process.readyReadStandardOutput.connect(self.handle_internal_output)
        self.internal_render_process.finished.connect(self.handle_internal_finish)
        self.internal_render_process.errorOccurred.connect(self.handle_error)

        cmd = [self.settings.nuke_exe,
                '-ti',
                "-V", "2", #this is verbose mode, level 2, https://learn.foundry.com/nuke/content/comp_environment/configuring_nuke/command_line_operations.html
                self.py_render_script,
                *file_paths,
                self.settings.write_node_name,
                self.xml_filepath
                ]
        print(cmd)
        self.internal_render_process.start(cmd[0], cmd[1:])
        #proc = subprocess.Popen(cmd, stderr=subprocess.PIPE)

        """while proc.poll() is None and not self.stop_flag:
            pass
        
        if not self.stop_flag:
            exit_code = proc.returncode
            self.render_done.emit()
        else:
            proc.terminate()
            self.render_stopped.emit(proc.returncode if not None else None)"""
    
    
    def handle_internal_output(self):
        #TODO, do something with this output???
        output = self.internal_render_process.readAllStandardOutput()


    def handle_internal_finish(self, exit_code, exit_status):
        self.render_stopped.emit(exit_code if exit_status == QProcess.NormalExit else None)
        self.internal_render_process.close()
        self.render_done.emit()

    
    def handle_external_output(self):
        #TODO, do something with this output???
        output = self.external_render_process.readAllStandardOutput()


    def handle_external_finish(self, exit_code, exit_status):
        self.external_error_code = exit_code if exit_status == QProcess.NormalExit else None
        self.external_render_process.close()


    def handle_error(self, error):
        #TODO, fill out these error modules
        if error == QProcess.FailedToStart:
            # Handle the case where the process fails to start
            print("Process failed to start")
            pass
        elif error == QProcess.Crashed:
            # Handle the case where the process crashes
            print("Process crashed")
            print(self.external_render_process.readAllStandardError())
            pass
        elif error == QProcess.Timedout:
            # Handle the case where the process times out
            print("Process timed out")
            pass


    def emit_update(self):
        self.update_gui.emit()


    def stop(self):
        self.internal_render_process.terminate()
        self.render_cancelled.emit()