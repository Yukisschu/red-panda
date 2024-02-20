import configparser
import json
import sqlite3
import time
import datetime
from urllib.parse import urljoin
import praw
from tqdm import tqdm

ONE_MINUTE = 60
COLLECT_LIMIT = 100


class RedditCollector:

    def __init__(self, table_name='posts'):
        self.collect_limit = COLLECT_LIMIT
        config = configparser.ConfigParser()
        config.read('./config/config.ini')
        self.subreddits = json.loads(config['FilteringOptions']['Subreddits'])
        self.conn = sqlite3.connect('reddit_posts.db')
        self.create_table(table_name)

    def create_table(self, table_name='posts'):
        cursor = self.conn.cursor()
        # Use submission_name as the unique identifier for a submission
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS {} (
                name TEXT PRIMARY KEY, 
                id TEXT,
                selftext TEXT,
                comments INTEGER,
                ups INTEGER,
                downs INTEGER,
                datetime NUMERIC,
                link TEXT
            )
        '''.format(table_name, ))
        self.conn.commit()

    def delete_post(self, name):
        cursor = self.conn.cursor()
        cursor.execute('''
            DELETE FROM posts WHERE name = ?
        ''', (name,))
        self.conn.commit()
        print(f"Post with name '{name}' deleted successfully.")

    def get_posts(self):
        reddit = praw.Reddit(
            client_id="###",
            client_secret="###",
            user_agent="###",
        )
        # Get multiple subreddits from different sources
        subreddits = '+'.join(self.subreddits)
        new_subreddits = reddit.subreddit(subreddits).new(limit=self.collect_limit)

        for post in tqdm(new_subreddits, desc='Collecting data', total=self.collect_limit):
            yield post

    def insert_post(self, post):
        # Insert a post into the database
        cursor = self.conn.cursor()
        permalink = urljoin("https://www.reddit.com/", post.permalink)
        # Convert unix timestamps to the format of 2024-01-28 17:21:07
        cursor.execute('''
            INSERT OR IGNORE INTO posts (name, id, selftext, comments, ups, downs, datetime, link) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (post.name, post.id, post.selftext, post.num_comments, post.ups, post.downs,
              datetime.datetime.utcfromtimestamp(post.created_utc), permalink))
        self.conn.commit()

    def start_collect(self):

        while True:
            print("Updating posts...")

            for post in self.get_posts():
                self.insert_post(post)

            print("Update complete. Waiting for the next update in 60 seconds...")
            time.sleep(ONE_MINUTE)


collector = RedditCollector()
collector.start_collect()
