#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：dataset.py 
@File    ：Cilent.py
@Author  ：Polaris
@Date    ：2022-05-21 9:25
'''

from socket import *
from threading import Thread
import time


class Client():

    def __init__(self, name, client_post, server_post):
        # 初始化
        self.ClientPort = client_post
        self.ServerPost = server_post
        self.udp_socket = socket(AF_INET, SOCK_DGRAM)
        self.userName = name
        self.thread_rece = Thread(target=self.recv_msg)
        self.thread_send = Thread(target=self.send_msg)

    def start(self):
        # 运行
        self.udp_socket.bind(self.ClientPort)
        # 新登录的用户向服务端发送创建用户的信号
        data_info = self.userName + ' -n'
        self.udp_socket.sendto(data_info.encode('gb2312'), self.ServerPost)
        print(self.getTime(), '系统：您已加入聊天')
        self.thread_rece.start()
        self.thread_send.start()
        self.thread_rece.join()
        self.thread_send.join()

    def recv_msg(self):
        # 接收服务端下线信息
        while True:
            recv_data, dest_ip = self.udp_socket.recvfrom(1024)  # 1024 表示接收最大字节  防止内存溢出

            if recv_data.decode("gb2312") == 'exit' and dest_ip == self.ServerPost:
                print(self.getTime(), '客户端已退出')
                self.udp_socket.close()
                break
            print(recv_data.decode("gb2312"))

    def send_msg(self):
        # 发送信息
        while True:
            data_info = input()
            self.udp_socket.sendto(data_info.encode('gb2312'), self.ServerPost)
            if data_info == 'exit':
                break

    def getTime(self):
        # 返回时间
        return '[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ']'


if __name__ == '__main__':
    Postnum = int(input('我方使用端口号: '))
    name = input('我方用户名: ')
    client = Client(name, ('192.168.254.1', Postnum), ('192.168.254.1', 5010))
    client.start()