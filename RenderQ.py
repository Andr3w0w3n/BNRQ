import sys
import os
import subprocess
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QHBoxLayout,
    QLabel, QLineEdit, QVBoxLayout, QGridLayout, QFileDialog,
    QMainWindow, QListWidget
)

def run_render(script_path):
    cmd = [nuke_exe,
            "-ti",
            render_script,
            script_path
            ]
    proc = subprocess.Popen(cmd)
    proc.communicate()

class MainWindow(QMainWindow):
    """
    This creates the primary window for the render queue
    
    """

    def __init__(self):
        super().__init__()

        #variables
        self.file_paths = []

        #Window setup
        self.resize(400, 400)
        #self.setWindowIcon(QIcon("ICON PATH GOES HERE"))
        self.setWindowTitle("Nuke Render Queue")
        self.setContentsMargins(40, 40, 40, 40)
        
        #elements
        self.add_script = QPushButton("+")
        self.remove_script = QPushButton("-")
        self.file_list = QListWidget()

        #layout setup
        add_minus_layout = QHBoxLayout()
        add_minus_layout.addWidget(self.add_script)
        add_minus_layout.addWidget(self.remove_script)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.file_list)
        main_layout.addLayout(add_minus_layout)

        #element layout setup
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        #connect the buttons
        self.add_script.clicked.connect(self.add_script_to_q)
        self.remove_script.clicked.connect(self.remove_script_from_q)

    
    def add_script_to_q(self):
        file_dialog = QFileDialog()
        file_path = file_dialog.getOpenFileName(self, "Select File")[0]
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

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())