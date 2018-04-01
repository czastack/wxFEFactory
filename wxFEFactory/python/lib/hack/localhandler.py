from fefactory_api import mem_read, mem_write
import ctypes
import struct


_LocalHandler__instance = None


class LocalHandler:
    ptr_size = ctypes.sizeof(ctypes.c_char_p)

    def read(self, addr, type, size=0):
        if type is int:
            return self.readUint(addr, size if size else self.ptr_size)
        elif type is float:
            data = mem_read(addr, size if size else 4)
            return struct.unpack('f', data)[0]
        elif type is bool:
            return bool(self.read8(addr))
        else:
            return mem_read(addr, size)

    def write(self, addr, data, size=0):
        _type = type(data)
        if _type is int:
            return self.writeUint(addr, data, size if size else self.ptr_size)
        elif _type is float:
            return mem_write(addr, struct.pack('f', data), size if size else 4)
        elif _type is bool:
            return self.write8(addr, data)
        else:
            return mem_write(addr, data, size)

    def readUint(self, addr, size=4, signed=False):
        return int.from_bytes(mem_read(addr, size), 'little', signed=signed)

    def writeUint(self, addr, data, size=4, signed=False):
        return mem_write(addr, data.to_bytes(size, 'little', signed=signed), size)

    def readInt(self, addr, size=4):
        return self.readUint(addr, size, signed=True)

    def writeInt(self, addr, data, size=4):
        return self.writeUint(addr, data, size, signed=True)

    def readAddr(self, addr):
        return self.readUint(addr, self.ptr_size)

    def readLastAddr(self, addr, offsets):
        for offset in offsets:
            addr = self.readAddr(addr)
            if addr is 0:
                return 0
            addr += offset
        return addr

    def read8(self, addr):
        return self.readUint(addr, 1)

    def read16(self, addr):
        return self.readUint(addr, 2)

    def read32(self, addr):
        return self.readUint(addr, 4)

    def read64(self, addr):
        return self.readUint(addr, 8)

    def write8(self, addr, data):
        return self.writeUint(addr, data, 1)

    def write16(self, addr, data):
        return self.writeUint(addr, data, 2)

    def write32(self, addr, data):
        return self.writeUint(addr, data, 4)

    def write64(self, addr, data):
        return self.writeUint(addr, data, 8)

    def readFloat(self, addr):
        return self.read(addr, float, 4)

    def writeFloat(self, addr, data):
        return self.write(addr, float(data), 4)

    def ptrRead(self, addr, offset, type, size=0):
        addr = self.readAddr(addr)
        if addr:
            return self.read(addr + offset, type, size)
        return False

    def ptrWrite(self, addr, offset, data, size=0):
        addr = self.readAddr(addr)
        if addr:
            return self.write(addr + offset, data, size)
        return False

    def ptrsRead(self, addr, offsets, type, size=0):
        addr = self.readLastAddr(addr, offsets)
        if addr:
            return self.read(addr, type, size)
        return False

    def ptrsWrite(self, addr, offsets, data, size=0):
        addr = self.readLastAddr(addr, offsets)
        if addr:
            return self.write(addr, data, size)
        return False

    @classmethod
    def get_instance(cls):
        global __instance
        if __instance is None:
            __instance = cls()
        return __instance