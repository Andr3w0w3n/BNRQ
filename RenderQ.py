import sys
import os
import subprocess
import concurrent.futures
import threading
import time
import pdb
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QHBoxLayout,
    QLabel, QLineEdit, QVBoxLayout, QGridLayout, QFileDialog,
    QMainWindow, QListWidget, QMessageBox, QTabWidget,
)
from PyQt5.QtCore import(QSettings)


class main_window_tab(QWidget):

    """
        This class defines the main render page, containing a list of Nuke scripts and a set of buttons to add/remove them, clear the list, and start a render process on the list. 

        Args:
            settings (QSettings): An instance of QSettings containing the user-defined and pre-set settings for the application.

        Attributes:
            settings (QSettings): An instance of QSettings containing the user-defined settings for the application.
            file_paths (list): A list containing the paths of the Nuke scripts to be rendered.
            nuke_exe (str): The path of the Nuke executable file, read from the user-defined settings.
            py_render_script (str): The path of the Python script used to render the Nuke scripts.
            write_node_name (str): The name of the Write node to be rendered in the Nuke scripts.
            folder_search_start (str): The default folder to search for Nuke scripts when adding them to the list.
            add_script (QPushButton): A button to add Nuke scripts to the list.
            remove_script (QPushButton): A button to remove Nuke scripts from the list.
            clear_files (QPushButton): A button to clear the list of Nuke scripts.
            render_button (QPushButton): A button to start the rendering process.
            file_list (QListWidget): A widget containing the list of Nuke scripts to be rendered.

        Methods:
            add_script_to_q(): Add a Nuke script to the list.
            remove_script_from_q(): Remove the selected Nuke scripts from the list.
            update_file_list(): Update the file list widget with the current list of Nuke scripts.
            clear_file_list(): Clear the list of Nuke scripts.
            run_render(): Start the rendering process for the Nuke scripts in the list.
            render_nuke_script(script_path): Execute the RenderScript.py script with the specified Nuke script as argument, and return the output/error message.
    """


    def __init__(self, settings):
        super().__init__()
        
        self.settings = settings
        self.file_paths = []
        self.nuke_exe = self.settings.nuke_exe
        #self.nuke_exe = "C:/Program Files/Nuke13.2v5/Nuke13.2.exe"
        self.py_render_script = "./RenderScript.py"
        #TODO - has yet to be fully implemented
        self.write_node_name = self.settings.write_node_name
        self.folder_search_start = self.settings.folder_search_start
        #careful using this value as the max workers, it can cause all the scripts to be rendered at once
        self.max_num_threads = os.cpu_count()
        #home computer test line
        #self.folder_search_start = "E:/Users/epica/OneDrive/Documents/Side Projects/Nuke/Add-Ons"
        
        self.add_script = QPushButton("+")
        self.remove_script = QPushButton("-")
        self.clear_files = QPushButton("Clear")
        self.clear_files.setStyleSheet("background-color: red;")
        self.render_button = QPushButton("Render")
        self.file_list = QListWidget()
        
        # Layout setup
        add_minus_layout = QHBoxLayout()
        add_minus_layout.addWidget(self.add_script)
        add_minus_layout.addWidget(self.remove_script)
        
        button_layout = QVBoxLayout()
        button_layout.addLayout(add_minus_layout)
        button_layout.addWidget(self.render_button)
        button_layout.addWidget(self.clear_files)

        total_button_layout = QHBoxLayout()
        total_button_layout.addWidget(self.file_list)
        total_button_layout.addLayout(button_layout)
        self.setLayout(total_button_layout)
        
        # Connect the buttons
        self.add_script.clicked.connect(self.add_script_to_q)
        self.remove_script.clicked.connect(self.remove_script_from_q)
        self.clear_files.clicked.connect(self.clear_file_list)
        self.render_button.clicked.connect(self.run_render)

    
    def add_script_to_q(self):
        file_dialog = QFileDialog()
        file_path = file_dialog.getOpenFileName(self, 
                                                "Select File", 
                                                self.settings.folder_search_start, 
                                                "Nuke Scripts (*.nk) ;; All Files(*)")[0]
        if file_path:
            self.file_paths.append(file_path)
            self.update_file_list()

    
    def remove_script_from_q(self):
        selected_items = self.file_list.selectedItems()
        for item in selected_items:
            self.file_paths.remove(item.text())
            self.file_list.takeItem(self.file_list.row(item))


    def update_file_list(self):
        self.file_list.clear()
        for file_path in self.file_paths:
            self.file_list.addItem(file_path)


    def clear_file_list(self):
        self.file_paths = []
        self.update_file_list()


    def run_render(self):
        
        if not self.file_paths:
            QtWidgets.QMessageBox.warning(self, "Warning", "There are no files in the queue!")
            return
        

        def get_error_message(output, script):
            if output == 404:
                return f"There was no script found named {script}."
            return self.error_codes.get(output)
    
        self.error_codes = {
            104: f"There is no write node with name {self.write_node_name}.",
            200: "Render was cancelled by user through Nuke.",
            201: "Render produced an error",
            203: "Memory error occured with Nuke.",
            204: "Progress was aborted.",
            205: "There was a licensing error for Nuke.",
            206: "The User aborted the render.",
            206: "Unknown Render error occured.",
            404: None #defined in "get_error_message()"
        }

        progress = 0
        self.progress_dialog = QtWidgets.QProgressDialog("Rendering scripts...", "Cancel", 0, len(self.file_paths), self)
        self.progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
        self.progress_dialog.setMinimumDuration(0)
        self.progress_dialog.setRange(0,len(self.file_paths))
        self.progress_dialog.setValue(int(progress))
        QtWidgets.QApplication.processEvents()
        
        
        for script in self.file_paths:            
            QtWidgets.QApplication.processEvents()
            
            if self.progress_dialog.wasCanceled():
                self.progress_dialog.close() 
                QtWidgets.QMessageBox.warning(self, "Warning", "Rendering was cancelled")
                print("I got into the rendering was cancelled section")
                return
            
            """
            self.thread = threading.Thread(target=self.render_nuke_script, args=(script,))
            self.thread.start()
            self.thread.join()
            output = self.thread.result
            """

            output = self.render_nuke_script(script)
            print("Output: " + str(output))

            if output in self.error_codes.values(): 
                error_box = QMessageBox()
                error_box.setIcon(QMessageBox.Critical)
                error_box.setText(get_error_message(output, script))
                error_box.exec_()
                QtWidgets.QApplication.processEvents()
                print("I got into the error section")          
                return
            else:
                render_item = self.file_list.findItems(script, QtCore.Qt.MatchExactly)
                self.file_paths.remove(script)
                self.file_list.takeItem(self.file_list.row(render_item[0]))
                progress += 1
                self.progress_dialog.setValue(int(progress))
                QtWidgets.QApplication.processEvents()
                print(f"rendered {script}")

        self.progress_dialog.setValue(100)
        #making double sure
        self.clear_file_list()
        
        self.progress_dialog.close()
        print("done")


    def render_nuke_script(self, script_path):
        cmd = [self.settings.nuke_exe,
                "-ti",
                self.py_render_script,
                script_path
                ]
        print(cmd)
        proc = subprocess.Popen(cmd, stderr=subprocess.PIPE)
        stderr = proc.communicate()[1]
        return stderr.decode("utf-8")           



class preferences_tab(QWidget):
    def __init__(self, settings):
        super().__init__()

        # Store a reference to the settings object
        self.settings = settings

        # Create the widgets for the preferences tab
        nuke_exe_label = QLabel("Nuke Executable Path:")
        self.nuke_exe_edit = QLineEdit(self.settings.nuke_exe)
        nuke_exe_file_finder = QPushButton("File Explorer")
        nuke_exe_file_finder.clicked.connect(self.update_nuke_path)
        search_start_label = QLabel("File Search Start:")
        self.search_start_edit = QLineEdit(self.settings.folder_search_start)
        file_path_start_finder = QPushButton("File Explorer")
        file_path_start_finder.clicked.connect(self.update_file_start_path)
        write_node_label = QLabel("Write Node Name:")
        self.write_node_edit = QLineEdit(self.settings.write_node_name)
        save_button = QPushButton("Save")
        save_button.clicked.connect(settings.save_settings)
        

        # Add the widgets to layouts
        nuke_exe_layout = QHBoxLayout()
        nuke_exe_layout.addWidget(nuke_exe_label)
        nuke_exe_layout.addWidget(self.nuke_exe_edit)
        nuke_exe_layout.addWidget(nuke_exe_file_finder)
        search_start_layout = QHBoxLayout()
        search_start_layout.addWidget(search_start_label)
        search_start_layout.addWidget(self.search_start_edit)
        search_start_layout.addWidget(file_path_start_finder)
        write_node_layout = QHBoxLayout()
        write_node_layout.addWidget(write_node_label)
        write_node_layout.addWidget(self.write_node_edit)
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(save_button)

        # Add the layouts to the preferences tab
        vbox = QVBoxLayout()
        vbox.addLayout(nuke_exe_layout)
        vbox.addLayout(search_start_layout)
        vbox.addLayout(write_node_layout)
        vbox.addLayout(button_layout)
        self.setLayout(vbox)
    
    def update_nuke_path(self):
        folder_dialog = QFileDialog()
        folder_dialog.setFileMode(QFileDialog.ExistingFile)
        folder_dialog.setFilter(QtCore.QDir.Executable)
        tempPath = folder_dialog.getOpenFileName(self, 
                                             "Select File", 
                                             self.settings.folder_search_start, 
                                             "Executables (*.exe) ;; All Files(*)")[0]
        if tempPath:
            self.settings.nuke_exe = tempPath
        self.nuke_exe_edit.setText(self.settings.nuke_exe)

    def update_file_start_path(self):
        folder_dialog = QFileDialog()
        folder_dialog.setFileMode(QFileDialog.ExistingFile)
        folder_dialog.setFilter(QtCore.QDir.Executable)
        tempPath = folder_dialog.getExistingDirectory(self, 
                                             "Select File", 
                                             self.settings.folder_search_start)
        if tempPath:
            self.settings.folder_search_start = tempPath
        self.search_start_edit.setText(self.settings.folder_search_start)


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


class MainWindow(QMainWindow):
    """
    This creates the primary window for the render queue
    
    """

    def __init__(self):
        super(MainWindow, self).__init__()

        #load settings
        self.settings = settings()
        self.settings.load_settings()
        
        #Window set
        self.resize(1000, 600)
        #self.setWindowIcon(QIcon("ICON PATH GOES HERE"))
        self.setWindowTitle("Nuke Render Queue")
        self.setContentsMargins(20, 20, 10, 10)
        
        #elements
        central_widget = QWidget()
        tab = QTabWidget()
        pref_tab = preferences_tab(self.settings)
        mw_tab = main_window_tab(self.settings)
        tab.addTab(mw_tab, "Render Queue")
        tab.addTab(pref_tab, "Preferences")
        main_layout = QVBoxLayout()
        main_layout.addWidget(tab)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        


    """
    def find_nuke_exe_path(self):
        base_dir = 'C:/Program Files/'
        pattern = 'Nuke'
        all_dirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d)) and pattern in d]
        sorted_dirs = sorted(all_dirs, reverse=True)
        
        if sorted_dirs:
            highest_version_folder = sorted_dirs[0]
            for filename in os.listdir(os.path.join(base_dir, highest_version_folder)):
                if filename.startswith("Nuke") and filename.endswith(".exe"):
                    return os.path.join(os.path.join(base_dir, highest_version_folder), filename)
        else:
            return None
    """


    def closeEvent(self, event):
        self.settings.save_settings()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    #pdb.run('main_window.show()', globals(), locals())
    main_window.show()
    sys.exit(app.exec_())