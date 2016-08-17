import unittest
import pymongo
import configparser
from src.Resources.Search import search


class TestSearch(unittest.TestCase):

    def setUp(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        db_host = config.get('mongodb', 'host')
        self.client = pymongo.MongoClient(host=db_host)
        self.db = self.client.get_database('guardian')

        self.db.test.insert_many([
            {
                "url": "sdfsdf",
                "title": "Alice likes Bob",
                "content": "Alice likes Bob",
                "author": "Alice"
            },
            {
                "url": "sdfsald;fjk",
                "title": "Bob loves Alice",
                "content": "Bob loves Alice",
                "author": "Bob"
            },
            {
                "url": "lsadkfjal",
                "title": "Charlie hates Bob",
                "content": "Charlie hates Bob",
                "author": "Charlie"
            }
        ])
        self.db.test.create_index([
            ("title", pymongo.TEXT),
            ("content", pymongo.TEXT)
        ])

    def test_none(self):
        # Should not get any result from the following keywords
        result = search("adsfasdf", self.db.test)
        self.assertIsNone(result)
        result = search(["Alice", "Bob", "Charlie"], self.db.test)
        self.assertIsNone(result)

    def test_hit(self):
        # Should get exact result from the following keywords
        result = search("Alice", self.db.test)
        self.assertIsInstance(result, dict)
        self.assertEqual(
            len(result), 2, msg="Search for\"Alice\" should get 2 results.")
        result = search("Bob", self.db.test)
        self.assertIsInstance(result, dict)
        self.assertEqual(
            len(result), 3, msg="Search for\"Bob\" should get 3 results.")
        result = search("Charlie", self.db.test)
        self.assertIsInstance(result, dict)
        self.assertEqual(
            len(result), 1, msg="Search for\"Charlie\" should get 1 results.")

    def test_logic(self):
        # Should perform logical conjunction between keywords
        result = search(["Alice", "Bob"], self.db.test)
        self.assertIsInstance(result, dict)
        self.assertEqual(
            len(result), 2, msg="Search for lovers should get 2 results.")
        result = search(["Alice", "Charlie"], self.db.test)
        self.assertIsNone(result)

    def tearDown(self):
        self.db.test.delete_many({})
        self.client.close()
