import scrapy


class MovisesSpider(scrapy.Spider):
    name = 'movises'
    allowed_domains = ['douban.com']
    start_urls = ['http://douban.com/']

    def parse(self, response):
        pass
