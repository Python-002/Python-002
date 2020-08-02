# -*- coding: utf-8 -*-

from scrapyweek02.config import db_mysql
from scrapyweek02.utils import mysql


# 注册到settings.py文件的ITEM_PIPELINES中，激活组件
class MaoYanPipeline:

    # 每一个item管道组件都会调用该方法，并且必须返回一个item对象实例或raise DropItem异常
    def process_item(self, item, spider):
        movie_name = item['movie_name']
        movie_type = item['movie_type']
        movie_date = item['movie_date']

        # db_name = db.DB_NAME
        sql = 'insert into mao_yan (`movie_name`, `movie_type`, `movie_date`) ' \
              'values ("%s", "%s", "%s")' % (movie_name, movie_type, movie_date)

        db = mysql.MySql(db_mysql.DB_CONN, sql)
        db.run()

        return item
