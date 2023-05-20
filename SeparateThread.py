import os
import sys
import subprocess
import time
from typing import Optional

from Settings import Settings
from ErrorCodes import ErrorCodes

from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import QThread, Signal, QObject
from PySide2.QtWidgets import QMessageBox

class SeparateThread(QObject):
    
    nuke_path_ready = Signal(str)
    render_script_update = Signal(str, int, float)
    render_done = Signal()
    quit_render_thread = Signal()
    quit_nuke_search_thread = Signal()
    
            
    def __init__(self):
        super().__init__()
        self.settings = Settings()
        self.settings.load_settings()
        self.error_obj = ErrorCodes()
        self.stop_flag = False


    def get_latest_nuke_path(self):
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

        temp_file_paths = file_paths.copy()

        for script in temp_file_paths:
            if self.stop_flag:
                return        
            start_time = time.time()
            output = self.render_nuke_script(script)
            self.render_script_update.emit(script, output, time.time()-start_time)
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
        print(nuke_script_path)
        try:
            self.py_render_script = os.path.join(sys._MEIPASS, "RenderScript.py")
        except AttributeError:
            self.py_render_script = "./RenderScript.py"

        print(self.settings.nuke_exe)
        cmd = [self.settings.nuke_exe,
                '-ti',
                "-V", "2", #this is verbose mode, level 2, https://learn.foundry.com/nuke/content/comp_environment/configuring_nuke/command_line_operations.html
                self.py_render_script,
                nuke_script_path,
                self.settings.write_node_name
                ]
        print(cmd)
        proc = subprocess.Popen(cmd, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        exit_code = proc.returncode
        #stderr = proc.communicate()[1]
        #output = str(stderr.decode("utf-8"))
        #print(f"stdout: {stdout}")
        #print(f"stderr: {stderr}")
        #print(f"Exit code: {exit_code}")
        return exit_code  

    #not being used but here if needed
    def quit_rt(self):
        self.quit_render_thread.emit()


    def quit_nst(self):
        self.quit_nuke_search_thread.emit()


    def stop(self):
        self.stop_flag = True