from lib.hack.models import Model, Field, ArrayField, CoordField, CoordData
from lib.lazy import lazy
import math
import struct


class NativeContext(Model):
    """原生函数调用的环境
    GTAIV中的实现拿来用
    """
    SIZE = 76

    m_pReturn = Field(0)                                               # void * m_pReturn;              // 00-04
    m_nArgCount = Field(4)                                             # unsigned int m_nArgCount;      // 04-08
    m_pArgs = Field(8)                                                 # void * m_pArgs;                // 08-0C
    m_TempStack = ArrayField(0x0C, 16, Field(0))                       # int m_TempStack[16];           // 0C-4C

    def __init__(self, addr, handler):
        super().__init__(addr, handler)
        self.m_pArgs = self.m_pReturn = self.m_TempStack.addr

    def push(self, signature, *args):
        """压入参数，m_nArgCount增大"""
        # signature
        # x: pad byte
        # c: char
        # b: signed char
        # B: unsigned char
        # ?: _Bool
        # h: short
        # H: unsigned short
        # i: int
        # I: unsigned int
        # l: long
        # L: unsigned long
        # q: long long
        # Q: unsigned long long
        # f: float
        # d: double
        # s: char[]
        # p: char[]
        # P: void *
        # 写入栈的地址
        addr = self.m_TempStack.addr_at(self.m_nArgCount)
        self.handler.write(addr, struct.pack(signature, *args))
        self.m_nArgCount += len(args)

    def push_manual(self, index, signature, *args):
        """手动压入参数，m_nArgCount不变"""
        addr = self.m_TempStack.addr_at(index)
        self.handler.write(addr, struct.pack(signature, *args))

    def get_stack_addr(self, i=0):
        """ 栈从前往后取地址，传递指针参数时可以用
        :param i: 从1开始
        """
        return self.m_TempStack.addr_at(i)

    def get_stack_value(self, i=0, type=int, size=0):
        return self.handler.read(self.get_stack_addr(i), type, size)

    def get_temp_addr(self, i=1):
        """ 从栈的最后开始往前取地址，传递指针参数时可以用
        :param i: 从1开始
        """
        return self.m_TempStack.addr_at(-i)

    def get_temp_addrs(self, start, end):
        """ 从栈的最后开始往前取地址，传递指针参数时可以用
        :param start: 其实序号
        :param end: 其实序号
        :return: 地址序列
        """
        span = range(start, end + 1) if start < end else range(start, end - 1, -1)
        return (self.get_temp_addr(i) for i in span)

    def get_temp_value(self, i=1, type=int, size=0):
        return self.handler.read(self.get_temp_addr(i), type, size)

    def get_temp_values(self, start, end, type=int, size=0, mapfn=None):
        span = range(start, end + 1) if start < end else range(start, end - 1, -1)
        result = (self.get_temp_value(i, type, size) for i in span)
        if mapfn:
            result = map(mapfn, result)
        return result

    def get_result(self, type, size=0):
        """获取调用结果"""
        return self.handler.read(self.m_pReturn, type, size)

    def get_vector_result(self, size=4, fixed=-1):
        if fixed is -1:
            r = self.handler.read_float
        else:
            def r(addr):
                return round(self.handler.read_float(addr), fixed)
        addr = self.m_pReturn
        return (r(addr), r(addr + size), r(addr + size + size))

    def reset(self):
        self.m_nArgCount = 0

    def __getitem__(self, index):
        return self.m_TempStack[index]

    def __setitem__(self, index, value):
        print(index, value)
        self.m_TempStack[index] = value

    def __enter__(self):
        self.reset()
        return self

    def __exit__(self, *args):
        pass


class NativeContext64(NativeContext):
    """x64原生函数调用环境 (GTAV)"""
    SIZE = 144
    ARG_MAX = 16

    m_pReturn = Field(0x00, size=8)                                    # void * m_pReturn;              // 00-04
    m_nArgCount = Field(0x08)                                          # unsigned int m_nArgCount;      // 04-08
    m_pArgs = Field(0x10, size=8)                                      # void * m_pArgs;                // 08-0C
    m_nDataCount = Field(0x18)                                         # unsigned int m_nArgCount;      // 04-08
    m_TempStack = ArrayField(0x20, ARG_MAX, Field(0, size=8))          # int m_TempStack[16];           // 10-90

    def __init__(self, addr, handler):
        super().__init__(addr, handler)
        # 前四个参数是否是float, double的标记, 0: 非浮点型, 1: float, 2: double
        self.fflag = bytearray(8)
        # 字符串参数占的块数，每块8字节
        self.str_arg_block = 0

    def reset(self):
        self.m_nArgCount = 0
        self.m_nDataCount = 0
        self.str_arg_block = 0
        for i in range(4):
            self.fflag[i] = 0

    def push(self, signature, *args):
        """压入参数"""
        # 除去fflag, dwFunc, this，剩余参数的序号
        arg_count = self.m_nArgCount
        # 调用NativeCall 汇编函数时用到
        if arg_count + self.str_arg_block >= 16:
            raise ValueError('参数缓冲区容量不足')

        buff = bytearray()
        # 重复次数，例如2L中为2，L中为1
        repeat = 0
        arg_it = iter(args)

        if isinstance(signature, str):
            signature = signature.encode()

        for ch in signature:
            if 0x30 <= ch <= 0x39:
                repeat = repeat * 10 + (ch - 0x30)
                continue
            else:
                fmt = chr(ch)

                if repeat is 0:
                    repeat = 1

                for i in range(repeat):
                    arg = next(arg_it)

                    if 3 <= arg_count < 7:
                        if fmt == 'f':
                            # float
                            self.fflag[arg_count - 3] = 1
                        elif fmt == 'd':
                            # double
                            self.fflag[arg_count - 3] = 2

                    if fmt == 'p' or fmt == 's':
                        # 字符串(s是c style, p是pascal style)
                        if repeat is not 1:
                            raise ValueError('对于字符串参数, s和p前暂不支持加数字')

                        length = len(arg) + 1
                        if isinstance(arg, str):
                            arg = arg.encode()
                        block_count = math.ceil(length / 8)

                        if arg_count + self.str_arg_block + block_count > self.ARG_MAX:
                            raise ValueError('字符串长度过长，参数缓冲区容量不足')

                        self.str_arg_block += block_count
                        temp_addr = self.get_temp_addr(self.str_arg_block)
                        self.handler.write(temp_addr, struct.pack('%ds' % (length + 1), arg))
                        arg = temp_addr
                        fmt = 'Q'

                    try:
                        data = struct.pack(fmt, arg)
                    except Exception:
                        print(fmt, arg)
                        raise
                    data_size = len(data)
                    buff.extend(data)
                    if data_size < 8:
                        # 对齐8个字节
                        buff.extend(bytes(8 - data_size))

                    arg_count += 1
                repeat = 0

        if args[0] is self.fflag:
            buff[:8] = self.fflag

        addr = self.m_TempStack.addr_at(self.m_nArgCount)
        self.handler.write(addr, buff)
        self.m_nArgCount = arg_count
