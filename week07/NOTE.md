学习笔记

第一节：对象
    python 的各种数据类型，比如字典元组都视为对象
    古典类和新式类
    对象是一个数据及其相关行为的集合
        属性：类属性和对象属性
            类属性在内存中只保存一份（）
            对象属性每个对象都保存一份
        方法

        类名.__dict__ 查看类的属性和方法，返回字典
        实例化对象名.__dict__ 查看改对象的对象属性，返回字典

    id(实例化对象名称) 返回类实例的唯一标识
    实例化对象名称.__class__() 返回对象信息，包含所在内存地址

    class test:
        live = 'live'
        def __init__(self):
            print('class init')

    c = test
    type(c) # 输出 <class 'type'>
    d = c() # 输出 class init
    type(d) # 输出 <class '__main__.test'>
    f = test() # 输出 class init
    type(f) # 输出 <class '__main__.test'>

    type(c) 输出 <class 'type'> 就很奇怪，这是啥东西
        网上的解释:
            type()是用来获对象的类型的。事实上，它既是一个对象，也是获取其它对象的类型的方法。
        所以上面的输出是指 c 是一个 type 类的对象?

    然后使用上述的类定义，发现 c = test 时是没有执行 print('class init') 的，
    也就是说这个 c 肯定不是一个已实例化的对象，那么它可能是类似一个指针之类的东西？
        因为 d = c() 时执行了构造函数，并且表现跟 f = test() 完全一致

    答案：
        c 是对象的引用

第二节
    __dict__ 和 dir(object)
    __dict__返回字典
    dir 返回列表

    setattr 给指定的类添加属性和值
        setattr(类名， 属性名， 属性值)

    _age 前置单下划线，内部属性，人为约定不可修改
    __fly 前置双下划线，私有变量，python 会实现不允许被修改
        __dict__ 返回的字典中，key 会变成 _类名__fly
    __init__ 前后双下划线，魔术方法

    显示 object 类的所有子类
    print(().__class__.__bases__[0].__subclasses__())
        ().__class__ 对象所属的类
        ().__class__.__bases__ 父类，输出元组
        ().__class__.__bases__[0].__subclasses__() 第一个父类的所有子类
        很好奇这里会输出什么东西啊

第三节 类方法描述器
    方法的三种类型：(普通)实例方法, classmethod, staticmethod
    @classmethod 和 @staticmethod 叫语法糖

    普通方法，至少一个 self 参数，标识该方法的对象
    classmethod， 至少一个 cls 参数，标识该方法的类，不管哪个类引用了这个方法，cls 就等于引用的类
        调用方法，类名.方法名()
        类方法中可以通过  cls.__name__ 获得当前类的类名
        类方法可以被继承
        类方法是可以调用类属性的, 类和类实例都可以调用 classmethod
        什么情况下应该用 classmethod
            1. cls 是指向调用类，所以涉及到类名的方法可以使用 classmethod
            2. 当类需要进行一系列预处理的"构造函数"的时候，就需要 classmethod
            3. python 中的构造函数有且仅有一个___new__,不满足使用所有有了 classmethod
    staticmethod， 由类调用，无参数,表示方法跟这个类有关系，但是又不想方法被强关联到类中

    __init__ 不是构造函数，是初始化函数
    __new__ 才是 python 的构造函数


第四节 静态方法描述器
    staticmethod 主要用于一些跟类需要用到又跟类实例关系不大的方法
        个人理解，静态方法只关注参数传入和输出的逻辑，不太涉及类实现功能的逻辑。

    staticmethod 不能引用类和对象的属性

第五节 描述器高级应用 __getattribute__
    对类属性的处理有前置的函数，拦截类实例化的变量赋值操作

    在类中,需要对实例获取属性这一行为进行操作，可以使用：
        __getattribute__
        __getattr__

        异同：
            1. 都可以对实例属性进行获取拦截
            2. __getattribute__() 对所有属性的访问都会调用该方法,就想一个对属性操作的钩子
            3. __getattr__() 适用于未定义的属性

第六节 另一个描述器的高级应用 __getattr__
    只在访问属性未在类的 __dict__ 中时被调用

    __getattribute__ 和 __getattr__ 的调用顺序:
        __getattribute__ > __getattr__ > __dict__
        __getattr__ 应该是在 super().__getattribute__ 中调用的

    注意：
        1. __getattribute__ 可能会导致性能问题
        2. __hasattr__ 和 dir 等内置方

第七节 描述器原理和属性描述器
    类似 __getattribute__ 等，也可以实现类属性的访问等的操作拦截，使用的技术就是描述器协议
    实现描述器协议的叫描述符

    django 中的 property
        property 本质上并不是函数，而是特殊的实现了数据描述符的类
        优点：
            1. 代码简介，可读性和可维护性更强(这点跟自己的思路不一样，没体会到可读性这点)
            2. 更好管理属性的访问
            3. 控制属性的访问权限，提高数据安全性
        作用
            1. 把方法伪装成一个属性(这个说法也没有很理解)
            2. 属性读写分离

    数据描述符：
        如果一个对象同时定义了 __get__() 和 __set__() 则称之为数据描述符
        如果仅定义了__get__() 则称为非数据描述符

    不是特别的理解这个实现逻辑和应用，这节要多看
    尝试在作业中使用 property

第八节 面向对象编程-继承
    封装-继承-承载-多态
    python3 的新式类，特点是所有的类都继承自一个类

    新式类和经典类的区别：当前类或者父类继承了 object 类的话就是新式类，否则就是经典类

    object 和 type 类的关系：
        1. object 和 type 都属于 type 类（class 'type'）
        2. type 类有 type 元类自身创建，object 由元类创建
            因为 type 是一个创建类对象的类，所以 type 成为元类，是一切的开始
            记住类由谁创建跟它们的父子类关系没有关联!!!!!
        3. object 的父类为空，没有继承任何类
        4. type 的父类为 object类（class 'object'）


    同时继承多个父类: class Son(Man, Woman)
            Base
          /     \
        Man     Woman
          \     /
            Son

        当两个父类有相同的功能实现时，类似菱形的继承关系，引入典型的继承问题，叫钻石继承
        钻石继承时，可以使用 mro 监测类的继承顺序：
            subClass.mro() 用列表按顺序列出了类方法查找的顺序

        经典类的查找方式是深度优先，新式类的查找方式是广度优先
            用 有向无环图DAG 的思路去分析其继承熟悉怒

    python 没有实现重载
第十二节 mixin模式
    mixin 解决的是多继承的问题