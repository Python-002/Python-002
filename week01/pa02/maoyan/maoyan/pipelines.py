# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pandas as pd
from os import path


class MaoyanPipeline:
    def process_item(self, item, spider):
        # Create the csv file if it doesn't exist
        if not path.exists('./movies.csv'):
            headers = pd.DataFrame(data=[['电影名称', '电影类型', '上映时间']])
            headers.to_csv('./movies.csv',
                           encoding='utf8', index=False, header=False)

        movie = pd.DataFrame(data=item)
        movie.to_csv('./movies.csv',
                     mode='a', encoding='utf8', index=False, header=False)
        return item
