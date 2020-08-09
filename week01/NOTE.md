学习笔记

第一节: 获取网页源代码
    requests 第三方,更简介
        导入: import requests
        requests.get(url, headers)
            url 即爬取目标网站地址
            headers 为了模拟人为操作伪造的浏览器请求头

    urllib 原生库
        导入: from urllib import request
        resp = request.urlopen(url, data, timeout)
            url 爬取目标网站地址
            data 可选参数
            timeout 可选参数,请求超时断开时长
        resp.read().decode()
            read() 读取 urllib.request 包获取到的网页内容,理解为固定写法
            decode() 理解为解码方法

    ext:
        pip3 install -r requirements.txt 根据配置文件指定版本号批量安装包,类似 composer require 安装 composer.json


第二节: 针对网页源代码做一些过滤
    beautifulSoup bs4库中的一个包,python 实现,每次查找均会扫描整个页面
        bs_info = bs(response.text, 'html.parser')
            html 是 bs 内置默认的/较为低效的解析方式
        bs_info.find_all('div', attrs={'class':'hd'})
            获取网页源代码中的所有 class 属性为 hd 的 div 标签
            attrs 参数可选,类型为字典
            返回类型: 列表,区别 get
        atag.get('href')
            获取 atag 指向的标签的 href 属性值
            返回类型: 字符串
        atag.find('span',).text
            获取 atag 下的 span 标签的 text 文本值
            返回类型: 字符串


第三节: 将浏览器操作翻译为 python 代码
    XPath 比 beautifulSoup 更高效的网页源码处理库
        导入: import lxml.etree (ext: pip3 install lxml)
        selector = lxml.etree.HTML(response.text)
            进行 xml 化处理,传递给下一步的选择器
            返回类型: selector 对象
        selector.xpath(xpath) 根据 xpath 定位选择器包含的内容详情
            xpath 字符串,唯一定位到该目标元素的 xpath 代码,chrome 右键-> Copy -> Copy XPath 直接复制到能唯一定位到目标元素的 xpath 代码
            返回类型: 字符串
    
    pandas 数据操作和保存的库,嗯其实人家主要是数据分析,输出数据统计结果只是其中一部分,除了 csv 还支持很多其他格式和模版
        导入: import pandas as pd
        movie1 = pd.DataFrame(data)
            data 需要格式化的数据
        movie1.to_csv(file_path, encoding, index, header) 将格式化后的内容输出到 csv 格式的文件中
            file_path 输出文件路径
            encoding 使用编码
            index 行名
            header 列名
            mode 模式,a 附加 w 写入(覆盖)

    ext:
        print(f'out: {aaa}') 中的 f 的意思是: 输出使用另一种替换模式,等价于 print('out: %s' % aaa)
            python 3.6 开始支持


第四节: 爬虫翻页
    tuple() 生成元组
    tuple(f'http://douban.com/top250?start={page * 25}&filter=' for page in range(10))
    这个写法要好好领会一下,一下子感觉好不习惯


第五节: python 的基础
    1. python 的调试模式(命令行执行 python3 进入)
    2. dir(math) 罗列包支持的方法列表
    3. help math 查看包的使用手册
    4. python 的关键字,基本都是常见语言的关键字,需要留意的有 lambda,yield
    5. python 的数据类型: int float dict list string 
    6. 流程控制语句: if(else) for(else) while(else) pass break continue yield la
    7. 推导式 yield
    8. 类和函数

    math 数学运算库
        import math


第六节: 前端基础知识
    http 协议
        和浏览器的关系
            浏览器解析前端代码渲染页面,前端代码在网络上通过 HTTP 协议传输
            爬虫就是模拟浏览器跟服务器通信,并对返回信息进行解析的程序
        请求和返回
            request response
        请求方式: get post delete head put
            get 限长,传参显式可见
            post 不定长只要不超过
        状态码
    W3C 标准
        一个协议体系,定义了网页的组成的结构(html)/表现(css)/行为(js)
    HTML 常用标签和属性
        html link meta script body head div a span input button p table li hr ol hr iframe style h1 img br footer
    CSS,JS,JSON


第七节: HTTP 协议
    HTTP 五层协议和 TCP/IP 七层协议
    headers
        HTTP CODE 具体问题具体分析,见笔记
        cookies
            客户端,鉴权
        User-Agent
            主要用于鉴别浏览器和反扒

第八节: Scrapy
    pip3 install scrapy
    import scrapy
    scrapy startproject project_name [dict_name] 原来还可以指定目录名
    scrapy crawl spider_name
    核心组件: 
        engine 核心
        scheduler 调度器,负责管理爬虫处理的队列
        spiders 爬虫使用框架主要编写的部分
        downloader 下载器,start_request 后框架为我们下载网页内容的地方
        item piplines 结构化解析数据的管道,用法跟自己理解的函数传入传出不太一样,应该理解成框架给定义好了一套数据解析的流程
    流程:
        启动爬虫 -> engine 协调将任务放入调度器的队列 -> 调度器管理任务状态记录等并通过 engine 调起 downloader 下载目标网站内容
        -> 内容被返回给 spiders 的 parse 过滤 -> 爬虫通过 item piplines 做数据层面的清洗和持久化

    ext: 有个问题就是我们写的 start_requests 方法是跑在哪个步骤的,是 engine 处理 start_requests 内容直接告诉下载器目标网址还是下载器自己接到任务去分析的？


第九节: scrapy 使用
    pip install scrapy
    scrapy startproject project_name
    目录结构:
        scrapy.cfg 
            setting 配置模块
        settings.py 爬虫配置,使用 pipline 要在这里配置开启
        spiders 爬虫模块,放我们的爬虫文件
        pipline.py 管道
    
    ext: allowed_domain 可选
        scrapy 会通过 start_urls 请求的第一个链接记录对方返回的头部信息并保存以作后续使用


第十节: 使用 scrapy 编写爬虫
    start_requests 和 parse:
        scrapy 内置的方法,分别在处理爬虫请求前置逻辑如指定链接等和解析爬虫结果

    ext: item 的意义不是很明白,有点像个监听事件,
        先实例化 Item 对象,处理好属性值,最后触发 piplines 中数据保存逻辑


第十一节: 
    pipline 有点像其它语言框架的 Model 的地位,处理数据保存落地的逻辑
    with.open 无需特地关闭文件
    to_csv 
        mode 默认 w 覆盖写, a 表示追加
        index_label 感觉是附加列分组的使用吧
        decimal 指定分隔符,直接用列表就不需要用这个了


第十二节:  xpath 效率比 beautiful 快 10 倍以上,基于 xml 解析(C 实现),基于当前选择器所在位置继续查找
    // 从上至下顺序查找匹配元素
    / 从上往下严格按照规则层级逐个查找匹配元素
    . 查找当前选择器所在元素的下级元素
    .. 查找当前选择器所在元素的所有平级元素
    text() 获取当前所在元素的 text 文本
    @href 获取当前所在元素的 href 属性
    extract
    extract_first
    strip 雷同 PHP 的 trim
    dont_filter=true 时指解除 allowed_domains 允许跨域名爬取

第十三节: yield 和 推导式
    yield: 逐个返回的 return,返回对象,队列
    推导式: 简写的 for
        每次循环的处理逻辑 for i in 循环次数 if 边界判断

问题和解决:
1. 爬取猫眼电影被检测,要求通过人机验证
    问题: 
        估计是爬虫伪装浏览器的参数就用了 User-Agent 和 Cookie 导致被美团识别, 要求进行滑动条、图片识别验证,也遇到了直接返回 json 内容是无权限。
    思路: 
        估计是爬虫伪装浏览器的参数就用了 User-Agent 和 Cookie 导致被美团识别,
        打算尝试补全更多浏览器参数模拟,或者更换 IP,IP 库使用还是一知半懂就很尴尬
        跟同学交流发现有的老哥是遇到 302 就手动处理验证码然后再跑爬虫来绕过,也就是人工验证。但是一方面我应该是进了黑名单,另一方面怎么人工处理命令行的验证页面是个问题
    解决:
        更新浏览器版本(但是我的 User-Agent 似乎没变),更换网络环境也就是更换 IP,然后还是遇到了验证码(这么看来应该是模拟的 Request Headers 被记录了),但是发现只要 iterm2 输出验证码页面后刷新猫眼电影页面就也可以进入验证页面,手动验证后重新执行爬虫就可以了。也就是同学分享的方法,这波是无敌交流,不过其实自己之前也误打误撞这么处理过,但是没能总结到这个经验真是遗憾
    ext: 
        另外发现取 Cookie 时,不是所有 Cookie 都是对的。Host: monitor.maoyan.com 才行, Host 为 wreport1.meituan.net 和 catfront.dianping.com 的 Cookie 都不行,这里暂时只是猜测看看老师会不会教

