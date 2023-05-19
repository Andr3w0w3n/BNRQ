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