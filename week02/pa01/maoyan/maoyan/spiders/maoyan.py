# -*- coding: utf-8 -*-
import scrapy
from maoyan.items import MaoyanItem
from scrapy.selector import Selector


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    movie_number = 10
    movies_list_xpath = '//*[@id="app"]/div/div[2]/div[2]/dl'

    # def parse(self, response):
    #     raise Exception("maoyan test exception")

    def parse(self, response):
        movies = Selector(response=response).xpath('//div[@class="movie-hover-info"]')  # noqa: E501

        m_count = 0
        for m in movies:
            if m_count < self.movie_number:
                m_count += 1
                yield MaoyanItem({
                    'movie_name': m.xpath('.//span[@class="name " or @class="name noscore"]/text()').extract()[0],  # noqa: E501
                    'movie_type': m.xpath('.//span[@class="hover-tag"]/following-sibling::text()')[0].extract().strip(),  # noqa: E501
                    'movie_date': m.xpath('.//span[@class="hover-tag"]/following-sibling::text()')[2].extract().strip()  # noqa: E501
                })
