import os
import sys
import json

class FourCCTranslator():
    def __init__(self):
        super().__init__()
        self.json_fcc = None
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        json_filepath = os.path.join(base_path, "FourCharacter-Codes.json")
        with open(json_filepath, "r") as settings_file:
            self.json_fcc = json.load(settings_file)


    def get_codec(self, key):
        if self.json_fcc[key] is None:
            return "<i>UNKNOWN CODEC</i>"
        return self.json_fcc[key]


    #need to re-do these methods
    def remove_codec(self, key):
        del self.four_cc_list[key]


    def add_codec(self, key, value):
        self.four_cc_list[key] = value