# -*-coding:utf8-*-
import _tkinter
import socket
import sys
import os
import tkinter
from tkinter import filedialog
import time
import getpass
import base64
import hashlib


# 向服务器发起ls请求，收到返回信息表示当前文件目录结构


def IfLs(s, se):
    s.send(se[0].encode('utf-8'))
    print(s.recv(1024).decode('utf-8'))


# 向服务器发起cd请求，收到返回信息表示cd执行结果，若失败，输出Error Dir!
def IfCd(s, se):
    s.send(se[0].encode('utf-8'))
    s.send(se[1].encode('utf-8'))
    rec = s.recv(1024).decode('utf-8')
    if rec == 'Error Dir!':
        print(rec)


# 向服务器发起exit请求，断开连接并退出当前客户端
def IfExit(s, se):
    s.send(se[0].encode('utf-8'))
    print(s.recv(1024).decode('utf-8'))


# 向服务器发起upload请求，使用tk库，打开图形化文件管理器选择文件并发送
def IfUpload(s, se):
    s.send(se[0].encode('utf-8'))
    root_window = tkinter.Tk()
    root_window.mainloop()
    fi = filedialog.askopenfilename()
    if fi == '': 
        return
    # print filename
    filename = fi.split('/')[-1]
    s.send(filename.encode('utf-8'))
    m = hashlib.md5()
    m.update(filename.encode('utf-8'))
    with open(fi, 'rb') as f:
        while True:
            data = f.read(1024)
            if not data:
                break
            m.update(data)
    s.send(m.hexdigest().encode('utf-8'))

    with open(fi, 'rb') as f:
        while True:
            data = f.read(1024)
            if not data:
                break
            s.sendall(data)
        time.sleep(1)
        s.sendall('EOF'.encode('utf-8'))
        print("upload file success!")


# 向服务器发出download请求，收到服务器发来的文件，并下载到当前目录
def IfDownload(s, se):
    s.send(se[0].encode('utf-8'))
    if (len(se) < 1):
        print("please input download file name")
        return
    filename = se[1]
    s.send(filename.encode('utf-8'))
    print("downloading~~")
    with open(filename, 'wb') as f:
        while True:
            data = s.recv(1024)
            if data.decode('utf-8') == 'EOF':
                print("download file success!")
                break
            f.write(data)


def Regist(s):
    print('Registing')
    username = input('please input username: ')
    while True:
        s.send(username.encode('utf-8'))
        passwd = input('please input passwd: ')
        s.send(passwd.encode('utf-8'))
        passwd = input('please input passwd again: ')
        s.send(passwd.encode('utf-8'))
        data = s.recv(1024).decode('utf-8')
        if data == 'create':
            print('creat successfully')
            break
        else:
            print('creat Failed,please input password again')
            

# 向服务器发送用户名密码，返回是否登录成功
def Login(s):
    if not os.path.getsize('user_pass.txt'):
        print('User Dictionary is Empty,Please Registe a User')
        Regist(s)
        return True
    print('Please Login First')
    cnt = 3
    isLogin = False
    while cnt > 0:
        username = input("Your Username: ")
        s.send(username.encode('utf-8'))
        passwd = input('Your Password: ')
        s.send(passwd.encode('utf-8'))
        isLogin = s.recv(1024).decode('utf-8')
        if isLogin == 'OK':
            return True
        cnt = cnt - 1
        print('Error Login! You have %d times.' % cnt)
        print('or you want to regist a user? y:yes n:enter')
        choose = input()
        if choose == "yes":
            s.send('start regist'.encode('utf-8'))
            Regist(s)
            return True
    return False


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('10.106.203.97', 9999))

    if Login(s) is False:
        s.close()
        exit()

    print('''Please Input Next Choose:
    1) ls               -- list all files and dirs
    2) cd <dir>         -- change dir
    3) download <file>  -- download your files
    4) upload           -- upload your files
    5) exit             -- exit our client''')

    while True:
        data = input(">>")
        se = data.split()
        if se[0] == 'ls':
            IfLs(s, se)
        elif se[0] == 'cd':
            IfCd(s, se)
        elif se[0] == 'exit':
            IfExit(s, se)
            break
        elif se[0] == 'upload':
            IfUpload(s, se)
        elif se[0] == 'download':
            IfDownload(s, se)
        else:
            print('Error Input!')

    s.close()
