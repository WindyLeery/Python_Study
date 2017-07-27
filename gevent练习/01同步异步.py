#！/usr/bin/python
#coding:utf-8


import gevent

def foo():
    print('Running in foo')
    gevent.sleep(0) # 通过它各自yield向对方
    print('Explicit context switch to foo again')

def bar():
    print('Explicit context to bar')
    gevent.sleep(0)
    print('Implicit context switch back to bar')

gevent.joinall([
    gevent.spawn(foo),
    gevent.spawn(bar),
])
