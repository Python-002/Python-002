# -*- coding: utf-8 -*-
import scrapy
import sys
from spider.doubanmovie.items import MaoyanmovieItem
from scrapy.selector import Selector


class MaoyanSpider(scrapy.Spider):
    # 定义爬虫名称
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    # 起始URL列表
    start_urls = ['https://maoyan.com/films?showType=3&sortId=1']
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36 SE 2.X MetaSr 1.0'
    accept = 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
    cookie = '__mta=120987447.1595662508981.1595664459431.1595664552067.6; uuid_n_v=v1; uuid=5D3C7880CE4911EABF7AA517BC081B3029BC39D1AB324275A57B403348686B9C; _csrf=044622383354484e931ae1c7a80e07e66498fb1eb14ffbe17a277116ca90463b; _lxsdk_cuid=17384e5a0f8c8-0f0dbeba219912-c7d6957-121886-17384e5a0f8c8; _lxsdk=5D3C7880CE4911EABF7AA517BC081B3029BC39D1AB324275A57B403348686B9C; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1595662509; mojo-uuid=434943cc8a2cb209fa22064f9ca2b97d; mojo-session-id={"id":"4dc9f94198bd097c878e6c04c6ad90d5","time":1595662508885}; mojo-trace-id=13; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1595664648; __mta=120987447.1595662508981.1595664552067.1595664648636.7; _lxsdk_s=17384e5a0f9-c77-ecb-4fd%7C%7C20'
    header ={"user-agent":user_agent,"Cookie":cookie}
    def start_requests(self):
            url = f'https://maoyan.com/films?showType=3&sortId=1'
            yield scrapy.Request(url=url, callback=self.parse,headers = self.header, dont_filter=False)

    # 解析函数
    def parse(self, response):
        # 打印网页的url
        print(response.url)
        # 打印网页的内容
        print(response.text)

        movies = Selector(response=response).xpath('//*[@id="app]/div/div[2]div[2]/dl/dd[1]/div[2]/a/div/div[1]/span[1]/text()')
        print(movies)
#         for movie in movies:
#             # 路径使用 / .  .. 不同的含义　
#             title = movie.xpath('./div/span/text()')
#             # moive_type = moive.xpath('./')
#             link = movie.xpath('./a/@href')
#             print('-----------')
#             print(title)
#             print(link)
#             print('-----------')
#             print(title.extract())
#             print(link.extract())
#             print(title.extract_first())
#             print(link.extract_first())
#             print(title.extract_first().strip())
#             print(link.extract_first().strip())
#
# if __name__ == "__main__":
#     MaoyanSpider.start_requests(sys.argv[0])