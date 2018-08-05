import re
import struct


def is_bytes(data):
    return data and hasattr(data, '__iter__') and type(data[0]) is int


def bytes_hex(data):
    return ''.join(("%02X" % b for b in data))


def bytes_beautify(data, offset=0, step=1):
    if offset == 0 and step == 1:
        return " ".join("%02X" % x for x in data)

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


def r1(data):
    """先输出低字节的HEX"""
    return bytes_hex(struct.pack('L', data))


def rol(a, n, N=32):
    # 循环左移
    return ((a >> (N - n)) | (a << n)) & ((1 << N) - 1)


def ror(a, n, N=32):
    # 循环右移
    return ((a << (N - n)) | (a >> n)) & ((1 << N) - 1)


REG_HEX = re.compile('([\\da-fA-F]+)')


def compute_hex(expr):
    """计算16进制算式"""
    return "%X" % eval(REG_HEX.sub('0x\\1', expr))
