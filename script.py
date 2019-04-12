""" A script that scrapes various bits of data from subreddits
"""
import praw
import requests
import os
import sqlite3

SQ_LITE_FILE = "avexchange_data.db"

def init_database():
    if not os.path.isfile(os.path.dirname(os.path.abspath(__file__)) + "/{}".format(SQ_LITE_FILE)):
        print("creating db {}-".format(SQ_LITE_FILE))

    conn = sqlite3.connect(SQ_LITE_FILE)
    # reddit fullname as primary key
    conn.execute("""CREATE TABLE IF NOT EXISTS posts
                    (fullname TEXT PRIMARY KEY,
                    title TEXT NOT NULL, 
                    post_info TEXT NOT NULL)""")
    conn.commit()
    conn.close()

def get_urls(subreddit):
    """ scrape for certain keywords on a subreddit
    """
    print("getting urls from r/{}".format(subreddit))
    reddit = praw.Reddit("bot1")
    conn = sqlite3.connect(SQ_LITE_FILE)
    c = conn.cursor()
    # find posts in the last hour
    for submission in reddit.subreddit(subreddit).search("KZ OR Final OR Sennheiser OR Hifiman OR Pro", sort="new", time_filter="hour"):
        print("Title: {}".format(submission.title))
        print("Text: {}".format(submission.selftext))
        # c.execute("SELECT 1 FROM posts WHERE fullname=? LIMIT 1", (submission.fullname, ))
        # post_exists = c.fetchone() is not None
        # if not post_exists:
        try:
            c.execute("INSERT INTO posts VALUES({}, {}, {}) ESCAPE '|'"
            .format(submission.fullname, submission.title, submission.selftext))
        except sqlite3.IntegrityError as e:
            pass

        # print("--------\n")
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_database()
    get_urls("avexchange")

