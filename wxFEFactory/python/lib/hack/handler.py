from fefactory_api.emuhacker import ProcessHandler
import struct


class MemHandler(ProcessHandler):
    _raw_addr = False

    def prepareAddr(self, addr, size):
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

    def ptrRead(self, addr, offset, type, size):
        addr = self.readAddr(addr)
        if addr:
            return self.read(addr + offset, type, size)
        return False

    def ptrWrite(self, addr, offset, data, size):
        addr = self.readAddr(addr)
        if addr:
            return self.write(addr + offset, data, size)
        return False

    def ptrsRead(self, addr, offsets, type, size):
        addr = self.readLastAddr(addr, offsets)
        if addr:
            return self.read(addr, type, size)
        return False

    def ptrsWrite(self, addr, offsets, data, size):
        addr = self.readLastAddr(addr, offsets)
        if addr:
            return self.write(addr, data, size)
        return False

    def raw_env(self):
        return _RawEnv(self)


class BigendHandler(MemHandler):
    """大端处理器"""
    def read(self, addr, type, size):
        if type is int:
            return self.readUint(addr, size if size else self.ptr_size)
        elif type is float:
            data = ProcessHandler.read(self, addr, bytes, size if size else 4)
            return struct.unpack('>f', data)[0]
        elif type is bool:
            return bool(self.read8(addr))
        else:
            return ProcessHandler.read(self, addr, type, size)

    def write(self, addr, data, size):
        _type = type(data)
        if _type is int:
            return self.writeUint(addr, data, size if size else self.ptr_size)
        elif _type is float:
            return ProcessHandler.write(self, addr, struct.pack('>f', data), size if size else 4)
        elif _type is bool:
            return self.write8(addr, data)
        else:
            return ProcessHandler.write(self, addr, data, size)

    def readUint(self, addr, size):
        return int.from_bytes(ProcessHandler.read(self, addr, bytes, size), 'big')

    def writeUint(self, addr, data, size):
        return ProcessHandler.write(self, addr, data.to_bytes(size, 'big'), size)


class _RawEnv:
    def __init__(self, owner):
        self.owner = owner

    def __enter__(self):
        self.owner._raw_addr = True
        return self

    def __exit__(self, *args):
        self.owner._raw_addr = False


class ProxyHandler():
    def __init__(self, handler=None):
        self.handler = handler

    def __getattr__(self, name):
        if self.handler:
            return getattr(self.handler, name)
        else:
            raise ValueError("handler未初始化")

    def set(self, handler):
        self.handler = handler

    def active(self):
        return self.handler and self.handler.active