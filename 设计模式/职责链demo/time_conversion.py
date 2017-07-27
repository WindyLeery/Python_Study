# -*- coding: utf-8 -*-
# @Time    : 2017/7/27 10:22
# @Author  : 哎哟卧槽
# @Site    : 用作时间格式转换；例如 ：3小时之前 3天之前
# @File    : time_conversion.py
# @Software: PyCharm

import re
from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta


def re_findall(pattern, string, flags=0):
    """
    :param pattern: 正则表达式
    :param string: 需要匹配的字符串
    :param flags:
    :return: 与结果相匹配的列表
    """
    string = re.findall(pattern, string, flags)
    return string or ''


class Handler(metaclass=ABCMeta):

    name = '时间转换基类'

    def __init__(self,):
        self.successor = None

    def setsuccessor(self, successor):
        self.d = datetime.now()
        self.successor = successor

    @abstractmethod
    def handler(self, data): return


class MinutesBefore(Handler):

    name = '分钟之前'

    def handler(self, data):
        value = re_findall(r'(\d+)分钟', data)
        if value:
            d1 = self.d + timedelta(minutes=-int(value))
            return d1.strftime('%Y-%m-%d %H:%M:%S')
        else:
           return self.successor.handler(data)


class HoursBefore(Handler):

    name = '小时之前'

    def handler(self, data):
        value = re_findall(r'(\d+)小时', data)
        if value:
            d1 = self.d + timedelta(hours=-int(value))
            return d1.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return self.successor.handler(data)


class MonthsBefore(Handler):

    name = '月份前'

    def handler(self, data):
        value = re_findall(r'(\d{1,2}月\d{1,2}日\s+\d{2}:\d{2})', data)
        if value:
            d1 = datetime.strptime(' '.join(value), '%m月%d日 %H:%M')
            return str(self.d.year) + '-' + d1.strftime('%m-%d %H:%M:%S')
        else:
            return self.successor.handler(data)


class YearsBefore(Handler):

    name = '年之前'

    def handler(self, data):
        value = re_findall(r'(\d{4}-\d{1,2}-\d{1,2}\s+\d{2}:\d{2}:\d{2})', data)
        if value:
            return ''.join(value)
        else:
            return self.successor.handler(data)


class TodayBefore(Handler):

    name = '今天'

    def handler(self, data):
        value = re_findall(r'今天(\d{2}:\d{2})', data)
        if value:
            d2 = self.d.strftime('%Y-%m-%d')
            return d2 + ''.join(value)
        else:
            return self.successor.handler(data)


class Yesterday(Handler):

    name = '昨天'

    def handler(self, data):
        value = re_findall(r'昨天\s(\d{2}:\d{2})', data)
        if value:
            d1 = datetime.now() + timedelta(days=-1)
            return d1.strftime('%Y-%m-%d') + ' ' + ''.join(value) + ':00'
        else:
            return self.successor.handler(data)


class YesterdayBefore(Handler):

    name = '前天'

    def handler(self, data):
        value = re_findall(r'前天\s(\d{2}:\d{2})', data)
        if value:
            d1 = datetime.now() + timedelta(days=-2)
            return d1.strftime('%Y-%m-%d') + ' ' + ''.join(value) + ':00'
        else:
            return self.successor.handler(data)


class DefalutValue(Handler):

    name = '没有匹配到的默认'

    def handler(self, data):
        return '{}:没有匹配到任何东西'.format(data)


def time_conversion(data):
    p1 = TodayBefore()
    p2 = YearsBefore()
    p3 = MonthsBefore()
    p4 = HoursBefore()
    p5 = MinutesBefore()
    p6 = Yesterday()
    p7 = YesterdayBefore()
    p1.setsuccessor(p2)
    p2.setsuccessor(p3)
    p3.setsuccessor(p4)
    p4.setsuccessor(p5)
    p5.setsuccessor(p6)
    p6.setsuccessor(p7)
    return p1.handler(data)


if __name__ == '__main__':
    print(time_conversion('前天 15:05'))
