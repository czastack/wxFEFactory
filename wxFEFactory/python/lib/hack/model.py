from lib.utils import normalFloat


class Model:
    def __init__(self, addr, handler):
        self.addr = addr
        self.handler = handler

    def next(self):
        self.addr += self.SIZE
        return self

    def clone(self):
        return self.__class__(self.addr, self.handler)


class Field:
    def __init__(self, offset, type_=int, size=4):
        self.offset = offset
        self.type = type_
        self.size = size

    def __get__(self, obj, type=None):
        ret = obj.handler.read(obj.addr + self.offset, self.type, self.size)
        if self.type is float:
            ret = normalFloat(ret)
        return ret

    def __set__(self, obj, val):
        obj.handler.write(obj.addr + self.offset, self.type(val), self.size)


class OffsetsField(Field):
    def __get__(self, obj, type=None):
        ret = obj.handler.ptrsRead(obj.addr + self.offset[0], self.offset[1:], self.type, self.size)
        if self.type is float:
            ret = normalFloat(ret)
        return ret

    def __set__(self, obj, val):
        obj.handler.ptrsWrite(obj.addr + self.offset[0], self.offset[1:], self.type(val), self.size)


class ModelField(Field):
    def __init__(self, offset, modelClass):
        super().__init__(offset)
        self.modelClass = modelClass

    def __get__(self, obj, type=None):
        return self.modelClass(super().__get__(obj, type), obj.handler)

    def __set__(self, obj, val):
        raise AttributeError("can't set attribute")


class CoordsField:
    def __init__(self, offset):
        self.offset = offset

    def __get__(self, obj, type=None):
        return CoordsData(obj.addr + self.offset, obj.handler)

    def __set__(self, obj, val):
        if isinstance(val, CoordsData) and val.addr == obj.addr + self.offset:
            print('The val is a copy of this CoordsData')
        else:
            it = iter(val)
            for i in range(3):
                value = next(it)
                if value is None or value == '':
                    continue
                value = float(value)
                obj.handler.writeFloat(obj.addr + self.offset + i * 4, value)


class CoordsData:
    def __init__(self, addr, handler):
        self.handler = handler
        self.addr = addr
        self._pos = 0

    def values(self):
        return [self.handler.readFloat(self.addr + i * 4) for i in range(3)]

    def __getitem__(self, i):
        return self.handler.readFloat(self.addr + i * 4)

    def __setitem__(self, i, val):
        return self.handler.writeFloat(self.addr + i * 4, float(val))

    def __iter__(self):
        self._pos = 0
        return self

    def __next__(self):
        if self._pos < 3:
            ret = self[self._pos]
            self._pos += 1
            return ret
        raise StopIteration