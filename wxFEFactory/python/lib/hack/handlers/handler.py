from fefactory_api.emuhacker import ProcessHandler
import struct


class MemHandler(ProcessHandler):
    _raw_addr = False

    def attach(self):
        pass

    def address_map(self, addr):
        return addr

    def raw_read(self, addr, type=int, size=0):
        self._raw_addr = True
        result = self.read(addr, type, size)
        self._raw_addr = False
        return result

    def raw_write(self, addr, data, size=0):
        self._raw_addr = True
        result = self.write(addr, data, size)
        self._raw_addr = False
        return result

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

    def inject_dll(self, path):
        LoadLibrary = getattr(self, '_LoadLibrary', None)
        if LoadLibrary is None:
            module = self.get_module('KERNEL32.DLL')
            helper = self.get_proc_helper(module)
            self._LoadLibrary = LoadLibrary = helper.get_proc_address('LoadLibraryW')
            self._FreeLibrary = LoadLibrary = helper.get_proc_address('FreeLibrary')

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
            return self.read_uint(addr, size if size else self.ptr_size)
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
            return self.write_uint(addr, data, size if size else self.ptr_size)
        elif _type is float:
            return ProcessHandler.write(self, addr, struct.pack('>f', data), size if size else 4)
        elif _type is bool:
            return self.write8(addr, data)
        else:
            return ProcessHandler.write(self, addr, data, size)

    def read_uint(self, addr, size=0):
        return int.from_bytes(ProcessHandler.read(self, addr, bytes, size), 'big')

    def write_uint(self, addr, data, size=0):
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