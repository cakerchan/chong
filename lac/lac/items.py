# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LacItem(scrapy.Item):
    title = scrapy.Field()
    article = scrapy.Field()
    des = scrapy.Field()
    img = scrapy.Field()
    datime = scrapy.Field()
    category = scrapy.Field()
    image_urls = scrapy.Field()
