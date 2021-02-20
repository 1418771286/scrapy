# -*- coding: utf-8 -*-
import scrapy
from lxml import etree
from dictionary_spider.items import Dictionary
import os
from dictionary_spider.settings import WORD_TYPE
from dictionary_spider.settings import VIDEO_PATH

BIG = [chr(i) for i in range(65, 91)]
SMALL = [chr(i) for i in range(97, 123)]

class XdfSpider(scrapy.Spider):
    name = 'xdf'
    allowed_domains = ['koolearn.com']
    start_urls = ['https://www.koolearn.com/dict/zimu_{}_1.html'.format(WORD_TYPE)]

    # def start_requests(self):
    #     other_url = 'https://www.koolearn.com/dict/zimu_{}_1.html'.format(WORD_TYPE)
    #     yield scrapy.Request(other_url, callback=self.parse)

    def parse(self, response):
        html = response.text
        html = etree.HTML(html)
        rect = html.xpath('//div[@class="content-wrap"]/div[@class="left-content"]//div[@class="word-box"]/a')
        for i in rect:
            # word = i.xpath('./text()')[0]
            src = i.xpath('./@href')[0]
            src = "https://www.koolearn.com" + src
            # print(word)
            # self.n += 1
            # print(self.n)
            yield scrapy.Request(src, callback=self.parse_content)

        next = html.xpath('//div[@class="content-wrap"]/div[@class="left-content"]/div[@class="i-page"]/a[last()]/@href')[
            0] if html.xpath(
            '//div[@class="content-wrap"]/div[@class="left-content"]/div[@class="i-page"]/a[last()]/@href') else None
        if next != None:
            url = "https://www.koolearn.com{}".format(next)
            yield scrapy.Request(url, callback=self.parse)


    def parse_content(self, response):
        html = response.text
        html = etree.HTML(html)
        # 创建对象
        item = Dictionary()

        # 单词
        word = html.xpath('//div[@class="content-wrap"]//div[@class="word-title"]/h1/text()')[0] if html.xpath(
            '//div[@class="content-wrap"]//div[@class="word-title"]/h1/text()') else ''
        # 单词解释
        means = html.xpath('//div[@class="content-wrap"]//div[@class="details-content"]//div/li')
        # 没有单词解释的直接跳过
        if len(means) != 0 and word != '':
            # 有'在单词里面的直接跳过，因为数据库会报错
            if "'" not in word:
                item['word'] = word
                mean = ''
                for i in means:
                    key = i.xpath('./span/text()')[0] if i.xpath('.//span/text()') else ''
                    value = i.xpath('./p/span/text()') if i.xpath('./p/span/text()') else ''
                    str = ''
                    for i in value:
                        str += i
                    mean = mean + key + str + "  "
                    item['mean'] = mean

                if "网络" not in mean:
                    # 发音
                    pronounce = ''
                    rect = html.xpath(
                        '//div[@class="content-wrap"]//div[@class="details-content"]//span[@class="word-spell"]/text()')
                    for i in rect:
                        pronounce += i + ' '
                    item['pronounce'] = pronounce

                    # 其他形式
                    style = ''
                    styles = html.xpath('//div[@class="content-wrap"]//div[@class="details-content"]//div/p[1]/span/text()')
                    for i in styles:
                        if len(i) != 0:
                            if i[0] not in SMALL and i[0] not in BIG:
                                style += i + '  '
                    item['style'] = style

                    # 音频
                    rect = html.xpath('//div[@class="content-wrap"]//div[@class="details-content"]/div/span/@data-url')
                    for video in rect:
                        video_url = 'http:{}'.format(video)
                        print(item)
                        # yield scrapy.Request(video_url, callback=self.parse_video, meta={'item':item})

    def parse_video(self, response):
        """存储音频"""
        item = response.meta['item']
        # print(item)
        mp3 = response.body
        # print(item['word'])
        # print(type(mp3))
        # 判断是否已经存在该文件，存在则另外创建一个,都存在跳过
        # 后缀1是英式，2是美式
        is_exist1 = os.path.exists('{}\{}\{}-1.mp3'.format(VIDEO_PATH, WORD_TYPE, item['word']))
        is_exist2 = os.path.exists('{}\{}\{}-2.mp3'.format(VIDEO_PATH, WORD_TYPE, item['word']))
        if is_exist1 and is_exist2:
            pass
        elif is_exist1:
            name = "{}\{}\{}-2.mp3".format(VIDEO_PATH, WORD_TYPE, item['word'] )
            with open(name, 'wb') as f:
                f.write(mp3)
                # print("存储成功")
        else:
            name = "{}\{}\{}-1.mp3".format(VIDEO_PATH, WORD_TYPE, item['word'] )
            with open(name, 'wb') as f:
                f.write(mp3)
                print("存储音频")
        # yield item