import os
import sys
import appdirs
import json

from blyzer.common.singleton import Singleton

APP_NAME = "blyzer"

DEFAUL_SETTINGS = {
    "protocol": "tcp",
    "ip": "192.168.1.18",
    "port": 1217,
    "secret_key": "zec7wiuSuf9naix",
    "tcp_client_buffer_size": 1048576,
    "upload_buffer_max_size": 65536,
    "color_unknown": [134, 89, 182],
    "max_detection_targets": 3,
    "keypoints_confidence_threshold":0.5,
    "video_extension": "mp4",
    "position_filter_type":"moving_average",
    "position_filter_params":[5],
    "bounding_box":False,
    "show_trajectory":False,
    "skeleton":True,
    "show_name": False,
    "show_state": False,
    "show_type": True,
    "show_rate": True,
    "project": "Vienna"
}


class BlyzerSettings(object, metaclass=Singleton):
    __settings = None

    def __init__(self):
        pass

    def getParam(self, key:str, default_value = None):
        if self.__settings is None:
            self._load_setting()
        if key not in self.__settings.keys():
            self.setParam(key, default_value)
        return self.__settings.get(key, default_value)

    def setParam(self, key:str, value, force=True):
        if key in self.__settings.keys() or force:
            self.__settings[key] = value
            self._save_setting()
            return True
        else:
            return False

    def _load_setting(self):
        settigs_filename = BlyzerSettings.get_settings_filename()
        if not os.path.exists(settigs_filename):
            self._create_default_settings_file()
        try:
            with open(settigs_filename, 'r', encoding='utf-8') as file:
               self.__settings = json.load(file)
        except:
            print("Error: some troubles with configuration")
        pass

    def _create_default_settings_file(self):
        settigs_filename = BlyzerSettings.get_settings_filename()
        os.makedirs(os.path.dirname(settigs_filename), exist_ok=True)
        with open(settigs_filename, 'w', encoding='utf-8') as file:
            json.dump(DEFAUL_SETTINGS, file, indent=2, sort_keys=True)

    def _save_setting(self):
        settigs_filename = BlyzerSettings.get_settings_filename()
        os.makedirs(os.path.dirname(settigs_filename), exist_ok=True)
        with open(settigs_filename, 'w', encoding='utf-8') as file:
            json.dump(self.__settings, file, indent=2, sort_keys=True)

    @staticmethod
    def get_settings_filename():
        return os.path.join(appdirs.user_config_dir(APP_NAME, False), "settings.json")

if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')))
    print(BlyzerSettings.get_settings_filename())
    blset = BlyzerSettings().getParam("protocol")
    print(blset)
