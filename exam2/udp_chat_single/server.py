#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：dataset.py 
@File    ：server.py
@Author  ：Polaris
@Date    ：2022-05-21 9:23
'''

from socket import *
from threading import Thread
import time


class Server():
    user_name = {}  # dict 用户名:ip地址
    user_ip = {}  # dict ip地址:用户名
    __ServerOpen = True

    def __init__(self, post):


        self.ServerPort = post
        self.udp_socket = socket(AF_INET, SOCK_DGRAM)
        # 服务器端口
        self.udp_socket.bind(self.ServerPort)
        self.thread_rece = Thread(target=self.recv_msg)  # 接收信息线程
        self.thread_send = Thread(target=self.send_msg)  # 发送信息线程

    def start(self):
        print(self.getTime(), '服务端已启动')
        self.thread_rece.start()
        self.thread_send.start()
        self.thread_rece.join()  # 确保子线程按顺序执行
        self.thread_send.join()

    def recv_msg(self):

        # 接收信息
        while True:

            recv_data, dest_ip = self.udp_socket.recvfrom(1024)  # 1024 表示接收最大字节  防止内存溢出
            # 服务器关闭后就停止接收客户端信息，等待所有用户退出
            if not self.__ServerOpen:
                self.udp_socket.sendto('exit'.encode('gb2312'), dest_ip)
                name = self.user_ip.pop(dest_ip)
                self.sent_to_all(self.getTime() + ' 系统：%s已退出聊天' % name)
                # 重复直到所有用户退出
                while len(self.user_ip):
                    recv_data, dest_ip = self.udp_socket.recvfrom(1024)
                    self.udp_socket.sendto('exit'.encode('gb2312'), dest_ip)
                    name = self.user_ip.pop(dest_ip)
                    self.sent_to_all(self.getTime() + ' 系统：%s已退出聊天' % name)
                # 所有用户退出后关闭套接字
                print(self.getTime(), '服务端已关闭')
                self.udp_socket.close()
                break

            print(self.getTime(), dest_ip, recv_data)
            info_list = str(recv_data.decode("gb2312")).split(' ')  # 切割命令

            # 处理用户下线信号
            if str(recv_data.decode("gb2312")) == 'exit':
                self.udp_socket.sendto('exit'.encode('gb2312'), dest_ip)
                name = self.user_ip.pop(dest_ip)
                self.sent_to_all(self.getTime() + ' 系统：%s已退出聊天' % name)

            # -t处理私聊信号
            elif info_list[-2] == '-t':
                if info_list[-1] not in self.user_name.keys():  # 目前查询不到目标用户，向发送用户发起警告
                    data_info = self.getTime() + ' 系统：发送失败！用户不存在！'
                    self.udp_socket.sendto(data_info.encode('gb2312'), dest_ip)
                    continue
                # 查找目标用户ip地址并向目标用户发送消息
                dest_port = self.user_name[info_list[-1]]  # 接收方端口
                data_info = self.getTime() + ' %s：' % self.user_ip[dest_ip] + ' '.join(info_list[:-2])  # 需发送的信息
                self.udp_socket.sendto(data_info.encode('gb2312'), dest_port)

            elif info_list[-1] == '-n':
                # 新用户注册  用户名 端口号 -n
                data_info = self.getTime() + ' 系统：' + info_list[0] + '加入了聊天'
                self.sent_to_all(data_info)
                # 更新字典
                self.user_name[info_list[0]] = dest_ip
                self.user_ip[dest_ip] = info_list[0]

            elif info_list[-1] == '-ta':
                # 群发消息
                name = self.user_ip[dest_ip]
                data_info = self.getTime() + ' %s：' % name + ' '.join(info_list[:-1])
                self.sent_to_all_notMe(name, data_info)

    def sent_to_all(self, data_info):
        # 系统广播信息,包括给自己
        for i in self.user_ip.keys():
            self.udp_socket.sendto(data_info.encode('gb2312'), i)

    def sent_to_all_notMe(self, name, data_info):
        # 广播消息除了指定用户
        for i in self.user_name.keys():
            if i != name:
                self.udp_socket.sendto(data_info.encode('gb2312'), self.user_name[i])

    def getTime(self):
        return '[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ']'

    def send_msg(self):
        # 服务端输入exit后下线并通知所有用户
        while self.__ServerOpen:
            data_info = input()
            if data_info == 'exit':
                self.__ServerOpen = False
                print(self.getTime(), '服务端关闭中，等待所有用户下线')
                self.sent_to_all(self.getTime() + ' 服务器系统已关闭，请自行下线')
                break


if __name__ == '__main__':
    server1 = Server(('192.168.254.1', 5010))
    server1.start()
