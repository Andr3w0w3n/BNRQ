import os
import sys

from Settings import Settings

class ErrorCodes():
    #create the error codes so that they do not need to be created again
    

    def __init__(self):    
        super().__init__()
        self.settings = Settings(True)
        self.settings.load_settings()

        self.error_codes = {
            103: "There are no write nodes in this script",
            104: f"There is no write node with name \"{self.settings.write_node_name}\".",
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

    def get_error_message(self, output, script):
        if output == 404:
            return f"There was no script found named {script}."
        return self.error_codes[output]
    
    def check_error_codes(self, code):
        if code in self.error_codes:
            return True
        return False