# -*- coding: utf-8 -*-
import pymysql
from dictionary_spider.settings import MYSQL_HOST, MYSQL_PORT, MYSQL_DB, MYSQL_PASSWORD, MYSQL_USER
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from dictionary_spider.spiders.mdanci import MdanciSpider
from dictionary_spider.spiders.xdf import XdfSpider
from dictionary_spider.settings import WORD_TYPE
from dictionary_spider.spiders.xdfj import XdfjSpider


class DictionarySpiderPipeline(object):

    def open_spider(self, spider):
        self.connection = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, db=MYSQL_DB, user=MYSQL_USER, password=MYSQL_PASSWORD)
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()

    def process_item(self, item, spider):

        if isinstance(spider, XdfjSpider):
            select_count_sql = "SELECT COUNT(1) FROM zjapan WHERE word = '{}'".format(item['word'])
            # 执行查询是否有相同名字的查询语句
            self.cursor.execute(select_count_sql)
            # 获取查询结果
            count = self.cursor.fetchone()[0]
            if count == 0:
                # 先将item转化成字典，然后用items()取出所有的键值对，再用zip将键和值分开，把所有的键放在keys，把所有的值放在values
                keys, values = zip(*dict(item).items())
                # print(123456)
                # spider.logger.into(keys)
                # 构建插入数据，','.join()用逗号把所有的键拼接再一起，因为值太长，所以不能直接拼接，下面values可以用keys代替
                insert_sql = "INSERT INTO zjapan ({}) VALUES ({})".format(
                    ','.join(keys), ','.join(['%s'] * len(keys))
                )
                # 执行sql
                self.cursor.execute(insert_sql, values)
                # 提交事务
                self.connection.commit()
                spider.logger.into('插入单词')
            else:
                # 否则重复了
                spider.logger.into('已有单词')

            return item

        if isinstance(spider, MdanciSpider):
            select_count_sql = "SELECT COUNT(1) FROM dictionary WHERE name = '{}'".format(item['name'])
            # 执行查询是否有相同名字的查询语句
            self.cursor.execute(select_count_sql)
            # 获取查询结果
            count = self.cursor.fetchone()[0]

            if count == 0:
                # 先将item转化成字典，然后用items()取出所有的键值对，再用zip将键和值分开，把所有的键放在keys，把所有的值放在values
                keys, values = zip(*dict(item).items())
                # print(123456)
                # spider.logger.into(keys)
                # 构建插入数据，','.join()用逗号把所有的键拼接再一起，因为值太长，所以不能直接拼接，下面values可以用keys代替
                insert_sql = "INSERT INTO dictionary ({}) VALUES ({})".format(
                    ','.join(keys), ','.join(['%s'] * len(keys))
                )
                # 执行sql
                self.cursor.execute(insert_sql, values)
                # 提交事务
                self.connection.commit()
                spider.logger.into('插入单词')

                # 否则重复了
            else:
                spider.logger.into('已有单词')

            return item

        if isinstance(spider, XdfSpider):
            select_count_sql = "SELECT COUNT(1) FROM {} WHERE word = '{}'".format(WORD_TYPE, item['word'])
            # 执行查询是否有相同名字的查询语句
            self.cursor.execute(select_count_sql)
            # 获取查询结果
            count = self.cursor.fetchone()[0]
            if count == 0:
                # 先将item转化成字典，然后用items()取出所有的键值对，再用zip将键和值分开，把所有的键放在keys，把所有的值放在values
                keys, values = zip(*dict(item).items())
                # print(123456)
                # spider.logger.into(keys)
                # 构建插入数据，','.join()用逗号把所有的键拼接再一起，因为值太长，所以不能直接拼接，下面values可以用keys代替
                insert_sql = "INSERT INTO {} ({}) VALUES ({})".format(WORD_TYPE,
                    ','.join(keys), ','.join(['%s'] * len(keys))
                )
                # 执行sql
                self.cursor.execute(insert_sql, values)
                # 提交事务
                self.connection.commit()
                spider.logger.into('插入单词')
            else:
                # 区分大小写插入不同的表
                select_sql = "SELECT word FROM {} where word = '{}'".format(WORD_TYPE,item['word'] )
                self.cursor.execute(select_sql)
                result = self.cursor.fetchone()
                word = result[0]
                if word != item['word']:
                    keys, values = zip(*dict(item).items())
                    insert_sql = "INSERT INTO other ({}) VALUES ({})".format(
                                     ','.join(keys), ','.join(['%s'] * len(keys))  )
                    self.cursor.execute(insert_sql, values)
                    # 提交事务
                    self.connection.commit()
                    spider.logger.into('插入重复单词')
            return item



if __name__ == '__main__':
    item = {'name': 'Sunday',
 'pronounce': '英 [ˈsʌndeɪ] 美 [ˈsʌnˌdeɪ] ',
 'style': '*第三人称复数：Sundays    ',
 'views': '*名词：星期日，星期天; 每逢星期日出版的报纸; 星期日报; [人名] 森迪.   '}
    keys, values = zip(*dict(item).items())
    print(keys, values)
    print(len(keys))
    print("{},{}".format(
                ','.join(keys), ','.join(['%s'] * len(keys))
            ))