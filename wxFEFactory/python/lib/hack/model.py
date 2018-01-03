from lib.utils import float32


class Model:
    def __init__(self, addr, handler):
        self.addr = addr
        self.handler = handler

    def next(self):
        self.addr += self.SIZE
        return self

    def clone(self):
        return self.__class__(self.addr, self.handler)

    def addrof(self, field):
        return self.addr + self.offsetof(field)

    def offsetof(self, field):
        if isinstance(field, str):
            field = self.__class__.__dict__[field]

        if isinstance(field, Field):
            return field.offset
        else:
            raise TypeError('expected a Field object, got ' + str(field))

    def __and__(self, field):
        return self.addrof(field)


class Field:
    def __init__(self, offset, type_=int, size=4):
        self.offset = offset
        self.type = type_
        self.size = size

    def __get__(self, obj, type=None):
        ret = obj.handler.read(obj.addr + self.offset, self.type, self.size)
        if self.type is float:
            ret = float32(ret)
        return ret

    def __set__(self, obj, value):
        if not isinstance(value, self.type):
            value = self.type(value)
        obj.handler.write(obj.addr + self.offset, value, self.size)


class PtrField(Field):
    def __init__(self, offset, size=0):
        super().__init__(offset, int, size)

    def __get__(self, obj, type=None):
        if self.size is 0:
            # 对于ProcessHandler，根据目标进程获取指针大小
            self.size = obj.handler.ptr_size
        ret = obj.handler.readUint(obj.addr + self.offset, self.size)
        return ret


class SignedField(Field):
    def __get__(self, obj, type=None):
        return obj.handler.readInt(obj.addr + self.offset, self.type, self.size)

    def __set__(self, obj, value):
        if not isinstance(value, self.type):
            value = self.type(value)
        obj.handler.writeInt(obj.addr + self.offset, value, self.size)


class OffsetsField(Field):
    def __get__(self, obj, type=None):
        ret = obj.handler.ptrsRead(obj.addr + self.offset[0], self.offset[1:], self.type, self.size)
        if self.type is float:
            ret = float32(ret)
        return ret

    def __set__(self, obj, value):
        if not isinstance(value, self.type):
            value = self.type(value)
        obj.handler.ptrsWrite(obj.addr + self.offset[0], self.offset[1:], value, self.size)


class ModelField(Field):
    def __init__(self, offset, modelClass):
        super().__init__(offset)
        self.modelClass = modelClass

    def __get__(self, obj, type=None):
        return self.modelClass(super().__get__(obj, type), obj.handler)

    def __set__(self, obj, value):
        raise AttributeError("can't set attribute")


class CoordField:
    size = 12
    length = 3

    def __init__(self, offset, length=None):
        self.offset = offset
        if length:
            self.length = length
            self.size = self.length * 4

    def __get__(self, obj, type=None):
        return CoordData(obj.addr + self.offset, obj.handler, self.length)

    def __set__(self, obj, value):
        if isinstance(value, CoordData) and value.addr == obj.addr + self.offset:
            print('The value is a copy of this CoordData')
        else:
            it = iter(value)
            for i in range(self.length):
                item = next(it)
                if item is None or item == '':
                    continue
                obj.handler.writeFloat(obj.addr + self.offset + i * 4, item)


class CoordData:
    def __init__(self, addr, handler, length=3):
        self.addr = addr
        self.handler = handler
        self.length = length
        self._pos = 0

    def values(self):
        return [self.handler.readFloat(self.addr + i * 4) for i in range(self.length)]

    def set(self, value):
        it = iter(value)
        for i in range(self.length):
            item = next(it)
            if item is None or item == '':
                continue
            self[i] = item

    def __getitem__(self, i):
        return self.handler.readFloat(self.addr + i * 4)

    def __setitem__(self, i, value):
        return self.handler.writeFloat(self.addr + i * 4, float(value))

    def __iter__(self):
        self._pos = 0
        return self

    def __next__(self):
        if self._pos < self.length:
            ret = self[self._pos]
            self._pos += 1
            return ret
        raise StopIteration


class ArrayField(Field):
    def __init__(self, offset, length, field):
        self.offset = offset
        self.length = length
        self.field = field

    def __get__(self, obj, type):
        return ArrayData(obj, self.offset, self.length, self.field)

    def __set__(self, obj, value):
        data = self.__get__(obj, type(obj))
        it = iter(value)
        for i in range(self.length):
            item = next(it)
            if item is None or item == '':
                continue
            data[i] = item


class ArrayData:
    def __init__(self, obj, offset, length, field):
        self.obj = obj
        self.offset = offset
        self.addr = obj.addr + offset
        self.length = length
        self.field = field
        if field.size is 0:
            """传入了延迟设置size的field"""
            field.__get__(obj)

    def __getitem__(self, i):
        field = self.field
        field.offset = self.offset + field.size * i
        return field.__get__(self.obj)

    def __setitem__(self, i, value):
        field = self.field
        field.offset = self.offset + field.size * i
        return field.__set__(self.obj, value)

    def __iter__(self):
        self._pos = 0
        return self

    def __next__(self):
        if self._pos < self.length:
            ret = self[self._pos]
            self._pos += 1
            return ret
        raise StopIteration

    def addr_at(self, i):
        if i < 0:
            i += self.length

        if i < 0 or i >= self.length:
            raise IndexError

        return self.addr + self.field.size * i

    @property
    def size(self):
        return self.length * self.field.size


class StringField(Field):
    def __init__(self, offset, size=0, encoding='gbk'):
        super().__init__(offset, bytes, size)
        self.encoding = encoding

    def __get__(self, obj, type=None):
        ret = obj.handler.read(obj.addr + self.offset, self.type, self.size or 64)
        return ret.rstrip(b'\x00').decode(self.encoding)

    def __set__(self, obj, value):
        if isinstance(value, str):
            value = bytes(value, self.encoding)
        if value[-1] != 0:
            value += b'\x00'
        super().__set__(obj, value)