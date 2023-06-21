import sys
import os
import subprocess
import concurrent.futures
import threading
import time
import pdb
import statistics
import re

from CodecLookup import FourCCTranslator
from SeparateThread import SeparateThread
from ErrorCodes import ErrorCodes

from functools import partial

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QHBoxLayout,
    QLabel, QLineEdit, QVBoxLayout, QGridLayout, QFileDialog,
    QMainWindow, QListWidget, QMessageBox, QTabWidget
)
from PySide6.QtCore import(
    QSettings, QCoreApplication, QThread, QObject, QTimer,
    QFile, QXmlStreamReader, QDir, QFileSystemWatcher
)


class MainWindowTab(QWidget):

    """
        This class defines the main render page, containing a list of Nuke scripts and a set of buttons to add/remove them, clear the list, and start a render process on the list. 

        Args:
            settings (QWidget): An instance of QWidget.

        Attributes:
            settings (Settings): An instance of the Settings class for managing application settings.
            file_paths (list): A list of file paths to be rendered.
            file_info (dict): A dictionary containing information about the files.
            py_render_script (str): The path to the RenderScript.py file.
            max_num_threads (int): The maximum number of threads to use for rendering.
            continue_rendering (bool): Flag indicating whether rendering should continue.
            done_rendering (bool): Flag indicating whether rendering has completed.
            full_filepath_name (str): The full file path name.
            add_script (QPushButton): Button for adding scripts.
            remove_script (QPushButton): Button for removing scripts.
            clear_files (QPushButton): Button for clearing the file list.
            render_button (QPushButton): Button for starting the rendering process.
            file_list (QListWidget): List widget displaying the file list.
            write_details (QLabel): Label for displaying write details.
            translator (FourCCTranslator): An instance of the FourCCTranslator class for translating FourCC codes.
            timer (QTimer): Timer for updating the application.
            remove_timer: Timer for removing temporary files.
            render_queue_folder (str): The folder path for the render queue.
            temp_folder (str): The folder path for temporary files.
            xml_filepath (str): The file path for the CurrentRenderScriptInfo.xml file.
            directory (QDir): QDir object representing the temporary folder.
            watcher (QFileSystemWatcher): File system watcher for monitoring file changes.
            file_change_count (int): The number of file changes detected.

        Methods:
            add_script_to_q(): Add a Nuke script to the list.
            remove_script_from_q(): Remove the selected Nuke scripts from the list.
            update_file_list(): Update the file list widget with the current list of Nuke scripts.
            clear_file_list(): Clear the list of Nuke scripts.
            run_render(): Runs the render of the nuke scripts in a separate thread.
            handle_render_update(script, exit_code, elapsed_time): Called on signal recieved, updates the progress bar.
            handle_render_finish(): Called when render is complete, performs cleanup tasks.
            handle_render_cancelled(): Called when the rendered is cancelled by the user.
            get_estimated_times(render_times, items_left): Find the average(mean) time of each render to show the user an estimated finish time.
            get_write_info(): Reads the script as a text file and finds the write info through the text file.
            update(): method called on a timer to update the look of the list, primarily for the filename view change.
            handle_new_info_file(): Called when a new file is made in the designated folder. Used for updating progress bar.
            file_changed(): Called when a file changes in the designated folder.
    """


    def __init__(self, settings):
        """
        Initializes the main window of BNRQ application.

        Args:
            settings (Settings): An instance of the Settings class for managing application settings.
        """

        super().__init__()
       

        self.settings = settings
        self.settings.load_settings()
        self.file_paths = []
        self.file_info = {}
        self.py_render_script = r"./RenderScript.py"
        #careful using this value as the max workers, it can cause all the scripts to be rendered at once
        self.max_num_threads = os.cpu_count()

        self.continue_rendering = True
        self.done_rendering = False
        

        #update variables
        self.full_filepath_name = self.settings.full_filepath_name
        
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

        self.translator = FourCCTranslator()

        #update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(500)

        self.remove_timer = None

        #file watching stuff
        self.render_queue_folder = self.settings.render_queue_folder
        self.temp_folder = self.settings.temp_folder
        self.xml_filepath = os.path.join(self.temp_folder, "CurrentRenderScriptInfo.xml")

        if not QDir(self.temp_folder).exists():
            QDir().mkpath(self.temp_folder)
        elif os.path.exists(self.xml_filepath):
            os.remove(self.xml_filepath)

        self.directory = QDir(self.temp_folder)
        self.watcher = QFileSystemWatcher()
        self.watcher.addPath(self.directory.absolutePath())
        self.file_change_count = 0
        self.watcher.directoryChanged.connect(self.handle_new_info_file)
        self.watcher.fileChanged.connect(self.file_changed)

        self.wrong_write_node_name_list = []


    def add_script_to_q(self):
        """   
            This method opens a file dialog to allow the user to select a Nuke script file. If a file is selected, its path
            is added to the list of file paths in the instance variable `self.file_paths`. The method then calls the
            `update_file_list` method to refresh the file list displayed in the user interface.
        """
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 
                                                "Select File", 
                                                self.settings.folder_search_start, 
                                                "Nuke Scripts (*.nk)")
        if file_path:
            if file_path in self.file_paths:
                self.add_confirmation_box = QMessageBox.question(self, 'Warning', 'This file is already in the list. \
                                                             \nDo you still wish to add it?',
                                                             QMessageBox.Yes | QMessageBox.No,
                                                             QMessageBox.No)
                #self.add_confirmation_box.setStandardIcon(QMessageBox.Critical)

                if self.add_confirmation_box == QMessageBox.Yes:
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
            if item.text() in self.file_info:
                self.file_paths.remove(self.file_info[item.text()])
            else:
                self.file_paths.remove(item.text())
            self.file_list.takeItem(self.file_list.row(item))


    #could optimize this by not making it update the list every update call
    def update_file_list(self):
        """
            This method clears the file_list an then adds all the file_paths into the file_list. 
            Updating all the list to the latest files in the file_path list.
        """
        self.file_list.clear()

        if self.full_filepath_name:
                self.file_list.addItems(self.file_paths)
                self.file_info = {}     
        else:
            for file_path in self.file_paths:
                self.file_list.addItem(os.path.basename(file_path))
                self.file_info[os.path.basename(file_path)] = file_path 


    def clear_file_list(self, finish_clear = False):
        """
            This method updates file_paths to hold no list objects and then calls for the list
            to be updated. If the list count is above 5 then it prompts the user if they want to
            continue clearing the list. If the method call is from clearing the list after the render
            then the method skips any checks and just clears everything.

            Args: 
                finish_clear (Boolean): This argument tells the method whether the call to this method
                    is from the render being finished and clearing the list or if it was from the user. 
        """
        if not finish_clear:
            if len(self.file_paths) > 5:
                self.clear_confirmation_box = QMessageBox.question(self, 'Warning', 'You have a large number of files in the list. \
                                                                \nDo you still wish to clear the list?',
                                                                QMessageBox.Yes | QMessageBox.No,
                                                                QMessageBox.No)
                if self.clear_confirmation_box == QMessageBox.Yes:
                    self.file_paths = []
                    self.update_file_list()
            else:
                self.file_paths = []
                self.update_file_list()

        else:
            self.file_paths = []
            self.update_file_list()
        self.file_info = {}


    def run_render(self):
        """
        Executes the rendering process for the queued files.

        If there are no files in the queue, it displays a warning message and returns.
        Otherwise, it initializes the necessary variables and objects for rendering,
        including the error object, progress dialog, and render worker thread.
        """
        self.file_list.clearSelection()

        if not self.file_paths:
            QtWidgets.QMessageBox.warning(self, "Warning", "There are no files in the queue!")
            return
        
        if self.check_write_nodes():
            message_text = "The following scripts have the wrong write node name"
            for script in self.wrong_write_node_name_list:
                message_text += f"<br>{script}"
            message_text += "<br>Rendering will not happen"
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)
            message_box.setWindowTitle("Warning")
            message_box.setText(message_text)
            message_box.setStandardButtons(QMessageBox.Ok)
            message_box.exec_()
            return
        
        self.done_rendering = False
        
        self.settings.remove_temp_files()

        self.work_threads = QThread(self)
        self.total_script_count = len(self.file_paths)
        self.render_times = []
        self.progress = 0

        self.error_obj = ErrorCodes()
        
        self.progress_dialog = QtWidgets.QProgressDialog("Rendering scripts...", None, 0, len(self.file_paths), self)
        self.progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
        self.progress_dialog.setMinimumDuration(0)
        self.progress_dialog.setRange(0,self.total_script_count)
        self.progress_dialog.setValue(int(self.progress))
        self.progress_dialog.setLabelText(f"Rendering script {self.progress+1} of {self.total_script_count}"+
                                        f"\nEstimated Time: {self.get_estimated_time(self.render_times, self.total_script_count-self.progress)}")
        QtWidgets.QApplication.processEvents()

        self.remove_timer = time.time()
        
        self.nuke_render_worker = SeparateThread()
        self.nuke_render_worker.moveToThread(self.work_threads)

        if self.settings.render_nuke_open:
            self.work_threads.started.connect(partial(self.nuke_render_worker.render_script_list, self.file_paths))
        else:
            self.work_threads.started.connect(partial(self.nuke_render_worker.render_list, self.file_paths))
        self.nuke_render_worker.render_script_update.connect(self.handle_render_update)
        self.nuke_render_worker.render_done.connect(self.handle_render_finish)
        self.nuke_render_worker.update_gui.connect(self.update)
        self.progress_dialog.canceled.connect(self.nuke_render_worker.stop)
        self.nuke_render_worker.render_cancelled.connect(self.handle_render_cancelled) #this is added as a signal, maybe its not needed and just link it to the progress bar being cancelled?
        self.work_threads.start()


    def handle_render_update(self, script, exit_code, elapsed_time):
        """
        Handles updating the progress bar while application is rendering.

        If the given exit code indicates an error, the method terminates work threads,
        displays an error message box, and performs necessary cleanup.
        Otherwise, it handles the successful update by removing the script from the file paths and file list,
        updating the progress, and displaying the progress in the progress dialog.

        Args:
            script (str): The script being rendered.
            exit_code (int or None): The exit code of the render process. None if not available.
            elapsed_time (float): The elapsed time of the render process.
        """
        if self.error_obj.check_error_codes(exit_code):
            #self.nuke_render_worker.quit_rt()
            self.work_threads.terminate()
            error_box = QMessageBox()
            error_box.setIcon(QMessageBox.Critical)
            error_box.setText(self.error_obj.get_error_message(exit_code, script))
            error_box.exec()
            self.progress_dialog.close()
            QtWidgets.QApplication.processEvents()
            self.handle_render_finish()
        else:
            render_item = None
            if self.full_filepath_name:
                render_item = self.file_list.findItems(script, QtCore.Qt.MatchExactly)
            else:
                render_item = self.file_list.findItems(os.path.basename(script), QtCore.Qt.MatchExactly)

            self.file_paths.remove(script)
            self.file_list.takeItem(self.file_list.row(render_item[0]))
                        
            self.progress += 1
            self.render_times.append(elapsed_time)
            self.progress_dialog.setValue(int(self.progress))
            self.progress_dialog.setLabelText(f"Rendering script {self.progress+1} of {self.total_script_count}"+
                                        f"\nEstimated Time: {self.get_estimated_time(self.render_times, self.total_script_count-self.progress)}")
            QtWidgets.QApplication.processEvents()  


    def handle_render_finish(self):
        """
        Handles the rendering finishing. Performs final cleanups and quits the render thread.
        """
        self.done_rendering = True
        self.work_threads.quit()
        self.progress_dialog.setValue(100)
        #making double sure
        self.clear_file_list(True)
        self.progress_dialog.close()

    
    def handle_render_cancelled(self):
        """
        Called when the thread needs to be stopped (from user cancelling). 
        """
        self.work_threads.quit()
        self.progress_dialog.close()
          

    def get_estimated_time(self, render_times, items_left):
        """This method gets how much time is estimated for the render to complete. It does this by gathering an
            average of each render time and then multiplying it by the number of scripts left to render.

        Args:
            render_times (List[]): The list of times each script took to render
            items_left (): The count of scripts that have yet to be rendered

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


    #could potentially make the output look nicer    
    def get_write_info(self):
        """
        Retrieves and displays information about the selected write node in the UI.

        If no write node is selected, the method sets the write details text to an empty string and returns.
        Otherwise, it retrieves the selected script, extracts information related to the write node,
        and updates the write details text with the gathered information.
        """

        if not self.file_list.selectedItems():
            self.write_details.setText("")
            return
            
        index = self.file_list.row(self.file_list.selectedItems()[0])
        selected_script = open(self.file_paths[index], 'r').read()
        
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

        write_node_index = next((i for i, wn in enumerate(write_nodes) if self.settings.write_node_name in wn), None)

        if write_node_index is None:
            self.write_details.setText(f"<b>NO WRITE NODE BY {self.settings.write_node_name} EXISTS <i>FILLED OUT</i> IN THIS PROJECT!</b>")
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
            codec = "<br><b>Codec:</b> " + self.translator.get_codec(codec_four_cc)

        colorspace_line = f"<br><b>Colorspace:</b> {colorspace_type}" if colorspace_type else ""
        self.write_details.setText(f"<b>Output:</b> {os.path.basename(output_name)}"
                                    f"<br><b>File Type:</b> {file_type}"
                                    f"{extra_info}"
                                    f"{colorspace_line}"
                                    f"{codec}")
        

    def check_write_nodes(self):
        """
            Checks to see if there are any scripts missing the proper write node name.

            Returns:
                True if every script does not have the proper name. False if every script does not. 
        """
        self.wrong_write_node_name_list = []
        for script in self.file_paths:
            selected_script = open(script, 'r').read()
            write_node_pattern = r'Write\s*{\s*((?:.*\n)*?)\s*}'
            write_nodes = re.findall(write_node_pattern, selected_script)

            write_node_index = next((i for i, wn in enumerate(write_nodes) if self.settings.write_node_name in wn), None)
            if write_node_index is None:
                self.wrong_write_node_name_list.append(os.path.basename(script))
        return bool(self.wrong_write_node_name_list)

    def update(self):
        """
        Updates the application state based on the settings.

        If the current full file path name is different from the settings' full file path name,
        the method updates the full file path name and calls the update_file_list method to update the file list.
        """
        
        if str(self.full_filepath_name).lower() != str(self.settings.full_filepath_name).lower():
            self.full_filepath_name = self.settings.full_filepath_name
            self.update_file_list()
        QtWidgets.QApplication.processEvents()


    def handle_new_info_file(self):
        """
        Handles the processing of a new info file.

        If the rendering is already done or the specified time interval since the last removal has not elapsed,
        the method returns and exits the system. This is to catch any file being read twice

        Otherwise, it reads the XML files in the directory and extracts relevant information, such as the script name
        and execution time. The extracted information is then passed to the handle_render_update method.
        """

        if self.done_rendering or time.time() - self.remove_timer <= 0.01:
            return
            sys.exit()
        
        self.remove_timer = time.time()
        self.files = self.directory.entryList()
        #This loop reads all files that are xml
        for file in self.files:
            if file == "." or file == "..":
                continue
            file_path = os.path.join(self.directory.absolutePath(), file)
            #file_info = QFileInfo(file_path)
            if file_path.lower().endswith(".xml"):
                qfile = QFile(file_path)
                if qfile.open(QFile.ReadOnly | QFile.Text):
                    reader = QXmlStreamReader(qfile)

                    while not reader.atEnd():
                        reader.readNext()
                        if reader.isStartElement() and reader.name() == "Script":
                            if reader.readNextStartElement() and reader.name() == "Info":
                                attributes = reader.attributes()
                                script = attributes.value("name")
                                execute_time = float(attributes.value("execute_time"))
                                self.handle_render_update(script, None, execute_time)

                    qfile.close()


    def file_changed(self):
        """
        Handles a file being changed.
        """
        self.handle_new_info_file()

        """if self.file_change_count == 9:
            self.handle_new_info_file()
            self.file_change_count += 1
        elif self.file_change_count == 10:
            self.file_change_count = 0
        else:
            self.file_change_count += 1"""


