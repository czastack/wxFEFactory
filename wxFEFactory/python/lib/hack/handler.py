from fefactory_api.emuhacker import ProcessHandler
import struct


class MemHandler(ProcessHandler):
    _raw_addr = False

    def prepareAddr(self, addr, size):
        return addr

    def rawRead(self, addr, type=int, size=0):
        self._raw_addr = True
        result = self.read(addr, type, size)
        self._raw_addr = False
        return result

    def rawWrite(self, addr, data, size=0):
        self._raw_addr = True
        result = self.write(addr, data, size)
        self._raw_addr = False
        return result

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

    def inject_dll(self, path):
        LoadLibrary = getattr(self, '_LoadLibrary', None)
        if LoadLibrary is None:
            module = self.get_module('KERNEL32.DLL')
            helper = self.getProcAddressHelper(module)
            self._LoadLibrary = LoadLibrary = helper.getProcAddress('LoadLibraryW')
            self._FreeLibrary = LoadLibrary = helper.getProcAddress('FreeLibrary')

        if LoadLibrary and path:
            print(LoadLibrary)
            data = path.encode('unicode_internal') + b'\x00\x00'
            lpname = self.alloc_data(data)
            result = self.remote_call(LoadLibrary, lpname)
            self.free_memory(lpname)
            return result
        return False

    def free_dll(self, name):
        FreeLibrary = getattr(self, '_FreeLibrary', None)
        if FreeLibrary is not None:
            module = self.get_module(name)
            return self.remote_call(FreeLibrary, module)
        return False

    def raw_env(self):
        return _RawEnv(self)


class BigendHandler(MemHandler):
    """大端处理器"""
    def read(self, addr, type, size=0):
        if type is int:
            return self.readUint(addr, size if size else self.ptr_size)
        elif type is float:
            data = ProcessHandler.read(self, addr, bytes, size if size else 4)
            return struct.unpack('>f', data)[0]
        elif type is bool:
            return bool(self.read8(addr))
        else:
            return ProcessHandler.read(self, addr, type, size)

    def write(self, addr, data, size=0):
        _type = type(data)
        if _type is int:
            return self.writeUint(addr, data, size if size else self.ptr_size)
        elif _type is float:
            return ProcessHandler.write(self, addr, struct.pack('>f', data), size if size else 4)
        elif _type is bool:
            return self.write8(addr, data)
        else:
            return ProcessHandler.write(self, addr, data, size)

    def readUint(self, addr, size=0):
        return int.from_bytes(ProcessHandler.read(self, addr, bytes, size), 'big')

    def writeUint(self, addr, data, size=0):
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