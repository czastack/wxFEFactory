import struct
from dataclasses import dataclass


@dataclass
class Cheat:
    addr: int
    value: 'typing.Any'
    size: 4

    def write(self, handler):
        handler.write(self.addr, self.value, self.size)


@dataclass
class WriteUInt(Cheat):
    value: int


@dataclass
class Write8(WriteUInt):
    size: 1


@dataclass
class Write16(WriteUInt):
    size: 2


@dataclass
class Write32(WriteUInt):
    size: 4


@dataclass
class WriteBytes(Cheat):
    size: 0


@dataclass
class LoopWrite(Cheat):
    count: 0  # 循环次数
    step: 0  # 步进
    inc: 0  # 数据步进

    def write(self, handler):
        value = self.value
        if self.step == self.size:
            if self.inc is 0:
                value = self.value.to_bytes(self.size, 'little') * self.count
            else:
                fmt = ('B', 'H', 'I', 'Q')[self.size >> 1]
                value = struct.pack('%d%s' % (self.count, fmt),
                    *range(self.value, self.value + self.inc * self.count, self.inc))
            handler.write(self.addr, value, 0)
        else:
            addr = self.addr
            for i in range(self.value, self.value + self.inc * self.count, self.inc):
                handler.write(addr, value, self.size)
                addr += self.step
                value += self.inc
