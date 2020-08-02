学习笔记

第一节：捕获异常
    意义：程序的健壮
    语法：
        try: ... except: 允许嵌套
        try: ... except Exception as e: 捕获所有异常,e 指异常提示信息
        try: ... except (AException, BException) as e:同时捕获多个异常
    traceback 异常跟踪,异常信息在 Trace back 信息的最后一行
    异常捕获过程
        1. 异常类吧错误信息打包到一个对象
        2. 该对象会自动查找调用栈
        3. 直到运行系统找到明确声明如何处理此类异常的位置后程序终止
    抛出异常 raise 关键字
    finally 无论异常有没有捕获处理,都要做的逻辑,设置这个 finally 的原因还是因为上述的 “异常后的程序不会被执行”
    自定义异常：
        继承自 Exception,注意这里不是 BaseException
        必须实现两个方法 __init__ 和 __str__
    知识点：
        异常也是一个类,所有异常都继承 BaseException
        如果程序中间抛出异常并被捕获,异常后的部分程序不会被执行,应该结合内核对程序的解析调用理解
    
    pretty_errors: 异常堆栈信息美化的包
        pip3 install pretty_errors

    with 优雅的类调用操作关键字
        最常见是用在文件操作了
        with open('a.txt', encoding='utf-8') as file_obj:
            pass
        不需要自主处理 file.close()
    
    魔术方法：
        __init__ 构造函数
        __str__
        __enter__ 类被调用是执行,有点像 __init__ 但是应该在它之后
        __exit__ 类调用执行完毕的最后时刻执行,析构
        __call__ 将类伪装成一个函数,使得可以直接调用类


第二节：mysql
    PyMySql
        import pymysql
        创建数据库连接,获取游标,操作,关闭游标,释放连接
        pymysql.connect
        pymysql 的事务不需要定义开启,conn.cursor 就是同时初始化事务
        视频示例返回元祖而且元祖最后一个值都是空字符串

        conn = pymysql.connect(...) 建立数据库连接
        cur = conn.cursor() 获取游标
        cur.execute(sql) 执行 sql
        cur.fetchone() 获取一条返回结果
        cur.fetchall() 获取所有返回结果
        conn.commit() 提交事务
        conn.rollback() 回滚事务
        cur.close() 关闭游标
        conn.close() 关闭连接
    
    python 的传参统一定义为类型？我曹这个点是真的吗
    if __name__ == '__main__' 只有在直接运行时会为真
    字符编码,常见的 utf8 utf8mb4


第三节：模拟浏览器请求头 User-Agent
    反爬虫和反反爬虫
    浏览器
        headers
        cookie
        refreer 指明从哪个链接跳转过来

    from fake_useragent import UserAgent
    ua = UserAgent(verifyssl=False)
    ua.chrome
    ua.random


第四节：Cookies
    解决 cookies 有效期的方法就是模拟用户登录
    request.session


第五节：WebDriver
    chromeDriver
        get
        switch_to_frame
        find_element_by_xpath
        find_element_by_id
        get_cookies
        close

    分块下载
        for chunk in r.iter_content(chunk_size=2014):
            if chunk:
                pdf.write(chunk)


第六节：验证码识别
    pillow
    from PIL import image


第七节：爬虫中间件和代理 IP
    下载器中间件和爬虫中间件（用得少）
    下载器中间件
        按优先级顺序，请求和响应分别按相反的顺序,优先级小的在请求时先加载,如果需要临时关闭中间件则把优先级改成 NONE
        代理 IP
    setting.py 设置
    python 读取 http_proxy 环境变量值：Request.meta['proxy']
    scrapy crawl spider_name --nolog


第八节：自定义中间件和随机代理 IP
    通过自定义选择实现以下方法来自定义下载中间件：
        process_request(request, spider)
            request 对象经过下载中间件时调用，优先级高先调用
        process_response(request, response, spider)
            response 对象经过下载中间件时调用，跟 process_request 反过来优先级低先调用
        process_exception(request, exception, spider)
            当 process_request 或 process_response 抛出异常时调用，实现它可以避免异常直接抛出去给到用户
        from_crawler(cls, crawler)
            cls 指类本身
            使用 crawler 来创建中间件对象，并（必须）返回一个中间件对象

    随机代理 IP
        配置 HTTP_PROXY_LIST 列表
        继承 HttpProxyMiddleware (from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware)
        crawler.settings.get
        from urllib import urlparse
            urlparse(proxy) 将 url 拆分
        random.choice
        流程： 实现 from_crawler 读取自定义的代理列表并返回给 __init__ 的自定义参数，__init__ 将各项代理并入到系统代理列表 self.proxies[scheme]，然后在 _set_proxy 方法对可选代理进行随机选择并设置到请求参数中


第九节：分布式爬虫
    分布式的意义：突破单机性能的限制
    难点
        1. 调度
        2. 存储的压力
        3. 接力
    scrapy 通过 redis 实现队列和管道的共享进而使得自己支撑分布式部署 pip3 install scrapy-redis
    使用 scrapy-redis 后 scrapy 的变化：
        1. 使用 RedisSpider 类替代 Spider
        2. Scheduler 的 queue 由 Redis 实现
        3. item pipeline 由 Redis 实现
    deamnize yes 避免在关闭中断后中断 redis 服务
    settings.py
        REDIS_HOST
        REDIS_PORT
        Scheduler
        DUPEFILTER_CLASS
        SCHEDULER_QUEUE_DUPEFILTER_CLASS
        SCHEDULER_PERSIST
        ITEM_PIPELINES