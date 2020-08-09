学习笔记


第一节: scrapy 并发处理爬虫
    CONCURRENT_REQUESTS = 32
    DOWNLOAD_DELAY = 3 每次下载延时,每次下载后等待 3S 后再次下载
    CONCURRENT_

    卡点:
        1. 爬取目标网站的压力承载
        2. 爬虫运行机器可支撑的压力

    twisted 多任务的异步编程模型


第二节: 多进程
        了解进程的父子关系,父进程和子进程

        res = os.fork() 更贴近系统底层
            fork 会生成一个新的子进程,子进程也会执行 fork 后的程序
            res == 0 时代表当前进程是子进程,非 0 时代表当前进程为父进程且 res 值为父进程的进程号
            os.getpid() 获取当前进程的进程号
            os.getppid() 获取当前进程的父进程的进程号
            
        multiprocessing.Process() 更符合 python 思维,适合使用
            在 python 将每个任务视为一个函数,将函数通过 target 传递则表示创建一个进程用以执行传入函数名代表函数的逻辑
            group 分组
            target 表示调用对象
            name 别名
            args 表示被调用对象的位置参数元组,比如 target 是函数 a,它有两个参数 m n,那么 args 传入 (m, n)
            kwargs 表示调用对象的元组,和 args 都用于给函数 target 传参

            p = Process(target=f,args=('join',))
                定义一个子进程,其将执行 f 函数的逻辑,同时将元组作为参数传递进去
            p.start()
                启动一个进程
            p.join([timeout])
                父进程等待所有子进程结束后再结束,最多等待 timeout
                join 不能在进程启动前执行,不能 join 自身进程

            ext: 通过检查进程的 exitcode 以确定它是否终止


第四节：利用队列进行进程间通信
    队列使用最多
    queue 本身有引入锁机制，所以是进程安全的


第五节：进程通信的另外两种方式
    管道 pipe
        父进程, 子进程 = Pipe()
        父进程.recv()
        子进程.send()
            如果两个进程/线程同时对管道进行同时写入或读取，可能导致数据损坏

    共享内存
        a = Value('d', 3.14)
        b = Array('i', [1,2])
        进程不安全


第六节: 解决资源抢占问题
    如何保证进程和线程是安全的 -> 锁机制
    锁不保证顺序问题，只保证资源抢占问题

    from multiprocessing as mp
    l = mp.Lock() 定义锁
    l.acquire() 加锁
    l.release() 释放锁

    for _ in range(5):  下划线的作用只占位


第七节：进程池
    多进程处理时，当某个进程处理完以后，能自动创建一个新的进程去保证 CPU 利用率，而不是等待所有进程处理完再创建新的进程
    进程池体现的是多任务并发的概念，而不是顺序的概念，顺序由队列体现

    import Pool
    p = Pool(CPU 核数)
    p.apply_async(run, args=(i,)) run 指进程处理的函数对象 args 类型要求是元组
    p.close 关闭进程池，必须要在 p.join 前执行
    p.terminate 不管任务是否完成，强制结束进程池
    p.join 的目的是让父进程等待所有子进程处理结束后，继续父进程的工作,然后结束父进程
           不使用 join 将会导致死锁

    pool = p.apply_async(time.sleep, (10,))
    pool.get(timeout=1)
        上述两行代码会抛出 TimeoutError 的异常，说明 get() 尝试获取进程返回结果的 timeout 时间是指进程池启动子进程后就开始计时的
        而不是改行代码执行到了开始计时，这里感觉有点反常规思维
    pool.map 输出列表
    i = pool.imap 输出迭代器
        next(i)
        迭代器里的每个元素的类型可以是多样的

    random.choice([1,2,3,4])

第八节
    python 的多进程和多线程之间存在瓶颈，也是 python 和其它语言的区别之一
    多进程、多线程、协程
        进程
            进程之内除了执行内容还有很多系统额外的开销
            使用多进程可以让程序同时在跨 CPU 物理核心上运行，而仅仅多进程则是无法做到(因为当个进程的所在 CPU 核心是确定的)
        多线程
            跑在同一个同一个进程内
            线程间同步数据要简单的多
            使用方法：
                面向过程：
                    threading.Thread(target=run, args=("thread_1",)
                面向对象：
                    class MyThread(threading.Thread)
            线程的阻塞和异步描述
                阻塞：得到调用结果前，线程会被挂起
                非阻塞：不能立刻得到结果，不会阻塞线程
                同步：得到结果前调用不会响应
                异步：接收请求后，调用立刻返回，没有返回结果，通过回调函数发送实际结果
        协程
            进程和线程的调度都是系统控制的
            协程是为了让用户可以自主控制进程切换和实现进程切换的轻量级操作
    同步、异步 -> 被调用方的响应描述
    阻塞、非阻塞 -> 调用方的描述

    多进程和多线程不是对立的,可以同时混合使用

第九节：线程锁
    RLock 可以嵌套的 Lock
    加锁通常来说是加载每个线程处理实际逻辑的代码块
    高级锁
        条件锁
        信号量
        事件
        定时器

第十节：
    队列在在进程间使用主要用于进程间变量共享。但是在线程中的利用不同，因为线程间的变量本身就是共享的
    队列和堆栈：先进先出和先进后出
    队列是线程安全的
    优先级队列
        import queue
        q = queue.PriorityQueue()
        优先级越小越先出，优先级相同则先进先出
    堆栈
        q = queue.LifoQueue()


    ext:生产者的示例 p11_queue.py 38 line 的 with 用法是什么意思，没明白

第十一节：线程池
    跟进程池类似
    一般线程池 from multiprocessing.dummy import Pool as ThreadPool
    并行任务的高级封装(python >= 3.2) from concurrent.futures import ThreadPoolExecutors
    照例的需要注意互相死锁的问题，老师介绍了因为线程间互相等待导致的死锁示例

第十二节：单、多进程线程的新能对比和 GIL
    单进程、线程和多进程、线程的效率对比
    CPython 解析器的底层实现导致所谓的多线程是一个伪多线程,它有一个全局锁 GIL(全局解析锁)
    GIL 锁是为了降低解析器实现难度推出的进程锁，用于控制不同线程对 CPU 资源的争抢上，实际上多线程同一时刻只有一个线程在使用 CPU
        每个进程只有一个 GIL
        线程只有拿到 GIL 锁才可以使用 CPU 资源
        多线程在不涉及 CPU 操作时是可以同时运行的，例如等待请求回调等
        GIL 锁导致在纯 CPU 开销时会发现跟单进程单线程效率相近(可以认为相等)，但是在 IO 密集时效率会得到提高


第十三节：实现迷你 scrapy