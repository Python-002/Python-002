# 学习笔记 week02

还是格言式为主吧，每节课记几句，其实看的不太系统，没有大块儿时间踏实儿仔细地看的，花插着看的

按每节课来吧

# 异常捕获预处理

+ python的异常trace 打印和Java是反着的？课程里面也说了，这个和直觉相反，不知道python这个设计怎么想的，估计是觉得直接tail log到最后所以这样看着方便？
+ 可能资源连接里的pretty_errors 都没印象在课程里提到了，可见看的多么的不认真
+ try...except...finally，我目前理解就是它叫except，而不是catch，从动作上挺传神的，主动的去匹配异常？而不是被动等待捕获？
+ Java叫throw，python是叫raise
+ with有点像try resource，上下文管理器对应的Closeable接口？存疑，后面还得再看

# MySQL

## MySQL本身

+ 安装个开发目的的很熟悉了，跳过

## MySQL Python 库

+ 选的PyMySQL
  - 课程里说是更稳定？
  - 但好像有地方看到说，是因为它安装最容易，因为纯python的
    * 安装就是```pip install pymysql```
+ 配置文件的部分...没听明白，不应该对接环境变量么？（12 factor）
  - 有[这么个](https://juejin.im/post/6844904079496314894) 地方可以参考，里面提到一个[库](https://pypi.org/project/environs/)
  - 后面再看这个吧

+ 好像哪里听说过有个Django的兼容和速度会更好一点
+ 课程里面提到Python的方法签名？是类型提示 typo hint？不是类型定义

... to be continue ...
