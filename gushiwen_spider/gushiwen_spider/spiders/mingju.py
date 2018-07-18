# -*- coding: utf-8 -*-
import scrapy
import re
from gushiwen_spider.items import MingJuItem

class MingJuSpider(scrapy.Spider):
    name = 'mingju'
    allowed_domains = ['gushiwen.org']
    start_urls = ['https://so.gushiwen.org/mingju/']

    def parse(self, response):
        sents = response.xpath("//div[@class='left']//div[@class='sons']//a[1]/text()")
        sent_hrefs =  response.xpath("//div[@class='left']//div[@class='sons']//a[1]/@href")
        srcs = response.xpath("//div[@class='left']//div[@class='sons']//a[2]/text()")
        srcs_hrefs =  response.xpath("//div[@class='left']//div[@class='sons']//a[2]/@href")
        for sent, sent_href, src, src_href in zip(sents, sent_hrefs, srcs, srcs_hrefs):
            item = MingJuItem()
            item['sent'] = sent.extract()
            item['sent_href'] = sent_href.extract()
            item['src'] = src.extract()
            item['src_href'] = src_href.extract()
            yield item

        for link in  response.xpath('//a[@class="amore"]/@href').extract():
            yield response.follow(link, callback=self.parse)
