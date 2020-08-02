

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class   MaoyanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 注释原有的pass
    # pass
    movies_name = scrapy.Field()
    movies_type = scrapy.Field()
    movies_time = scrapy.Field()
