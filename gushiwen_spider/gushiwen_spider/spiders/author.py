# -*- coding: utf-8 -*-
import scrapy
from gushiwen_spider.items import AuthorItem 

class AuthorSpider(scrapy.Spider):
    name = 'author'
    allowed_domains = ['gushiwen.org']
    start_urls = ['http://so.gushiwen.org/authors/']

    def parse(self, response):
        item = AuthorItem()
        for a in response.xpath('//div[@class="sonspic"]'):
            item['url'] =  a.xpath('.//div[@class="divimg"]/a/@href').extract_first(),
            item['image'] = a.xpath('.//div[@class="divimg"]/a/img/@src').extract_first(),
            item['name'] = a.xpath('.//div[@class="divimg"]/a/img/@alt').extract_first(),
            item['desc'] = a.xpath('.//div[@class="cont"]/p[2]/text()').extract_first(),
            item['like'] =  a.xpath('.//div[@class="good"]//span/text()').extract_first(),
            yield item

        for link in  response.xpath('//div[@class="pages"]/a/@href').extract():
            yield response.follow(link, callback=self.parse)
