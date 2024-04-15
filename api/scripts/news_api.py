from newsapi import NewsApiClient
import mysql.connector
from datetime import datetime

def fetch_soccer_news():
    # API key for accessing the NewsAPI
    news_api = NewsApiClient(api_key='83844c06a9884370a3a1c4119ffe0764')

    all_articles = news_api.get_everything(q='cricket',
        sources='espn, sky-sports',
        domains='espn.com, skysports.com',
        language='en',
        sort_by='relevancy',
        page=2)
    
    return all_articles

# Example usage
soccer_news = fetch_soccer_news()
date_format = "%Y-%m-%dT%H:%M:%SZ"
connection = mysql.connector.connect(
    host='localhost',  # Name of the MySQL container in the Docker network
    port='10301',
    user='swiftsearch',
    password='swiftsearch',
    database='swiftsearch'
)
cursor = connection.cursor()
for article in soccer_news['articles']:
    
    sql = "INSERT INTO sports_news (title, author, content, source, url, published_at) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (article['title'], article['author'], article['content'], article['source']['name'], article['url'] , datetime.strptime(article['publishedAt'], date_format))

    cursor.execute(sql, val)
    connection.commit()
    
# Close connection
cursor.close()
connection.close()
    

