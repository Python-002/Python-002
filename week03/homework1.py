#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from multiprocessing.pool import Pool
from time import sleep, time
import time
import random
import os
# from socket import *
from multiprocessing.dummy import Pool as ThreadPool
import threading
import multiprocessing as mp
import sys
import getopt
import socket
import struct
import json



def ping_run(new_ip,filename):
    iplist = []
    try:
        backinfo = os.system('ping -c 1 -w 1 %s'% new_ip) # 实现pingIP地址的功能，-c1指发送报文一次，-w1指等待1秒
        if backinfo != 0: #表示ping不同
            pass
        else:
            iplist.append(new_ip)
            fi = open(filename,'a+',encoding='utf-8')
            print('+++++++++++++++++++')
            print(new_ip)
            fi.write(json.dumps({'ip': new_ip}))
            fi.close()
            
    except Exception as e:
        print(e)
     

def tcp_run(ip,port,filename):
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        result = s.connect((ip,port))
        print('%d open' % port)
        fi = open(filename,'a+',encoding='utf-8')
        fi.write(json.dumps({'port': port}))
        fi.close()
    except Exception as e:
        print(e)
        pass
    finally:
        # if s:
        s.close()
        # if fi:
        # fi.close()

def ping_test(num_concurrent,start_ip,end_ip,filename):
    print("开始ping测试")
    # setdefaulttimeout(1)
    threads = []
    pool = ThreadPool(num_concurrent)
    #ip转化成int
    start_num = socket.ntohl(struct.unpack("I",socket.inet_aton(str(start_ip)))[0])
    end_num = socket.ntohl(struct.unpack("I",socket.inet_aton(str(end_ip)))[0])
    p = Pool(num_concurrent)#本机CPU是16核
    for intip in range(start_num,end_num+1):
        #int to ip
        new_ip = socket.inet_ntoa(struct.pack('I',socket.htonl(intip)))
        print(new_ip)
        t = threading.Thread(target=ping_run,args=(new_ip,filename))
        threads.append(t)
        t.start()
    t.join()
          
def tcp_test(num_concurrent,ip,filename):
    print("开始tcp端口测试")
    # setdefaulttimeout(1)
    threads = []
    pool = ThreadPool(num_concurrent)
    for port in range(10000):
        t = threading.Thread(target=tcp_run,args=(ip,port,filename))
        threads.append(t)
        t.start()
    t.join()
    




def main(argv):
    global get_time
    str_num_concurrent=''
    cmd=''
    ipaddr=''
    filename=''
    try:
        opts, args = getopt.getopt(argv,"n:f:w:v",["ip="])
    except getopt.GetoptError:
        print(
            """
            命令行参数举例如下：
            -n 4 -f ping --ip 192.168.0.1-192.168.0.100 -w result.json -v
            -n 10 -f tcp --ip 192.168.0.1 -w result.json -v
            说明：
            -n：指定并发数量。
            -f ping：进行 ping 测试
            -f tcp：进行 tcp 端口开放、关闭测试。
            --ip：连续 IP 地址支持 192.168.0.1-192.168.0.100 写法。
            -w：扫描结果进行保存。
            -v:打印扫描器运行耗时
            -w -v 为可选项
            """
        )
        sys.exit(2)
    # print(opts)
    for opt, arg in opts:
        if opt == "-n":
            str_num_concurrent = arg
        elif opt == "-f":
            cmd = arg
        elif opt == "--ip":
            ipaddr = arg
        elif opt == "-w":
            filename = arg
        elif opt == "-v":
            print("******************执行扫描器运行耗时****************") 
            get_time = True    
    num_concurrent = int(str_num_concurrent)
    if "ping" == cmd:
        print("进行ping测试")
        try:
            start_ip = ipaddr.split("-")[0]
            end_ip = ipaddr.split("-")[1]
            print(start_ip)
            print(type(start_ip))
            print(end_ip)
            ping_test(num_concurrent,start_ip,end_ip,filename)
        except expression as identifier:
            print("输入正确格式的命令")
    elif "tcp" == cmd:
        print("进行tcp测试")
        ip = ipaddr
        # print('tcp测试的ip' + ip)
        tcp_test(num_concurrent,ip,filename)


            
if __name__ == "__main__":
    get_time = False
    start_time = time.time()
    main(sys.argv[1:]) 
    if get_time: 
        end_time = time.time()
        print("***********************************************")
        print("time-consuming：%.2fs" %(end_time - start_time))
