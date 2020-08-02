# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import time

# 这个基本上是照抄
class LspidersPipeline:

    def __init__(self):
        super().__init__()
        self.db = ConnDB(dbInfo)

    # 仅有一点的改动，还不熟悉python快速输出个人类可读时间戳咋整...
    file_name = "maoyan-movies-hot" + str(round(time.time())) + ".csv"
    def process_item(self, item, spider):
        title = item['title']
        genre = item['genre']
        release_time = item['release_time']
        # 作为csv，其实有点问题，当内容中有逗号怎么办？先不管了，所以说这里为了减少中间数据缓存？？直接落盘了这方法似乎不如pandas
        output = f'{title},{genre},{release_time}\n'
        with open(self.file_name, 'a+', encoding='utf-8') as article:
            article.write(output)
        self.db.run([f'INSERT INTO `pythontrainhomework`.`maoyan-hot-250-top-10` ( `name`, `genre`, `release_time`) VALUES ("{title}","{genre}","{release_time}");'])
        return item

# 抄自课程示例，稍作修改，之所以直接放下面，是因为不懂import from 包啊，模块儿的咋回事，后面再调吧

import pymysql

dbInfo = {
    'host' : 'rm-hp3p14nd9bp1rmbj1to.mysql.huhehaote.rds.aliyuncs.com',
    'port' : 3306,
    'user' : 'adm',
    'password' : 'gUxXaNyxKRZBFQ93',
    'db' : 'pythontrainhomework'
}

# 仅作main调试用，

sqls = ['select 1', 
'select VERSION()',
'INSERT INTO `pythontrainhomework`.`maoyan-hot-250-top-10` ( `name`, `genre`, `release_time`) VALUES ("黑寡妇","超级英雄/动作","2020-8-14");' ,
'select * from `pythontrainhomework`.`maoyan-hot-250-top-10`']

# 基本照抄，除了result那个

class ConnDB(object):

    def __init__(self, dbInfo):
        self.host = dbInfo['host']
        self.port = dbInfo['port']
        self.user = dbInfo['user']
        self.password = dbInfo['password']
        self.db = dbInfo['db']

    # 这不应该有个连接池什么的么，后面估计到框架会有？

    def run(self,sqls):
        conn = pymysql.connect(
            host = self.host,
            port = self.port,
            user = self.user,
            password = self.password,
            db = self.db
        )
        
        cur = conn.cursor()
        try:
            for command in sqls:
                cur.execute(command)
                print(cur.fetchone())
            # 关闭游标
            cur.close()
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()
        conn.close()

if __name__ == "__main__":
    db = ConnDB(dbInfo)
    db.run(sqls)
