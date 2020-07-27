

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class   MaoyanmovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 注释原有的pass
    # pass
    moive_name = scrapy.Field()
    moive_type = scrapy.Field()
    online_time = scrapy.Field()
