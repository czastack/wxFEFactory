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


def float32(f):
    return round(f, 6)

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