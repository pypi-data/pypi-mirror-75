import logging
from datetime import datetime

import praw

from krider.bot_config import config

REDDIT_CLIENT_ID = config("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = config("REDDIT_CLIENT_SECRET")
REDDIT_USER = config("REDDIT_USER")
REDDIT_PASSWORD = config("REDDIT_PASSWORD")
REDDIT_USERAGENT = config("REDDIT_USERAGENT")
SUB_REDDIT = config("SUB_REDDIT")


class RedditNotifier:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            username=REDDIT_USER,
            password=REDDIT_PASSWORD,
            user_agent=REDDIT_USERAGENT
        )
        self.sub_reddit = self.reddit.subreddit(SUB_REDDIT)

    def send_notification(self, content):
        logging.info(content.get('body'))
        self.sub_reddit.submit(
            title="{} : {}".format(content.get('title'), datetime.now().strftime("%Y-%m-%d")),
            selftext=content.get('body'),
            flair_id=content.get('flair_id')
        )


reddit_notifier = RedditNotifier()
