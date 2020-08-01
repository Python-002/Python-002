# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import time

# 这个基本上是照抄
class LspidersPipeline:
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
        return item
