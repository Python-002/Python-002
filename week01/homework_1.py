import requests
import lxml.etree

url = 'https://maoyan.com/films?showType=3'

# 声明为字典使用字典的语法赋值

header = {
    'Host': 'maoyan.com',
    'Connection' : 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'https://u.geekbang.org/lesson/24?article=261567',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'

}


response = requests.get(url, headers=header)
print(response.text)


# xml化处理
selector = lxml.etree.HTML(response.text)


links = selector.xpath('//*[@id="app"]/div/div[2]/div[2]/dl/dd[13]/div[1]/a/text()')
print('========================')
print(links)

#  电影id
# movies = selector.xpath('//div[@class="movie-item film-channel"]')
# print(movies)
# for movie in movies:
#     movie_id = movie.xpath('./a/@href')
#     print('===========')
#     print(movie_id)