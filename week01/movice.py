import requests
from bs4 import BeautifulSoup as bs
import pandas
url = 'https://maoyan.com/films?showType=3'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36 SE 2.X MetaSr 1.0'
accept = 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
cookie = '__mta=120987447.1595662508981.1595664459431.1595664552067.6; uuid_n_v=v1; uuid=5D3C7880CE4911EABF7AA517BC081B3029BC39D1AB324275A57B403348686B9C; _csrf=044622383354484e931ae1c7a80e07e66498fb1eb14ffbe17a277116ca90463b; _lxsdk_cuid=17384e5a0f8c8-0f0dbeba219912-c7d6957-121886-17384e5a0f8c8; _lxsdk=5D3C7880CE4911EABF7AA517BC081B3029BC39D1AB324275A57B403348686B9C; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1595662509; mojo-uuid=434943cc8a2cb209fa22064f9ca2b97d; mojo-session-id={"id":"4dc9f94198bd097c878e6c04c6ad90d5","time":1595662508885}; mojo-trace-id=13; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1595664648; __mta=120987447.1595662508981.1595664552067.1595664648636.7; _lxsdk_s=17384e5a0f9-c77-ecb-4fd%7C%7C20'
accept_Language = 'zh-CN,zh;q=0.9'
Upgrade_Insecure_Requests = '1'
#定义头信息
header = {'user-agent':user_agent,'Cookie':cookie,'Accept':accept,'Accept-Language':accept_Language,'Upgrade-Insecure-Requests':Upgrade_Insecure_Requests}
response = requests.get(url,headers=header)

if response.status_code ==200:
    print("请求成功")
else:
    print("错误代码:"+response.status_code)

bs_info = bs(response.text,'html.parser')
div_list =[]
num = 0
for tags in bs_info.find_all('div', attrs={"class": "movie-item-hover"}):
#     # print(tags)
#     div_list = div_list + tags
#     # num = num+1
#     # if tags <10:
#     #     div_list = bs_info.find_all('div', attrs={"class": "movie-item-hover"})
#     # else:
#     #     break
# print(div_list)

    for atag in tags.find_all("a"):
        print(atag.get("href"))
        tmp_url = atag.get("href")
        real_url = "https://maoyan.com" + tmp_url
        print(real_url)
        contain = requests.get(real_url,headers=header)
        real_info = bs(contain.text,"html.parser")
        mylist = []
        j=0
        for tags2 in real_info.find_all("div",attrs={"class":"movie-brief-container"}):
            print("----------------")
            # print(tags2)
            if tags2.h1["class"][0] == "name":
                moive_name = "电影名称："+ tags2.h1.get_text()
                print(moive_name)
                i = 0
                a = []
            for litags in tags2.find_all("li",attrs={"class":"ellipsis"}):
                a = tags2.find_all("li",attrs={"class":"ellipsis"})
            movietype = "类型："
            for atags in a[0].find_all("a"):
                # print(atags.get_text())
                movietype = movietype + atags.get_text()
            print(movietype)
            online_time = "上线时间："+ a[2].get_text()
            print(online_time)
            # print(a[2].get_text())
            # print("@@@@@@@@@@@@@@@")
            moive_info = [moive_name, movietype , online_time]
            print(moive_info)
            # mylist =moive_info

            movie1 = pandas.DataFrame(data = moive_info)
    # windows需要使用gbk字符集
            movie1.to_csv('./movie1.csv', encoding='utf8', index=False, header=0,mode='a')


