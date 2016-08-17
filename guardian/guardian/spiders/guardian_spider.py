import scrapy
import urllib
import configparser


class GuardianSpider(scrapy.Spider):
    name = 'guardian'
    allowed_domains = ['theguardian.com']
    start_urls = [
        'https://www.theguardian.com/australia-news/'
    ]
    custom_settings = {
        'DEPTH_LIMIT': 1
    }

    def __init__(self, category=None, *args, **kwargs):
        super(GuardianSpider, self).__init__(*args, **kwargs)
        config = configparser.ConfigParser()
        config.read('../config.ini')
        self.parser_token = config.get('readability', 'token')

    def parse(self, response):
        for href in response.css("a::attr('href')"):
            link = href.extract()
            if link.startswith(
                    'https://www.theguardian.com/australia-news/2016/aug/'):
                yield scrapy.Request(link, callback=self.parse_item)
            elif link.startswith('https://www.theguardian.com/'):
                yield scrapy.Request(link, callback=self.parse)

    def parse_item(self, response):
        url = 'https://www.readability.com/api/content/v1/parser?'
        url = url + 'token=' + self.parser_token + '&'
        url = url + 'url=' + response.url
        with open('output.txt', 'a') as f:
            with urllib.request.urlopen(url) as req:
                f.write(url + '\n')
                f.write(req.read().decode('utf-8'))
