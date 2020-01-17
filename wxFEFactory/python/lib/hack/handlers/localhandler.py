import ctypes
import struct
from pyapi import mem_read, mem_write
from ..models import Model


_LocalHandler__instance = None


class LocalHandler:
    ptr_size = ctypes.sizeof(ctypes.c_char_p)
    memory_map = {}  # 申请的buffer {addr: array}

    def read(self, addr, type, size=0):
        if type is int:
            return self.read_uint(addr, size if size else self.ptr_size)
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
            return self.write_uint(addr, data, size if size else self.ptr_size)
        elif _type is float:
            return mem_write(addr, struct.pack('f', data), size if size else 4)
        elif _type is bool:
            return self.write8(addr, data)
        else:
            if _type is bytearray:
                data = bytes(data)
            return mem_write(addr, data, size)

    def read_uint(self, addr, size=4, signed=False):
        return int.from_bytes(mem_read(addr, size), 'little', signed=signed)

    def write_uint(self, addr, data, size=4, signed=False):
        return mem_write(addr, data.to_bytes(size, 'little', signed=signed), size)

    def read_int(self, addr, size=4):
        return self.read_uint(addr, size, signed=True)

    def write_int(self, addr, data, size=4):
        return self.write_uint(addr, data, size, signed=True)

    def read_addr(self, addr):
        return self.read_uint(addr, self.ptr_size)

    def read_last_addr(self, addr, offsets):
        for offset in offsets:
            addr = self.read_addr(addr)
            if addr == 0:
                return 0
            addr += offset
        return addr

    def read8(self, addr):
        return self.read_uint(addr, 1)

    def read16(self, addr):
        return self.read_uint(addr, 2)

    def read32(self, addr):
        return self.read_uint(addr, 4)

    def read64(self, addr):
        return self.read_uint(addr, 8)

    def write8(self, addr, data):
        return self.write_uint(addr, data, 1)

    def write16(self, addr, data):
        return self.write_uint(addr, data, 2)

    def write32(self, addr, data):
        return self.write_uint(addr, data, 4)

    def write64(self, addr, data):
        return self.write_uint(addr, data, 8)

    def read_float(self, addr):
        return self.read(addr, float, 4)

    def write_float(self, addr, data):
        return self.write(addr, float(data), 4)

    def ptr_read(self, addr, offset, type, size=0):
        addr = self.read_addr(addr)
        if addr:
            return self.read(addr + offset, type, size)
        return False

    def ptr_write(self, addr, offset, data, size=0):
        addr = self.read_addr(addr)
        if addr:
            return self.write(addr + offset, data, size)
        return False

    def ptrs_read(self, addr, offsets, type, size=0):
        addr = self.read_last_addr(addr, offsets)
        if addr:
            return self.read(addr, type, size)
        return False

    def ptrs_write(self, addr, offsets, data, size=0):
        addr = self.read_last_addr(addr, offsets)
        if addr:
            return self.write(addr, data, size)
        return False

    def alloc_memory(self, init, size=None):
        """ 申请内存
        (aBytes)
        (anInteger)
        (aBytes, anInteger)
        """
        if self.memory_map is None:
            self.memory_map = {}
        buff = ctypes.create_string_buffer(init, size)
        addr = ctypes.addressof(buff)
        self.memory_map[addr] = buff
        return addr

    def alloc_data(self, data):
        return self.alloc_memory(data)

    def free_memory(self, addr):
        if self.memory_map:
            return self.memory_map.pop(addr, None)

    @classmethod
    def get_instance(cls):
        global __instance
        if __instance is None:
            __instance = cls()
        return __instance


class LocalModel(Model):
    def tolocal(self):
        p = ctypes.create_string_buffer(self.to_bytes())
        local_ins = self.__class__(ctypes.addressof(p), LocalHandler.get_instance())
        local_ins.buff = p
        return local_ins
