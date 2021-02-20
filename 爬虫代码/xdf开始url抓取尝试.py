import requests
from lxml import etree

url = "https://www.koolearn.com/dict/zimu_y_2.html"
# url = "https://www.koolearn.com/dict/zimu_a_1.html"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36",
           'Referer': 'https://www.baidu.com/s?'}

response = requests.get(url, headers=headers)
html = response.content.decode()
# print(html)
html = etree.HTML(html)

# rect = html.xpath('//div[@class="content-wrap"]/div[@class="left-content"]//div[@class="word-box"]/a')
# for i in rect:
#     word = i.xpath('./text()')[0]
#     src = i.xpath('./@href')[0]
#     src = "https://www.koolearn.com" + src
#     print(word)
#     print(src)
    # https://www.koolearn.com

next = html.xpath('//div[@class="content-wrap"]/div[@class="left-content"]/div[@class="i-page"]/a[last()]/@href')[0] if html.xpath('//div[@class="content-wrap"]/div[@class="left-content"]/div[@class="i-page"]/a[last()]/@href') else None
if next != None:
    url = "https://www.koolearn.com{}".format(next)
    print(url)