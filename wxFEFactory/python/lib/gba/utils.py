import re
import struct


def is_bytes(data):
    return data and hasattr(data, '__iter__') and type(data[0]) is int


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
