import json
import os
import sys

class Config:
    checks =[]

    def __init__(self, config_json_file):
        self.__config_json_file = config_json_file

        if not os.path.isfile(self.__config_json_file):
            print(f"Config file does not exist {self.__config_json_file}")
            sys.exit(1)

        with open(self.__config_json_file, "r") as f:
            config_json = json.load(f)

        self._wallpapers_path = config_json["wallpapersPath"]
        self._image_extensions:list[str] = config_json["imageExtensions"]

        if "~" in self._wallpapers_path:
            self._wallpapers_path = os.path.expanduser(self._wallpapers_path)

   
    @property
    def wallpapers_path(self):
        return self._wallpapers_path
   
    @property
    def image_extensions(self):
        return self._image_extensions