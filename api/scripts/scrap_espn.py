import scrapy
import mysql.connector

class SoccerNewsSpider(scrapy.Spider):
    name = 'soccer_news'
    start_urls = ['https://www.espn.com/soccer/story/_/id/38196464/how-var-decisions-affect-premier-league-club-2023-24']

    def parse(self, response):
        # Extracting news article links
        news_links = response.css('a.story-link')
        for link in news_links:
            article_url = link.css('::attr(href)').get()
            if article_url.startswith('/'):
                article_url = 'https://www.espn.com' + article_url  # Prepend missing scheme
            yield scrapy.Request(url=article_url, callback=self.parse_article)

    def parse_article(self, response):
        # Extracting details from the news article
        title = response.css('h1::text').get()
        content = ' '.join(response.css('div.article-body p::text').getall())
        source = 'ESPN'
        url = response.url
        published_at = response.css('span.timestamp span::text').get()
        
        connection = mysql.connector.connect(
            host='localhost',  # Name of the MySQL container in the Docker network
            port='10301',
            user='swiftsearch',
            password='swiftsearch',
            database='swiftsearch'
        )
        # Insert data into MySQL database
        cursor = connection.cursor()
        sql = "INSERT INTO sports_news (title, content, source, url, published_at) VALUES (%s, %s, %s, %s, %s)"
        val = (title, content, source, url , published_at)
        cursor.execute(sql, val)
        connection.commit()
        
        # Close connection
        cursor.close()
        connection.close()
