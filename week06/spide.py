import requests
import lxml.etree
from lxml import etree
import pymysql
import random
import re

session = requests.Session()

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
            cur.close()
            conn.commit()
        except:
            conn.rollback()
        # 关闭数据库连接
        conn.close()


def get_inf():
    urls = tuple(f'https://movie.douban.com/subject/26794435/comments?start={20*page}&limit=20&sort=new_score&status=P' for page in range(3))
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'bid=iy4ZgCJ5WWI; __gads=ID=9064a9397b02eed2:T=1595212164:S=ALNI_MbcWi4YdUydGN-MV41Ye95_QKgPUQ; ll="118318"; __yadk_uid=ozTvxxP73Wa6fR5wq5UbPMjHK8VUOTJ8; _vwo_uuid_v2=D177D2ED2AED42280208CA32108EF06A7|a4a8dd1f8d8066e1f6196c2c685d0f57; douban-fav-remind=1; _ga=GA1.2.1087807558.1595212164; _gid=GA1.2.614159891.1598425852; ap_v=0,6.0; __utma=30149280.1087807558.1595212164.1598425859.1598429028.14; __utmc=30149280; __utmz=30149280.1598429028.14.8.utmcsr=m.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/search/; __utma=223695111.1899884097.1595212164.1598425859.1598429028.11; __utmc=223695111; __utmz=223695111.1598429028.11.7.utmcsr=m.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/search/; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1598429028%2C%22https%3A%2F%2Fm.douban.com%2Fsearch%2F%3Fquery%3D%25E5%2593%25AA%22%5D; _pk_id.100001.4cf6=fbc2ff951bcdedda.1595212162.11.1598429037.1598427201.',
        'Host': 'movie.douban.com',
        'Referer': 'https://movie.douban.com/subject/26794435/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
    }
    for url in urls:
        response = session.get(url, headers=header)
        pattern = re.compile('<div class="comment-item".*?comment-info">.*?rating".*?title="(.*?)">.*?"comment-time.*?title="(.*?)">.*?short">(.*?)</span>.*?</div>', re.S)
        items = re.findall(pattern, response.text)
        for item in items:
            movie_comment = item[2].strip().replace('\n', '').replace('\r', '')
            movie_star0 = item[0]
            coment_time = item[1][0:10]
            if movie_star0 == "力荐":
                movie_star = 5
            elif movie_star0 == "推荐":
                movie_star = 4
            elif movie_star0 == "还行":
                movie_star = 3
            elif movie_star0 == "较差":
                movie_star = 2
            else:
                movie_star = 1
            result = {
                'movie_star' : movie_star,
                'movie_comment' : movie_comment,
                'comment_time' : coment_time,
            }
            movielist.append(result)
    return movielist


if __name__ == "__main__":
    movielist = []
    dbInfo = {
        'host': 'localhost',
        'port': 3306,
        'user': 'caiwei',
        'password': '123456',
        'db': 'movies'
    }
    get_inf()
    #存入数据库
    try:
        sqls = 'insert into movie_tbl(movie_comment, movie_star,comment_time) values'
        for i in range(len(movielist)):
            sqls += f'("{movielist[i]["movie_comment"]}", "{movielist[i]["movie_star"]}","{movielist[i]["comment_time"]}"),'
        sqls=sqls[:-1]
        db = ConnDB(dbInfo, sqls)
        db.run()
    except Exception as e:
        print(e)