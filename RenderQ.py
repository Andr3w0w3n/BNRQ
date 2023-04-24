import sys
import os
import subprocess
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QHBoxLayout,
    QLabel, QLineEdit, QVBoxLayout, QGridLayout, QFileDialog,
    QMainWindow, QListWidget, QtCore, QMessageBox
)


class MainWindow(QMainWindow):
    """
    This creates the primary window for the render queue
    
    """

    def __init__(self):
        super().__init__()

        #variables
        self.file_paths = []
        self.nuke_exe = "C:/Program Files/"
        self.py_render_script = "./RenderScript.py"
        
        #TODO, have yet to fully implement
        self.write_node_name = "Write1"
        self.folder_search_start = "C:/"

        #Window setup
        self.resize(400, 400)
        #self.setWindowIcon(QIcon("ICON PATH GOES HERE"))
        self.setWindowTitle("Nuke Render Queue")
        self.setContentsMargins(40, 40, 40, 40)
        
        #elements
        self.add_script = QPushButton("+")
        self.remove_script = QPushButton("-")
        self.clear_files = QPushButton("Clear")
        self.render_button = QPushButton("Render")
        self.file_list = QListWidget()

        #layout setup
        add_minus_layout = QHBoxLayout()
        add_minus_layout.addWidget(self.add_script)
        add_minus_layout.addWidget(self.remove_script)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.file_list)
        main_layout.addLayout(add_minus_layout)

        #element layout setup
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        #connect the buttons
        self.add_script.clicked.connect(self.add_script_to_q)
        self.remove_script.clicked.connect(self.remove_script_from_q)
        self.clear_files.clicked.connect(self.clear_file_list)

    def get_default_nuke_path():
        for root, dirs, files in os.walk(os.environ.get("ProgramFiles")):
            if 'nuke.exe' in files:
                return os.path.join(root, 'nuke.exe')


    def update_nuke_path(self):
        folder_dialog = QFileDialog()
        folder_dialog.setNameFilter("Executables (*.exe)")
        self.nuke_exe = folder_dialog.getOpenFileName(self, "Select File", directory = "C:/")[0]

    
    def add_script_to_q(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Nuke scripts (*.nk)")
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

        for script in self.file_paths:
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
                self.file_paths.remove(script)
                self.file_list.takeItem(self.file_list.row(script))
                progress_dialog.setValue(i)
        progress_dialog.setValue(len(self.file_paths))


    def render_nuke_script(self, script_path):
        cmd = [self.nuke_exe,
                "-ti",
                self.py_render_script,
                script_path
                ]
        print(cmd)
        proc = subprocess.Popen(cmd, stderr=subprocess.PIPE)
        stderr = proc.communicate()[1]
        return stderr.decode("utf-8")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())