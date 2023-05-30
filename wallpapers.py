import os
import praw
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import random
import time
import requests
from datetime import datetime
from config import Config
from page_render import PageRender


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

    def get_random_keyword(self):
        keyword = random.choice(self.config.keywords )
        return self.convert_keyword(keyword)
                     
    def need_more_wallpapers(self):

        files = self.get_all_wallpapers()
        if len(files) <=5:
            return True
        
        file = files[0]
        timestamp = os.path.getmtime(os.path.join(self.wallpapers_dir, file))
        formatted_time = datetime.fromtimestamp(timestamp)
        print(f"timestamp: {formatted_time}")
        current_time = datetime.now()

        # Get the time difference
        time_diff = (current_time - formatted_time).total_seconds() / 60 /60

        # Print the time difference in seconds
        if time_diff <= 60:
            return False
        else:
            return True

    def download_image(self, url):
        file_extension = os.path.splitext(url)[1][1:]
        filename = os.path.basename(url)
        file_exists=os.path.isfile(os.path.join(self.wallpapers_dir,filename))
        file_extension_good=file_extension in self.config.image_extensions 

        print(f"url: {url}")
        print(f"file_extension: {file_extension}")
        print(f"filename: {filename}")
        print(f"file_exists: {file_exists}")
        print(f"file_extension_good: {file_extension_good}")

        if file_extension_good and not file_exists:             
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
        reddit = praw.Reddit(
            client_id = self.config.client_id,
            client_secret= self.config.client_secret,
            user_agent = self.config.user_agent)
        
        subreddit = reddit.subreddit(self.config.search_sub_reddits)
        search_keywords=self.config.get_all_keywords()
        
        try:
            print(f"Searching {self.config.search_sub_reddits} with query={search_keywords}, time_filter={self.config.time_filter}, limit={self.config.post_limit } sort={self.config.sort}")
            posts = subreddit.search(query=search_keywords, time_filter=self.config.time_filter, limit=self.config.post_limit , sort=self.config.sort)
        except praw.exceptions.PRAWException as e:
            print(f"An error occurred: {e}")

        count=0
        download_imgs = []

        for post in posts:        
            count=count+1
            print(f"count: {count}")
            try:
                url = (post.url)
                file_extension = os.path.splitext(url)[1][1:]

                if file_extension == "" and "imgur.com" in url:
                    print(f"Imgur image: {url}")
                    
                    response = PageRender.downloadCode(url)
                    soup = BeautifulSoup(response, "html.parser")
                    classname = "image-placeholder"
                    all_imgs = soup.find_all('img', class_=classname)
                    imgs = all_imgs[:5] if len(all_imgs) > 4 else all_imgs

                    for image in imgs:
                        img_src=image['src']
                        if img_src.startswith("//"):
                            img_src=f"https:{img_src}"

                        print(f"image src from imgur {img_src}")
                        img = self.download_image(img_src)
                        if img != "":
                            download_imgs.append(img)

                        
                else:
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
        if self.config.pull_only_from_new_imgs :
            print("Setting new back grounds")
            files = self.get_submissions()
            print(len(files))
            if len(files) <= 0:
                files = self.get_all_wallpapers()
        elif self.need_more_wallpapers():
            print("Getting backgrounds and  choosing from the pile")
            self.get_submissions()
            files = self.get_all_wallpapers()
        else:
            files = self.get_all_wallpapers()
            print("Choosing from the pile")
        
        file = random.choice(files)
        self.set_wallpaper(file)