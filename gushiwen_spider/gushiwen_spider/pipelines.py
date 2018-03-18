# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
from scrapy import log

class GushiwenSpiderPipeline(object):
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(
            port=settings['MONGODB_PORT'],
            username=settings['MONGODB_USER'],
            password=settings['MONGODB_PWD'],
            authSource=settings['MONGODB_DB']
            )
        db = self.client[settings['MONGODB_DB']]
        self.author = db[settings['MONGODB_COLLECTION_AUTHOR']]
        self.shiwen = db[settings['MONGODB_COLLECTION_SHIWEN']]
        # set the site_id as unique id
        self.shiwen.create_index([("site_id", pymongo.ASCENDING)],
                                background=True,
                                unique=True)
        # set author url as uniqe id
        self.author.create_index([("url", pymongo.ASCENDING)],
                                background=True,
                                unique=True)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if spider.name == 'author':
            log.msg("Insert author [%s]" % item['name'])
            self.author.insert(dict(item))
        elif spider.name == 'shiwen':
            log.msg("Insert shiwen [%s]" % item['title'])
            self.shiwen.insert(dict(item))
        return item
