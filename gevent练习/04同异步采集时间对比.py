#！/usr/bin/python
#coding:utf-8


# 同步异步采集一个HTML的时间对比


import time
import requests
session = requests.Session()
import gevent.monkey
gevent.monkey.patch_socket()
start = time.time()
tic = lambda: 'at %1.1f seconds' % (time.time() - start)

def fetch(pid):
    response = session.get('http://www.baidu.com')
    if response.status_code == 200:
        print('已经采集到了！时间：%s', tic())

def synchronous():
    for i in range(1,10):
        fetch(i)

def asynchronous():
    threads = []
    for i in range(1,10):
        threads.append(gevent.spawn(fetch, i))
    gevent.joinall(threads)

print('Synchronous:')
synchronous()

print('Asynchronous:')
asynchronous()
