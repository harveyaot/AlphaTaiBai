# -*- coding: utf-8 -*-
import scrapy
import re
from gushiwen_spider.items import ShiwenItem

pat = re.compile("default_4A([\d]{1})A")

num_style_mapping = {
    '1': "shi",
    '2': "ci",
    '3': 'qu',
    '4': 'wen'
}

def get_style(url):
    style = ""
    res = pat.search(url)
    if res:
        num = res.group(1)
        style = num_style_mapping.get(num, "")
    return style
        

class ShiwenSpider(scrapy.Spider):
    name = 'shiwen'
    allowed_domains = ['gushiwen.org']
    start_urls = ['http://www.gushiwen.org/shiwen/default_4A1A1.aspx',
                'http://www.gushiwen.org/shiwen/default_4A2A1.aspx',
                'http://www.gushiwen.org/shiwen/default_4A3A1.aspx',
                'http://www.gushiwen.org/shiwen/default_4A4A1.aspx',
                ]

    def parse(self, response):
        for div in response.xpath('//div[@class="sons"]'):
            item = ShiwenItem()
            item['title'] = div.xpath(".//div/p[1]/a/b/text()").extract_first()
            item['author'] = div.xpath('.//div/p[@class="source"]/a[2]/text()').extract_first()
            item['dynasty'] = div.xpath('.//div/p[@class="source"]/a[1]/text()').extract_first()
            item['body'] = "\n".join(div.xpath('.//div[@class="contson"]/text()').extract())
            item['like'] = div.xpath('.//div[@class="good"]/a/span/text()').extract_first()
            if item['like'] is not None:
                item['like'] = item['like'].strip()
            item['tags'] = "\n".join(div.xpath('.//div[@class="tag"]/a/text()').extract())
            item['style'] = get_style(response.url)
            item['detail_url'] = div.xpath(".//div/p[1]/a/@href").extract_first()
            # 7 is length of prefix contson
            item['site_id'] = div.xpath('.//div[@class="contson"]/@id').extract_first()
            if item['site_id'] is None:
                continue
            else:
                item['site_id'] = item['site_id'][7:]
            yield item

        for link in  response.xpath('//div[@class="pages"]/a/@href').extract():
            yield response.follow(link, callback=self.parse)
