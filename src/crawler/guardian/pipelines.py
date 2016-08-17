import pymongo
import configparser
import json
from scrapy.exceptions import DropItem


class GuardianPipeline(object):

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('../../config.ini')
        db_host = config.get('mongodb', 'host')
        self.client = pymongo.MongoClient(host=db_host)
        self.db = self.client.get_database('guardian')
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['id'])
            result = self.db.news.insert_one(dict(item))
            return item

    def close_spider(self, spider):
        self.client.close()
