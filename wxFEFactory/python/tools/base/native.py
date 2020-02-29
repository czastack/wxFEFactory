import math
import struct
from abc import ABC, abstractmethod
from lib.hack.models import Model, Field, ArrayField, CoordField, CoordData
from lib.hack.utils import iter_signature
from lib.lazy import lazy
from lib.extypes import DataClass


class NativeContext(Model):
    """原生函数调用的环境"""
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

    # def push(self, signature, *args):
    #     """压入参数"""
    #     # 写入栈的地址
    #     index = self.m_nArgCount
    #     if index + self.temp_index >= self.ARG_MAX:
    #         raise ValueError('参数缓冲区容量不足')
    #     addr = self.m_TempStack.addr_at(index)
    #     try:
    #         self.handler.write(addr, struct.pack(signature, *args))
    #     except Exception as e:
    #         print('打包参数出错', signature, *args)
    #         raise e
    #     self.m_nArgCount += len(args)

    def push(self, signature, *args, align=4, index=None, update=True):
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
        if index is None:
            index = self.m_nArgCount
        origin_index = index
        # 调用 native_call 汇编函数时用到
        if index + self.temp_index >= self.ARG_MAX:
            raise ValueError('参数缓冲区容量不足')

        buff = bytearray()
        arg_it = iter(args)

        for fmt in iter_signature(signature):
            arg = next(arg_it)

            if fmt == 'S':
                # 临时字符串
                arg = self.put_temp_string(arg, index)
                fmt = 'L'

            elif fmt == 'P':
                # 32为要转成L
                fmt = 'L'

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
            if datasize < align:
                # 对齐字节
                buff.extend(bytes(align - datasize))

            index += 1

        addr = self.m_TempStack.addr_at(origin_index)
        self.handler.write(addr, buff)
        if update:
            self.m_nArgCount = index

    def push_manual(self, index, signature, *args):
        """手动压入参数，m_nArgCount不变"""
        self.push(signature, *args, index=index, update=False)

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

    def put_temp_string(self, data, index=None):
        """存放临时字符串
        :return: 字符串地址"""
        length = len(data) + 1
        if isinstance(data, str):
            data = data.encode()
        if index is None:
            index = self.m_nArgCount
        block_count = math.ceil(length / self.ITEM_SIZE)

        if index + self.temp_index + block_count > self.ARG_MAX:
            raise ValueError('字符串长度过长，参数缓冲区容量不足')

        self.temp_index += block_count
        addr = self.get_temp_addr(self.temp_index)
        self.handler.write(addr, struct.pack('%ds' % (length + 1), data))
        return addr

    def put_temp_simple_array(self, signature, args, index=None):
        """存放临时简单数组
        :return: 数组地址"""
        data = struct.pack(signature, *args)
        block_count = math.ceil(len(data) / self.ITEM_SIZE)
        if index is None:
            index = self.m_nArgCount
        if index + self.temp_index + block_count > self.ARG_MAX:
            raise ValueError('数据过长，参数缓冲区容量不足')
        self.temp_index += block_count
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
        if fixed == -1:
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
        if n != -1:
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
            if size == 1:
                return 'B'
            elif size == 2:
                return 'H'
            elif size == 4:
                return 'I'
            elif size == 8:
                return 'Q'
        elif type is float:
            if size == 8:
                return 'd'
            return 'f'


class NativeContext64(NativeContext):
    """x64原生函数调用环境"""
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

    def push(self, signature, *args, align=8, index=None, update=True):
        """压入参数"""
        # 除去fflag, dwFunc, this，剩余参数的序号
        if index is None:
            index = self.m_nArgCount
        origin_index = index
        # 调用 native_call 汇编函数时用到
        if index + self.temp_index >= self.ARG_MAX:
            raise ValueError('参数缓冲区容量不足')

        buff = bytearray()
        arg_it = iter(args)

        for fmt in iter_signature(signature):
            arg = next(arg_it)

            if 3 <= index < 7:
                if fmt == 'f':
                    # float
                    self.fflag[index - 3] = 1
                elif fmt == 'd':
                    # double
                    self.fflag[index - 3] = 2

            if fmt == 'S':
                # 字符串(s是c style, p是pascal style)
                arg = self.put_temp_string(arg, index)
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
            if datasize < align:
                # 对齐字节
                buff.extend(bytes(align - datasize))

            index += 1

        if args[0] is self.fflag:
            buff[:8] = self.fflag

        addr = self.m_TempStack.addr_at(origin_index)
        self.handler.write(addr, buff)
        if update:
            self.m_nArgCount = index

    def get_result(self, type, size=0):
        """获取调用结果"""
        if type is not float:
            return super().get_result(type, size)
        else:
            if size == 8:
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


class TempPtr(DataClass):
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


class TempArrayPtr(DataClass):
    """临时指针数组地址占位符 (void **params)"""
    fields = ('signature', 'args')

    def pack_for(self, context, fmt):
        addr = self.pack_array_ptr(context)
        return fmt, addr

    def pack_array_ptr(self, context):
        # 注意：格式为P的已经是指针，不需要再放到临时数组中
        addr_list = []
        buff = bytearray()
        arg_it = iter(self.args)
        offset = 0  # 用于计算最终数组中的地址

        for fmt in iter_signature(self.signature):
            arg = next(arg_it)

            if fmt == 'P':
                # 已经是指针则直接用
                addr_list.append(arg)
            else:
                addr_list.append(offset)
                offset += struct.calcsize(fmt)

                try:
                    data = struct.pack(fmt, arg)
                except Exception:
                    print(fmt, arg)
                    raise
                buff.extend(data)

        block_count = math.ceil(len(buff) / context.ITEM_SIZE)
        if context.m_nArgCount + context.temp_index + block_count + len(addr_list) > context.ARG_MAX:
            raise ValueError('数据过长，参数缓冲区容量不足')
        context.temp_index += block_count
        # 数据临时数组地址
        addr = context.get_temp_addr(context.temp_index)
        context.handler.write(addr, buff)

        # 把偏移转为地址
        addr_count = len(addr_list)
        for i in range(addr_count):
            if addr_list[i] < offset:
                addr_list[i] += addr

        buff = struct.pack('%d%s' % (addr_count, 'L' if context.ITEM_SIZE == 4 else 'Q'), *addr_list)
        context.temp_index += addr_count
        addr = context.get_temp_addr(context.temp_index)
        context.handler.write(addr, buff)
        return addr


CustomPacker.register(TempPtr)
CustomPacker.register(TempArrayPtr)
ResultResolver.register(TempPtr)
