import scrapy

from scrapy.selector import Selector
from lspiders.items import LspidersItem

class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com','httpbin.org']
    start_urls = ['https://maoyan.com/films?showType=3']

    def start_requests(self):
        # for week01 homework , set range max value is 1
        for i in range(0 ,1):
            url = f'https://maoyan.com/films?showType=3&offset={i*30}'
            yield scrapy.Request(url=url, callback=self.parse)

    # 还没来得及改批改部分，仅增加了一些打印
    def parse(self, response):
        print(f"PARSE: {response.url},{response.request.meta}")
        # 仅为瞜一眼到底用没用代理啊，一开始以为是httpbin.org慢，最后才发现应该是maoyan在start_requests里面就没用代理...
        # 本来想象的是配置错误的代理地址，然后捕获相关异常，把异常的作业部分完成，不过就是试图调这个case时候，发现，捅猫眼确实没用代理啊
        yield scrapy.Request(url='http://httpbin.org/ip', callback=self.checkIp)
        divs_with_hover = Selector(response=response).xpath('//div[@class="movie-item-hover"]')
        divs_with_hover = divs_with_hover[:10]
        print(len(divs_with_hover))
        for div in divs_with_hover:

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
        
    def checkIp(self,response):
        print(f"PARSE: {response.url},{response.request.meta}")
        # 好像应该证明是真用了
        print(f'IP is {response.text}')

