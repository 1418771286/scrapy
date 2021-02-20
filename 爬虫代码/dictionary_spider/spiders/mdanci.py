# -*- coding: utf-8 -*-


import scrapy
from lxml import etree

from dictionary_spider.items import Dictionary911


class MdanciSpider(scrapy.Spider):
    name = 'mdanci'
    allowed_domains = ['mdanci.911cha.com']
    # 最大是739页
    # start_urls = ['https://mdanci.911cha.com/lesson_1.html']

    def start_requests(self):

        for i in range(739):
            other_url = 'https://mdanci.911cha.com/lesson_{}.html'.format(i+1)
            yield scrapy.Request(other_url, callback=self.parse)

    def parse(self, response):
        # print(response.text)
        html_str = response.text
        html = etree.HTML(html_str)
        rect = html.xpath('//li[@class="arrow"]')
        # print(rect)
        for small_rect in rect:
            item = small_rect.xpath('//a/@href')[27:-28]
            # 取到每个单词的地址
            # print(item)
            # print(len(item))
            for i in item:
                src = i[2:]
                # print(src)
                word_url = "https://mdanci.911cha.com/{}".format(src)
                # print(word_url)
                yield scrapy.Request(word_url, callback=self.parse_word)

    def parse_word(self, response):

        n = 1

        # print(response.text)
        html = etree.HTML(response.text)
        # print(html)
        for result in html:
            if n % 2 == 1:
                n += 1
                continue
            item = Dictionary911()
            # print(1)
            # 获取名字
            name = result.xpath('//div[@class="cont"]/h2/text()')[0]
            if ' 'in name or "'" in name:
                # print(name)
                continue
            item['name'] = name
            # print(item)

            # 获取意思
            mean_str = ''
            rect = result.xpath('//div[5]/div/p')
            # print(word_type)
            for i in rect:
                mean_key = i.xpath('./span/text()')[0] if len(i.xpath('./span/text()')) else None
                mean_value = i.xpath('./text()')[0] if len(i.xpath('./text()')) > 0 else None
                # print(mean_key)
                # print(mean_value)
                str1 = str(mean_key) + "：" + str(mean_value)
                if "None" in str1 or "int." in str1:
                    # print(str1)
                    continue
                mean_str += ("*" + str1 + ".   ")
            # print(mean)
            item['views'] =  mean_str
            # print(item)

            # 获取发音
            pronounce = ''
            rect = result.xpath('//div[4]/div/h2//span/text()')
            for i in rect:
                pronounce += str(i).strip() + " "
                # print(str1)
            item['pronounce'] = pronounce
            # print(item)

            # 获取单词其他形式
            word_type = ''
            rect = result.xpath('//div[4]/div/p')
            for i in rect:
                type_value = i.xpath('./a/text()')[0] if len(i.xpath('./a/text()')) else None
                type_key = i.xpath('./text()')[0] if len(i.xpath('./text()')) > 0 else None
                str1 = str(type_key) + str(type_value)
                if "None" in str1:
                    # print(str1)
                    continue
                word_type += ("*" + str1 + "    ")
            item['style'] = word_type
            # print(item)
            yield item

if __name__ == '__main__':

    pass


