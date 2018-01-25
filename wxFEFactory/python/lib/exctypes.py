from .lazy import lazy
import ctypes
_SimpleCData = ctypes._SimpleCData


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
    TYPE = ctypes.c_uint8
    

class Uint16Array(CArray):
    TYPE = ctypes.c_uint16


class Uint32Array(CArray):
    TYPE = ctypes.c_uint32


class Uint64Array(CArray):
    TYPE = ctypes.c_uint64


def ival(value):
    if isinstance(value, _SimpleCData):
        value = value.value
    return value


class cint:
    def __int__(self):
        return self.value

    def __oct__(self):
        return oct(self.value)

    def __hex__(self):
        return hex(self.value)

    def __add__(self, other):
        return self.__class__(self.value.__add__(ival(other)))

    def __sub__(self, other):
        return self.__class__(self.value.__sub__(ival(other)))

    def __mul__(self, other):
        return self.__class__(self.value.__mul__(ival(other)))

    def __floordiv__(self, other):
        return self.__class__(self.value.__floordiv__(ival(other)))

    __truediv__ = __floordiv__

    def __mod__(self, other):
        return self.__class__(self.value.__mod__(ival(other)))

    def __pow__(self, other):
        return self.__class__(self.value.__pow__(ival(other)))

    def __lshift__(self, other):
        return self.__class__(self.value.__lshift__(ival(other)))

    def __rshift__(self, other):
        return self.__class__(self.value.__rshift__(ival(other)))

    def __and__(self, other):
        return self.__class__(self.value.__and__(ival(other)))

    def __or__(self, other):
        return self.__class__(self.value.__or__(ival(other)))

    def __xor__(self, other):
        return self.__class__(self.value.__xor__(ival(other)))

    def __rsub__(self, other):
        return self.__class__(self.value.__rsub__(ival(other)))

    def __rmul__(self, other):
        return self.__class__(self.value.__rmul__(ival(other)))

    def __rmul__(self, other):
        return self.__class__(self.value.__rmul__(ival(other)))

    def __rfloordiv__(self, other):
        return self.__class__(self.value.__rfloordiv__(ival(other)))

    def __rdiv__(self, other):
        return self.__class__(self.value.__rdiv__(ival(other)))

    def __rmod__(self, other):
        return self.__class__(self.value.__rmod__(ival(other)))

    def __rdivmod__(self, other):
        return self.__class__(self.value.__rdivmod__(ival(other)))

    def __rpow__(self, other):
        return self.__class__(self.value.__rpow__(ival(other)))

    def __rlshift__(self, other):
        return self.__class__(self.value.__rlshift__(ival(other)))

    def __rrshift__(self, other):
        return self.__class__(self.value.__rrshift__(ival(other)))

    def __ror__(self, other):
        return self.__class__(self.value.__ror__(ival(other)))

    def __rxor__(self, other):
        return self.__class__(self.value.__rxor__(ival(other)))

    def __iadd__(self, other):
        self.value += ival(other)

    def __isub__(self, other):
        self.value -= ival(other)

    def __imul__(self, other):
        self.value *= ival(other)

    def __ifloordiv__(self, other):
        self.value /= ival(other)

    __itruediv__ = __ifloordiv__

    def __imod__(self, other):
        self.value %= ival(other)

    def __ipow__(self, other):
        self.value **= ival(other)

    def __ilshift__(self, other):
        self.value <<= ival(other)

    def __irshift__(self, other):
        self.value >>= ival(other)

    def __iand__(self, other):
        self.value &= ival(other)

    def __ior__(self, other):
        self.value |= ival(other)

    def __ixor__(self, other):
        self.value ^= ival(other)


class int8(ctypes.c_int8, cint):
    pass

class int16(ctypes.c_int16, cint):
    pass

class int32(ctypes.c_int32, cint):
    pass

class int64(ctypes.c_int64, cint):
    pass

class u8(ctypes.c_uint8, cint):
    pass

class u16(ctypes.c_uint16, cint):
    pass

class u32(ctypes.c_uint32, cint):
    pass

class u64(ctypes.c_uint64, cint):
    pass
