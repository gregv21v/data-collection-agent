from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.item import Item
import logging


from pymongo import MongoClient

#from dirbot.items import Website


class TestSpider(Spider):
    name = "test"
    allowed_domains = []
    start_urls = []

    def parse(self, response):
        '''
            I'm highjacking this, so I can do my own thing with it.
        '''
        self.logger.info("Bacon")
        self.logger.info("Bannanas")
        self.logger.info("Spinach")

        self.mongoClient = MongoClient(
            "mongodb://default:testing@ds147975.mlab.com:47975/craigslist"
        )

        self.db = self.mongoClient.get_default_database()
        self.db["test"].insert_one({"a": 0})

        return [Item()];
