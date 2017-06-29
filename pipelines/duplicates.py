import pymongo
from bson.objectid import ObjectId
from scrapy.exceptions import DropItem
from deeplearning_settings import GlobalSettings


class DuplicatesPipeline(object):

    def __init__(self):
        self.client = pymongo.MongoClient(GlobalSettings.MONGO_URI)
        self.db = self.client[GlobalSettings.DATABASE_PAGES]

    def process_item(self, item, spider):
        document = self.client.db.collection.find_one({'_id': ObjectId(item._id)})

        if document is None:
            return item
        else:
            raise DropItem("Duplicate item found: %s" % item)
