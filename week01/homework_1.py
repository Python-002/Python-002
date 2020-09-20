import requests
import lxml.etree
import pandas as pd



url = 'https://maoyan.com/films?showType=3'

header = {
    'Host': 'maoyan.com',
    'Connection' : 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Cookie':'__mta=175529629.1595214567832.1595430300201.1595433159879.24; uuid_n_v=v1; uuid=6B328860CA3611EAB2AE8B45D9A9C865974183C5D3AA45E4A09EFB519D772754; mojo-uuid=e56aa0eccb888ffcd01b0d9d6070e73b; _lxsdk_cuid=1736a32992fc8-054119405378e3-1d231c08-1fa400-1736a32992fc8; _lxsdk=6B328860CA3611EAB2AE8B45D9A9C865974183C5D3AA45E4A09EFB519D772754; _csrf=50c2b93637f7ec8e6324f38d52c9e6ee955f3d39509047be8ee5979c2f9f56ba; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1595262333,1595423488,1595424742,1595425145; __mta=175529629.1595214567832.1595298288312.1595425145065.22; mojo-session-id={"id":"8eab5a2bc245c2d52a0dc064639edcf5","time":1595433159681}; mojo-trace-id=1; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1595433160; _lxsdk_s=173773a0811-a3b-097-32d%7C%7C3'
}


response = requests.get(url, headers=header)


# xml化处理
selector = lxml.etree.HTML(response.text.replace("<dd>","</dd><dd>"))

#  得到新链接
new_links = selector.xpath('//*[@class="channel-detail movie-item-title"]/a/@href')
# print(new_links)
links = tuple(f'https://maoyan.com' + str(i) for i in new_links)
# print(links)
movie_infor = []
for i in range(10):
    new_url = links[i]
    response = requests.get(new_url, headers=header)
    selector = lxml.etree.HTML(response.text.replace("<dd>","</dd><dd>"))
    movie_name = selector.xpath('/html/body/div[3]/div/div[2]/div[1]/h1/text()')
    movie_genre = selector.xpath('//html/body/div[3]/div/div[2]/div[1]/ul/li[1]/a/text()')
    # 讲列表类型转化为字符串，更容易处理
    genre = "".join(movie_genre)
    movie_date = selector.xpath('/html/body/div[3]/div/div[2]/div[1]/ul/li[3]/text()')
    movie_infor.append(f'电影名称:{movie_name[0]}\n电影类型:{genre}\n上映时间:{movie_date[0]}\n')
    
    


movie1 = pd.DataFrame(data = movie_infor)
# windows需要使用gbk字符集
movie1.to_csv('./movie1.csv', encoding='utf8', index=False, header=False)



