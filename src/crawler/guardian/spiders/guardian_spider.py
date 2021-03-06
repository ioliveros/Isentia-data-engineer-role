import scrapy
import urllib
import configparser
import json
from guardian.items import GuardianItem
import re


class GuardianSpider(scrapy.Spider):
    name = 'guardian'
    allowed_domains = ['theguardian.com']
    start_urls = [
        'https://www.theguardian.com/au'
    ]
    custom_settings = {
        'DEPTH_LIMIT': 1
    }

    def __init__(self, category=None, *args, **kwargs):
        super(GuardianSpider, self).__init__(*args, **kwargs)

        # Read Readability API configuration
        config = configparser.ConfigParser()
        config.read('../../config.ini')
        self.parser_token = config.get('readability', 'token')

    def parse(self, response):
        for href in response.css("a::attr('href')"):
            link = href.extract()
            if re.search("^https://www.theguardian.com/[a-zA-Z\-/]+/2016/aug/", link):
                yield scrapy.Request(link, callback=self.parse_item)
            # Recursively parse the all the links in the page
            elif link.startswith('https://www.theguardian.com/'):
                yield scrapy.Request(link, callback=self.parse)

    def parse_item(self, response):
        url = 'https://www.readability.com/api/content/v1/parser?'
        url = url + 'token=' + self.parser_token + '&'
        url = url + 'url=' + response.url

        # Use Readability parser API to parse page
        with urllib.request.urlopen(url) as req:
            result = json.loads(req.read().decode('utf-8'))
            item = GuardianItem()
            item['title'] = result.get('title')
            item['author'] = result.get('author')
            item['excerpt'] = result.get('excerpt')
            item['url'] = result.get('url')
            item['date'] = result.get('date_published')
            item['content'] = result.get('content')
            yield item
