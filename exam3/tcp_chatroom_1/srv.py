
from socket import *
from time import ctime
from threading import Thread
import re

sockets = []

Host = '192.168.254.1'
Port = 10000
Addr = (Host, Port)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(Addr)
tcpSerSock.listen(5)
names = []


def main():
    while True:
        print("waiting for connection...")
        tcpCliSock, addr = tcpSerSock.accept()
        sockets.append(tcpCliSock)
        print('connected from:', addr, addr[0], ctime())
        t = Thread(target=readMsg, args=(tcpCliSock,))
        t.start()


def readMsg(tcpCliSock):
    while True:
        data = tcpCliSock.recv(1024)
        if data.decode('utf-8').endswith("exit"):
            data_info = data.decode('utf-8')
            name = data_info.split('->')[1]
            name = name.split('\n')[0]
            sockets.remove(tcpCliSock)
            tcpCliSock.send('exit'.encode('utf-8'))
            tcpCliSock.close()
            # print('客户端 %s 退出' % name)
            data = '!客户端 %s 退出' % name
            data = data.encode('utf-8')
            for socket in sockets:
                socket.send(data)
            print(data.decode('utf-8'))
            break
        if data.decode('utf-8').split(' ')[0] == "!usr":
            user = data.decode('utf-8').split(' ')[1]
            names.append(user)
            data = '!user %s in' % user
            data = data.encode('utf-8')
        for socket in sockets:
            socket.send(data)
        print(data.decode('utf-8'))
    tcpCliSock.close()


if __name__ == '__main__':
    main()
