# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class GushiwenSpiderItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass

class AuthorItem(Item):
    url = Field()
    image = Field()
    desc = Field()
    name = Field()
    like = Field()
    dynasty = Field()

class ShiwenItem(Item):
    title = Field()
    author = Field()
    dynasty = Field()
    body= Field()
    like = Field()
    tags = Field()
    style = Field() #shixing : shi, ci, qu, wen
    detail_url = Field()
    site_id = Field()
    fanyi = Field()
    zhushi = Field()
    shangxi = Field()
