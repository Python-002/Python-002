# -*- coding: utf-8 -*-

from itemadapter import ItemAdapter
import pymysql

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# 注册到settings.py文件的ITEM_PIPELINES中，激活组件
class DoubanmoviePipeline:

    def __init__(self,config):
        self.config = config

    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler.settings.get('MYSQL_CONFIG'))

    def open_spider(self, spider):
        self.conn = pymysql.connect(
            host=self.config['host'],
            port=self.config['port'],
            user=self.config['user'],
            password=self.config['password'],
            db=self.config['db']
        )

    def close_spider(self, spider):
        self.conn.close()

    # 每一个item管道组件都会调用该方法，并且必须返回一个item对象实例或raise DropItem异常
    def process_item(self, item, spider):
        with self.conn.cursor() as cur:
            sql = "INSERT INTO `movies` (`movies_name`, `movies_type`, `movies_time`) VALUES (%s, %s, %s)"
            cur.execute(sql, (item['movies_name'], item['movies_type'], item['movies_time']))
        self.conn.commit()
        return item

        # print("!!!!!!!!!!!!!!")
        # print(item)
        # print("@@@@@@@@@@@@@@@@")
        # movies_name = item['movies_name']
        # movies_type = item['movies_type']
        # movies_time = item['movies_time']
        # output = f'|{movies_name}|\t|{movies_type}|\t|{movies_time}|\n\n'
        # print(output)
        # with open('./maoyanmovie.csv', 'a+', encoding='utf-8') as article:
        #     article.write(output)
        # return item


