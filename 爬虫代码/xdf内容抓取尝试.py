import requests
from lxml import etree

# 音频下载
def download(video):
    response = requests.get(video, headers=headers, stream = True)
    name = "F:\EnglishVideo\{}.mp3".format(word)
    # print(type(response.content))
    # with open(name, 'wb') as f:
    #     f.write(response.content)

for i in range(10):

    url = "https://www.koolearn.com/dict/wd_14375{}.html".format(i)
    # url = "https://www.koolearn.com/dict/zimu_a_1.html"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36",
               'Referer': 'https://www.baidu.com/s?'}

    response = requests.get(url, headers=headers)
    html = response.content.decode()
    # print(html)
    html = etree.HTML(html)

    # 单词解释
    means = html.xpath('//div[@class="content-wrap"]//div[@class="details-content"]//div/li')
    if len(means) != 0:
        mean = ''
        for i in means:
            key = i.xpath('./span/text()')[0] if i.xpath('.//span/text()') else ''
            value = i.xpath('./p/span/text()') if i.xpath('./p/span/text()') else ''
            # print(value)
            str = ''
            for i in value:
                str += i
            mean = mean+key+str+"  "

        # 单词
        word = html.xpath('//div[@class="content-wrap"]//div[@class="word-title"]/h1/text()')[0] if html.xpath(
            '//div[@class="content-wrap"]//div[@class="word-title"]/h1/text()') else None

        # 发音
        pronounce = ''
        rect = html.xpath(
            '//div[@class="content-wrap"]//div[@class="details-content"]//span[@class="word-spell"]/text()')
        for i in rect:
            pronounce += i + ' '

        # 其他形式
        style = ''
        styles = html.xpath('//div[@class="content-wrap"]//div[@class="details-content"]//div/p//span/text()')
        print(styles)

        big = [chr(i) for i in range(65, 91)]
        small = [chr(i) for i in range(97, 123)]
        for i in styles:
            if len(i) != 0:
                if i[0] not in small and i[0] not in big:
                    style += i + '  '

        print(word)
        print(mean)
        print(pronounce)
        print(style)

        # 音频
        rect = html.xpath('//div[@class="content-wrap"]//div[@class="details-content"]/div/span/@data-url')
        for video in  rect:
            video = 'http:{}'.format(video)
            print(video)
            download(video)





