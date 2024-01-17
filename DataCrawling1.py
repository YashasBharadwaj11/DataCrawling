import scrapy
from selenium import webdriver
from scrapy.selector import Selector
from datetime import datetime, timedelta

class TOISpider(scrapy.Spider):
    name = 'toi_spider'
    start_urls = ['https://timesofindia.indiatimes.com/topic/Accident/news']

    def parse(self, response):
        current_datetime = datetime.now()

        for article_link in response.css('span.title a::attr(href)').extract():
            yield scrapy.Request(article_link, callback=self.parse_article, meta={'current_datetime': current_datetime})

    def parse_article(self, response):
        current_datetime = response.meta.get('current_datetime')

        title = response.css('h1::text').get().strip()
        article_date_str = response.css('div.publish_on::text').get().strip()

        try:
            article_date = datetime.strptime(article_date_str, '%d %b %Y, %H:%M')
            if current_datetime - timedelta(hours=24) <= article_date <= current_datetime:
                yield {'title': title, 'link': response.url}
        except Exception as e:
            self.log(f"Error processing article: {title} - {response.url}")
            self.log(f"Error details: {e}")
            self.log("HTML content of the article page:")
            self.log(response.text)

# Use the following command to run the Scrapy spider:
# scrapy runspider your_spider_script_name.py -o output.json
