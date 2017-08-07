
class Field:
    def __init__(self, offset, type_=None, size=4):
        self.offset = offset
        self.type = type_
        self.size = size

    def __get__(self, obj, type=None):
        return obj.handler.read(obj.addr + self.offset, self.size, self.type)

    def __set__(self, obj, val):
        obj.handler.write(obj.addr + self.offset, self.size, self.type(val))


class CoordsField:
    def __init__(self, offset):
        self.offset = offset

    def __get__(self, obj, type=None):
        return CoordsData(obj.handler, obj.addr + self.offset)

    def __set__(self, obj, val):
        if isinstance(val, CoordsData) and val.addr == obj.addr + self.offset:
            print('The val is a copy of this CoordsData')
        else:
            it = iter(val)
            for i in range(3):
                obj.handler.writeFloat(obj.addr + self.offset + i * 4, float(next(it)))


class CoordsData:
    def __init__(self, handler, addr):
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

    def next(self):
        if self._pos < 3:
            return self[self._pos]
        raise StopIteration


class Model:
    def __init__(self, addr, handler):
        self.addr = addr
        self.handler = handler