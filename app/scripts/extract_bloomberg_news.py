import json
import mysql.connector
from datetime import datetime
import pytz

def format_date(date_string):
    if date_string is None:
        return None
    date_format = '%d %b %Y, %I:%M %p'
    date_time = datetime.strptime(date_string[:-4], date_format)

    # Define the timezone (replace 'IST' with your actual timezone)
    timezone = pytz.timezone('Asia/Kolkata')

    # Localize the datetime object with the timezone
    localized_time = timezone.localize(date_time)

    return localized_time

connection = mysql.connector.connect(
    host='localhost',  # Name of the MySQL container in the Docker network
    port='10301',
    user='swiftsearch',
    password='swiftsearch',
    database='swiftsearch'
)
with open('../data/bloomberg_quint_news.json', 'r') as file:
    data = json.load(file)
    for article in data:
        try:
            cursor = connection.cursor()
            sql = "INSERT INTO sites (title, description, author, source, url, published_at, scraped_at) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (article['title'], article['short_description'], article['author'], 'Bloomberg Quint', article['url'], format_date(article['date_created']), article['scraped_at'])
            cursor.execute(sql, val)
            connection.commit()
            cursor.close()
        except:
            continue
connection.close()
