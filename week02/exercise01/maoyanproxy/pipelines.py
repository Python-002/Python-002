# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
from maoyanproxy import settings

sqls = {
    'DELETE': "delete from `movie`", 
    'CREATE': "insert into `movie` (`title`, `catetory`, `release`) value (%s, %s, %s)"
}


class MaoyanproxyPipeline:
    def __init__(self):
        self.conn = pymysql.connect(
            host = settings.MYSQL_HOST,
            port = settings.MYSQL_PORT,
            user = settings.MYSQL_USER,
            password = settings.MYSQL_PASSWORD,
            db = settings.MYSQL_DB,
            charset = settings.MYSQL_CHARSET)
        self.cur = self.conn.cursor()
        try:
            self.cur.execute(sqls['DELETE'])
            self.conn.commit()
        except:
            self.conn.rollback()

    def close_spider(self, spider):
        self.conn.close

    def process_item(self, item, spider):
        try:
            self.cur.execute(sqls['CREATE'], (item['title'], item['category'], item['release']))
            self.conn.commit()
        except:
            self.conn.rollback()
        return item

