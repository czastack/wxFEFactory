import math
import os
import struct
from lib import extypes


class HistoryList(list):
    """历史记录列表"""
    __slots__ = ('_index', 'maxsize')

    def __init__(self, data=None, maxsize=-1):
        if data:
            super().__init__(data)
        self._index = 0
        self.maxsize = maxsize

    def prev(self):
        if self:
            if self._index == 0:
                self._index = len(self)
            self._index -= 1
            return self[self._index]

    def next(self):
        if self:
            self._index += 1
            if self._index == len(self):
                self._index = 0
            return self[self._index]

    def append(self, e):
        try:
            i = self.index(e)
            self.append(self.pop(i))
        except ValueError:
            if self.maxsize is not -1 and self.maxsize == len(self):
                self.pop(0)
            super().append(e)
        self._index = 0


class Accumulator:
    """累加器"""
    def __init__(self, value=0):
        self.value = value

    def add(self, i):
        self.value += i
        return self.value

    def sub(self, i):
        self.value -= i
        return self.value

    def inc(self):
        return self.add(1)

    def dec(self):
        return self.sub(1)

    def __int__(self):
        return self.value

    __index__ = __int__


def float32(number):
    """浮点数保留6位小数"""
    return round(number, 6)


def round_s(number, ndigits=0):
    rate = 10 ** ndigits
    return math.floor(number * rate + 0.5) / rate


def tuple2rgb(rgbtuple):
    """颜色3元组转整型rgb"""
    return rgbtuple[0] << 16 | rgbtuple[1] << 8 | rgbtuple[2]


def rgb2tuple(rgb):
    """整型rgb转颜色3元组"""
    return ((rgb >> 16) & 0xff), ((rgb >> 8) & 0xff), (rgb & 0xff)


def rgb2bgr(rgb):
    """rgb颜色转bgr颜色"""
    return ((rgb & 0xff) << 16 | ((rgb >> 8) & 0xff) << 8 | ((rgb >> 16) & 0xff))


def gen_values(items):
    """生成自然数元组"""
    return tuple(range(len(items)))


def gen_flag(items):
    """生成标记元组 1, 2, 4, 8..."""
    return tuple(1 << i for i in range(len(items)))


def flag_generator(n):
    """标记生成器"""
    return (1 << i for i in range(n))


def split_value_label(options):
    """把(value, label)分开"""
    return tuple(item[1] for item in options), tuple(item[0] for item in options)


def split_label_value(options):
    """把(label, value)分开"""
    a, b = split_value_label(options)
    return b, a


def prepare_option(choices, values):
    """预处理选项"""
    if values is None:
        if choices is not None:
            if not extypes.is_list_tuple(choices):
                choices = tuple(choices)
            if choices and extypes.is_list_tuple(choices[0]):
                fn = split_label_value if isinstance(choices[0][0], str) else split_value_label
                choices, values = fn(choices)
    return choices, values


def dirfind(obj, text):
    """dir属性中查找"""
    return list(filter(lambda x: text in x, dir(obj)))


def compose(*funs):
    """合并装饰器"""
    def _deco(self):
        for func in reversed(funs):
            f = fun(f)
        return f
    return _deco
