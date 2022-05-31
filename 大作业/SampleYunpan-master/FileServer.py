# -*-coding:utf-8-*-
import socket
import threading
import subprocess
import sys
import os
import time
import base64
import shutil
import time

md5list = './md5list.txt'


# 获取当前路径下文件和文件夹列表
def GetLs(path):
    fileList = os.listdir(path)
    result = []
    for f in fileList:
        if os.path.isdir(f):
            f = f + '/'
        result.append(f)
    return result


# 收到客户端的exit请求，断开连接并返回信息
def IfExit(sock, addr):
    sock.send('Bye!'.encode('utf-8'))
    sock.close()
    print('Connection from %s:%s closed.' % addr)


# 收到客户端的ls请求，获取当前文件夹的文件列表并返回给客户端
def IfLs(sock, path):
    # print 'IfLs ' + path
    fileList = GetLs(path)
    list_file = ' '.join(fileList)
    # print list_file
    sock.send(list_file.encode('utf-8'))


# 收到客户端的cd请求，更改全局变量path的值，在其后加入cd的目录，一遍ls命令中使用
def IfCd(sock, path):
    rec = sock.recv(1024).decode('utf-8')
    if rec == "..":
        tmp = path.split('/')
        if path[-1] == '/':
            tmp = tmp[:-2]
        else:
            tmp = tmp[:-1]
        newpath = '/'.join(tmp) + '/'
        if path == '.':
            newpath = '.'
    elif rec[0] == '.':
        if rec[-1] == '/':
            newpath = rec
        else:
            newpath = rec + '/'
    else:
        if rec[-1] == '/':
            newpath = path + '/' + rec
        else:
            newpath = path + '/' + rec + '/'
    if os.path.isdir(newpath):
        sock.send('OK'.encode('utf-8'))
        return newpath
    else:
        sock.send('Error Dir!'.encode('utf-8'))
        return path


# 收到客户端的upload请求，首先接受文件MD5码，与md5list比较是否存在相同的MD5码，如果有直接执行cp即可；如果没有，服务器接收客户端发来的文件，存在path目录，并更新md5list
def IfUpload(sock, path):
    print("starting reve file!")
    filename = sock.recv(1024)
    m = sock.recv(1024)
    with open(md5list, 'rb') as f:
        while True:
            str = f.readline()
            if not str:
                break
            list = str.split()
            if len(list) >= 2:
                if m == list[0]:
                    src = list[1] + filename
                    det = path
                    shutil.copy(src.decode('utf-8'), det)
                    return

    with open(md5list, 'a+') as f:
        str = m.decode('utf-8') + ' ' + path + '\n'
        f.write(str)
    path = path + filename.decode('utf-8')
    # print path
    with open(path, 'wb') as f:
        while True:
            data = sock.recv(1024)
            if data.decode('utf-8') == 'EOF':
                print("recv file success!")
                break
            f.write(data)


# 收到客户端的download请求，向客户端发送文件
def IfDownload(sock, path):
    print("starting send file!")
    filename = sock.recv(1024).decode('utf-8')
    path = path + filename
    with open(path, 'rb') as f:
        while True:
            data = f.read(1024)
            if not data:
                break
            sock.send(data)
            time.sleep(1)
    sock.send('EOF'.encode('utf-8'))
    print("send file success!")


# 收到客户端发来的用户名密码，验证是否正确，返回登录信息
def isLogin(sock):
    cnt = 3
    if not os.path.getsize('user_pass.txt'):
        while not isRegist(sock):
            pass
        return True
    while cnt > 0:
        username = sock.recv(1024).decode('utf-8')
        if username == 'start regist':
            while not isRegist(sock):
                pass
            return True
        passwd = sock.recv(1024).decode('utf-8')
        with open('user_pass.txt', 'r') as f:
            for i in f:
                user = ' '
                pswd = ' '
                if len(i) > 0:
                    user, pswd = i.split()
                if username == user and passwd == pswd:
                    sock.send('OK'.encode('utf-8'))
                    print(username, 'login')
                    return True
            sock.send('FAIL'.encode('utf-8'))
        cnt = cnt - 1
    return False


def isRegist(sock):
    username = sock.recv(1024).decode('utf-8')
    fpasswd = sock.recv(1024).decode('utf-8')
    spasswd = sock.recv(1024).decode('utf-8')
    if fpasswd == spasswd:
        with open('user_pass.txt', 'a') as f:
            f.write(username)
            f.write(' ' + fpasswd + '\n')
            sock.send('create'.encode('utf-8'))
        print(username, 'created and login')
        return True
    else:
        sock.send('FAIL'.encode('utf-8'))
        return False


# 多线程要执行的main函数，实现上述功能
def main(sock, addr, path):
    print('Accept new connection from %s:%s' % addr)
    cnt = 0

    if isLogin(sock) is False:
        return

    while True:
        data = sock.recv(1024).decode('utf-8')
        if data == 'exit':
            IfExit(sock, addr)
            break
        elif data == 'ls':
            print(path)
            IfLs(sock, path)
        elif data == 'cd':
            path = IfCd(sock, path)
            # print path
        elif data == 'upload':
            IfUpload(sock, path)
        elif data == 'download':
            IfDownload(sock, path)
        elif data == 'registe':
            while not isRegist(sock):
                pass


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('10.106.203.97', 9999))
    s.listen(5)
    print('Waiting for connection...')

    while True:
        sock, addr = s.accept()
        path = './'
        t = threading.Thread(target=main, args=(sock, addr, path))  # 多线程
        t.start()
