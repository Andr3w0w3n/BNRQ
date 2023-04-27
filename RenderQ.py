import sys
import os
import subprocess
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
    def __init__(self, settings):
        super().__init__()
        
        self.settings = settings
        self.file_paths = []
        self.nuke_exe = self.settings.value("Nuke executable")
        #self.nuke_exe = "C:/Program Files/Nuke13.2v5/Nuke13.2.exe"
        self.py_render_script = "./RenderScript.py"
        #TODO - has yet to be fully implemented
        self.write_node_name = self.settings.value("")
        self.folder_search_start = self.settings.value("")
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
        file_dialog.setNameFilter("Nuke scripts (*.nk *.nknc)")
        file_path = file_dialog.getOpenFileName(self, "Select File", directory = self.folder_search_start)[0]
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
            return None

        progress_dialog = QtWidgets.QProgressDialog("Rendering scripts...", "Cancel", 0, len(self.file_paths), self)
        progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
        progress_dialog.setMinimumDuration(0)

        def get_error_message(output, script):
            if output == 404:
                return f"There was no script found named {script}."
            return error_codes.get(output)
    
        error_codes = {
            104: f"There is no write node with name {self.write_node_name}.",
            200: "Render was cancelled by user through Nuke.",
            201: "Memory error occured with Nuke.",
            202: "Progress was aborted.",
            203: "There was a licensing error for Nuke.",
            204: "The User aborted the render.",
            206: "Unknown Render error occured.",
            404: None #defined in "get_error_message()"
        }

        progress = 0
        progress_dialog.setRange(0,len(self.file_paths))
        progress_dialog.setValue(int(progress))
        for script in self.file_paths:            
            QtWidgets.QApplication.processEvents()
            output = self.render_nuke_script(script)
            if progress_dialog.wasCanceled():
                    break
            if output in error_codes.values():               
                error_box = QMessageBox()
                error_box.setIcon(QMessageBox.Critical)
                error_box.setText(get_error_message(output, script))
                error_box.exec_()
                break
            else:
                render_item = self.file_list.findItems(script, QtCore.Qt.MatchExactly)
                #self.file_paths.remove(script)
                self.file_list.takeItem(self.file_list.row(render_item[0]))
                progress += 1
                progress_dialog.setValue(int(progress))
                QtWidgets.QApplication.processEvents()
        progress_dialog.setValue(100)
        self.clear_file_list()
        progress_dialog.close()        


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
        #need to figure out how to only show executables in this, as this code does not only show executables
        folder_dialog.setNameFilter("Executables (*.exe)")
        folder_dialog.setFileMode(QFileDialog.ExistingFile)
        folder_dialog.setFilter(QtCore.QDir.Executable)
        temp = folder_dialog.getOpenFileName(self, "Select File", directory = self.settings.value("Nuke executable"))[0]
        if temp:
            self.settings.nuke_exe = temp
        
        self.nuke_exe_edit.setText(self.settings.nuke_exe)


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