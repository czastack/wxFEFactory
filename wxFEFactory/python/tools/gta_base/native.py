from lib.hack.model import Model, Field, ArrayField, ModelField, CoordField, CoordData
from lib.lazy import lazy
import struct


class NativeContext(Model):
    """原生函数调用的环境
    GTAIV中的实现拿来用
    """
    SIZE = 160

    m_pReturn = Field(0)                                               # void * m_pReturn;              // 00-04
    m_nArgCount = Field(4)                                             # unsigned int m_nArgCount;      // 04-08
    m_pArgs = Field(8)                                                 # void * m_pArgs;                // 08-0C
    m_nDataCount = Field(12)                                           # unsigned int m_nDataCount;     // 0C-10
    m_pOriginalData = ArrayField(16, 4, ModelField(0, CoordData))      # CVector3 * m_pOriginalData[4]; // 10-20
    m_TemporaryData = ArrayField(32, 4, CoordField(0, 4))              # Vector4 m_TemporaryData[4];    // 20-60
    m_TempStack = ArrayField(0x60, 16, Field(0))

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
        # while(m_nDataCount > 0)
        # {
        #     m_nDataCount--;
        #     CVector3 * pVec3 = m_pOriginalData[m_nDataCount];
        #     Vector4 * pVec4 = &m_TemporaryData[m_nDataCount];
        #     pVec3->fX = pVec4->fX;
        #     pVec3->fY = pVec4->fY;
        #     pVec3->fZ = pVec4->fZ;
        # }
        if self.m_nDataCount:
            for i in range(self.m_nDataCount):
                self.m_pOriginalData[i].set(self.m_TemporaryData[i])

            self.m_nDataCount = 0

        return self.handler.read(self.m_TempStack.addr, type, size)

    def reset(self):
        self.m_nArgCount = 0
        self.m_nDataCount = 0

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