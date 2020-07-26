import random
import requests
from bs4 import BeautifulSoup as bs
from time import sleep
import pandas as pd


def get_data():
    url = 'https://maoyan.com/films?showType=3'
    headers = {
        # 'user-agent': user_agent,
        'Cookie': 'uuid=b264e5beac28458db35f.1595511123.1.0.0; mtcdn=K; userTicket=tQTZaCEckOTWIQrpSomnYdNwWpQbhemHZLMuAbwd; u=290257956; n=LTF444070036; lt=q9lbT-q8Ot2yymfq7P___PN3odUAAAAAHAsAADUu-rsjxttUmmb2VcAx0zInyoFjnpzYZQsrCzlAh03y4Z8_Cbb2Asw78MVkKXHYrA; mt_c_token=q9lbT-q8Ot2yymfq7P___PN3odUAAAAAHAsAADUu-rsjxttUmmb2VcAx0zInyoFjnpzYZQsrCzlAh03y4Z8_Cbb2Asw78MVkKXHYrA; token=q9lbT-q8Ot2yymfq7P___PN3odUAAAAAHAsAADUu-rsjxttUmmb2VcAx0zInyoFjnpzYZQsrCzlAh03y4Z8_Cbb2Asw78MVkKXHYrA; lsu=',
        # 'Accept': '*/*',
        # 'Accept-Encoding': 'gzip, deflate, br',
        # 'Accept-Language': 'zh-CN,zh;q=0.9',
        # 'Cache-Control': 'no-cache',
        # 'Connection': 'keep-alive',
        # 'Content-Type': 'application/x-www-form-urlencoded',
        # 'Host': 'monitor.maoyan.com',
        # 'Origin': 'https://maoyan.com',
        # 'Pragma': 'no-cache',
        # 'Referer': 'https://maoyan.com/films?showType=3',
        # 'Sec-Fetch-Dest': 'empty',
        # 'Sec-Fetch-Mode': 'cors',
        # 'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    }

    bs_info = bs(requests.get(url, headers=headers).text, 'html.parser')

    data_list = [['电影名', '类型', '上映时间']]
    times = 0

    for div in bs_info.find_all('div', attrs={'class': 'movie-hover-info'}):
        movie_name = div.find('span', class_='name').text
        movie_type = div.find_all('div', attrs={'class': 'movie-hover-title'}, limit=2)[1].text\
            .replace(' ', '').replace('\n', '').replace('类型:', '')
        movie_date = div.find_next('div', attrs={'class': 'movie-hover-title movie-hover-brief'}).text\
            .replace(' ', '').replace('\n', '').replace('上映时间:', '')

        print('%s %s %s' % (movie_name, movie_type, movie_date))
        data_list.append([movie_name, movie_type, movie_date])
        times = times + 1
        if times >= 10:
            break

        sleep(random.randrange(1, 3))

    return data_list


def save_data(data_list):
    data = pd.DataFrame(data=data_list)

    # windows需要使用gbk字符集
    data.to_csv('./movie1.csv', encoding='utf8', index=False, header=False)


save_data(get_data())
# get_data()
# test_data = [['釜山行2：半岛', '动作／惊悚', '上映时间:2020-08-12'], ['唐人街探案2', '喜剧／动作／悬疑', '上映时间:2018-02-16']]
# save_data(test_data)
