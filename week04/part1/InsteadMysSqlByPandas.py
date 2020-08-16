# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import pymysql
from sqlalchemy import create_engine


class InsteadMysSqlByPandas:
    """
    将常见 MySql 语句翻译成 pandas 语法
    """
    def __init__(self, db_host, db_port, db_user, db_passwd, db_database):
        self.db_host = db_host
        self.db_port = db_port
        self.db_user = db_user
        self.db_passwd = db_passwd
        self.db_database = db_database
        self.conn = pymysql.connect(
            host=db_host,
            port=int(db_port),
            user=db_user,
            passwd=db_passwd,
            db=db_database
        )

        global user_table_name
        global order_table_name

        # 准备好两个 DataFrame 数据
        self.df_all_user = self.select_all(user_table_name)
        self.df_all_order = self.select_all(order_table_name)

    def select_all(self, table_name=''):
        """
        SELECT * FROM data;
        """
        if not table_name:
            table_name = user_table_name

        sql = f'SELECT *  FROM {table_name}'
        df_res = pd.read_sql(sql, self.conn)
        return df_res

    def select_limit(self, num):
        """
        SELECT * FROM data LIMIT 10;
        """
        return self.df_all_user[:num]

    def select_column(self, column_name):
        """
        SELECT id FROM data;
        """
        return self.df_all_user[[column_name]]

    def select_count_of_column(self, column_name):
        """
        SELECT COUNT(id) FROM data
        """
        return self.df_all_user.loc[:, [column_name]].count()

    def select_condition(self, condition_dict):
        """
        SELECT * FROM data WHERE id<1000 AND age>30
        """
        # assemble_judge = (self.df_all_user['id'] < 1000) & (self.df_all_user['age'] > 30)
        assemble_judge = (self.df_all_user['id'] > 0)
        for con in condition_dict:
            if con['judge'] == '>':
                assemble_judge = assemble_judge & (self.df_all_user[con['column']] > con['num'])
            else:
                assemble_judge = assemble_judge & (self.df_all_user[con['column']] < con['num'])

        return self.df_all_user[assemble_judge]

    def select_group_by(self, group_by_column='id'):
        """
        SELECT user_id,COUNT(DISTINCT order_sn) FROM table1 GROUP BY user_id
        """
        return self.df_all_order.groupby(group_by_column).order_sn.nunique()

    def select_join(self):
        """
        SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id
        """
        return pd.merge(self.df_all_order, self.df_all_user, left_on='user_id', right_on='id', how='inner')

    def select_unit(self):
        """
        SELECT * FROM table1 UNION SELECT * FROM table2
        """
        return pd.concat([self.df_all_user, self.df_all_user])

    def delete(self, column_name, column_value):
        """
        DELETE FROM table1 WHERE id=10
        """
        return self.df_all_user[(self.df_all_user[column_name] != column_value)]

    def drop_column(self, column_name):
        """
        ALTER TABLE table1 DROP COLUMN column_name
        """
        return self.df_all_user.drop(column_name, axis=1)

    def __del__(self):
        self.conn.close()


class InitData:
    """
    MySQL 数据填充类，可以提前准备好数据以供 pandas 测试使用
    """
    def __init__(self, db_host, db_port, db_user, db_passwd, db_database, fill_data_num):
        self.db_host = db_host
        self.db_port = db_port
        self.db_user = db_user
        self.db_passwd = db_passwd
        self.db_database = db_database

        # 每次执行生产的数据条数
        self.fill_data_num = fill_data_num

        global user_table_name
        global order_table_name

    def save_data_frame(self, init_df, table_name):
        sql_engine = create_engine(
            f'mysql+pymysql://{self.db_user}:{self.db_passwd}@{self.db_host}:{self.db_port}/{self.db_database}',
            # echo=True
        )

        init_df.to_sql(table_name, con=sql_engine, if_exists='append', index=False)

    def init_user_data(self):
        # user
        print('init user -------------------------------')
        group = ['a', 'b', 'c']
        df_user = pd.DataFrame({
            "user": [group[x] for x in np.random.randint(0, len(group), self.fill_data_num)],
            "age": np.random.randint(5, 70, self.fill_data_num),
            "sex": np.random.choice(['man', 'woman', None], self.fill_data_num),
        })

        self.save_data_frame(df_user, user_table_name)

    def init_order_data(self):
        # order
        print('order -------------------------------')
        import hashlib
        md = hashlib.md5()

        order_log = []
        # 抽取 10 个用户，为之生成一些订单
        for user_id in np.random.randint(0, self.fill_data_num, 10):
            order_num = np.random.randint(1, 3)

            # 每位用户有 1-3 笔不同订单
            for i in range(0, order_num):
                # 按照订单的状态 0 未支付 -> 1 支付中 -> 2 已完成设计，任何订单可能不会有支付成功记录
                max_status = np.random.choice([0, 1, 2])
                money = np.random.randint(10, 100)

                order = '%s%s%s' % (user_id, money, i)
                md.update(order.encode('utf-8'))
                order_sn = md.hexdigest()

                for status in range(0, max_status):
                    order_log.append({
                        "user_id": user_id,
                        "order_sn": order_sn,
                        "money": money,
                        "status": status,
                    })

        self.save_data_frame(pd.DataFrame(order_log), order_table_name)


if __name__ == '__main__':
    host = '192.168.20.222'
    port = '3306'
    user = 'root'
    passwd = ''
    db = 'hwq_test'

    # 模拟的用户表名
    user_table_name = 'study_pandas_user'
    # 模拟的订单日志表名
    order_table_name = 'study_pandas_order'

    # 与作业无关，为了测试初始化数据库数据用的
    data_module = InitData(host, port, user, passwd, db, 20)
    data_module.init_user_data()
    data_module.init_order_data()

    # 将 sql 翻译成 pandas
    translation = InsteadMysSqlByPandas(host, port, user, passwd, db)
    output = 'please open the comment below'

    """
    1. SELECT * FROM data;
    2. SELECT * FROM data LIMIT 10;
    3. SELECT id FROM data;  //id 是 data 表的特定一列
    4. SELECT COUNT(id) FROM data;
    5. SELECT * FROM data WHERE id<1000 AND age>30;
    6. SELECT id,COUNT(DISTINCT order_id) FROM table1 GROUP BY id;
    7. SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id;
    8. SELECT * FROM table1 UNION SELECT * FROM table2;
    9. DELETE FROM table1 WHERE id=10;
    10. ALTER TABLE table1 DROP COLUMN column_name;
    """
    # 下面每个方法按顺序实现了上述的 SQL
    output = translation.select_all()
    # output = translation.select_limit(10)
    # output = translation.select_column('id')
    # output = translation.select_count_of_column('id')
    # output = translation.select_condition([
    #     {'column': 'id', 'judge': '<', 'num': 1000},
    #     {'column': 'age', 'judge': '>', 'num': 30}
    # ])
    # output = translation.select_group_by(group_by_column='user_id')
    # output = translation.select_join()
    # output = translation.select_unit()
    # output = translation.delete('id', 10)
    # output = translation.drop_column('user')

    print('output: >>>>>>>>>>>>>>')
    print(output)
