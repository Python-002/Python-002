# Python 3.7连接到MySQL数据库的模块推荐使用PyMySQL模块
# pip install pymysql
#  /usr/local/mysql/support-files/mysql.server start
# 一般流程
# 开始-创建connection-获取cursor-CRUD(查询并获取数据)-关闭cursor-关闭connection-结束
import pymysql


class MySql(object):
    def __init__(self, db_info, sql):
        self.host = db_info['host']
        self.port = db_info['port']
        self.user = db_info['user']
        self.password = db_info['password']
        self.db = db_info['db']
        self.sql = sql

    def run(self):
        conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.db
        )
        result = []

        # 游标建立的时候就开启了一个隐形的事物
        cur = conn.cursor()
        try:
            # for command in self.sqls:
            # cancel 'for' loop for reconnect forever
            cur.execute(self.sql)
            result.append(cur.fetchone())
            # 关闭游标
            cur.close()
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(e)
            # 关闭数据库连接
            conn.close()
            return e

        conn.close()
        return result
