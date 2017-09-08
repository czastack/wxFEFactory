from .lazy import lazy
import ctypes

u8  = ctypes.c_uint8
u16 = ctypes.c_uint16
u32 = ctypes.c_uint32
u64 = ctypes.c_uint64

class CArray:
    def __init__(self, size):
        self.array = (self.TYPE * size)()
        self.__getitem__ = None

    @property
    def array_t(self):
        return type(self.array)

    @lazy
    def buffer(self):
        length  = ctypes.sizeof(self.array)
        ptr     = ctypes.cast(ctypes.pointer(self.array), ctypes.POINTER(ctypes.c_char * length))
        return ptr.contents

    def to_bytes(self):
        return self.buffer.raw

    def __getattr__(self, name):
        return getattr(self.array, name)

    def __getitem__(self, key):
        return self.array.__getitem__(key)

    def __setitem__(self, key, value):
        return self.array.__setitem__(key, value)


class Uint8Array(CArray):
    TYPE = u8
    

class Uint16Array(CArray):
    TYPE = u16


class Uint32Array(CArray):
    TYPE = u32


class Uint64Array(CArray):
    TYPE = u64
