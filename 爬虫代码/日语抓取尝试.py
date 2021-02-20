import requests
from lxml import etree


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36",
           'Referer': 'https://www.baidu.com/s?'}
# 26184
for i in range(10):
    url = "https://www.koolearn.com/japdict/wd_1521{}.html".format(i)
    response = requests.get(url, headers=headers)
    html = response.content.decode()
    # print(html)
    html = etree.HTML(html)

    # 单词
    word = html.xpath('//div[@class="content-wrap"]/div/div[@class="word-title"]/h1/text()')[0] if html.xpath('//div[@class="content-wrap"]/div/div[@class="word-title"]/h1/text()') else ''
    print(word)

    # 发音
    pronounce = html.xpath('//div[@class="content-wrap"]/div//span[@class="word-spell"]/text()')[0] if html.xpath('//div[@class="content-wrap"]/div//span[@class="word-spell"]/text()') else ''
    print(pronounce)

    mean = html.xpath('//div[@class="content-wrap"]/div/div//dl//p/text()')
    # mean = html.xpath('/html/body/div/div/div/div//div/div/span/text()')
    # print(c_mean)
    str = ''
    for i in mean:
        str += i + '  '
    print(str)
    print("")


    # 音频
    video = html.xpath('//div[@class="content-wrap"]/div//span[@class="word-spell-audio"]/@data-url')[0] if html.xpath('//div[@class="content-wrap"]/div//span[@class="word-spell-audio"]/@data-url') else ''
    audio = "http:" + video
    print(audio)
