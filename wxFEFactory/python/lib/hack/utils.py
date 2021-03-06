import math
from lib.utils import split_label_value


class BaseItemProvider:
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
        values = tuple(range(self.start, self.end))
        if self.can_empty:
            if isinstance(self.datas, list):
                choices.insert(0, "无")
                values.insert(0, 0)
            elif isinstance(self.datas, tuple):
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
        self._choices, self._values = split_label_value(self.datas)


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


def loword(n):
    """低字"""
    return n & 0xFFFF


def hiword(n):
    """高字"""
    return (n >> 16) & 0xFFFF


def u32(n):
    """截取32位整型"""
    return n & 0xFFFFFFFF


def qword(n):
    """截取64位整型"""
    return n & 0xFFFFFFFFFFFFFFFF


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
    if size is 0:
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
        else:
            fmt = chr(ch)

        if repeat is 0:
            repeat = 1

        for i in range(repeat):
            yield fmt
        repeat = 0
