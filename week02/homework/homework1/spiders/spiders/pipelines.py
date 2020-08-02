# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from itemadapter import ItemAdapter
import pandas as pd
import pymysql

#要修改setting.py
class PymysqlPipeline(object):
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host='localhost',
            db='week02',
            user='caiwei',
            passwd='123456',
            charset='utf8mb4',
            port=3306,
            use_unicode=True)
        self.cursor = self.connect.cursor()
 
    def process_item(self, item, spider):
        cursor = self.cursor
        try:
            sql = 'insert into movies_tbl(movie_name, movie_genre, movie_date) values (%s,%s,%s)'
            cursor.execute(sql, (
            item['movie_name'], item['movie_genre'], item['movie_date']))
            self.connect.commit()
        except Exception as e:
            print(e)

 
        return item
        
