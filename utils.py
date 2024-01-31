import sqlite3
import time
import datetime


def get_time():
    time_str = time.strftime("%m{}%d{}%Y{}  %X")
    return time_str.format(".", ".", "  ")


def get_conn():
    conn = sqlite3.connect('reddit_posts.db')
    cursor = conn.cursor()
    return conn, cursor


def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()


# Simplify query process
def query(sql, *args):
    """

    :param sql:
    :param args:
    :return:
    """
    conn, cursor = get_conn()
    cursor.execute(sql, args)
    res = cursor.fetchall()
    close_conn(conn, cursor)
    return res


def get_posts_today():
    # Count the number of posts for today
    today = datetime.datetime.utcnow().date()
    conn, cursor = get_conn()
    cursor.execute('''
        SELECT COUNT(*) FROM posts
        WHERE DATE(datetime) = ?
    ''', (today,))
    result = cursor.fetchone()
    return result[0] if result else 0

def get_comments_today():
    today = datetime.datetime.utcnow().date()
    conn, cursor = get_conn()
    cursor.execute('''
        SELECT SUM(comments) FROM posts
        WHERE DATE(datetime) = ?
    ''', (today,))
    result = cursor.fetchone()
    return result[0] if result else 0

def get_ups_today():
    today = datetime.datetime.utcnow().date()
    conn, cursor = get_conn()
    cursor.execute('''
        SELECT SUM(ups) FROM posts
        WHERE DATE(datetime) = ?
    ''', (today,))
    result = cursor.fetchone()
    return result[0] if result else 0

def get_downs_today():
    today = datetime.datetime.utcnow().date()
    conn, cursor = get_conn()
    cursor.execute('''
        SELECT SUM(downs) FROM posts
        WHERE DATE(datetime) = ?
    ''', (today,))
    result = cursor.fetchone()
    return result[0] if result else 0

def get_counts_per_hour(column):
    today = datetime.datetime.utcnow().date()
    conn, cursor = get_conn()

    counts_per_hour = [0] * 24  # Initialize counts for each hour to 0

    for hour in range(24):
        start_time = datetime.datetime.combine(today, datetime.time(hour, 0, 0))
        end_time = datetime.datetime.combine(today, datetime.time(hour, 59, 59))

        cursor.execute(f'''
            SELECT SUM({column}) FROM posts
            WHERE datetime >= ? AND datetime <= ?
        ''', (start_time, end_time))

        result = cursor.fetchone()
        counts_per_hour[hour] = result[0] if result else 0

    return counts_per_hour

def get_comments_per_hour():
    return get_counts_per_hour('comments')

def get_ups_per_hour():
    return get_counts_per_hour('ups')

def get_downs_per_hour():
    return get_counts_per_hour('downs')


def get_selftext_today():
    conn, cursor = get_conn()
    cursor.execute('''
         SELECT selftext FROM posts
         WHERE DATE(datetime) = DATE('now')
     ''')
    result = cursor.fetchall()
    return result if result else 0

# def avg_comment_pasthour(self):
#     cursor = self.conn.cursor()
#     cursor.execute('''
#         SELECT AVG(comments) FROM posts
#         WHERE datetime >= datetime('now', '-1 hour')
#     ''')
#     result = cursor.fetchone()
#     return result[0] if result else 0
#
# def avg_comment_day(self):
#     cursor = self.conn.cursor()
#     cursor.execute('''
#         SELECT AVG(comments) FROM posts
#         WHERE DATE(datetime) = DATE('now')
#     ''')
#     result = cursor.fetchone()
#     return result[0] if result else 0
#
# def avg_ups_pasthour(self):
#     cursor = self.conn.cursor()
#     cursor.execute('''
#         SELECT AVG(ups) FROM posts
#         WHERE datetime >= datetime('now', '-1 hour')
#     ''')
#     result = cursor.fetchone()
#     return result[0] if result else 0
#
# def avg_ups_day(self):
#     cursor = self.conn.cursor()
#     cursor.execute('''
#         SELECT AVG(ups) FROM posts
#         WHERE DATE(datetime) = DATE('now')
#     ''')
#     result = cursor.fetchone()
#     return result[0] if result else 0
#
# def avg_downs_pasthour(self):
#     cursor = self.conn.cursor()
#     cursor.execute('''
#         SELECT AVG(downs) FROM posts
#         WHERE datetime >= datetime('now', '-1 hour')
#     ''')
#     result = cursor.fetchone()
#     return result[0] if result else 0
#
# def avg_downs_day(self):
#     cursor = self.conn.cursor()
#     cursor.execute('''
#         SELECT AVG(downs) FROM posts
#         WHERE DATE(datetime) = DATE('now')
#     ''')
#     result = cursor.fetchone()
#     return result[0] if result else 0
#
# def avg_comment_fixhour(self):
#     cursor = self.conn.cursor()
#     cursor.execute('''
#         SELECT strftime('%H', datetime) AS hour, ROUND(AVG(comments), 1) AS avg_comments
#         FROM posts
#         WHERE DATE(datetime) = DATE('now')
#         GROUP BY hour
#     ''')
#     results = cursor.fetchall()
#
#     avg_comments_per_hour = [{'hour': str(hour).zfill(2), 'avg_comments': 0.00} for hour in range(24)]
#
#     # Update the list with actual values
#     for hour, avg_comments in results:
#         avg_comments_per_hour[int(hour)]['avg_comments'] = avg_comments
#
#     return avg_comments_per_hour
#
# def avg_ups_fixhour(self):
#     cursor = self.conn.cursor()
#     cursor.execute('''
#         SELECT strftime('%H', datetime) AS hour, ROUND(AVG(ups),1) AS avg_ups
#         FROM posts
#         WHERE DATE(datetime) = DATE('now')
#         GROUP BY hour
#     ''')
#     results = cursor.fetchall()
#     avg_ups_per_hour = [{'hour': str(hour).zfill(2), 'avg_ups': 0.00} for hour in range(24)]
#
#     # Update the list with actual values
#     for hour, avg_ups in results:
#         avg_ups_per_hour[int(hour)]['avg_ups'] = avg_ups
#
#     return avg_ups_per_hour
#
# def avg_downs_fixhour(self):
#     cursor = self.conn.cursor()
#     cursor.execute('''
#         SELECT strftime('%H', datetime) AS hour, ROUND(AVG(downs),1) AS avg_downs
#         FROM posts
#         WHERE DATE(datetime) = DATE('now')
#         GROUP BY hour
#     ''')
#     results = cursor.fetchall()
#     avg_downs_per_hour = [{'hour': str(hour).zfill(2), 'avg_downs': 0.00} for hour in range(24)]
#
#     # Update the list with actual values
#     for hour, avg_downs in results:
#         avg_downs_per_hour[int(hour)]['avg_downs'] = avg_downs
#
#     return avg_downs_per_hour
#
# def selftext_pasthour(self):
#     cursor = self.conn.cursor()
#     cursor.execute('''
#          SELECT selftext FROM posts
#          WHERE datetime >= datetime('now', '-1 hour')
#      ''')
#     result = cursor.fetchall()
#     return result if result else 0
#

#
# def top5_commented_selftext_pasthour(self):
#     cursor = self.conn.cursor()
#     cursor.execute('''
#          SELECT selftext FROM posts
#          WHERE datetime >= datetime('now', '-1 hour')
#          ORDER BY comments DESC LIMIT 5
#      ''')
#     result = cursor.fetchall()
#     return result if result else 0
#
# def top5_ups_selftext_past_hour(self):
#     cursor = self.conn.cursor()
#     cursor.execute('''
#          SELECT selftext FROM posts
#          WHERE datetime >= datetime('now', '-1 hour')
#          ORDER BY ups DESC LIMIT 5
#      ''')
#     result = cursor.fetchall()
#     return result if result else 0
#
# def get_latest5_selftext_past_hour(self):
#     cursor = self.conn.cursor()
#     cursor.execute('''
#          SELECT selftext FROM posts
#          WHERE datetime >= datetime('now', '-1 hour')
#          ORDER BY datetime DESC LIMIT 5
#      ''')
