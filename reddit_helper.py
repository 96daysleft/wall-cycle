import praw


class RedditHelper:

    def __init__(self, client_id,client_secret,user_agent):
        self.reddit = praw.Reddit(
            client_id = client_id,
            client_secret= client_secret,
            user_agent = user_agent)

      
    def get_submissions(self,search_sub_reddits,search_keywords, time_filter, post_limit, sort):       
        subreddit = self.reddit.subreddit(search_sub_reddits)

        # format keyword list
        
        
        try:
            print(f"Searching {search_sub_reddits}")
            print(f"query={search_keywords}")
            print(f"time_filter={time_filter}")
            print(f"limit={post_limit }")
            print(f"sort={sort}")
            return subreddit.search(query=search_keywords, time_filter=time_filter, limit=post_limit , sort=sort)
        except praw.exceptions.PRAWException as e:
            print(f"An error occurred: {e}")
            return []

    
    