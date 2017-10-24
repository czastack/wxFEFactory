import os
import json
import struct


class Configurable:
    """
    virtual getConfigFile() -> str
    """

    def __init__(self):
        self.config_changed = False

    def setConfig(self, key, value):
        self.config[key] = value
        self.config_changed = True

    def loadConfig(self):
        try:
            with open(self.getConfigFile()) as file:
                self.config = json.load(file)
        except FileNotFoundError:
            self.config = {}

    def writeConfig(self):
        if self.config_changed:
            with open(self.getConfigFile(), 'w') as file:
                self.config = json.dump(self.config, file)


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