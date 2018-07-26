# -*- coding: utf-8 -*-
import scrapy
import re
import pymongo
import json

from scrapy.conf import settings

#DATA_FILE = '../data/sent_pic_urls.txt'
DATA_FILE = "../data/sent_pic_urls_top1k.txt"

class ImageCrawlerSpider(scrapy.Spider):
    name = 'image'

    def __init__(self,):
        super(ImageCrawlerSpider, self).__init__()
        self.url_names = {}
        with open(DATA_FILE, 'r') as fin:
            for line in fin:
                name, urls =  line.strip().split('\t')
                urls = json.loads(urls)
                url_names = [(url,"%s_%s"%(name, i)) for i, url in enumerate(urls)]
                self.url_names.update(dict(url_names))

    def start_requests(self,):
        for url in self.url_names:
            yield scrapy.Request(url)

    def parse(self, response):
        name = self.url_names.get(response.url)
        url =  response.url
        suffix = url.split('.')[-1].lower().strip()
        ending = 'jpg'
        if suffix in ['png', 'jpg', 'jpeg']:
            ending = suffix
        else:
            print(ending)
        path = "%s/%s.%s" %('images_top1k', name, ending)
        with open(path, 'wb') as fout:
            fout.write(response.body)

