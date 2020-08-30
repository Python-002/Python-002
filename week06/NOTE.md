学习笔记

Django
    开源 python 源码
    2005 年 7 月在 BSD 许可证下发布
    MTV(model,template,view) 和 MVC
    DRY 代码复用原则
        ORM、正则URL、模版可继承、用户认证、admin 管理系统、表单模型、存储、国际化系统
        除了国际化系统外都是常见的后台框架的特性
        哦国际化是指时区配置，那也是常见的配置了
    安装
        pip3 install [--upgrade] django==2.2.13
        >>> import django
        >>> django.__version__

Django
    django-admin startproject MyDjango

    项目目录结构
        manage.py 命令行工具
        /MyDjango/setting.py 项目配置文件

    python manage.py help
    python manage.py startapp index 创建应用
    应用目录
        index/migrations 数据库迁移文件夹
        index/models.py 模型
        index/apps.py 当前应用的配置文件
        index/admin.py 管理后台
        index/tests.py 自动化测试
        index/views.py 视图
        tpl 自主创建

    python manage.py 中 startapp 和 startproject 的区别
    python manage.py runserver [0.0.0.0:80]
        ctl + c 结束


第三节：setting.py 的配置
    项目路径、秘钥、域名访问权限、APP 列表、静态资源、模版文件、数据库配置、缓存、中间件
    os.path.dirname
    默认的调试模式是单用户访问的，多用户会互相阻塞，需要 WSGI

    INSTALLED_APPS 加载的应用列表，顺序加载，我们自定义的一般放在最后除非修改源码之类的
    MIDDLEWARE 中间件同样是顺序的
    ROOT_URLCONF url 匹配的文件路径，也就是路由文件
    TEMPLATES 模版设置
    WSGI_APPLICATION WSGI应用
    DATABASES 数据库配置
    STATIC_URL 静态文件目录

第四节：URLConf
    类比 laravel 的路由
    1. 如果传入 HTTPRequest 对象有 urlconf 属性（中间件设置），它的值会被 ROOT_URLCONF 替代
    2. django 加载 URLConf 模块并寻找匹配可用的 urlpatterns，Django 一次匹配每个 URL 模式直到成功或失败
    3. 一旦匹配成功，Django 会导入并调用相关的视图并传递以下信息：
        一个 HTTPRequest 实例
        一个或多个位置参数
    4. 如果匹配失败或者程序异常会调用错误处理视图

    from django.contrib import admin
    from django.urls import path,include
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('index.urls'))   # include 指往 index 应用的 urls 程序去匹配（必须跟进配置 urlpatterns 并制定视图）
    ]

    from . import views 在当前目录的同级下导入 views

    from django.shortcuts import render
    from django.http import HttpResponse
    def index(request):
        return HttpResponse('hello Django')

    请求调用路径
        MyDjango -> manage.py
        MyDjango -> setting.py -> ROOT_URLCONF
        MyDjango -> urls.py
        MyDjango -> setting.py -> INSTALLED_APPS
        index -> urls
        index -> views.index 视图

第五节：模块和包
    模块： .py 结尾的 python 程序
    包：存放多个模块的目录
        __init__.py 包被导入时执行的文件

    import 引入的时候，python 会从 site-packages 目录开始找需要的包
        site-packages 目录为:
            import os
            os.path.dirname(os.__file__)
        所以直接指定 from 是更高效的写法

第六节：让 URL 支持变量
    url 支持类型 str，int，slug（备注）, uuid（唯一 ID）, path

    path('<int:year>', views.year) 通过 <int> 校验 year 变量是否为整数，通过则传递给 views.year

    方法接收参数的方式：第一个参数 request 是固定的
        def year(request, year)
        def year2(request, **kwargs)
            print(kwargs['year'])

第七节：正则判断引入
    from django.urls import re_path
    re_path 代替 path
    re_path('(?P<year>[0-9]{4}).html', views.year, name='urlyear')
        ?P 指定紧跟的 <> 内的是匹配接收的变量名
        name 是给路径绑定名称，相当于 laravel 的 route()->name('urlyear')
            使用 <a herf="{% url 'urlyear' 2020 %}">2020 year</a>

    自定义匹配正则
        from . import converters
        register_converter(converters.IntConverter, 'myint')
        path('myint:year', views.year)

        converters 模版(三部分)
            class IntConverter:
                regex = '[0-9]+'
                def to_python(self, value):
                    # 从 url 读取后转成 python 程序处理的值转换
                    return int(value)
                def to_url(self, value):
                    # 跟 to_python 反过来
                    return str(value)

第八节： views
    HttpResponse('HELLO')                            200
    HttpResponseRedirect('/admin/')                  302
    HttpResponsePermanentRedirect('/admin/')         301
    HttpResponseBadRequest('BAD')                    400
    HttpResponseNorFound('not found')                401
    HttpResponseForbidden('error')                   403
    HttpResponseNotAllowed('refused')                405
    HttpResponseServerError('error')                 500


    快捷函数
        render 渲染视图
        redirect 重定向
        get_object_or_404 在给定的模型管理器上调用 get() 但他会引发 Http404 而不是 DoesNotExist 异常


第九节：ORM
    每个模型类都继承 django.db.models.Model
    模型类的每个属性都相当于一个数据库的字段

    from django.db import models
    class Person(models.Model):
        id = models.IntegerField(primary_key=True)
        name = models.CharField(max_length=10)
        还有诸如 AutoField 等

    python manage.py makemigrations 将 model 转成 python 的中间程序
    python manage.py migrate 将 python 中间程序应用到 ORM 的数据库上

    在 MyDjango 的 __init__.py 中处理数据库初始化

    将 Django 默认的数据库链接改成 pymysql
        import pymysql
        pymysql.install_as_MySQLdb()

第九节：ORM API(在 views 中使用)
    字段类型
    字段选项

    from index.models import *
    n = Name() # 实例化模型
    或
    from .models import Name

    增 Name.objects.create(name='xxx', ...)
    查 Name.objects.get(id=2).name
       Name.objects.values_list('name') # 注意返回类型是 QuerySet 对象
    改 Name.objects.filter(id=1).update(name='xxx')
    删 Name.objects.filter(id=2).delete()
       Name.objects.all().delete()

第十节： 模版 Templates
    1. 模版变量 {{ xxx }}
    2. 从 URL 获取模版变量 {% url 'urlyear' 2020 %} 读取名字叫 urlyear 的 url 路径并将 2020 作为参数传递进去
    3. 读取静态资源 {% static "css/wel.css" %}
    3. for 遍历输出标签 {% for type in list %} 和 {% endfor %}
    3. if 判断输出标签 {% if name.type == type.type %} 和 {% endif %}

第十一节：打通 MTV 展示数据库内容
    n = Name.objects.all()
    return render(request, 'books.html', locals())
        locals() 将所有当前函数的所有变量将作为参数传递过去,比如上面的 n 变量

第十二节：豆瓣需求的讲解
    bootstrap admin

第十三节:
    应用的创建应该根据系统模块的区分来划分不同应用

    在表已经存在时，就不需要通过 Django 来生成表了,此时可以通过以下直接从数据库表输出 Models
        python manage.py inspectdb > models.py
        反向之前需要配置好数据库的链接信息(setting.py)

第十四节:
    conditions = {'column__gte':0.5} column 字段的平均值大于等于 0.5

    取平均值
        from django.db.models import Avg

    star_avg = f"{T1.objects.aggregate(Avg('n_star'))['n_star__avg']:0.1f}"
        最后 0.1f 的意思是值取小数点后一位，0.2f 就是取两位
        这种写法还可以更优化

第十六节:
    {% extends "base_layout.html" %} 继承 base_layout 模版
    {% load static %} 读取 static 目录下文件一遍使用
    {% block head %} 和 {% block.super %}
        将 extends 继承的模版中的 head 部分引用并保留


第十七节:
    python 是一门解释性的语言不需要预先编译，所有没有所谓的入口函数
    从 manage.py 开始
        main() 开始针对特定功能去深入追代码，例如 runserver 执行步骤如下：
            解释参数
            加载 runserver
            检查 ORM 等
            服务化 WSGI
            动态创建类以接收请求

    python 是如何实现 if __name__ == '__main__' 的呢


第十八节: manage.py
    以 python3 django runserver 8080 为例

    main()
        os.environ.setdefault 设置环境变量
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv) 将命令行的参数悉数传入

    execute_from_command_line(runserver 8080)
        utility = ManagementUtility(argv)
        utility.execute() 调用 ManagementUtility 中的 execute 方法

    ManagementUtility.__init__ 初始化
    ManagementUtility.execute
        subcommand 就是 runserver
        setting.INSTALLED_APPS 读取配置
        if subcommand == 'runserver' and ... 这里针对 runserver 进行错误检查
            autoreload.check_errors
        self.fetch_command(runserver).run_from_argv(8080)


    fetch_command(runserver)
        app_name = commands[runserver]
        if isinstance(app_name, BaseCommand): # BaseCommand 判断 runserver 是否已经被加载到内存
            klass = load_command_class(runserver, subcommand)

    load_command_class(app_name, subcommand)
        module = import_module('%s.management.commands.%s' % (app_name, name)
        return module.Command()

    class Command(RunserverCommand) # 它继承了 RunserverCommand


    class RunserverCommand(BaseCommand) # 继承了 BaseCommand
    class BaseCommand # base.py
        self.execute(*args, **cmd_options) # 这里定义了这个方法，但是执行的不是它而是继承它的类











    经验：
        要注意追代码过程中 类似 __init__.py 文件导入或初始化的逻辑