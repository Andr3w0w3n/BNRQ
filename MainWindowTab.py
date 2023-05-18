import sys
import os
import subprocess
import concurrent.futures
import threading
import time
import pdb
import statistics
import re

from CodecLookup import FourCCTranslator as codec_finder

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QHBoxLayout,
    QLabel, QLineEdit, QVBoxLayout, QGridLayout, QFileDialog,
    QMainWindow, QListWidget, QMessageBox, QTabWidget
)
from PyQt5.QtCore import(QSettings)
"""
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QHBoxLayout,
    QLabel, QLineEdit, QVBoxLayout, QGridLayout, QFileDialog,
    QMainWindow, QListWidget, QMessageBox, QTabWidget
)
from PySide2.QtCore import(QSettings)
"""

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
            render_nuke_script(nuke_script_path): Execute the RenderScript.py script with the specified Nuke script as argument, and return the output/error message.
            get_render_times(render_times): Find the average(mean) time of each render to show the user an estimated finish time
    """


    def __init__(self, settings):
        """
            Initializes a new instance of the `RenderQueue` class.

            Args:
                settings (Settings): The `Settings` object containing the settings for the render queue.

            Attributes:
                settings (Settings): The `Settings` object containing the settings for the render queue.
                file_paths (List[str]): The list of file paths to render.
                nuke_exe (str): The path to the Nuke executable.
                py_render_script (str): The path to the Python render script.
                write_node_name (str): The name of the write node to render.
                folder_search_start (str): The path to the folder to start searching for files to render.
                max_num_threads (int): The maximum number of threads to use for rendering.

                add_script (QPushButton): The "Add" button to add a file path to the render queue.
                remove_script (QPushButton): The "Remove" button to remove a file path from the render queue.
                clear_files (QPushButton): The "Clear" button to clear the file path list.
                render_button (QPushButton): The "Render" button to start the rendering process.
                file_list (QListWidget): The list widget containing the file paths to render.
        """
        super().__init__()
        
        self.settings = settings
        self.file_paths = []
        self.nuke_exe = self.settings.nuke_exe
        self.py_render_script = r"./RenderScript.py"      
        self.write_node_name = self.settings.write_node_name
        #TODO - has yet to be fully implemented
        self.folder_search_start = self.settings.folder_search_start
        #careful using this value as the max workers, it can cause all the scripts to be rendered at once
        self.max_num_threads = os.cpu_count()
        #TODO - settings file to minimize boot time
        
        self.add_script = QPushButton("+")
        self.remove_script = QPushButton("-")
        self.clear_files = QPushButton("Clear")
        self.clear_files.setStyleSheet("background-color: red;")
        self.render_button = QPushButton("Render")
        self.file_list = QListWidget()
        self.write_details = QLabel("")
        self.write_details.setWordWrap(True)
        
        
        # Layout setup
        add_minus_layout = QHBoxLayout()
        add_minus_layout.addWidget(self.add_script)
        add_minus_layout.addWidget(self.remove_script)
        
        
        button_layout = QVBoxLayout()
        button_layout.addLayout(add_minus_layout)
        button_layout.addWidget(self.render_button)
        button_layout.addWidget(self.clear_files)
        button_layout.addWidget(self.write_details)
        #button_layout.setSizeConstraint(QVBoxLayout.SetFixedSize)

        
        total_button_layout = QHBoxLayout()
        total_button_layout.addWidget(self.file_list)
        total_button_layout.addLayout(button_layout)
        self.setLayout(total_button_layout)
        
        
        # Connect the buttons/actions
        self.add_script.clicked.connect(self.add_script_to_q)
        self.remove_script.clicked.connect(self.remove_script_from_q)
        self.clear_files.clicked.connect(self.clear_file_list)
        self.render_button.clicked.connect(self.run_render)
        self.file_list.itemSelectionChanged.connect(self.get_write_info)

        #create the error codes so that they do not need to be created again
        self.error_codes = {
            103: "There are no write nodes in this script",
            104: f"There is no write node with name {self.write_node_name}.",
            200: "Render was cancelled by user through Nuke.",
            201: "Render produced an error",
            202: "Memory error occured with Nuke.",
            203: "Progress was aborted.",
            204: "There was a licensing error for Nuke.",
            205: "The User aborted the render.",
            206: "Unknown Render error occured.",
            
            404: None #defined in "get_error_message()"
        }

        self.nuke_error_messages = {
            103: "no active Write operators"
        }

    
    def add_script_to_q(self):
        """   
            This method opens a file dialog to allow the user to select a Nuke script file. If a file is selected, its path
            is added to the list of file paths in the instance variable `self.file_paths`. The method then calls the
            `update_file_list` method to refresh the file list displayed in the user interface.
        """
        file_dialog = QFileDialog()
        file_path = file_dialog.getOpenFileName(self, 
                                                "Select File", 
                                                self.settings.folder_search_start, 
                                                "Nuke Scripts (*.nk) ;; All Files(*)")[0]
        if file_path:
            if file_path in self.file_paths:
                self.confirmation_box = QMessageBox.question(self, 'Warning', 'This file is already in the list. \
                                                             \nDo you still wish to add it?',
                                                             QMessageBox.Yes | QMessageBox.No,
                                                             QMessageBox.No)

                if self.confirmation_box == QMessageBox.Yes:
                    self.file_paths.append(file_path)
                    self.update_file_list()
            else:
                self.file_paths.append(file_path)
                self.update_file_list()
            
    
    def remove_script_from_q(self):
        """
            This method removes the selected file paths from the file path list and the file list view.
            It first gets the list of selected items from the file list view. Then, it iterates through
            the selected items and removes their corresponding file paths from the file path list and the
            file list view. If no items are selected, this method does nothing.
        """
        selected_items = self.file_list.selectedItems()
        for item in selected_items:
            self.file_paths.remove(item.text())
            self.file_list.takeItem(self.file_list.row(item))


    def update_file_list(self):
        """
            This method clears the file_list an then adds all the file_paths into the file_list. 
            Updating all the list to the latest files in the file_path list.
        """
        self.file_list.clear()
        for file_path in self.file_paths:
            self.file_list.addItem(file_path)


    def clear_file_list(self):
        """
            This method updates file_paths to hold no list objects and then calls for the list
            to be updated.
        """
        self.file_paths = []
        self.update_file_list()


    def run_render(self):
        """
            Render the Nuke scripts in the queue.

            If there are no scripts in the queue, a warning message is displayed and
            the method returns immediately. Otherwise, the scripts are rendered one
            by one in a loop. The progress is displayed in a modal dialog with a
            cancel button.

            The estimated time left for the current script and the total queue is
            displayed in the dialog. The render times for each script are recorded
            and used to calculate the estimated time.

            If the rendering is cancelled by the user, a warning message is displayed
            and the method returns immediately. If an error occurs during the rendering
            of a script, an error message is displayed and the rendering is stopped.

            The error codes are stored in a dictionary with a message for each code.
        """
        
        if not self.file_paths:
            QtWidgets.QMessageBox.warning(self, "Warning", "There are no files in the queue!")
            return
        

        def get_error_message(output, script):
            if output == 404:
                return f"There was no script found named {script}."
            return self.error_codes[output]
        

        progress = 0
        render_times = []
        total_script_count = len(self.file_paths)
        self.progress_dialog = QtWidgets.QProgressDialog("Rendering scripts...", "Cancel", 0, len(self.file_paths), self)
        self.progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
        self.progress_dialog.setMinimumDuration(0)
        self.progress_dialog.setRange(0,total_script_count)
        self.progress_dialog.setValue(int(progress))
        QtWidgets.QApplication.processEvents()
        
        temp_file_paths = self.file_paths.copy()
        for script in temp_file_paths:
            start_time = time.time()
                     
            QtWidgets.QApplication.processEvents()
            
            if self.progress_dialog.wasCanceled():
                self.progress_dialog.close()
                QtWidgets.QApplication.processEvents()
                QtWidgets.QMessageBox.warning(self, "Warning", "Rendering was cancelled")
                return
            
            """
            self.thread = threading.Thread(target=self.render_nuke_script, args=(script,))
            self.thread.start()
            self.thread.join()
            output = self.thread.result
            """
            self.progress_dialog.setLabelText(f"Rendering script {progress+1} of {total_script_count}"+
                                              f"\nEstimated Time: {self.get_estimated_time(render_times, total_script_count-progress)}")
            QtWidgets.QApplication.processEvents()  
            output = self.render_nuke_script(script)

            if output in self.error_codes:
                error_box = QMessageBox()
                error_box.setIcon(QMessageBox.Critical)
                error_box.setText(get_error_message(output, script))
                error_box.exec_()
                self.progress_dialog.close()
                QtWidgets.QApplication.processEvents()
                return
            else:
                render_item = self.file_list.findItems(script, QtCore.Qt.MatchExactly)
                self.file_paths.remove(script)
                self.file_list.takeItem(self.file_list.row(render_item[0]))
                progress += 1
                render_times.append(time.time()-start_time)
                #self.progress_dialog.setBottomLabelText(f"Estimated Time: {self.get_estimated_time(render_times)}")
                self.progress_dialog.setValue(int(progress))
                QtWidgets.QApplication.processEvents()
                
                

        del temp_file_paths
        self.progress_dialog.setValue(100)
        #making double sure
        self.clear_file_list()
        
        self.progress_dialog.close()


    def render_nuke_script(self, nuke_script_path):
        """This method calls for nuke to render the project passed into it. It will render it by running the render script in 
            the instance of nuke

        Args:
            nuke_script_path (str): This is the path where the script will

        Returns:
            str: it returns the exit code as a string (not bit) so that it can be read and interpreted 
        """
        #this line is to make sure the packaged executable is able to keep RenderScript.py for use
        try:
            self.py_render_script = os.path.join(sys._MEIPASS, "RenderScript.py")
        except AttributeError:
            self.py_render_script = "./RenderScript.py"

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
        print(f"stdout: {stdout}")
        print(f"stderr: {stderr}")
        print(f"Exit code: {exit_code}")
        return exit_code  


    def get_estimated_time(self, render_times, items_left):
        """This 

        Args:
            render_times (List[]): _description_
            items_left (): _description_

        Returns:
            str: the method either returns that it is estimating how much time is left
                for the rendering to be complete or returns the estimated time till 
                completion
        """
        if render_times:
            total_time_left = items_left * statistics.mean(render_times)
            hours, remainder = divmod(total_time_left, 3600)
            minutes, seconds = divmod(remainder, 60)
            hours = round(hours)
            minutes = round(minutes)
            seconds = round(seconds)
            
            #just seconds
            if hours == 0 and (minutes < 1):
                return f"{seconds:02} seconds"
            
            #1 minutes and x seconds
            elif hours == 0 and (minutes >= 1 and minutes <=2):
                return f"{minutes:02} minute, {seconds:02} seconds"
            
            #y minutes and x seconds
            elif hours == 0 and minutes >= 2:
                return f"{minutes:02} minutes, {seconds:02} seconds"
            
            #1 hour and x seconds
            elif (hours >= 1 and hours <=2) and minutes < 1:
                return f"{hours:02} hour, {seconds:02} seconds"
            
            #y hours and x seconds
            elif hours >= 2 and minutes < 1:
                return f"{hours:02} hours, {seconds:02} seconds"
           
            #1 hour and 1 minute and x seconds
            elif (hours >= 1 and hours <=2) and (minutes >= 1 and minutes <=2):
                return f"{hours:02} hour, {minutes:02} minute, {seconds:02} seconds"
            
            #1 hour and y minutes and x seconds
            elif (hours >= 1 and hours <=2) and minutes >= 2:
                return f"{hours:02} hour, {minutes:02} minutes, {seconds:02} seconds"
            
            #y hours and 1 minute and x seconds
            elif hours >= 2 and (minutes >= 1 and minutes <=2):
                return f"{hours:02} hours, {minutes:02} minute, {seconds:02} seconds"
            
            #y hours and z minutes and x seconds
            else:
                return f"{hours:02} hours, {minutes:02} minutes, {seconds:02} seconds"
            
        return "Estimating...."

    """#old version of the get_write_info
    def get_write_info(self):
        if not self.file_list.selectedItems():
            self.write_details.setText("")
        else:
            selected_item = self.file_list.selectedItems()[0]
            selected_script = (open(selected_item.text(), 'r')).read()
            
            write_node_pattern = r'Write\s*{\s*((?:.*\n)*?)\s*}'
            write_nodes = re.findall(write_node_pattern, selected_script)
            write_line = selected_script.splitlines()[1]

            #output_name_pattern = r'file\s+"(.+)"'
            #file_type_pattern = r'file_type\s+(.+)'
            extra_info = ("")
            if re.search("#write_info", write_line) is not None:
                format_pattern = r'format:\s*"\d+\s\d+\s\d+"'
                channel_pattern = r'chans:"(.+?)"'
                colorspace_pattern = r'colorspace:"(.+?)"'

                format = re.search(format_pattern, write_line)
                channel = re.search(channel_pattern, write_line)
                colorspace = re.search(colorspace_pattern, write_line)

                if format:
                    format = re.search(r'"(.+?)"', format.group(0)).group(1)
                else:
                    format = "N/A"

                if channel:
                    #channel_temp = re.search(r'chans:":((?:[^:"]*":)*[^"]*)', channel.group(0))
                    channel_temp = re.search(r'(?<=chans:")[^"]+', channel.group(0))
                    if channel_temp is not None:
                        channel = channel_temp.group(0).strip(":").replace(":", ",")
                    else:
                        channel = "N/A"
                    
                else:
                    channel = "N/A"

                if colorspace:
                    colorspace_temp = re.search(r'"(.+?)"', colorspace.group(0))
                    if colorspace_temp is not None:
                        colorspace = colorspace_temp.group(0).strip("\"")
                    else:
                        colorspace = "N/A"
                else:
                    colorspace = "N/A"
                
                extra_info = (f"<br><b>Format:</b> {format}"+
                            f"<br><b>Channels:</b> {channel}"+
                            f"<br><b>Colorspace:</b> {colorspace}")
            else:
                self.write_details.setText("<br><i><b>NO WRITE NODE EXISTS IN THIS PROJECT</b><i>")
                return

            position = 0
            found = False
            for wn in write_nodes:
                if re.search(self.write_node_name, wn) is not None:
                    found = True
                    break
                else:
                    position += 1

            if not found:
                self.write_details.setText(f"<b>NO WRITE NODE BY {self.settings.write_node_name} IN THIS PROJECT!</b>")
                return
            
            output_name_pattern = r'file\s+"(.+\..+?)"'
            file_type_pattern = r'file_type\s+(\w+)'
            colorspace_type1_pattern = r'colorspace (.+)'
            colorspace_type2_pattern = r'out_colorspace (.+)'
            
            output_name = re.search(output_name_pattern, write_nodes[position]).group(1)
            file_type = re.search(file_type_pattern, write_nodes[position]).group(1)
            colorspace_t1 = re.search(colorspace_type1_pattern, write_nodes[position])
            colorspace_t2 = re.search(colorspace_type2_pattern, write_nodes[position])
            if colorspace_t1 is not None and extra_info == "":
                self.write_details.setText(f"<b>Output:</b> {os.path.basename(output_name)}<br>"+
                                       f"<b>File Type:</b> {file_type}<br>"+
                                       f"<b>Colorspace:</b> {colorspace_t1.group(1)}")
            elif colorspace_t2 is not None and extra_info == "":
                self.write_details.setText(f"<b>Output:</b> {os.path.basename(output_name)}<br>"+
                                       f"<b>File Type:</b> {file_type}<br>"+
                                       f"<b>Colorspace:</b> {colorspace_t2.group(1)}")
            else:
                self.write_details.setText(f"<b>Output:</b> {os.path.basename(output_name)}<br>"+
                                       f"<b>File Type:</b> {file_type}"+
                                       extra_info)
            
            
            #if output_name and file_type:
            #    return [output_name, file_type]
            #
            #return None
            """

    #could potentially make the output look nicer    
    def get_write_info(self):
        if not self.file_list.selectedItems():
            self.write_details.setText("")
            return
            
        selected_item = self.file_list.selectedItems()[0]
        selected_script = open(selected_item.text(), 'r').read()
        
        extra_info = ""
        write_line = selected_script.splitlines()[1]

        if "#write_info" in write_line:
            format_match = re.search(r'format:\s*"(\d+\s\d+\s\d+)"', write_line)
            channel_match = re.search(r'chans:"(.+?)"', write_line)
            colorspace_match = re.search(r'colorspace:"(.+?)"', write_line)

            format_value = format_match.group(1) if format_match else "N/A"
            channel_value = channel_match.group(1).strip(":").replace(":", ",") if channel_match else "N/A"
            colorspace_value = colorspace_match.group(1) if colorspace_match else "N/A"

            extra_info = f"<br><b>Format:</b> {format_value}" \
                        f"<br><b>Channels:</b> {channel_value}" \
                        f"<br><b>Colorspace:</b> {colorspace_value}"
        else:
            self.write_details.setText("<br><i><b>NO WRITE NODE EXISTS IN THIS PROJECT</b><i>")
            return

        write_node_pattern = r'Write\s*{\s*((?:.*\n)*?)\s*}'
        write_nodes = re.findall(write_node_pattern, selected_script)

        write_node_index = next((i for i, wn in enumerate(write_nodes) if self.write_node_name in wn), None)

        if write_node_index is None:
            self.write_details.setText(f"<b>NO WRITE NODE BY {self.settings.write_node_name} IN THIS PROJECT!</b>")
            return

        write_node = write_nodes[write_node_index]
        output_name = re.search(r'file\s+"(.+\..+?)"', write_node).group(1)
        file_type = re.search(r'file_type\s+(\w+)', write_node).group(1)
        colorspace_type = re.search(r'(?:colorspace|out_colorspace)\s+(.+)', write_node, re.IGNORECASE).group(1) if re.search(r'(?:colorspace|out_colorspace)\s+(.+)', write_node, re.IGNORECASE) else ""

        codec = ""
        words = write_node.split()

        if "mov64_codec" in write_node:
            index = words.index("mov64_codec")
            codec_four_cc = words[index+1]
            codec = "<br><b>Codec:</b> " + codec_finder.get_codec(codec_finder, codec_four_cc)

        colorspace_line = f"<br><b>Colorspace:</b> {colorspace_type}" if colorspace_type else ""
        self.write_details.setText(f"<b>Output:</b> {os.path.basename(output_name)}"
                                    f"<br><b>File Type:</b> {file_type}"
                                    f"{extra_info}"
                                    f"{colorspace_line}"
                                    f"{codec}")