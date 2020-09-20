import requests
from lxml import etree
from queue import Queue
import threading
import json
import random
import pymysql
import matplotlib.pyplot as plt


class CrawlThread(threading.Thread):
    '''
    爬虫类
    '''

    def __init__(self, thread_id, pageQueue, cityQueue):
        super().__init__()
        self.thread_id = thread_id
        self.pageQueue = pageQueue
        self.cityQueue = cityQueue

    def run(self):
        '''
        重写run方法
        '''
        print(f'启动线程：{self.thread_id}')
        self.scheduler()
        print(f'结束线程：{self.thread_id}')

    # 模拟任务调度
    def scheduler(self):
        while not self.cityQueue.empty():
            city = self.cityQueue.get()
            while True:
                if self.pageQueue.empty():
                    for i in range(11):
                        pageQueue.put(i)
                    break
                else:
                    USER_AGENT_LIST = [
                        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
                        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
                        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
                        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
                        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
                    ]
                    ua = random.choice(USER_AGENT_LIST)
                    page = self.pageQueue.get()
                    print('下载线程为：', self.thread_id, " 下载页面：", page)
                    if "beijing" == city:
                        url = f'https://www.lagou.com/beijing-zhaopin/Python/{page}/?filterOption=2&sid=55bdf020d706454ab9fc23220e4ff8ed'
                    elif "shanghai" == city:
                        url = f'https://www.lagou.com/shanghai-zhaopin/Python/{page}/?filterOption=2&sid=516f8c23e04540e7ab03c2e5d064319b'
                    elif "guangzhou" == city:
                        url = f'https://www.lagou.com/guangzhou-zhaopin/Python/{page}/?filterOption=2&sid=2c634cb4c9b04789a9bc13af22c9a788'
                    elif "shenzhen" == city:
                        url = f'https://www.lagou.com/shenzhen-zhaopin/Python/{page}/?filterOption=2&sid=0ba8b92cfab8440db462f5f40faefaf5'
                    # url = f'https://www.lagou.com/shenzhen-zhaopin/Python/{page}/?filterOption=2&sid=9962f4d98d5443ccb635396f74898e0b'
                    headers = {
                        'User-Agent': ua
                        # 'cookie':'user_trace_token=20200730180137-5ab1c191-2892-4810-bd67-d7b1d0aad7d3; JSESSIONID=ABAAABAABAGABFAEA94C3D546CB4574E6CE27487DB2FA41; WEBTJ-ID=08052020%2C214542-173bededa1ef-05f410cbb69d76-1d231c08-2073600-173bededa1fad3; RECOMMEND_TIP=true; LGUID=20200805214542-074a315a-088a-4bcd-b5e7-b02b5a765e6f; _ga=GA1.2.1712621782.1596635143; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1596635143; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221739f2b8de4116-0c27318a4df559-1d231c08-2073600-1739f2b8de54fd%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24os%22%3A%22UNIX%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%2284.0.4147.89%22%2C%22%24latest_referrer_host%22%3A%22%22%7D%2C%22%24device_id%22%3A%221739f2b8de4116-0c27318a4df559-1d231c08-2073600-1739f2b8de54fd%22%7D; _gid=GA1.2.635507442.1596770824; TG-TRACK-CODE=index_navigation; index_location_city=%E6%B7%B1%E5%9C%B3; X_HTTP_TOKEN=527d82653f3fbdac2991976951e87017f523970cb3; SEARCH_ID=733f091d27a1400cb51489f7449cd851; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1596792053; LGRID=20200807172053-b9fa3bbf-27c3-4a1b-b3a7-21c311b5e012'
                    }
                    try:
                        # downloader 下载器
                        response = requests.get(url, headers=headers)
                        dataQueue.put(response.text)
                    except Exception as e:
                        print('下载出现异常', e)


class ParserThread(threading.Thread):
    '''
    页面内容分析
    '''

    def __init__(self, thread_id, queue, info_list):
        threading.Thread.__init__(self)  # 上面使用了super()
        self.thread_id = thread_id
        self.queue = queue
        self.info_list = info_list

    def run(self):
        print(f'启动线程：{self.thread_id}')
        while not flag:  # 这里有什么优化思路？
            try:
                item = self.queue.get(False)  # 参数为false时队列为空，抛出异常
                if not item:  # 为什么要判断？
                    continue
                self.parse_data(item)
                self.queue.task_done()  # get之后检测是否会阻塞
            except Exception as e:
                pass
        print(f'结束线程：{self.thread_id}')

    def parse_data(self, item):
        '''
        解析网页内容的函数
        :param item:
        :return:
        '''
        try:
            html = etree.HTML(item)
            current_city = html.xpath('//*[@id="filterCollapse"]/div[1]/div[2]/li/div[1]/a[1]/text()')[0]
            works = html.xpath('//*[@id="s_position_list"]/ul/li')
            for work in works:
                try:
                    # city = work.xpath()
                    companyname = work.xpath('./div[1]/div[2]/div[1]/a/text()')[0]
                    workname = work.xpath('./div[1]/div[1]/div[1]/a/h3/text()')[0]
                    salary = work.xpath('./div[1]/div[1]/div[2]/div/span/text()')[0]
                    response = {
                        'current_city': current_city,
                        'companyname': companyname,
                        'workname': workname,
                        'salary': salary
                    }
                    # print(response)
                    info_list.append(response)
                except Exception as e:
                    print('work error', e)

        except Exception as e:
            print('page error', e)


class ConnDB(object):
    def __init__(self, dbInfo, sqls):
        self.host = dbInfo['host']
        self.port = dbInfo['port']
        self.user = dbInfo['user']
        self.password = dbInfo['password']
        self.db = dbInfo['db']
        self.sqls = sqls

    def run(self):
        conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.db,
        )

        cur = conn.cursor()
        try:
            cur.execute(sqls)
            # 关闭游标
            cur.close()
            conn.commit()
        except:
            conn.rollback()
        # 关闭数据库连接
        conn.close()


cityQueue = Queue()
cityQueue.put('beijing')
cityQueue.put('shanghai')
cityQueue.put('guangzhou')
cityQueue.put('shenzhen')
dataQueue = Queue()
flag = False

if __name__ == '__main__':
    dbInfo = {
        'host': 'localhost',
        'port': 3306,
        'user': 'caiwei',
        'password': '123456',
        'db': 'week03'
    }
    info_list = []

    pageQueue = Queue(16)
    for page in range(1, 11):
        pageQueue.put(page)

    # 爬虫线程
    crawl_threads = []
    crawl_name_list = ['crawl_1', 'crawl_2', 'crawl_3']
    for thread_id in crawl_name_list:
        thread = CrawlThread(thread_id, pageQueue, cityQueue)
        thread.start()
        crawl_threads.append(thread)

    # 解析线程
    parse_thread = []
    parser_name_list = ['parse_1', 'parse_2', 'parse_3']
    for thread_id in parser_name_list:
        thread = ParserThread(thread_id, dataQueue, info_list)
        thread.start()
        parse_thread.append(thread)

    # 结束crawl线程
    for t in crawl_threads:
        t.join()

    # 结束parse线程
    flag = True
    for t in parse_thread:
        t.join()

    print(info_list)

    # 存入数据库
    try:
        sqls = 'insert into workinfo_tbl(current_city, companyname, workname, salary) values'
        for i in range(len(info_list)):
            # sqls += '(' + ','.join(info_list[i]) + ')'
            sqls += f'("{info_list[i]["current_city"]}", "{info_list[i]["companyname"]}", "{info_list[i]["workname"]}", "{info_list[i]["salary"]}"),'
        sqls=sqls[:-1]
        print(sqls)
        db = ConnDB(dbInfo, sqls)
        db.run()
    except Exception as e:
        print(e)
