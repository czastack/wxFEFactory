from lib.hack.model import Field, ArrayField
from ..gta_base.native import NativeContext
import struct


class NativeContext(NativeContext):
    """GTAV原生函数调用的环境"""
    SIZE = 144

    m_pReturn = Field(0x00, size=8)                                    # void * m_pReturn;              // 00-04
    m_nArgCount = Field(0x08)                                          # unsigned int m_nArgCount;      // 04-08
    m_pArgs = Field(0x10)                                              # void * m_pArgs;                // 08-0C
    m_nDataCount = Field(0x18)                                         # unsigned int m_nArgCount;      // 04-08
    m_TempStack = ArrayField(0x20, 16, Field(0, size=8))               # int m_TempStack[16];           // 10-90

    def __init__(self, addr, handler):
        super().__init__(addr, handler)
        # 前四个参数是否是float, double的标记, 0: 非浮点型, 1: float, 2: double
        self.fflag = bytearray(8)

    def reset(self):
        self.m_nArgCount = 0
        self.m_nDataCount = 0
        self.fflag.clear()

    def push(self, signature, *args):
        """压入参数"""
        if isinstance(signature, str):
            signature = signature.encode()
        
        buff = bytearray()
        # 重复次数，例如2L中为2，L中为1
        repeat = 0
        # 除去fflag, dwFunc, this，剩余参数的序号
        arg_index = self.m_nArgCount - 3
        arg_it = iter(args)

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

                    if 0 <= arg_index < 4:
                        if fmt == 'f':
                            # float
                            self.fflag[arg_index] = 1
                        elif fmt == 'd':
                            # double
                            self.fflag[arg_index] = 2
                    data = struct.pack(fmt, arg)
                    data_size = len(data)
                    buff.extend(data)
                    if data_size < 8:
                        # 对齐8个字节
                        buff.extend(bytes(8 - data_size))

                    arg_index += 1
                repeat = 0

        if args[0] is self.fflag:
            buff[:8] = self.fflag

        addr = self.m_TempStack.addr_at(self.m_nArgCount)
        self.handler.write(addr, buff)
        self.m_nArgCount += len(args)
