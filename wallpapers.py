import os
import random
from config import Config


class WallPapers:

    def __init__(self, config: Config):
        self.config =  config
        self.wallpapers_dir = config.wallpapers_path

        if not os.path.exists(self.wallpapers_dir):
            print(f"Wallpaper dir {self.wallpapers_dir} does not exist ")


    def get_all_wallpapers(self):
        files= [os.path.join(self.wallpapers_dir, fn) for fn in os.listdir(self.wallpapers_dir)
        if any(fn.endswith(ext) for ext in self.config.image_extensions)]
        files.sort(key=lambda x: os.path.getctime(os.path.join(self.wallpapers_dir, x)), reverse=True)
        return files
     
    def set_wallpaper(self,fullPath):
        command = "gsettings set org.cinnamon.desktop.background picture-uri "
        image_path = 'file://%s' % os.path.abspath(fullPath)
        os.system('%s "%s"' % (command, image_path))

    def choose_random_wallpaper(self):
        files = self.get_all_wallpapers()       
        file = random.choice(files)
        self.set_wallpaper(file)