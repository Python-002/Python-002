import scrapy

from scrapy.selector import Selector
from lspiders.items import LspidersItem

class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    def start_requests(self):
        # for week01 homework , set range max value is 1
        for i in range(0 ,1):
            url = f'https://maoyan.com/films?showType=3&offset={i*30}'
            yield scrapy.Request(url=url, callback=self.parse)

    # 必须得承认这个解法，基本还是bs那道题思路改过来的，仅仅是换成了scrapy自己的Selector
    def parse(self, response):
        print(response.url)

        divs_with_hover = Selector(response=response).xpath('//div[@class="movie-item-hover"]')
        divs_with_hover = divs_with_hover[:10]
        print(len(divs_with_hover))
        for div in divs_with_hover:

            # 可以这么思考这个问题，当一页能解决问题的时候，可能不值得再去请求另一页
            # 但是如果预先把请求到另一页的代码组织起来，当需要爬更多数据的时候，相对会容易点
            # 所以目前，按MVP的角度还好，但是有可能给后面课程作业挖坑了
            # 其实主要还是时间不够，得带娃出去玩儿啊

            print(div.xpath("./a/@href").get())

            # 时间所限，没有找到更利落直观的办法了
            item_divs = div.xpath('.//div[@class="movie-hover-title"]')
            item_divs_time = div.xpath('.//div[@class="movie-hover-title movie-hover-brief"]')
            item_divs = item_divs+ item_divs_time

            item = LspidersItem()
            for item_div in item_divs:
                text_content = item_div.get()
                # print(text_content)
                if '类型' in text_content:
                    item['title'] = item_div.attrib["title"]
                    item['genre'] = "".join(item_div.xpath('./text()').getall()).strip()
                elif '上映时间' in text_content:
                    item['release_time'] = "".join(item_div.xpath('./text()').getall()).strip()
            yield item
