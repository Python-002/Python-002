import scrapy
from scrapy.selector import Selector
from maoyanproxy.items import MaoyanproxyItem

class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['http://maoyan.com/films']

    def start_requests(self):
        # print('Start to crawl')
        url = 'http://maoyan.com/films?showType=3'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # print(response.url)

        movies = Selector(response=response).xpath('//dd/div[@class="movie-item film-channel"]/div[@class="movie-item-hover"]/a/div[@class="movie-hover-info"]')
        
        for movie in movies[:10]:
            item = MaoyanproxyItem()
            
            # print('------------------------------')
            title = movie.xpath('./div[1]/span/text()').extract()[0]
            category = movie.xpath('./div[2]/text()').extract()[1].strip()
            release = movie.xpath('./div[4]/text()').extract()[1].strip()

            item['title'] = title
            item['category'] = category
            item['release'] = release

            yield item

