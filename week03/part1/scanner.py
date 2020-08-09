# -*- coding: utf-8 -*-

import argparse
import os
import queue
from multiprocessing import Process, Queue
import threading
import time
import socket
import json


class Scanner:
    """
    scanner class 检查各IP段和端口可用性的扫描器
    """
    can_use_ip_list = Queue()
    cant_use_ip_list = Queue()
    can_use_port_list = Queue()
    cant_use_port_list = Queue()

    def __init__(
            self,
            ip='127.0.0.1',
            times=1,
            file=None,
            func='ping',
            is_multi_process=False,
            process_num=1,
            is_multi_thread=False,
            thread_num=1,
            count_use_times=True
    ):
        self.ip = ip
        self.times = times
        self.file = None
        self.func = func
        self.is_multi_process = is_multi_process
        self.process_num = process_num
        self.is_multi_thread = is_multi_thread
        self.thread_num = thread_num
        self.count_use_times = count_use_times

        self.ip_list = Queue()
        self.get_ip()

        if file:
            self.file = open(file, encoding='utf-8', mode='w')

    def start(self):
        """
        scanner 入口方法，处理进程级的任务调起
        :return:
        """
        if self.is_multi_process:
            for _ in range(self.process_num):
                Process(target=self.run_thread).start()

        else:
            self.run_thread()

    def run_thread(self):
        """
        通过线程级别处理任务
        :return:
        """
        if self.is_multi_thread:
            for _ in range(self.thread_num):
                threading.Thread(target=self.run).start()

        else:
            # 一个进程里单线程
            self.run()

    def run(self):
        print(f'当前进程号:{os.getpid()}, 自定义线程标识:{time.time()}')

        if self.func == 'ip':
            self.ping()
        elif self.func == 'port':
            self.socket()
        else:
            print('error func')

    def ping(self):
        # for ip in self.ip_list.get():
        while True:
            try:
                # 最长等待 1s
                ip = self.ip_list.get(True, 1)
                res = os.system('ping -c %s %s' % (self.times, ip))
                print(f'ping res: {res}')

                if res:
                    # cant
                    self.cant_use_ip_list.put(ip)
                else:
                    self.can_use_ip_list.put(ip)
            except queue.Empty:
                print('while end')
                break

    def socket(self):
        """
        检测ip上的端口是否开放
        """
        socket.setdefaulttimeout(2)
        socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while True:
            try:
                # 最长等待 1s
                ip = self.ip_list.get(True, 1)
                print(f'ip: {ip} >>>>>>>>>>>>>')

                for port in range(1, 1025):
                    try:
                        print(f'socket test {ip}:{port}')
                        result = socket_obj.connect_ex((ip, int(port)))
                        # socket_obj.connect((ip, int(port)))
                        # socket_obj.shutdown(2)

                        if result == 0:
                            print(f'{ip}:{port} is open')
                            self.can_use_port_list.put(ip + ':' + str(port))
                        else:
                            print(f'{ip}:{port} is close')
                            self.cant_use_port_list.put((ip + ':' + str(port)))

                    except Exception as e:
                        print(e)
                        print(f'{ip}:{port} is close')
                        self.cant_use_port_list.put((ip + ':' + str(port)))

            except queue.Empty:
                # 尝试捕抓 queue.Empty 异常在多进程下是无效的，只有在明确知道队列长度并尝试取超出长度的次数值时才会是 queue.Empty
                print('while end')
                break

    def get_ip(self):
        """
        根据输入准备好待处理的 IP 列表
        :return:
        """
        if '-' in self.ip:
            ips = self.ip.split('-')
            start_ip_num = self.ip_2_num(ips[0])
            end_ip_num = self.ip_2_num(ips[1])

            for ip_num in range(start_ip_num, end_ip_num + 1):
                self.ip_list.put(self.num_2_ip(ip_num))

        else:
            self.ip_list.put(self.ip)

    @staticmethod
    def ip_2_num(ip):
        # ip to int num
        lp = [int(x) for x in ip.split('.')]
        return lp[0] << 24 | lp[1] << 16 | lp[2] << 8 | lp[3]

    @staticmethod
    def num_2_ip(num):
        # int num to ip
        ip = ['', '', '', '']
        ip[3] = (num & 0xff)
        ip[2] = (num & 0xff00) >> 8
        ip[1] = (num & 0xff0000) >> 16
        ip[0] = (num & 0xff000000) >> 24
        return '%s.%s.%s.%s' % (ip[0], ip[1], ip[2], ip[3])

    @staticmethod
    def queue_2_list(the_queue):
        the_list = []

        try:
            for i in range(10000):
                msg = the_queue.get(True, 1)
                the_list.append(msg)
        except queue.Empty:
            # 尝试捕抓 queue.Empty 异常在多进程下是无效的，只有在明确知道队列长度并尝试取超出长度的次数值时才会是 queue.Empty
            print('queue_2_list end')

        return the_list

    def out(self):
        """
        通过 Output 类处理输出
        """
        output = Output(
            self.queue_2_list(self.can_use_ip_list),
            self.queue_2_list(self.cant_use_ip_list),
            self.queue_2_list(self.can_use_port_list),
            self.queue_2_list(self.cant_use_port_list),
            self.file
        )
        output.output_2_cmd()

        if self.count_use_times:
            print('use time:', time.time() - st)


class Output:
    """
    output class 专门提供给扫描器的输出管理类
    """
    def __init__(self, can_ip_list, cant_ip_list, can_port_list, cant_port_list, file):
        print('output --------------------')
        self.can_ip_list = can_ip_list
        self.cant_ip_list = cant_ip_list
        self.can_port_list = can_port_list
        self.cant_port_list = cant_port_list
        self.file = file

    def output_2_cmd(self):
        file_json = {}
        if self.can_ip_list:
            self.output('发现可用 IP 列表如下: ', self.can_ip_list)
            file_json['can_use_ip_list'] = self.can_ip_list

        if self.cant_ip_list:
            self.output('发现不可用 IP 列表如下: ', self.cant_ip_list)
            file_json['cant_use_ip_list'] = self.cant_ip_list

        if self.can_port_list:
            self.output('开放端口列表如下: ', self.can_port_list)
            file_json['can_use_port_list'] = self.can_port_list

        if self.cant_port_list:
            self.output('未开放端口列表如下: ', self.cant_port_list)
            file_json['cant_use_port_list'] = self.cant_port_list

        if self.file:
            json.dump(file_json, fp=self.file, ensure_ascii=False)

    @staticmethod
    def output(title, output_list):
        print(title)
        for item in output_list:
            print(item)


if __name__ == "__main__":

    '''
    -n ping 命令的并发数量
    -f 执行检查 ip / port 操作
    -p 指定 IP，可以单个或多个,多格式用 "-" 分割
    -w 结果输出到指定文件名
    -mp 是否多进程
    -pn 多进程时的进程数
    -mt 是否多线程
    -tn 多线程时的线程数
    -v 是否统计用时，默认 True
    
    test command:
    python3 part1/scanner.py -f ip -n 2 -p 192.168.0.1-192.168.0.3 -mp 1 -pn 2 -mt 1 -tn 2 -w output_ip.json
    python3 part1/scanner.py -f port -p 192.168.0.1-192.168.0.3 -mp 1 -pn 2 -mt 1 -tn 2 -w output_port.json
    '''
    parser = argparse.ArgumentParser(description='this is a IP scanner')
    parser.add_argument('-p', type=str, default=None)
    parser.add_argument('-n', type=int, default=1)
    parser.add_argument('-f', type=str, default=None)
    parser.add_argument('-w', type=str, default=None)
    parser.add_argument('-mp', type=bool, default=False)
    parser.add_argument('-pn', type=int, default=1)
    parser.add_argument('-mt', type=bool, default=False)
    parser.add_argument('-tn', type=int, default=1)
    parser.add_argument('-v', type=bool, default=True)
    args = parser.parse_args()
    st = time.time()
    print(args)

    scanner = Scanner(
        ip=args.p, times=args.n, func=args.f, file=args.w,
        is_multi_process=args.mp,
        process_num=args.pn,
        is_multi_thread=args.mt,
        thread_num=args.tn,
        count_use_times=args.v
    )

    scanner.start()
    # 很不灵活，需要优化每次请求超时时间
    time.sleep(60)
    scanner.out()
