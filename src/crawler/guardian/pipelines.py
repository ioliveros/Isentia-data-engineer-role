import pymongo
import configparser
import json
from scrapy.exceptions import DropItem
import html2text


class GuardianPipeline(object):

    def __init__(self):
        # Filter the duplicate item
        self.ids_seen = set()

    def open_spider(self, spider):
        # Read MongoDB connection from config file
        config = configparser.ConfigParser()
        config.read('../../config.ini')
        db_host = config.get('mongodb', 'host')
        self.client = pymongo.MongoClient(host=db_host)
        self.db = self.client.get_database('guardian')

    def process_item(self, item, spider):
        if item['url'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            item['content'] = html2text.html2text(item['content'])
            self.ids_seen.add(item['url'])
            result = self.db.news.insert_one(dict(item))
            return item

    def close_spider(self, spider):
        self.client.close()
