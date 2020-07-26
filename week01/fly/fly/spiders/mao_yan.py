# -*- coding: utf-8 -*-
import scrapy
from fly.items import MaoYanItem
from scrapy.selector import Selector


class MaoYanSpider(scrapy.Spider):
    # 定义爬虫名称
    name = 'maoyan'
    allowed_domains = ['maoyan.com']

    def start_requests(self):
        yield scrapy.Request(
            url='https://maoyan.com/films?showType=3', callback=self.parse,
            headers={
                'Cookie': 'uuid=b264e5beac28458db35f.1595511123.1.0.0; mtcdn=K; userTicket=tQTZaCEckOTWIQrpSomnYdNwWpQbhemHZLMuAbwd; u=290257956; n=LTF444070036; lt=q9lbT-q8Ot2yymfq7P___PN3odUAAAAAHAsAADUu-rsjxttUmmb2VcAx0zInyoFjnpzYZQsrCzlAh03y4Z8_Cbb2Asw78MVkKXHYrA; mt_c_token=q9lbT-q8Ot2yymfq7P___PN3odUAAAAAHAsAADUu-rsjxttUmmb2VcAx0zInyoFjnpzYZQsrCzlAh03y4Z8_Cbb2Asw78MVkKXHYrA; token=q9lbT-q8Ot2yymfq7P___PN3odUAAAAAHAsAADUu-rsjxttUmmb2VcAx0zInyoFjnpzYZQsrCzlAh03y4Z8_Cbb2Asw78MVkKXHYrA; lsu=',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
            }
         )

    # 解析函数
    def parse(self, response):
        # 打印网页的url
        print(response.url)
        print('---------------------------------')

        divs = Selector(response=response).xpath('//div[@class="movie-hover-info"]')

        for i in range(10):
            movie_name = divs[i].xpath('./div[1]/span[1]/text()').extract_first().strip()
            # normalize-space 用到相对路径下不知道为啥失败了，搞不明白
            # movie_type = divs[i].xpath('normalize-space(./div[2]/text())').extract_first().strip()
            movie_type = divs[i].xpath('normalize-space(//*[@id="app"]/div/div[2]/div[2]/dl/dd[1]/div[1]/div[2]/a/div/div[2])').extract_first().strip()
            movie_date = divs[i].xpath('./div[4]/text()').extract()[1].strip()

            item = MaoYanItem()
            item['movie_name'] = movie_name
            item['movie_type'] = movie_type
            item['movie_date'] = movie_date

            print('%s - %s - %s' % (movie_name, movie_type, movie_date))
            yield item
