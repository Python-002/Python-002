import scrapy
from spiders.items import SpidersItem
import lxml.etree
import requests


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['http://maoyan.com/films?showType=3']

    # def parse(self, response):
    #     pass
    def start_requests(self):
        url = self.start_urls[0]
        yield scrapy.Request(url=url, callback=self.parse)
    

    # 解析函数，获得新链接
    def parse(self, response):
        selector = lxml.etree.HTML(response.text.replace("<dd>","</dd><dd>"))
        new_links = selector.xpath('//*[@class="channel-detail movie-item-title"]/a/@href')
        links = tuple(f'https://maoyan.com' + str(i) for i in new_links)
        for i in range(10):
            item = SpidersItem()
            item['link'] = links[i]
            yield scrapy.Request(url=links[i],meta={'item':item},callback=self.parse2)

    
    # 解析具体页面,获得信息
    def parse2(self, response):
        item = response.meta['item']
        selector = lxml.etree.HTML(response.text.replace("<dd>","</dd><dd>"))
        # 转化为字符串，展示结果时更干净
        movie_name1 = selector.xpath('/html/body/div[3]/div/div[2]/div[1]/h1/text()')
        movie_name = "".join(movie_name1)
        movie_genre = selector.xpath('//html/body/div[3]/div/div[2]/div[1]/ul/li[1]/a/text()')
        genre = "".join(movie_genre).strip()
        movie_date1 = selector.xpath('/html/body/div[3]/div/div[2]/div[1]/ul/li[3]/text()')
        movie_date = "".join(movie_date1)
        item['movie_name'] = movie_name
        item['genre'] = genre
        item['movie_date'] = movie_date
        # items.append(item)
        yield item