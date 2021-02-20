# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# 新东方爬虫
class Dictionary(scrapy.Item):
    #xindongfang爬虫
    # 单词名称
    word = scrapy.Field()
    # 单词意思
    mean = scrapy.Field()
    # 单词发音
    pronounce = scrapy.Field()
    # 单词形式
    style = scrapy.Field()

# 新东方日语词典
class DictionaryJapan(scrapy.Item):
    #xindongfang爬虫
    # 单词名称
    word = scrapy.Field()
    # 单词意思
    mean = scrapy.Field()
    # 单词发音
    pronounce = scrapy.Field()

# mdanci爬虫
class Dictionary911(scrapy.Item):
    # 单词名称
    name = scrapy.Field()
    # 单词意思
    views = scrapy.Field()
    # 单词发音
    pronounce = scrapy.Field()
    # 单词形式
    style = scrapy.Field()
