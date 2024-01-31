import configparser
import json
import sqlite3
import time
import datetime
from urllib.parse import urljoin
import praw
from tqdm import tqdm

ONE_MINUTE = 60

class redditScraper:

    def __init__(self):
        self.webscraper_limit = 100
        config = configparser.ConfigParser()
        config.read('./config/config.ini')
        ## add new section
        # config.add_section('section_name')
        # config.set('section_name', 'key_name', 'value')
        ## write into the config file
        # with open('config.ini', 'w') as config_file:
        #     config.write(config_file)
        self.subreddits = json.loads(config['FilteringOptions']['Subreddits'])
        stop_words = set(json.loads(config['FilteringOptions']['StopWords']))
        block_words = set(json.loads(config['FilteringOptions']['BlockWords']))
        self.exclude = stop_words | block_words

        self.conn = sqlite3.connect('reddit_posts.db')
        self.create_table()
    def create_table(self):
        # Create a table to store posts if it doesn't exist
        cursor = self.conn.cursor()
        # Name is the unique identifier for a submission
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                name TEXT PRIMARY KEY, 
                id TEXT,
                selftext TEXT,
                comments INTEGER,
                ups INTEGER,
                downs INTEGER,
                datetime NUMERIC,
                link TEXT
            )
        ''')
        self.conn.commit()

    def get_posts(self):
        # Scrape subreddits. Currently, it fetches additional data, only using title for now
        reddit = praw.Reddit(
            client_id="###",
            client_secret="###",
            user_agent="###",
        )
        # Get multiple subreddits
        subreddits = '+'.join(self.subreddits)
        new_bets = reddit.subreddit(subreddits).new(limit=self.webscraper_limit)

        for post in tqdm(new_bets, desc='Selecting relevant data from webscraper', total=self.webscraper_limit):
            yield post

    def insert_post(self, post):
        # Insert a post into the database
        cursor = self.conn.cursor()

        permalink = urljoin("https://www.reddit.com/", post.permalink)

        # Convert unix timestamps to 2024-01-28 17:21:07
        cursor.execute('''
            INSERT OR IGNORE INTO posts (name, id, selftext, comments, ups, downs, datetime, link) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (post.name, post.id, post.selftext, post.num_comments, post.ups, post.downs, datetime.datetime.utcfromtimestamp(post.created_utc), permalink))
        self.conn.commit()

    def start_collect(self):

        while True:
            print("Updating posts...")

            for post in self.get_posts():
                self.insert_post(post)

            print("Update complete. Waiting for the next update in 60 seconds...")
            # Sleep for 60s
            time.sleep(ONE_MINUTE)







scraper = redditScraper() #Create an instance of the redditScraper class

scraper.start_collect()
# Test function
# test_num = scraper.get_posts().post.permalink
# print(test_num)
# for post in scraper.get_posts():
#     print(post.permalink)
# Close the database connection (this won't be reached in the current example)
# scraper.conn.close()
