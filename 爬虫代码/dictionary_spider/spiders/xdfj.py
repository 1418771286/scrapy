# -*- coding: utf-8 -*-
import scrapy
import os
from lxml import etree

from dictionary_spider.items import DictionaryJapan

class XdfjSpider(scrapy.Spider):
    name = 'xdfj'
    allowed_domains = ['koolearn.com']
    # start_urls = ['https://www.koolearn.com/japdict/wd_1.html']

    def start_requests(self):
        # 26185
        for i in range(26185):
            other_url = 'https://www.koolearn.com/japdict/wd_{}.html'.format(i + 1)
            yield scrapy.Request(other_url, callback=self.parse)

    def parse(self, response):
        # print(1)
        html = response.text
        html = etree.HTML(html)

        # 单词
        word = html.xpath('//div[@class="content-wrap"]/div/div[@class="word-title"]/h1/text()')[0] if html.xpath(
            '//div[@class="content-wrap"]/div/div[@class="word-title"]/h1/text()') else ''

        # 单词意思
        # mean = html.xpath('//div[@class="content-wrap"]/div/div//dl//p/text()') if html.xpath(
        #     '//div[@class="content-wrap"]/div/div//dl//p/text()') else ''
        # if mean == '':
        #     mean = html.xpath('//div[@class="content-wrap"]/div/div//dl//p/text()') if html.xpath('//div[@class="content-wrap"]/div/div//dl//p/text()') else ''
        mean = html.xpath('//div[@class="content-wrap"]/div/div//div//span[@class="hidden_3_1"]/text()') if html.xpath('//div[@class="content-wrap"]/div/div//div//span[@class="hidden_3_1"]/text()') else ''
        # print(2)
        if len(word) != 0 and len(mean) != 0:
            # print(1)
            item = DictionaryJapan()
            item['word'] = word

            # 意思
            str = ''
            for i in mean:
                str += i + '  '
            # print(str)
            item['mean'] = str

            # 发音
            pronounce = html.xpath('//div[@class="content-wrap"]/div//span[@class="word-spell"]/text()')[0] if html.xpath(
                '//div[@class="content-wrap"]/div//span[@class="word-spell"]/text()') else ''
            # print(pronounce)
            item['pronounce'] = pronounce

            # 音频
            video = html.xpath('//div[@class="content-wrap"]/div//span[@class="word-spell-audio"]/@data-url')[
                0] if html.xpath('//div[@class="content-wrap"]/div//span[@class="word-spell-audio"]/@data-url') else ''
            video_url = "http:" + video

            yield scrapy.Request(video_url, callback=self.parse_video, meta={'item': item})


    def parse_video(self, response):
        item = response.meta['item']
        # print(item)
        mp3 = response.body
        is_exist1 = os.path.exists('F:\JapanVideo\JapanVideo.{}mp3'.format(item['word']))
        if is_exist1:
            pass
        else:
            name = "F:\JapanVideo.{}mp3".format(item['word'])
            with open(name, 'wb') as f:
                f.write(mp3)
                print("存储音频")
        yield item
