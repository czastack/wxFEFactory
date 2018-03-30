from lib.utils import float32, Accumulator
from lib.extypes import DataClass


class Model:
    def __init__(self, addr, handler):
        self.addr = addr
        self.handler = handler

    def next(self):
        self.addr += self.SIZE
        return self

    def to_bytes(self):
        return self.handler.read(self.addr, bytes, self.SIZE)

    def clone(self):
        return self.__class__(self.addr, self.handler)

    def addrof(self, field):
        return self.addr + self.offsetof(field)

    def offsetof(self, field):
        if isinstance(field, str):
            field = self.field(field)

        if isinstance(field, Field):
            return field.offset
        else:
            raise TypeError('expected a Field object, got ' + str(field))

    def __and__(self, field):
        return self.addrof(field)

    def __getattr__(self, name):
        data = test_comlex_attr(name)
        if data is not None:
            item = getattr(self, data.name)
            index = data.index
            # 计算偏移量(多用于分页)
            if index is not None and data.offset:
                index += getattr(self, data.offset)
            if index is not None:
                item = item[index]
            if data.attr:
                item = getattr(item, data.attr)
            return item

    def __setattr__(self, name, value):
        data = test_comlex_attr(name)
        if data is not None:
            item = getattr(self, data.name)
            index = data.index
            # 计算偏移量(多用于分页)
            if index is not None and data.offset:
                index += getattr(self, data.offset)
            if index is not None and not data.attr:
                item[index] = value
            else:
                if index is not None:
                    item = item[index]
                if data.attr:
                    setattr(item, data.attr, value)
        else:
            super().__setattr__(name, value)

    def test_comlex_attr(self, name):
        return test_comlex_attr(name)

    @classmethod
    def field(cls, name):
        for base in cls.__mro__:
            field = base.__dict__.get(name, None)
            if field:
                return field

    @property
    def addr_hex(self):
        return ("%08X" if self.addr < 0x100000000 else "%016X") % self.addr


class ManagedModel(Model):
    def __init__(self, addr, context):
        super().__init__(addr, context.handler)
        self.context = context

    def clone(self):
        return self.__class__(self.addr, self.context)


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

    def __str__(self):
        return "{}(offset={}, size={})".format(self.__class__.__name__, self.offset, self.size)

    __repr__ = __str__


class PtrField(Field):
    def __init__(self, offset, size=0):
        super().__init__(offset, int, size)

    def __get__(self, obj, type=None):
        if self.size is 0:
            # 对于ProcessHandler，根据目标进程获取指针大小
            self.size = obj.handler.ptr_size
        ret = obj.handler.readUint(obj.addr + self.offset, self.size)
        return ret


class ByteField(Field):
    def __init__(self, offset):
        super().__init__(offset, int, 1)


class WordField(Field):
    def __init__(self, offset):
        super().__init__(offset, int, 2)


DWordField = Field
U8Field = ByteField
U16Field = WordField
U32Field = DWordField


class SignedField(Field):
    def __get__(self, obj, type=None):
        return obj.handler.readInt(obj.addr + self.offset, self.type, self.size)

    def __set__(self, obj, value):
        if not isinstance(value, self.type):
            value = self.type(value)
        obj.handler.writeInt(obj.addr + self.offset, value, self.size)


class BitsField(Field):
    """位域字段"""
    def __init__(self, offset, size, bitoffset, bitlen):
        self.bitoffset = bitoffset
        self.bitlen = bitlen
        self.mask = (2 << bitlen) - 1
        super().__init__(offset, int, size)

    def __get__(self, obj, type=None):
        value = super().__get__(obj)
        return (value >> self.bitoffset) & self.mask

    def __set__(self, obj, value):
        old = super().__get__(obj)
        value = old & (~(self.mask << self.bitoffset) & 0xFFFFFFFFFFFFFFFF) | ((value & self.mask) << self.bitoffset)
        super().__set__(obj, value)

    @classmethod
    def create(cls, offset, size, bits):
        bitoffset = Accumulator()
        return (cls(offset, size, bitoffset.add(bit), bit) for bit in bits)


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


class ModelPtrField(PtrField):
    """模型指针字段"""
    def __init__(self, offset, modelClass, size=0):
        super().__init__(offset, size)
        self.modelClass = modelClass

    def __get__(self, obj, type=None):
        return self.modelClass(super().__get__(obj, type), obj.handler)

    def __set__(self, obj, value):
        if isinstance(value, Model):
            super().__set__(obj, value.addr)


class ManagedModelPtrField(ModelPtrField):
    """托管模型指针字段"""
    def __get__(self, obj, type=None):
        return self.modelClass(super().__get__(obj, type), obj.context)


class ModelField(Field):
    """模型字段"""
    def __init__(self, offset, modelClass, size=0):
        super().__init__(offset, None, size or modelClass.SIZE)
        self.modelClass = modelClass
        self.key = None

    def __get__(self, obj, type=None):
        ins = None
        if self.key:
            ins = getattr(obj, self.key, None)
        if ins is None:
            ins = self.modelClass(obj.addr + self.offset, obj.handler)
            if self.key:
                setattr(obj, self.key, ins)
        else:
            ins.addr = obj.addr + self.offset
        return ins

    def __set__(self, obj, value):
        raise AttributeError("can't set attribute")

    def __set_name__(self, owner, name):
        self.key = '_' + name


class CoordField:
    size = 12
    length = 3

    def __init__(self, offset, length=None, size=4):
        self.offset = offset
        self.size = size
        if length:
            self.length = length
            self.size = self.length * size

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
                obj.handler.writeFloat(obj.addr + self.offset + i * self.size, item)


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

    def __str__(self):
        return str(self.values())

    def __repr__(self):
        return self.__class__.__name__ + str(tuple(self.values()))


class ArrayField(Field):
    def __init__(self, offset, length, field):
        self.offset = offset
        self.length = length
        self.field = field
        self.key = None

    def __get__(self, obj, type):
        ins = None
        if self.key:
            ins = getattr(obj, self.key, None)
        if ins is None:
            ins = ArrayData(obj, self.offset, self.length, self.field)
            if self.key:
                setattr(obj, self.key, ins)
        return ins

    def __set__(self, obj, value):
        data = self.__get__(obj, type(obj))
        it = iter(value)
        for i in range(self.length):
            item = next(it)
            if item is None or item == '':
                continue
            data[i] = item

    def __set_name__(self, owner, name):
        self.key = '_' + name


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


"""
复杂字段名(多用于ArrayField)
:param name: 字段名称
:param index: 下标
:param attr: 下一层的属性
:param offset 偏移字段名: str
"""
CAttr = DataClass("CAttr", ("name", "index", "attr", "offset"))

COMLEX_ATTR_MAP = {}

def test_comlex_attr(text):
    """
    检查字段名是否是能构造CAttr的字符串
    格式: {name}.{index} 或 {name}.{index}.{attr} 或 {name}.{attr}
    若是，返回对应的CAttr实例，否则返回None
    """
    it = COMLEX_ATTR_MAP.get(text, None)
    if it is None:
        n = text.find('.')
        if n is not -1:
            index = None
            attr = None
            offset = None

            p = text.rfind('+')
            if p is not -1:
                offset = text[p + 1:]
            else:
                p = None

            name = text[:n]
            index = text[n + 1:p]

            m = index.find('.')
            if m is not -1:
                # {name}.{index}.{attr}
                attr = index[m + 1:]
                index = index[:m]
            elif not index.isdigit():
                # {name}.{attr}
                attr = index
            if index.isdigit():
                index = int(index)
            else:
                # {name}.{attr}
                index = None
            it = CAttr(name, index, attr, offset)
            COMLEX_ATTR_MAP[text] = it
    return it
