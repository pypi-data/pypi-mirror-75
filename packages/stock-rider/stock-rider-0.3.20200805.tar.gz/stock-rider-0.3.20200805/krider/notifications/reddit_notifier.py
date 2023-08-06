import logging
from datetime import datetime

import praw

from krider.bot_config import config


class RedditNotifier:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=config("REDDIT_CLIENT_ID"),
            client_secret=config("REDDIT_CLIENT_SECRET"),
            username=config("REDDIT_USER"),
            password=config("REDDIT_PASSWORD"),
            user_agent=config("REDDIT_USERAGENT"),
        )
        self.sub_reddit_name = config("SUB_REDDIT")
        self.sub_reddit = self.reddit.subreddit(self.sub_reddit_name)

    def send_notification(self, content):
        logging.info("Posting to reddit: {}".format(self.sub_reddit_name))
        self.sub_reddit.submit(
            title="{} : {}".format(
                content.get("title"), datetime.now().strftime("%Y-%m-%d")
            ),
            selftext=content.get("body"),
            flair_id=content.get("flair_id"),
        )


reddit_notifier = RedditNotifier()
