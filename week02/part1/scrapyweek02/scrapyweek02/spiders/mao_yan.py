# -*- coding: utf-8 -*-

import scrapy
from scrapyweek02.items import MaoYanItem
from scrapy.selector import Selector
from scrapyweek02.config import headers


class MaoYanSpider(scrapy.Spider):
    # 定义爬虫名称
    name = 'maoyan'
    allowed_domains = ['maoyan.com']

    def start_requests(self):
        try:
            self.check_request_proxy()

            yield scrapy.Request(
                url='https://maoyan.com/films?showType=3', callback=self.parse,
                headers={
                    'Cookie': headers.COOKIES,
                    'User-Agent': headers.USER_AGENT
                }
            )
        except Exception as e:
            print(e)

    def parse(self, response):

        divs = Selector(response=response).xpath('//div[@class="movie-hover-info"]')

        for i in range(10):
            try:
                movie_name = divs[i].xpath('./div[1]/span[1]/text()').extract_first().strip()
                movie_type = divs[i].xpath('./div[2]/text()').extract()[1].strip()
                movie_date = divs[i].xpath('./div[4]/text()').extract()[1].strip()

                item = MaoYanItem()
                item['movie_name'] = movie_name
                item['movie_type'] = movie_type
                item['movie_date'] = movie_date

                print('%s - %s - %s' % (movie_name, movie_type, movie_date))
                yield item
            except Exception as e:
                print(e)
                break

    def check_request_proxy(self):
        pass
