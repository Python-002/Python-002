# -*- coding: utf-8 -*-

'''

估计有时会碰到猫眼儿的反扒机制，有时候捅着捅着就跑到一个美团验证中心的页面，然后出不来内容...

曾经加上浏览器里面获取的cookie用于调试，但是估计是cookie里面内容那么一大串也实在不想动脑子去看，应该有过期吧，这时候刷新浏览器都会到验证中心页面，有个滑块儿的人类鉴别验证

没太讲究，以熟悉...其实主要是熟悉python相关的库文档的各种社区风格了吧

'''

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'

header = {'user-agent':user_agent}

myurl = 'https://maoyan.com/films?showType=3'

response = requests.get(myurl,headers=header)

bs_info = bs(response.text, 'html.parser')

print(bs_info.prettify())

divs = bs_info.find_all('div', attrs={'class': 'movie-item-hover'},limit=10)
dds = bs_info.find_all('dd',limit=10)
print(len(dds))
items = []

for dd in dds:
    # print(dd.div.a.get('href'))
    div_with_class_movie_item_hover = dd.div('div',attrs={"class": "movie-item-hover"})
    item_divs = div_with_class_movie_item_hover[0].find_all('div',attrs={"class": "movie-hover-title"})
    item = []
    for item_div in item_divs:
        text_content = item_div.get_text()
        if '类型' in text_content:
            item.append(item_div.get("title"))
            item.append(item_div.get_text().strip().split(":")[1].strip())
        elif '上映时间' in text_content:
            item.append(item_div.get_text().strip().split(":")[1].strip())
    items.append(item)
        # print(":".join(list(map(lambda s:s.strip() ,item_div.get_text().strip().split(":")))))
print(items)

import time

pd.DataFrame(data = items).to_csv('./cat-eyes-hot.csv', encoding='utf8', index=False, header=False)
