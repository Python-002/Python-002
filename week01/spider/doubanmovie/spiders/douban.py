# -*- coding: utf-8 -*-
import scrapy
from spider.doubanmovie.items import MaoyanItem
from scrapy.selector import Selector


class MaoyanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    movie_number = 10
    movies_list_xpath = '//*[@id="app"]/div/div[2]/div[2]/dl'

    def parse(self, response):
        try:
            movies = Selector(response=response).xpath('//div[@class="movie-hover-info"]')  # noqa: E501
            print(movies)
            m_count = 0
            print(len(movies))
            for m in movies  :
                if m_count < self.movie_number and m_count <10:
                    m_count += 1
                    movies_name = m.xpath('.//span[@class="name " or @class="name noscore"]/text()').extract()
                    movies_type = m.xpath('.//span[@class="hover-tag"]/following-sibling::text()')[0].extract().strip()
                    movies_time = m.xpath('.//span[@class="hover-tag"]/following-sibling::text()')[2].extract().strip()
                    print(str(movies_name) + "/" +str(movies_type) +"/"+str(movies_time))
                    print("-----------------")
                yield MaoyanItem(
                            movies_name=movies_name,
                            movies_type=movies_type,
                            movies_time=movies_time
                )
        except Exception as e:
            print(e)