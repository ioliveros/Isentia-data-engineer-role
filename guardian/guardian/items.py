# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GuardianItem(scrapy.Item):
    domain = scrapy.Field()
    url = scrapy.Field()
    author = scrapy.Field()
    excerpt = scrapy.Field()
    content = scrapy.Field()
    date = scrapy.Field()
    title = scrap.Field()
