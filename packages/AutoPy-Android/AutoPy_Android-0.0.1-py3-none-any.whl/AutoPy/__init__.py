# -*- coding: utf-8 -*-

import sys
import time
import os,_thread

if sys.version[0] == 2:
    from urllib2 import urlopen
else:
    from urllib.request import urlopen

server_url = 'http://127.0.0.1:33445?code='

def dian(x,y):
    f=urlopen(server_url+'0,'+str(x)+','+str(y))
    f.close()
    print(time.ctime()[11:19]+' [AutoPy]点击执行成功')
    time.sleep(0.1)
    
def tuo(x1,y1,x2,y2,t=1000):
    f=urlopen(server_url+'1,'+str(x1)+','+str(y1)+','+str(x2)+','+str(y2)+','+str(t))
    f.close()
    print(time.ctime()[11:19]+' [AutoPy]滑动执行成功')
    time.sleep(0.0023*t)

def swipe(x1,y1,x2,y2,t=1000):
    f=urlopen(server_url+'1,'+str(x1)+','+str(y1)+','+str(x2)+','+str(y2)+','+str(t))
    f.close()
    print(time.ctime()[11:19]+' [AutoPy]滑动执行成功')
    time.sleep(0.0023*t)

def tap(x,y):
    f=urlopen(server_url+'0,'+str(x)+','+str(y))
    f.close()
    print(time.ctime()[11:19]+' [AutoPy]点击执行成功')
    time.sleep(0.1)
    
def click(x,y):
    f=urlopen(server_url+'0,'+str(x)+','+str(y))
    f.close()
    print(time.ctime()[11:19]+' [AutoPy]点击执行成功')
    time.sleep(0.1)
    
def capturer():
    f=urlopen(server_url+'2,')
    f.close()
    print(time.ctime()[11:19]+' [AutoPy]截屏执行成功')
    
def ListenServer(_Screenshots_='/sdcard/DCIM/Screenshots/',_newdir_='/sdcard/qpython/'):#暂时无用
    _Screenshots_=_Screenshots_
    _newdir_=_newdir_
    t=os.listdir(_Screenshots_)
    while (True):
      nt=os.listdir(_Screenshots_)
      li=list(set(nt)-set(t))
      if(len(li)!=0):
         t=os.listdir(_Screenshots_)
         print('监控到截图',li)#监控到截图
         os.system('mv '+_Screenshots_+li[0]+' '+_newdir_+'AutoPy_Screenshots.jpg')



def StartServer(_Screenshots_='/sdcard/DCIM/Screenshots/',_newdir_='/sdcard/qpython/'):
     _thread.start_new_thread(ListenServer, (_Screenshots_,_newdir_) )


def gesturer(li):
    li=li
    f=urlopen(server_url+'3,'+','.join(map(str,li)))
    f.close()
    print(time.ctime()[11:19]+' [AutoPy]手势执行成功')
    
def HOME():
    f=urlopen(server_url+'HOME,')
    f.close()
    print(time.ctime()[11:19]+' [AutoPy]主页键执行成功')

def BACK():
    f=urlopen(server_url+'BACK,')
    f.close()
    print(time.ctime()[11:19]+' [AutoPy]返回键执行成功')
    
def RECENTS():
    f=urlopen(server_url+'RECENTS,')
    f.close()
    print(time.ctime()[11:19]+' [AutoPy]菜单键执行成功')


    
def Locker():
    f=urlopen(server_url+'Lock,')
    f.close()
    print(time.ctime()[11:19]+' [AutoPy]锁屏执行成功')

def floatWindowOpenApi():
    f=open('/sdcard/AutoFloatWindow.info','r+').read()
    if f=='1':
        return True
    #o=open('/sdcard/AutoFloatWindow.info',1w+').close()


def floatWindowCloseApi():
    f=open('/sdcard/AutoFloatWindow.info','r+').read()
    if f=='0':
        return True

def floatWindowClose():
    o=open('/sdcard/AutoFloatWindow.info','w+').close()
def systemCapturer():
    f=urlopen(server_url+'capturer,')
    f.close()
    print(time.ctime()[11:19]+' [AutoPy]返回键执行成功')
    
    
#作者:sunny开始学坏