import pymongo
import configparser
import json


class GuardianPipeline(object):

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('../config.ini')
        self.db_host = config.get('mongodb', 'host')

    def process_item(self, item, spider):
        
        return item
