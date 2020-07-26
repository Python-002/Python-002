# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pandas as pd

# 注册到settings.py文件的ITEM_PIPELINES中，激活组件
class MaoYanPipeline:

    # 每一个item管道组件都会调用该方法，并且必须返回一个item对象实例或raise DropItem异常
    def process_item(self, item, spider):
        movie_name = item['movie_name']
        movie_type = item['movie_type']
        movie_date = item['movie_date']

        data_list = [[movie_name, movie_type, movie_date]]
        data = pd.DataFrame(data=data_list)
        # windows需要使用gbk字符集
        data.to_csv('./movie2.csv', encoding='utf8', index=False, header=False, mode='a')
        return item