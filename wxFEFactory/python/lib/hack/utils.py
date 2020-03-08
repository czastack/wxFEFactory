import abc
import math
import struct
import sys
from lib.utils import split_tuple


class BaseItemProvider(metaclass=abc.ABCMeta):
    """基础items提供器"""
    def __init__(self):
        self._choices = None
        self._values = None

    @property
    def choices(self):
        if self._choices is None:
            self.generate()
        return self._choices

    @property
    def values(self):
        if self._values is None:
            self.generate()
        return self._values

    @abc.abstractmethod
    def generate(self):
        pass


class ItemProvider(BaseItemProvider):
    """截取部分items提供器"""
    def __init__(self, datas, start, end, can_empty=True):
        super().__init__()
        self.datas = datas
        self.start = start
        self.end = end
        self.can_empty = can_empty

    def generate(self):
        choices = self.datas[self.start:self.end]
        values = choices.__class__(range(self.start, self.end))
        if self.can_empty:
            if isinstance(choices, list):
                choices.insert(0, "无")
                values.insert(0, 0)
            elif isinstance(choices, tuple):
                choices = ("无",) + choices
                values = (0,) + values
        self._choices = choices
        self._values = values
        del self.datas, self.start, self.end, self.can_empty

    def __add__(self, items):
        return ItemProviders(self, items)


class ItemProviders(BaseItemProvider):
    """多个ItemProvider组合"""
    def __init__(self, *args):
        self.elems = list(args)
        super().__init__()

    def generate(self):
        choices = []
        values = []
        for elem in self.elems:
            choices.extend(elem.choices)
            values.extend(elem.values)
        self._choices = tuple(choices)
        self._values = tuple(values)
        del self.elems

    def __add__(self, items):
        self.elems.append(items)
        return self


class OptionProvider(BaseItemProvider):
    """分隔labels, values提供器"""
    def __init__(self, datas):
        super().__init__()
        self.datas = datas

    def generate(self):
        self._choices, self._values = split_tuple(self.datas)


class Descriptor:
    """获取getter, setter"""
    def __init__(self, instance_getter, attr):
        self.instance_getter = instance_getter
        self.attr = attr

    def getter(self):
        return getattr(self.instance_getter(), self.attr)

    def setter(self, value):
        setattr(self.instance_getter(), self.attr, value)

    def __iter__(self):
        yield self.getter
        yield self.setter


def loword(num):
    """低字"""
    return num & 0xFFFF


def hiword(num):
    """高字"""
    return (num >> 16) & 0xFFFF


def u32(num):
    """截取32位整型"""
    return num & 0xFFFFFFFF


def qword(num):
    """截取64位整型"""
    return num & 0xFFFFFFFFFFFFFFFF


def pack_dwords(*args):
    """打包多个DWORD为bytes"""
    return struct.pack('%dL' % len(args), *args)


def combine_dwords(*args):
    """打包多个DWORD为bytes"""
    return int.from_bytes(pack_dwords(*args), 'little')


def align_4(n):
    """对齐4字节"""
    tail = n & 3
    if tail:
        n += 4 - tail
    return n


def align_size(n, p):
    """对齐p字节"""
    tail = n & (p - 1)
    if tail:
        n += p - tail
    return n


def ceil_exp(c):
    """求大于c的最小2次幂"""
    n = c - 1
    n |= n >> 1
    n |= n >> 2
    n |= n >> 4
    n |= n >> 8
    n |= n >> 16
    return n + 1


def int_of_size(n, size=0, exp=True):
    """整形字节大小
    :param size: 给定的字节长度，若小于原长度，整形只截取该长度部分
    :param exp: 长度对齐2的幂
    """
    bitlen = n.bit_length()
    origin_size = math.ceil(bitlen / 8)
    if size == 0:
        size = (ceil_exp(bitlen) >> 3) if exp else origin_size
    elif size < origin_size:
        n &= (1 << (size << 3)) - 1
    return n, size


def u32_bytes(n):
    """32位整型转bytes"""
    try:
        return n.to_bytes(4, 'little')
    except Exception:
        return struct.pack('L', n)


def uint_bytes(n, size=0, byteorder='little', exp=True):
    """把整型转成bytes
    :param size: 字节数
    :param exp: 长度对齐2的幂
    """
    n, size = int_of_size(n, size, exp)
    return n.to_bytes(size, byteorder)


def uint_hex(n, size=0, exp=True):
    """把整型转成hex字符串
    :param size: 字节数
    :param exp: 长度对齐2的幂
    """
    n, size = int_of_size(n, size, exp)
    return "%0*X" % ((size << 1), n)


def bytes_hex(data, sep=''):
    """bytes转16进制字符串"""
    if not sep:
        return data.hex().upper()
    return sep.join(("%02X" % b for b in data))


def bytes_beautify(data, offset=0, step=1):
    """bytes转可读性强的16进制字符串"""
    if offset == 0 and step == 1:
        return bytes_hex(data, " ")

    length = len(data)
    i = offset
    result = []
    fmt = "%%0%dX" % (step << 1)
    while i < length:
        data = j = 0
        while j < step:
            data |= data[i] << (j << 3)
            j += 1
            i += 1
        result.append(fmt % data)
    return " ".join(result)


def iter_signature(signature):
    """迭代参数签名"""
    if isinstance(signature, str):
        signature = signature.encode()
    # 重复次数，例如2L中为2，L中为1
    repeat = 0
    for ch in signature:
        if 0x30 <= ch <= 0x39:
            repeat = repeat * 10 + (ch - 0x30)
            continue
        fmt = chr(ch)
        if repeat == 0:
            repeat = 1
        for _ in range(repeat):
            yield fmt
        repeat = 0


def resolve_type(instance, name):
    """处理字符串type"""
    if name == 'self':
        return instance.__class__
    else:
        return getattr(sys.modules[instance.__class__.__module__], name, None)
