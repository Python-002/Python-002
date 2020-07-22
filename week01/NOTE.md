# Week01 学习笔记

## 运行
作业一
进入作业目录
```
cd pa01
```
创建虚拟环境
```
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
```
运行脚本
```
./requests_crawler.py
```
作业二
进入作业目录
```
cd pa02
```
创建虚拟环境
```
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
```
进入scrapy project目录
```
cd maoyan
```
确认csv文件并不存在
```
test -f movies.csv && rm -rvf movies.csv
```
运行scrapy crawler
```
 scrapy crawl maoyan
```
## 感想
第一周学习里两种爬虫形式
* requests
* scrapy

以及两种html数据解析抓取的两种方式
* beautifulsoup
* xpath

requests相对简单直接，需要自己构造http请求
scrapy提供框架，不需要自己构造http请求，而且提供xpath的支持，另一种是css

bs的解析方式主要通过find来定位tag，而xpath提供更强大的xpath定位支持，相对易用直接，但是有自己的语法。
