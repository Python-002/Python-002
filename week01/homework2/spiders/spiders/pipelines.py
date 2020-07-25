# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from itemadapter import ItemAdapter
import pandas as pd

movie_infor = []
class SpidersPipeline:
    def process_item(self, item, spider):
        movie_name = item['movie_name']
        genre = item['genre']
        movie_date = item['movie_date']
        # output = f'|{movie_name}|\t|{genre}|\t|{movie_date}|\n\n'
        movie_infor.append(f'电影名称:{movie_name}\n电影类型:{genre}\n上映时间:{movie_date}\n')
        # with open('./movie2.csv','a+',encoding='utf-8') as article:
        #     article.write(output)
        #     article.close()
        movie2 = pd.DataFrame(data = movie_infor)
        # windows需要使用gbk字符集
        movie2.to_csv('./movie2.csv', encoding='utf8', index=False, header=False)
        return item
        
        
