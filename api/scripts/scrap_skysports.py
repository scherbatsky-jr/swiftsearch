import scrapy
import mysql.connector

class SoccerNewsSpider(scrapy.Spider):
    name = 'soccer_news'
    start_urls = ['https://www.skysports.com/football/news']

    def parse(self, response):
        # Extracting news article links
        news_links = response.css('a.sdc-site-tile__headline-link')
        show_more_button = response.css('button.sdc-site-load-more__button')
        print(response)
        if show_more_button:
            print("Show button was found")
        for link in news_links:
            article_url = link.css('::attr(href)').get()
            if article_url.startswith('/'):
                article_url = 'https://www.skysports.com' + article_url  # Prepend missing scheme
            yield scrapy.Request(url=article_url, callback=self.parse_article)
        
        show_more_button = response.css('button.sdc-site-load-more__button')
        # print("I reached here")
        # if show_more_button:
        #     print("I reached here again")
        #     ajax_url = show_more_button.attrib['data-ajax-url']
        #     yield scrapy.Request(url=ajax_url, callback=self.parse_more_content)

    def parse_more_content(self, response):
        # Extract news article links from the dynamically loaded content
        news_links = response.css('a.sdc-site-tile__headline-link')
        for link in news_links:
            article_url = link.css('::attr(href)').get()
            if article_url.startswith('/'):
                article_url = 'https://www.skysports.com' + article_url  # Prepend missing scheme
            yield scrapy.Request(url=article_url, callback=self.parse_article)

    def parse_article(self, response):
        # Extracting details from the news article
        title = response.css('span.sdc-article-header__long-title::text').get()
        content = ' '.join(response.css('div.sdc-article-body p::text').getall())
        source = 'Sky Sports'
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
