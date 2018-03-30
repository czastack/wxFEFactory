import os
import struct


class HistoryList(list):
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


def float32(f):
    return round(f, 6)

def u32(n):
    return n & 0xFFFFFFFF

def u32bytes(n):
    """32位整型转bytes"""
    try:
        return n.to_bytes(4, 'little')
    except:
        return struct.pack('L', n)


def tuple2rgb(rgbtuple):
    return rgbtuple[0] << 16 | rgbtuple[1] << 8 | rgbtuple[2]

def rgb2tuple(rgb):
    return ((rgb >> 16) & 0xff), ((rgb >> 8) & 0xff), (rgb & 0xff)

def rgb2bgr(rgb):
    return ((rgb & 0xff) << 16 | ((rgb >> 8) & 0xff) << 8 | ((rgb >> 16) & 0xff))

def gen_values(items):
    return tuple(range(len(items)))

def gen_flag(items):
    return tuple(1 << i for i in range(len(items)))

def split_value_label(options):
    """把(value, label)分开"""
    values = []
    labels = []
    for value, label in options:
        values.append(value)
        labels.append(label)
    return tuple(labels), tuple(values)

def split_label_value(options):
    """把(label, value)分开"""
    return reversed(split_value_label())