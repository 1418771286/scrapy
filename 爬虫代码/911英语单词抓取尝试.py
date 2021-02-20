import requests
from lxml import etree
import json
from jsonpath import jsonpath


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36",
           'Referer': 'https://www.baidu.com/s?'}

"""获取每个单词的地址"""
# 最大是739页
# url = "https://mdanci.911cha.com/lesson_676.html"
#
# response = requests.get(url, headers=headers)
#
# html_str = response.content.decode()
# # print(html_str)
# html = etree.HTML(html_str)
# # print(html)
# rect = html.xpath('//li[@class="arrow"]')
# print(rect)
#
# for small_rect in rect:
#     item = small_rect.xpath('//a/@href')[27:-28]
#     #取到每个单词的地址
#     # print(item)
#     for i in item:
#         src = i[2:]
#         print(src)

"""获取每个单词的名字name、意思mean、发音pronounce、单词的其他形式word_type"""
url = 'https://mdanci.911cha.com/good.html'
response = requests.get(url, headers=headers)
html_str = response.content.decode()
# print(html_str)
html = etree.HTML(html_str)

"""单词的名字name"""
name = html.xpath('//div[@class="cont"]/h2/text()')[0]
print(name)

"""获取单词的发音"""
pronounce = ''
str1 = ''
rect = html.xpath('//div[4]/div/h2//span/text()')
for i in rect:
    str1 += str(i).strip() + " "
    # print(str1)


"""获取单词的意思mean"""
mean_str = ""
rect = html.xpath('//div[5]/div/p')
# print(word_type)
for i in rect:
    mean_key = i.xpath('./span/text()')[0] if len(i.xpath('./span/text()')) else None
    mean_value = i.xpath('./text()')[0] if len(i.xpath('./text()'))>0 else None
    # print(mean_key)
    # print(mean_value)
    str1 = str(mean_key) + "：" + str(mean_value)
    if "None" in str1:
        # print(str1)
        continue
    mean_str += ("*" + str1 + ".   ")
print(mean_str)

"""获取单词的其他形式word_type的列表"""
word_type = []
rect = html.xpath('//div[4]/div/p')
# print(word_type)
for i in rect:
    type_value = i.xpath('./a/text()')[0] if len(i.xpath('./a/text()')) else None
    type_key = i.xpath('./text()')[0] if len(i.xpath('./text()'))>0 else None
    str1 = str(type_key) + "：" + str(type_value)
    if "None" in str1:
        # print(str1)
        continue
    word_type.append(str1)
print(word_type)

"""获取单词的其他形式word_type的字典"""
# word_type = {}
# rect = html.xpath('//div[4]/div/p')
# # print(word_type)
# for i in rect:
#     type_value = i.xpath('./a/text()')[0] if len(i.xpath('./a/text()')) else None
#     type_key = i.xpath('./text()')[0] if len(i.xpath('./text()'))>0 else None
#     word_type[type_key] = type_value
#     # 根据键返回值，并删除键值对，不存正在返回第二个参数
#     word_type.pop(None, True)
# try:
#     # 根据值获取相应的键
#     a = list(word_type.keys())[list(word_type.values()).index(None)]
#     # print(a)
#     word_type.pop(a, True)
# except:
#     pass
# print(word_type)









