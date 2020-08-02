import scrapy

from scrapy.selector import Selector
from lspiders.items import LspidersItem

class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com','httpbin.org']
    start_urls = ['https://maoyan.com/films?showType=3']

    def start_requests(self):
        # for week01 homework target, set range max value is 1
        for i in range(0 ,1):
            url = f'https://maoyan.com/films?showType=3&offset={i*30}'
            yield scrapy.Request(url=url, callback=self.parse,errback=self.on_err)
    
    # 确实作业异常部分有点让人费解，感觉任何异步回调的框架本身就应该是带捕获处理的，所以这里加异常大多不应该针对框架完成的主流程（请求、通过代理请求等）
    def on_err(self,failure):
        print("FAIL")
        self.logger.error(failure)

    # 还没来得及改批改部分，仅增加了一些打印
    def parse(self, response):
        # 这里纯粹是为了强行加上异常处理，按说一个字典的key应该这么费劲么
        try:
            debug_info = response.request.meta['proxy']
            print(f"PARSE proxy : {response.url},{debug_info}")
        except KeyError as e:
            self.logger.critical(f'proxy key ? : {e}')
            print(f"PARSE without proxy : {response.url},{response.request.meta}")
        
        '''
        + 下面这个httpbin仅为调试用
        + 纯粹是为了瞜一眼到底用没用代理... 
          - 一开始以为是httpbin.org慢，最后才发现应该是maoyan在start_requests里面就没用代理...
          - 慢的都是用了代理之后的请求
        + 本来想象的调试异常的case是：
          - 配置错误的代理地址，然后捕获相关异常，把异常的作业部分完成
          - 不过就是试图调这个case时候，发现，捅猫眼确实没用代理啊,response.request.meta 中才是检查是否设置了代理的正牌检查方法
        + 最后我是把middlewares里面抄的老师的代码稍微改了一下走了代理

        '''
        yield scrapy.Request(url='https://httpbin.org/ip', callback=self.checkIp)
        divs_with_hover = Selector(response=response).xpath('//div[@class="movie-item-hover"]')
        divs_with_hover = divs_with_hover[:10]
        print(len(divs_with_hover))
        for div in divs_with_hover:

            print(div.xpath("./a/@href").get())

            # 时间所限，还没顾得上去按批改意见改进以下内容
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
    
    # 调试用的，看看到底特么用没用代理
    def checkIp(self,response):
        print(f"PARSE: {response.url},{response.request.meta}")
        # 好像应该证明是真用了
        print(f'IP is {response.text}')

