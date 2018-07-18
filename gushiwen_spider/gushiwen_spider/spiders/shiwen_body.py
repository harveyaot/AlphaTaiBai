# -*- coding: utf-8 -*-
import scrapy
import re
import pymongo

from scrapy.conf import settings

pat_id = re.compile('id=([\d]+)')
pat_src = re.compile('value=([\w]+)$')

class ShiwenBodySpider(scrapy.Spider):
    name = 'shiwen_body'
    allowed_domains = ['gushiwen.org']
    start_urls = ['http://gushiwen.org/']

    def __init__(self,):
        super(ShiwenBodySpider, self).__init__()
        self.client = pymongo.MongoClient(
            port=settings['MONGODB_PORT'],
            username=settings['MONGODB_USER'],
            password=settings['MONGODB_PWD'],
            authSource=settings['MONGODB_DB']
            )
        db = self.client[settings['MONGODB_DB']]
        self.shiwen = db[settings['MONGODB_COLLECTION_SHIWEN']]
        self.url = "http://www.gushiwen.org/shiwen2017/ajaxshiwencont.aspx?id=%s&value=%s"

    def start_requests(self,):
        for d in self.shiwen.find({'site_id':"7722"}):
            if d.get('hyi', None) is not None:
                continue
            else:
                site_id = d.get('site_id', None)
                if site_id is None:
                    continue
                yield scrapy.Request(self.url %(site_id, 'yi'))
                yield scrapy.Request(self.url %(site_id, 'zhu'))
                yield scrapy.Request(self.url %(site_id, 'shang'))

    def parse(self, response):
        obj1 = pat_id.search(response.url)
        obj2 = pat_src.search(response.url)
        if obj1 and obj2:
            site_id = obj1.group(1)
            src = obj2.group(1)
        else:
            return 
        self.shiwen.update_one({'site_id':site_id},
            {
                "$set":{
                    src: response.text
                }
            } 
        )


