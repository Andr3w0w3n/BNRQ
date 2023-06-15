import os
import sys
import json

class FourCCTranslator():
    def __init__(self):
        """
        Initializes object by obtaining the json file and loading it into json_fcc to be read
        """
        super().__init__()
        self.json_fcc = None
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        json_filepath = os.path.join(base_path, "FourCharacter-Codes.json")
        with open(json_filepath, "r") as settings_file:
            self.json_fcc = json.load(settings_file)


    def get_codec(self, key):
        """
        This method returns the full codec name associated with the Key

        Args: 
            key (str): the 4 character code for a codec name
        """
        if key in self.json_fcc:
            return self.json_fcc[key]
        return "<i>UNKNOWN CODEC</i>"
        

    #need to re-do these methods
    def remove_codec(self, key):
        """
        This method allows access to remove a codec from the dictionary, currently not in use

        Args:
            key (str): the 4 character code for a codec name
        """
        del self.four_cc_list[key]


    def add_codec(self, key, value):
        """
        This method allows access to add a codec to the dictionary, currently not in use

        Args:
            key (str): the 4 character code for a codec name
            value (str): the full name of the codec to be associate with the key
        """
        self.four_cc_list[key] = value