#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：main.py 
@File    ：client.py
@Author  ：Polaris
@Date    ：2022-05-27 10:46
'''
from socket import *
from time import ctime
from threading import Thread
import time

flag = True

Host = '192.168.254.1'
Port = 10000
Addr = (Host, Port)

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(Addr)

name = input('请输入用户名:')
msg = '!usr %s'%name
tcpCliSock.send(msg.encode('utf-8'))

def getTime():
    return '[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ']'


def readMsg(tcpCliSock):
    global flag
    while flag:
        recv_data = tcpCliSock.recv(1024)
        data_infp = recv_data.decode('utf-8')
        if data_infp == "exit":
            print('%已成功退出')
            flag = False
            break
        elif data_infp.split()[0] == "!user" or data_infp.split()[0] == "!客户端":
            print(data_infp)
        else:
            mname = data_infp.split('\n')[1]
            command = mname.split('--')[1]
            if command == 'ta':
                print(recv_data.decode('utf-8').split('--')[0])
            else:
                myname = command.split(' ')[1]
                if myname == name:
                    print(recv_data.decode('utf-8').split('--')[0])

def writeMsg(tcpCliSock):
    global flag
    while flag:
        msg = input('')
        msg = getTime() + ' ->[' +name + ']\n' + msg
        tcpCliSock.send(msg.encode('utf-8'))


t1 = Thread(target=readMsg, args=(tcpCliSock,))
t1.start()

t2 = Thread(target=writeMsg, args=(tcpCliSock,))
t2.start()
t1.join()
t2.join()
tcpCliSock.close()