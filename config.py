import json
import os
import sys
from sort_options import SortOptions
from time_options import TimeOptions

class Config:
    checks =[]

    def __init__(self, config_json_file):
        self.__config_json_file = config_json_file

        if not os.path.isfile(self.__config_json_file):
            print(f"Config file does not exist {self.__config_json_file}")
            sys.exit(1)

        with open(self.__config_json_file, "r") as f:
            config_json = json.load(f)

        self.client_id = config_json["client_id"]
        self.client_secret= config_json["client_secret"]
        self.reddit_user = config_json["user_agent"]
        self.pull_only_from_new_imgs = config_json["pull_only_from_new_imgs"]

        self.user_agent = f"script by u/{self.reddit_user}"

        #self.time_filter = config_json["filter"]["time"]
        #self.sort = config_json["filter"]["sort"]
        self.last_time_filter = None
        self.last_sort = None
        self.image_num = config_json["filter"]["imageCount"]
        self.image_extensions = config_json["filter"]["imageExtensions"]
        self.post_limit = config_json["filter"]["postLimit"]
        self.keywords = config_json["filter"]["keywords"]
        self.sub_reddits = config_json["filter"]["sub_reddits"]

        self.search_sub_reddits ='+'.join(self.sub_reddits)

        self.sort_options = SortOptions()
        self.time_options = TimeOptions()

    def get_all_keywords(self):
        return ' OR '.join(['(' + self.convert_keyword(item) + ')' if ' ' in item else item for item in self.keywords])
    
    def convert_keyword(self, keyword):
        return keyword.replace(' ', ' AND ')
    
    @property
    def sort(self):
        #self.last_time_filter = random.choice(self.sort_options)
        self.last_time_filter = self.sort_options.new
        return self.last_time_filter
    
    @property
    def time_filter(self):
        #self.last_sort = random.choice(self.time_options)
        self.last_sort = self.time_options.year
        return self.last_sort