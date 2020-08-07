#!/usr/bin/env python3

# 我去，真乱，考虑到这次我拿vi写的，原谅自己了

import subprocess,multiprocessing
from multiprocessing import Queue,Manager
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
import argparse,time,datetime,sys
import json
import ipaddress

'''

找点儿乐子而已，认真点儿当然没啥，但是戾气重就不好了，特别是夹杂偏见的时候

'''

# 得承认没懂到底全局变量应该咋用，可能js的给我影响太大
VERBOSE = None

# 后来想改成logging的，但还是保留吧
# 当时主要写这个是因为习惯于命令行输出到管道，然后python -m json.tool格式化的，后来才意识到特么自己就是在py
def myPrint(*args, **kwargs):
  global VERBOSE
  if VERBOSE:
    print("[MYDEBUG] ",*args,file=sys.stderr,**kwargs)
  else:
    pass

# 这个忘了炒的argparse还是getOpt了
def main():

  parser = argparse.ArgumentParser(description='山寨打包简版 ping or nc')
  # 本来想 -1 的，但是万一是单核，又得写python这个很啰嗦的条件表达式
  # 所以python 没有三目运算符真的不太好理解，觉的表意不清？
  parser.add_argument('-n','--nums','--worker-numbers',help='指定并发数量',
      type=int,default=multiprocessing.cpu_count())
  parser.add_argument('-f', '--tool',required=True,choices=('ping','tcp'),
      help='工作模式，ping主机段还是指定ip的1024内端口扫描')
  # 这个参数命名上偏奇怪，而且，挺罗嗦的后面写的，限定了一种可以接受的参数格式吧
  parser.add_argument('-ip',required=True, 
      help='如果工作模式是ping，这里要指定一个我能接受的ip段...如果工作模式指定了tcp，这里只能给一个ip地址？')
  parser.add_argument('-m', '--mode' , help='多线程还是多进程，选1',default="thread",choices=('proc','thread'))
  # 这个一直想写一个 -w 不跟参数就是缺省的文件名，跟了就是自定义的，没写就是不输出文件，不得要领
  parser.add_argument('-w', help='如果给定了该选项，保存结果到指定路径（到底-w 和选3是不是一个东西，没看懂题）')
  # 把选2和自己的debug输出混一起了，其实想-vvv来着，先放一放
  parser.add_argument('-v', "--verbose", help='是否输出更详细日志（兼选2 吧）',action="store_true")
 
  args = parser.parse_args()
  myPrint("args type",type(args))
  myPrint("args : ",args)
  if args.verbose:
    global VERBOSE
    VERBOSE = args.verbose
  with Manager() as manager:
    q = manager.Queue()
  
    cs = CopycatScanner(args.ip,args.nums,args.tool,args.mode,q)
    start=datetime.datetime.now()
    cs.scan()
    end=datetime.datetime.now()
    if(args.w):
      with open(args.w,mode='w') as f:
        json.dump(cs.result(),f)
    else:
      print(json.dumps(cs.result(),indent=4))
    myPrint(end-start)
    # ...

class CopycatScanner:

  def __init__(self,ip_address,workers,which_tool,mode,q):
    # 这个自己写的时候很痛快，静态的写多了，对这种可以类型可以中途换的潜意识里就情有独钟，但生产代码觉的不该这么做
    self.ip_addr = ip_address
    self.workers = workers
    # 依赖查找，是不是应该扣一分，自查时候发现应该放外面好了
    self.excutor = ThreadPoolExecutor if mode=='thread' else ProcessPoolExecutor
    self.tool = which_tool
    # 这个算是合理的一个依赖注入？
    self.queue = q

  def result(self):
    result = {}
    # 还想过是不是另起一个线程那边边放这边就收集的，就不写while循环了，可是感觉也没什么特别的好处，没弄
    while self.queue.qsize()>0:
      ele = self.queue.get()
      result[ele[0]]=ele[1]
    # 要特么不调用它就关不了，这个还是得写在外部框架的生命周期定义的清理过程里比较好
    # 或者就是实例化CopycatScanner前，with 一个Queue，然后注入到CopycatScanner里面
    return result

  # 内部方法是不是该加前导下划线？是该看看编码风格约束的东西了
  # 好像据说我喜欢的2个空格缩进也不被提倡，歪果仁的显示器真大
  def regular_ip(self):
    self.ip_addr = str(ipaddress.ip_address(self.ip_addr))
  
  # 还是觉得应该找一个库，但是看了nmap得文档，它的target specification真不是题目这么定义的，
  # 我一开始也只想CIDR的，但是发现标准库network传单个地址不抛异常，和我预期不符，那算了...
  def regular_ips(self):
    # net4 = ipaddress.ip_network(self.ip_addr)
    # self.ip_addr = net4.hosts()
    ip_range_pair = self.ip_addr.split("-")
    if len(ip_range_pair) !=2:
      raise Exception("format is not support",self.ip_addr)
    start = [x for x in map(lambda x :int(x),ip_range_pair[0].split("."))];
    end = [x for x in map(lambda x :int(x) ,ip_range_pair[1].split("."))];
    if len(start) !=4 or len(end) !=4:
      raise Exception("format is not support",self.ip_addr)
    # 这堆异常的串串可以再整整
    for i in range(0,3):
      if start[i]!=end[i]:
        raise Exception("only support like 192.168.0.1-192.168.0.100 , but ",
            self.ip_addr,"and pos ",i," is different")
      if start[i]<0 or start[i]>255 or end[i]<0 or end[i]>255:
        raise Exception("only support like 192.168.0.1-192.168.0.100 , but ",
            self.ip_addr,
            f'and pos [{i}],value {start[i]} or {end[i]} or both is out of range')
    if start[3]>=end[3]:
        raise Exception("only support like 192.168.0.1-192.168.0.100 , but ",
            self.ip_addr)
    # 推导式写这么长...估计也就是写着时候还好
    # 可是推导式断哪里感觉精气神儿也都没了...
    self.ip_addr = [f'{str(end[0])}.{str(end[1])}.{str(end[2])}.' + str(x) 
        for x in range(start[3],end[3]+1 if end[3]<255 else 255)]

  def scan(self):
    if self.tool == 'tcp':
      self.scan_ports()
    else:
      self.scan_ips()

  def scan_ips(self):
    self.regular_ips()
    with self.excutor(max_workers=self.workers) as executor:
      for ip in self.ip_addr:
        executor.submit(self.scan_ip,str(ip))

  def scan_ip(self,ip):
    # 觉的不足以这周把python socket也撸一遍的，我一直不太确定这个run是个阻塞方法么？
    p = subprocess.run(["ping","-w 1 -c 1",ip],
        stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    self.queue.put((ip,"PONG" if (p.returncode==0) else "NO PONG"));
    myPrint(f'ip: {ip},ping exit code: {p.returncode}')

  def scan_ports(self):
    self.regular_ip()
    with self.excutor(max_workers=self.workers) as executor:
      # 好难受，我觉得一定有办法写成1024，比如0,1024，然后下面+1，也挺二的
      for port in range(1,1025):
        executor.submit(self.scan_port,str(port))
  
  def scan_port(self,port):
    try:
      # self 这东西挺二的，记得原来写js时候经常这样，不知道python的世界都怎么玩儿
      ip_addr = self.ip_addr
      # 确实没打算离开linux跑，我这个nc版本是Ncat: Version 7.50 ( https://nmap.org/ncat )，这货的版本也一直是我没太搞明白的一个东西
      p = subprocess.run(["nc","-w 10","-z",ip_addr,port])
      self.queue.put((port,"Connected" if (p.returncode==0) else "Connect Failed"));
      myPrint(f'port: {port},nc exit code: {p.returncode}')
    except Exception as e:
      # 这货竟然也是扔到池里面的错误不用点手段不打印
      myPrint("what's up?  ",e)
    finally:
      # 一开始有个拼写错，不打印错误是用这个检查出来的，跟渣渣是一样的...线程池和标准错误连起来得有点手段？
      myPrint("may the world peace with us ... , scan port ",port,self.queue[port])
      # time.sleep(2)
      pass

if __name__ == "__main__":
  main()

