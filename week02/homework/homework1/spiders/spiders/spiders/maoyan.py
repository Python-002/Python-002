import scrapy
from spiders.items import SpidersItem
import lxml.etree
import requests
from scrapy.selector import Selector


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    # def parse(self, response):
    #     pass
    def start_requests(self):
        url = 'https://maoyan.com/films?showType=3'
        # headers = {
        #     # 'Host':'maoyan.com',
        #     # 'Connection': 'keep-alive',
        #     # 'Cache-Control': 'max-age=0',
        #     # 'Upgrade-Insecure-Requests': '1'
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        #     # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        #     # 'Accept-Encoding': 'gzip, deflate, br',
        #     # 'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        #     'Cookie': '__mta=175529629.1595214567832.1595524395398.1596113800810.30; uuid_n_v=v1; uuid=6B328860CA3611EAB2AE8B45D9A9C865974183C5D3AA45E4A09EFB519D772754; mojo-uuid=e56aa0eccb888ffcd01b0d9d6070e73b; _lxsdk_cuid=1736a32992fc8-054119405378e3-1d231c08-1fa400-1736a32992fc8; _lxsdk=6B328860CA3611EAB2AE8B45D9A9C865974183C5D3AA45E4A09EFB519D772754; _csrf=4a1d963611c0dceec73d1fb62c4be2daddf8d4f0eea9ed93a9aacfc6693f334f; mojo-session-id={"id":"b021cf04743c5dcba2a95e77727f6e07","time":1596341650440}; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1595817839,1595863429,1596095849,1596341651; mojo-trace-id=4; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1596343112; __mta=175529629.1595214567832.1596113800810.1596343111937.31; _lxsdk_s=173ad60854e-18b-e39-62f%7C%7C8'
        # }

        yield scrapy.Request(url=url, callback=self.parse)





    def parse(self, response):
        movies = Selector(response=response).xpath('//div[@class="movie-hover-info"]')[0:10]
        for movie in movies:
            item = SpidersItem()
            item['movie_name'] = movie.xpath('./div[1]/span[1]/text()').extract_first()
            item['movie_genre'] = movie.xpath('./div[2]/text()').extract()[1].strip()
            item['movie_date'] = movie.xpath('./div[4]/text()').extract()[1].strip()
            yield item

