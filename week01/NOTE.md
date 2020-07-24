学习笔记

w3c标准官方文档：https://www.w3.org/standards/
网页分为3个部分：结构，表现和行为
1.结构：定义网页的形状和展现形式，结构用html语言
2.css主要是把我们的机构和表现形式做了分离
3 .js脚本：定义网页行为


当我们使用cookie时，代表着我们带着自己的用户名和密码的验证信息向网页发起请求。如果网页登录成功，也就是说cookie里面就包括了验证信息

文字一般反正<span>标签里面
链接一般用的<a>标签
图片一般使用的<img>标签

Scrapy的核心组件，见PPT p22-p24

scrapy的setting.py可以修改爬虫的很多设置

scrapy的选择器：
//div...:表示从上向下去找，匹配条件可以放任意长的路径的
./      :表示从你当前位置继续向下找
../     :表示从你当前的上一级的位置继续向下找

如果想取某个标签部分的属性的时候，要用/@href
                的内容的时候，要用/text()

scrapy.Request(....,dont_filter=False) dont_filter如果等于True,是用来解除去重功能。Scrapy 自带 url 去重功能，第二次请求之前会将已发送的请求自动进行过滤处理。所以将 dont_filter 设置为 True 起到的作用是解除去重功能，一旦设置成重 True，将不会去重，直接发送请求。

yiled作为语句 与 return的区别：
1.yiled更灵活，可以一个一个地返回所需要的值
2.return返回的是对象，yiled返回的是单独的一个值，不用去考虑返回的数据类型（视频中老师所讲 yield 返回的是单独的一个值，更准确的说返回的值必须是对象，在此章节我们暂定只把它理解返回一个值。在后面的章节多线程部分，我们会结合课程再对 yield 进行详解）
1. Scrapy Xpath 官方学习文档： https://docs.scrapy.org/en/latest/topics/selectors.html#working-with-xpaths
2. Xpath 中文文档：
https://www.w3school.com.cn/xpath/index.asp
3. Xpath 英文文档：
https://www.w3.org/TR/2017/REC-xpath-31-20170321/#nt-bnf
4. yield 表达式官方文档：
https://docs.python.org/zh-cn/3.7/reference/expressions.html#yieldexpr
5. yield 语句官方文档
https://docs.python.org/zh-cn/3.7/reference/simple_stmts.html#yield
6. Python 推导式官方文档：
https://docs.python.org/zh-cn/3.7/tutorial/datastructures.html#list-comprehensions

