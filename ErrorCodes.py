import os
import sys

from Settings import Settings

class ErrorCodes():
    #create the error codes so that they do not need to be created again

    """
        A class that defines error codes and provides error messages.

        Attributes:
            settings (Settings): The Settings object.
            error_codes (dict): A dictionary that maps error codes to their corresponding error messages.
            nuke_error_messages (dict): A dictionary that maps specific Nuke error codes to their error messages.

        Methods:
            __init__(): Initializes the ErrorCodes object.
            get_error_message(output, script): Returns the error message based on the provided output code and script name.
            check_error_codes(code): Checks if the provided code exists in the error_codes dictionary.
    """
    

    def __init__(self):    
        """
            Initialization method.

            Sets up error code dictionary.
        """
        super().__init__()
        self.settings = Settings()
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
        """
        Retrieves the error message based on the provided output code and script name.

        Args:
            output (int): The output code.
            script (str): The script name.

        Returns:
            str: The corresponding error message.

        """
        if output == 404:
            return f"There was no script found named {script}."
        return self.error_codes[output]
    
    def check_error_codes(self, code):
        """
        Checks if the provided code exists in the error_codes dictionary.

        Args:
            code (int): The error code to check.

        Returns:
            bool: True if the code exists, False otherwise.

        """
        if code is None:
            return False
        elif code in self.error_codes:
            return True
        return False