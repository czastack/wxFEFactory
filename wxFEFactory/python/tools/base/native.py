import math
import struct
from abc import ABC, abstractmethod
from lib.hack.models import Model, Field, ArrayField, CoordField, CoordData
from lib.hack.utils import iter_signature
from lib.lazy import lazy
from lib.extypes import DataClassMeta


class NativeContext(Model):
    """原生函数调用的环境
    借鉴GTAIV中的实现
    """
    SIZE = 140
    ARG_MAX = 32
    ITEM_SIZE = 4

    m_pReturn = Field(0)                                               # void * m_pReturn;              // 00-04
    m_nArgCount = Field(4)                                             # unsigned int m_nArgCount;      // 04-08
    m_pArgs = Field(8)                                                 # void * m_pArgs;                // 08-0C
    m_TempStack = ArrayField(0x0C, ARG_MAX, Field(0))                  # int m_TempStack[20];           // 0C-8C

    def __init__(self, addr, handler):
        super().__init__(addr, handler)
        self.m_pArgs = self.m_pReturn = self.m_TempStack.addr
        # 字符串、数组等临时参数占的块数，每块8字节
        self.temp_index = 0

    def reset(self):
        self.m_nArgCount = 0
        self.temp_index = 0

    def push(self, signature, *args):
        """压入参数"""
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
        arg_count = self.m_nArgCount
        if arg_count + self.temp_index >= self.ARG_MAX:
            raise ValueError('参数缓冲区容量不足')
        addr = self.m_TempStack.addr_at(arg_count)
        try:
            self.handler.write(addr, struct.pack(signature, *args))
        except Exception as e:
            print('打包参数出错', signature, *args)
            raise e
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

    def put_temp_value(self, value, size=0, index=None):
        if index is None:
            index = self.temp_index
            self.temp_index += 1
        self.handler.write(self.get_temp_addr(index), value, size)

    def put_temp_string(self, data, arg_count=None):
        """存放临时字符串
        :return: 字符串地址"""
        length = len(data) + 1
        if isinstance(data, str):
            data = data.encode()
        if arg_count is None:
            arg_count = self.m_nArgCount
        block_count = math.ceil(length / self.ITEM_SIZE)

        if arg_count + self.temp_index + block_count > self.ARG_MAX:
            raise ValueError('字符串长度过长，参数缓冲区容量不足')

        self.temp_index += block_count
        addr = self.get_temp_addr(self.temp_index)
        self.handler.write(addr, struct.pack('%ds' % (length + 1), data))
        return addr

    def put_temp_array(self, signature, *args, itemsize=None, arg_count=None):
        """存放临时数组
        :return: 数组地址"""
        if itemsize is None:
            itemsize = self.ITEM_SIZE
        block_count = math.ceil(itemsize * len(args) / self.ITEM_SIZE)
        if arg_count is None:
            arg_count = self.m_nArgCount

        if arg_count + self.temp_index + block_count > self.ARG_MAX:
            raise ValueError('数据过长，参数缓冲区容量不足')

        buff = bytearray()
        arg_it = iter(args)

        for fmt in iter_signature(signature):
            arg = next(arg_it)
            try:
                data = struct.pack(fmt, arg)
            except Exception:
                print(fmt, arg)
                raise
            datasize = len(data)
            buff.extend(data)
            if datasize < itemsize:
                # 对齐字节
                buff.extend(bytes(itemsize - datasize))
            elif datasize > itemsize:
                raise ValueError('datasize must <= itemsize')

        self.temp_index += block_count
        addr = self.get_temp_addr(self.temp_index)
        self.handler.write(addr, buff)
        return addr

    def put_temp_simple_array(self, signature, *args, arg_count=None):
        """存放临时简单数组
        :return: 数组地址"""
        data = struct.pack(signature, *args)
        block_count = math.ceil(len(data) / self.ITEM_SIZE)
        if arg_count is None:
            arg_count = self.m_nArgCount
        if arg_count + self.temp_index + block_count > self.ARG_MAX:
            raise ValueError('数据过长，参数缓冲区容量不足')
        self.temp_index += block_count
        addr = self.get_temp_addr(self.temp_index)
        self.handler.write(addr, data)
        return addr

    def put_temp_simple_array_ptr(self, signature, addr, arg_count=None):
        """存放临时简单指针数组
        :return: 指针数组地址"""
        addr_list = []
        for fmt in iter_signature(signature):
            addr_list.append(addr)
            addr += struct.calcsize(fmt)

        block_count = len(addr_list)
        if arg_count is None:
            arg_count = self.m_nArgCount
        if arg_count + self.temp_index + block_count > self.ARG_MAX:
            raise ValueError('数据过长，参数缓冲区容量不足')
        self.temp_index += block_count

        data = struct.pack('%d%s' % (block_count, 'L' if self.ITEM_SIZE == 4 else 'Q'), *addr_list)
        addr = self.get_temp_addr(self.temp_index)
        self.handler.write(addr, data)
        return addr

    def get_result(self, type, size=0):
        """获取调用结果"""
        if type is str:
            return self.get_string_result(size)
        return self.handler.read(self.m_pReturn, type, size)

    def get_vector_result(self, size=4, fixed=-1):
        """获取三个浮点数结果"""
        if fixed is -1:
            r = self.handler.read_float
        else:
            def r(addr):
                return round(self.handler.read_float(addr), fixed)
        addr = self.m_pReturn
        return (r(addr), r(addr + size), r(addr + size + size))

    def get_string_result(self, size):
        """获取字符串结果"""
        data = self.handler.read(self.handler.read_ptr(self.m_pReturn), bytes, size)
        n = data.find(0)
        if n is not -1:
            data = data[:n]
        return data

    def __getitem__(self, index):
        return self.m_TempStack[index]

    def __setitem__(self, index, value):
        self.m_TempStack[index] = value

    def __enter__(self):
        self.reset()
        return self

    def __exit__(self, *args):
        pass

    @staticmethod
    def type_signature(type, size=4):
        """type转参数签名"""
        if type is int:
            if size is 1:
                return 'B'
            elif size is 2:
                return 'H'
            elif size is 4:
                return 'I'
            elif size is 8:
                return 'Q'
        elif type is float:
            if size is 8:
                return 'd'
            return 'f'


class NativeContext64(NativeContext):
    """x64原生函数调用环境 (GTAV)"""
    SIZE = 160
    ARG_MAX = 16
    ITEM_SIZE = 8

    m_pReturn = Field(0x00, size=8)                                    # void * m_pReturn;              // 00-04
    m_nArgCount = Field(0x08)                                          # unsigned int m_nArgCount;      // 04-08
    m_pArgs = Field(0x10, size=8)                                      # void * m_pArgs;                // 08-0C
    m_nDataCount = Field(0x18)                                         # unsigned int m_nArgCount;      // 04-08
    m_TempStack = ArrayField(0x20, ARG_MAX, Field(0, size=8))          # int m_TempStack[16];           // 10-90

    def __init__(self, addr, handler):
        super().__init__(addr, handler)
        # 前四个参数是否是float, double的标记, 0: 非浮点型, 1: float, 2: double
        self.fflag = bytearray(8)

    def reset(self):
        super().reset()
        self.m_nDataCount = 0
        for i in range(4):
            self.fflag[i] = 0

    def push(self, signature, *args):
        """压入参数"""
        # 除去fflag, dwFunc, this，剩余参数的序号
        arg_count = self.m_nArgCount
        # 调用 native_call 汇编函数时用到
        if arg_count + self.temp_index >= self.ARG_MAX:
            raise ValueError('参数缓冲区容量不足')

        buff = bytearray()
        arg_it = iter(args)

        for fmt in iter_signature(signature):
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
                arg = self.put_temp_string(arg, arg_count)
                fmt = 'P'

            # 自定义打包
            if isinstance(arg, CustomPacker):
                fmt, arg = arg.pack_for(self, fmt)

            try:
                data = struct.pack(fmt, arg)
            except Exception:
                print(fmt, arg)
                raise
            datasize = len(data)
            buff.extend(data)
            if datasize < 8:
                # 对齐8个字节
                buff.extend(bytes(8 - datasize))

            arg_count += 1

        if args[0] is self.fflag:
            buff[:8] = self.fflag

        addr = self.m_TempStack.addr_at(self.m_nArgCount)
        self.handler.write(addr, buff)
        self.m_nArgCount = arg_count

    def get_result(self, type, size=0):
        """获取调用结果"""
        if type is not float:
            return super().get_result(type, size)
        else:
            if size is 8:
                return self.handler.read_double(self.m_pReturn + 16)
            return self.handler.read_float(self.m_pReturn + 8)


class NativeContextArray:
    def __init__(self, handler, size, NativeContext=NativeContext):
        self.handler = handler
        self.size = size
        self.NativeContext = NativeContext
        self.addr = handler.alloc_memory(NativeContext.SIZE * size)
        self.contexts = [NativeContext(self.addr + NativeContext.SIZE * i, handler) for i in range(size)]

    def __del__(self):
        self.release()

    def __len__(self):
        return self.size

    def release(self):
        if self.addr:
            self.handler.free_memory(self.addr)
            self.addr = 0
        self.contexts = None

    def __getitem__(self, index):
        return self.contexts[index] if self.contexts else None


class CustomPacker(ABC):
    @abstractmethod
    def pack_for(self, context, fmt):
        """打包自定义参数到NativeContext"""
        pass


class ResultResolver(ABC):
    @abstractmethod
    def get_result(self, context):
        """获取自定义结果"""
        pass


class TempPtr(metaclass=DataClassMeta):
    """临时地址占位符"""
    fields = ('index', 'type', 'size', 'value')
    defaults = {'type': int, 'size': 0}

    def pack_for(self, context, fmt):
        if self.index is None:
            self.index = context.temp_index
            context.temp_index += 1
        if self.value is not None:
            context.put_temp_value(self.value, self.size, self.index)
        addr = context.get_temp_addr(self.index)
        return fmt, addr

    def get_result(self, context):
        return context.get_temp_value(self.index, self.type, self.size)


class TempArrayPtr(metaclass=DataClassMeta):
    """临时指针数组地址占位符"""
    fields = ('signature', 'args')

    def pack_for(self, context, fmt):
        # 把参数压入数组
        addr = context.put_temp_simple_array(self.signature, *self.args)
        # 再压入每个参数的地址作为指针数组(void **params)
        addr = context.put_temp_simple_array_ptr(self.signature, addr)
        return fmt, addr


CustomPacker.register(TempPtr)
CustomPacker.register(TempArrayPtr)
ResultResolver.register(TempPtr)
