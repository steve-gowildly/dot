import pymongo
from deeplearning_settings import GlobalSettings


class MongoPipeline(object):

    collection_name = 'items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI', GlobalSettings.MONGO_URI),
            mongo_db=crawler.settings.get('MONGO_DATABASE', GlobalSettings.DATABASE_PAGES)
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if self.db[self.collection_name].find({'_id': item['_id']}).limit(1).count() == 0:
            self.db[self.collection_name].insert(dict(item))

        return item
