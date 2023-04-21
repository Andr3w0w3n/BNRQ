import sys
import os
import subprocess
from PyQt import QtWidgets, QtGui
from PyQt.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton,
    QLabel, QLineEdit, QVBoxLayout, QGridLayout
)

def run_render(script_path):
    cmd = [nuke_exe,
            "-ti",
            render_script,
            script_path
            ]
    proc = subprocess.Popen(cmd)
    proc.communicate()

class MainWindow(QWidget):
    """
    This creates the primary window for the render queue
    
    """

    def __init__(self):
        super().__init__()
        self.resize(400, 400)
        self.setWindowIcon(QIcon("ICON PATH GOES HERE"))
        self.setWindowTitle("Nuke Render Queue")
        self.setContentMargins(40, 40, 40, 40)

        layout = QGridLayout()
        self.setLayout(layout)

        add_script_button = QPushButton("+")
        layout.addWidget(add_script_button, 0, 0)

        remove_script_button = QPushButton("-")
        layout.addWidget(remove_script_button, 0, 1)

    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())