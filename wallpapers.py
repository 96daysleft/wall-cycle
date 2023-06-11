import os
import praw
from PIL import Image
from io import BytesIO
import random
import requests
from config import Config
from reddit_helper import RedditHelper

class WallPapers:

    def __init__(self, config: Config):
        ## Set and create the bakgrounds dir
        self.wallpapers_dir = os.path.join(os.path.expanduser('~'), "Pictures/backgrounds")
        self.config =  config

        if not os.path.exists(self.wallpapers_dir):
            os.mkdir(self.wallpapers_dir)


    def get_all_wallpapers(self):
        files= [os.path.join(self.wallpapers_dir, fn) for fn in os.listdir(self.wallpapers_dir)
        if any(fn.endswith(ext) for ext in self.config.image_extensions)]
        files.sort(key=lambda x: os.path.getctime(os.path.join(self.wallpapers_dir, x)), reverse=True)
        return files
                     
    def download_image(self, url):
        filename = os.path.basename(url)
        file_exists=os.path.isfile(os.path.join(self.wallpapers_dir,filename))

        print(f"url: {url}")
        print(f"filename: {filename}")
        print(f"file_exists: {file_exists}")

        if not file_exists:             
            full_path = os.path.join(self.wallpapers_dir, filename)
            response = requests.get(url)

            print(f"status: {response.status_code}")

            if response.status_code >= 200 and response.status_code < 300:

                try:
                    print("checking image")
                    img = Image.open(BytesIO(response.content))
                    print("checking aspect ratio")
                    is_good_aspect_ratio = self.is_good_aspect_ratio(img.width,img.height)
                    print(f"{img.width}/{img.height}")
                    print(f"Is a good aspect ratio {is_good_aspect_ratio}")

                    if is_good_aspect_ratio:
                        print(f"downloading {filename}")
                        img.save(full_path)
                        return full_path
                    else:
                        return ""
                except Exception as e:
                    print(f"An error occurred: {e}")
                    return ""
            else:
                return ""
        else:
            return ""

    def get_submissions(self):
        reddit_helper = RedditHelper(self.config.client_id,self.config.client_secret,self.config.user_agent)
        posts = reddit_helper.get_submissions(self.config.search_sub_reddits,self.config.get_search_keyword(), self.config.time_filter,self.config.post_limit, self.config.sort)
        
        count=0
        download_imgs = []

        for post in posts:
            if post.url.endswith(self.config.image_extensions_tupple):
                count=count+1
                print(f"count: {count}")
                
                try:
                    url = (post.url)
                    img = self.download_image(url)
                    if img != "":
                        download_imgs.append(img)

                    print(f"download_count: {len(download_imgs)}")         
                    if len(download_imgs) >= int(self.config.image_num):
                        print("Gathered enough images")
                        break
                except Exception as e:
                    print(f"url: {url}")
                    print(f"An error occurred: {e}")

        print('Done')
        return download_imgs
     
    def set_wallpaper(self,fullPath):
        command = "gsettings set org.cinnamon.desktop.background picture-uri "
        image_path = 'file://%s' % os.path.abspath(fullPath)
        os.system('%s "%s"' % (command, image_path))

    def is_good_aspect_ratio(self, width, height):
        ratio = abs(width/height)
        return True if 1.5 <= ratio <= 1.8 else False

    def get_wallpaper(self):
        if self.config.pull_new_images :
            print("Setting new back grounds")
            files = self.get_submissions()
            print(len(files))
            if len(files) <= 0:
                files = self.get_all_wallpapers()
        else:
            files = self.get_all_wallpapers()
            print("Choosing from the pile")
        
        file = random.choice(files)
        self.set_wallpaper(file)