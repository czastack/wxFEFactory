from lib.utils import float32, Accumulator
from lib.extypes import DataClass
from functools import partialmethod
from types import SimpleNamespace


class Model:
    def __init__(self, addr, handler):
        self.addr = addr
        self.handler = handler

    @classmethod
    def field(cls, name):
        for base in cls.__mro__:
            field = base.__dict__.get(name, None)
            if field:
                return field

    @property
    def addr_hex(self):
        return ("%08X" if self.addr < 0x100000000 else "%016X") % self.addr

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

    def set_with(self, namefrom, nameto):
        setattr(self, nameto, getattr(self, namefrom))

    def set_addr_by_index(self, i):
        self.addr = self.SIZE * i

    def test_comlex_attr(self, name):
        return test_comlex_attr(name)

    def __and__(self, field):
        return self.addrof(field)

    def __getitem__(self, attrs):
        if isinstance(attrs, str):
            return getattr(self, attr)
        else:
            return (getattr(self, attr) for attr in attrs)

    def __setitem__(self, attrs, values):
        if isinstance(attrs, str):
            setattr(self, attrs, values)
        else:
            valueiter = iter(values)
            for attr in attrs:
                setattr(self, attr, next(valueiter))

    def __getattr__(self, name):
        data = test_comlex_attr(name)
        if data is not None:
            item = self
            prev = None # 取offset的对象
            i = 0
            for attr in data.attrs:
                if isinstance(attr, int):
                    offset = data.offsets and data.offsets.get(i, None)
                    if offset is not None:
                        attr += getattr(prev, offset)
                    try:
                        item = item[attr]
                    except IndexError:
                        item = 0
                        break
                else:
                    prev = item
                    item = getattr(item, attr)
                    if item is None or item is 0:
                        break
                i += 1
            return item
        raise AttributeError("'{}' object has no attribute '{}'".format(self.__class__.__name__, name))

    def __setattr__(self, name, value):
        data = test_comlex_attr(name)
        if data is not None:
            item = self
            prev = None # 取offset的对象
            i = 0
            last = len(data.attrs) - 1
            for attr in data.attrs:
                if isinstance(attr, int):
                    offset = data.offsets and data.offsets.get(i, None)
                    if offset is not None:
                        attr += getattr(prev, offset)
                    try:
                        if i is last:
                            item[attr] = value
                        else:
                            item = item[attr]
                    except IndexError:
                        print("下标{}超过限制，长度为{}".format(attr, item.length))
                        break
                else:
                    if i is last:
                        setattr(item, attr, value)
                    else:
                        prev = item
                        item = getattr(item, attr)
                        if item is None or item is 0:
                            break
                    
                i += 1
        else:
            super().__setattr__(name, value)

    def datasnap(self, fields=None):
        data = SimpleNamespace()
        if fields:
            for name in fields:
                setattr(data, name, getattr(self, name))
        else:
            for name, value in self.__class__.__dict__:
                if isinstance(value, Field):
                    setattr(data, name, getattr(self, name))
        return data


class ManagedModel(Model):
    def __init__(self, addr, context):
        super().__init__(addr, context.handler)
        self.context = context

    def clone(self):
        return self.__class__(self.addr, self.context)


class Field:
    def __init__(self, offset, type=int, size=4, label=None):
        self.offset = offset
        self.type = type
        self.size = size
        self.label = label

    def __get__(self, instance, owner=None):
        ret = instance.handler.read(instance.addr + self.offset, self.type, self.size)
        if self.type is float:
            ret = float32(ret)
        return ret

    def __set__(self, instance, value):
        if not isinstance(value, self.type):
            value = self.type(value)
        if self.type is int and value < 0:
            value &= (1 << (self.size << 3)) - 1
        instance.handler.write(instance.addr + self.offset, value, self.size)

    def __str__(self):
        return "{}(offset={}, size={})".format(self.__class__.__name__, 
            hex(self.offset) if self.offset > 0xFF else self.offset, self.size)

    __repr__ = __str__


class Fields:
    """同步控制多个地址的值"""
    def __init__(self, *args, label=None):
        self.fields = args
        self.label = None

    def __get__(self, instance, owner=None):
        return self.fields[0].__get__(instance, owner)

    def __set__(self, instance, value):
        for field in self.fields:
            field.__set__(instance, value)


class Cachable:
    """可缓存对象"""
    key = None

    def __get__(self, instance, owner=None):
        cache = None
        key = self.key
        if key is not None:
            cache = getattr(instance, key, None)
        if cache is None:
            cache = self.create_cache(instance)
            if cache is not None and key is not None:
                setattr(instance, key, cache)
        else:
            self.update_cache(instance, cache)
        return cache

    def create_cache(self, instance):
        pass

    def update_cache(self, instance, cache):
        pass

    def __set_name__(self, owner, name):
        self.key = '_' + name


class PtrField(Field):
    __init__ = partialmethod(Field.__init__, size=0)

    def __get__(self, instance, owner=None):
        if self.size is 0:
            # 对于ProcessHandler，根据目标进程获取指针大小
            self.size = instance.handler.ptr_size
        return instance.handler.readUint(instance.addr + self.offset, self.size)


class ByteField(Field):
    __init__ = partialmethod(Field.__init__, size=1)


class WordField(Field):
    __init__ = partialmethod(Field.__init__, size=2)

class QWordField(Field):
    __init__ = partialmethod(Field.__init__, size=8)


DWordField = Field
U8Field = ByteField
U16Field = WordField
U32Field = DWordField
U64Field = QWordField


class SignedField(Field):
    """有符号字段"""
    def __get__(self, instance, owner=None):
        return instance.handler.readInt(instance.addr + self.offset, self.type, self.size)

    def __set__(self, instance, value):
        if not isinstance(value, self.type):
            value = self.type(value)
        instance.handler.writeInt(instance.addr + self.offset, value, self.size)


class ToggleField(Field):
    """开关字段"""
    # 几种情况: 1. data在Widget中, get, set使用真实值; 2. data在Field中，get, set使用布尔值
    def __init__(self, *args, enableData=None, disableData=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.enableData = enableData
        self.disableData = disableData
        self.type = type(enableData)
        if self.type is bytes:
            self.size = len(enableData)

    def __get__(self, instance, owner=None):
        value = super().__get__(instance, owner)
        if self.enableData is not None:
            return value == self.enableData
        return value

    def __set__(self, instance, value):
        if value is True:
            value = self.enableData
        elif value is False:
            value = self.disableData
        super().__set__(instance, value)


class ToggleFields:
    """同步控制多个ToggleField"""
    def __init__(self, *args, label=None):
        self.fields = args
        self.label = label

    def __get__(self, instance, owner=None):
        for field in self.fields:
            if field.__get__(instance, owner) is False:
                return False
        return True

    def __set__(self, instance, value):
        for field in self.fields:
            field.__set__(instance, value)


class BitsField(Field):
    """位域字段"""
    def __init__(self, offset, size, bitoffset, bitlen, label=None):
        self.bitoffset = bitoffset
        self.bitlen = bitlen
        self.mask = (2 << bitlen) - 1
        super().__init__(offset, int, size, label)

    def __get__(self, instance, owner=None):
        value = super().__get__(instance)
        return (value >> self.bitoffset) & self.mask

    def __set__(self, instance, value):
        old = super().__get__(instance)
        value = old & (~(self.mask << self.bitoffset) & 0xFFFFFFFFFFFFFFFF) | ((value & self.mask) << self.bitoffset)
        super().__set__(instance, value)

    @classmethod
    def create(cls, offset, size, bits):
        bitoffset = Accumulator()
        return (cls(offset, size, bitoffset.add(bit), bit) for bit in bits)


class OffsetsField(Field):
    def __get__(self, instance, owner=None):
        ret = instance.handler.ptrsRead(instance.addr + self.offset[0], self.offset[1:], self.type, self.size)
        if self.type is float:
            ret = float32(ret)
        return ret

    def __set__(self, instance, value):
        if not isinstance(value, self.type):
            value = self.type(value)
        instance.handler.ptrsWrite(instance.addr + self.offset[0], self.offset[1:], value, self.size)


class ModelPtrField(Cachable, PtrField):
    """模型指针字段"""
    def __init__(self, offset, modelClass, size=0, label=None):
        super().__init__(offset, size=size, label=label)
        self.modelClass = modelClass

    def create_cache(self, instance):
        return self.modelClass(PtrField.__get__(self, instance, None), instance.handler)

    def update_cache(self, instance, cache):
        cache.addr = PtrField.__get__(self, instance, None)

    def __set__(self, instance, value):
        if isinstance(value, Model):
            super().__set__(instance, value.addr)


class ManagedModelPtrField(ModelPtrField):
    """托管模型指针字段"""
    def create_cache(self, instance):
        return self.modelClass(super().__get__(instance, owner), instance.context)


class ModelField(Cachable, Field):
    """模型字段"""
    def __init__(self, offset, modelClass, size=0, label=None):
        super().__init__(offset, None, size or modelClass.SIZE, label)
        self.modelClass = modelClass

    def create_cache(self, instance):
        return self.modelClass(instance.addr + self.offset, instance.handler)

    def update_cache(self, instance, cache):
        cache.addr = instance.addr + self.offset

    def __set__(self, instance, value):
        if isinstance(value, self.modelClass):
            instance.handler.write(instance.addr + self.offset, value.to_bytes())
        elif isinstance(value, bytes):
            if len(value) != self.size:
                raise ValueError("value size {} not match Model size {}".format(len(value), self.size))
            instance.handler.write(instance.addr + self.offset, value)
        else:
            raise ValueError("can't set attribute, except bytes or Model object")


class ManagedModelField(ModelField):
    """托管模型字段"""
    def create_cache(self, instance):
        return self.modelClass(instance.addr + self.offset, instance.context)


class CoordField(Cachable):
    size = 4
    length = 3

    def __init__(self, offset, type=float, length=length, size=size, label=None):
        self.offset = offset
        self.type = type
        self.size = size
        self.length = length
        self.size = self.length * size
        self.label = label

    def create_cache(self, instance):
        return CoordData(instance, self)

    def __set__(self, instance, value):
        if isinstance(value, CoordData) and value.addr == instance.addr + self.offset:
            print('The value is a copy of this CoordData')
        elif isinstance(value, bytes):
            instance.handler.write(instance.addr + self.offset, value)
        else:
            it = iter(value)
            for i in range(self.length):
                item = next(it)
                if item is None or item == '':
                    continue
                instance.handler.write(instance.addr + self.offset + i * self.size, self.type, self.type(item))


class CoordData:
    def __init__(self, instance, field):
        self.instance = instance
        self.field = field
        self._pos = 0

    @property
    def addr(self):
        return self.instance.addr + self.field.offset

    def values(self):
        addr = self.addr
        return [self.instance.handler.read(addr + i * 4) for i in range(self.field.length)]

    def set(self, value):
        it = iter(value)
        for i in range(self.field.length):
            item = next(it)
            if item is None or item == '':
                continue
            self[i] = item

    def to_bytes(self):
        return self.instance.handler.read(self.addr, bytes, self.field.size)

    def __getitem__(self, i):
        return self.instance.handler.read(self.addr + i * 4, self.type)

    def __setitem__(self, i, value):
        return self.instance.handler.write(self.addr + i * 4, self.type(value))

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


class ArrayField(Cachable, Field):
    itemkeys = None

    def __init__(self, offset, length, field, itemcachable=False, label=None):
        self.length = length
        self.field = field
        self.itemcachable = itemcachable and isinstance(field, Cachable)
        super().__init__(offset, field, length * field.size, label)

    def __set_name__(self, owner, name):
        super().__set_name__(owner, name)
        if self.itemcachable:
            self.itemkeys = tuple("%s_%d" % (self.key, i) for i in range(self.length))

    def create_cache(self, instance):
        return ArrayData(instance, self.offset, self.length, self.field, self.itemkeys)

    def __set__(self, instance, value):
        if isinstance(value, bytes):
            instance.handler.write(instance.addr + self.offset, value)
        else:
            # iterable
            data = self.__get__(instance, type(instance))
            it = iter(value)
            for i in range(self.length):
                item = next(it)
                if item is None or item == '':
                    continue
                data[i] = item

    def __str__(self):
        return "{}(offset={}, length={}, field)".format(self.__class__.__name__, self.offset, self.length, self.field)

    __repr__ = __str__


class ArrayData:
    def __init__(self, instance, offset, length, field, itemkeys):
        """
        :param itemkeys: 元素可缓存时(itemkeys不为None)，itemkeys是元素对应的key
        """
        self.instance = instance
        self.offset = offset
        self.length = length
        self.field = field
        self.itemkeys = itemkeys
        if field.size is 0:
            """传入了延迟设置size的field"""
            field.__get__(instance)

    def __len__(self):
        return self.length

    def __getitem__(self, i):
        if i >= self.length:
            raise IndexError("array index out of range")
        field = self.field
        field.offset = self.offset + field.size * i
        if self.itemkeys:
            field.key = self.itemkeys[i]
        return field.__get__(self.instance)

    def __setitem__(self, i, value):
        if i >= self.length:
            raise IndexError("array index out of range")
        field = self.field
        field.offset = self.offset + field.size * i
        if self.itemkeys:
            field.key = self.itemkeys[i]
        return field.__set__(self.instance, value)

    def __iter__(self):
        self._pos = 0
        return self

    def __next__(self):
        if self._pos < self.length:
            ret = self[self._pos]
            self._pos += 1
            return ret
        raise StopIteration

    @property
    def addr(self):
        return self.instance.addr + self.offset

    @property
    def size(self):
        return self.length * self.field.size

    def fill(self, value):
        if isinstance(value, int) and isinstance(self.field, Field) and self.field.type is int:
            data = value.to_bytes(self.field.size, 'little') * self.length
            self.instance.handler.write(self.addr, data)
        else:
            for i in range(self.length):
                self[i] = value

    def addr_at(self, i):
        if i < 0:
            i += self.length

        if i < 0 or i >= self.length:
            raise IndexError

        return self.addr + self.field.size * i

    def to_bytes(self):
        return self.instance.handler.read(self.addr, bytes, self.size)


class StringField(Field):
    def __init__(self, offset, size=0, label=None, encoding='gbk'):
        super().__init__(offset, bytes, size or 64, label)
        self.encoding = encoding

    def __get__(self, instance, owner=None):
        ret = instance.handler.read(instance.addr + self.offset, self.type, self.size)
        return ret.rstrip(b'\x00').decode(self.encoding)

    def __set__(self, instance, value):
        if isinstance(value, str):
            value = bytes(value, self.encoding)
        if value[-1] != 0:
            value += b'\x00'
        super().__set__(instance, value)


class FieldPrep:
    def __init__(self, preget, preset=None, field=None):
        self.preget = preget
        self.preset = preset or preget
        self.field = field

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return self.preget(instance, self.field.__get__(instance, owner), self.field)

    def __set__(self, instance, value):
        self.field.__set__(instance, self.preset(instance, value, self.field))

    def __call__(self, field):
        return __class__(self.preget, self.preset, field)

    @property
    def offset(self):
        return self.field.offset

    @offset.setter
    def offset(self, value):
        self.field.offset = value

    @property
    def size(self):
        return self.field.size

    @property
    def type(self):
        return self.field.type


class AddFieldPrep(FieldPrep):
    """加预处理"""
    def __init__(self, diff, field=None):
        super().__init__(lambda ins, x, f: x + diff, lambda ins, x, f: int(x) - diff, field)


class MulFieldPrep(FieldPrep):
    """乘积预处理"""
    def __init__(self, p, field=None):
        super().__init__(lambda ins, x, f: x * p, lambda ins, x, f: int(x) // p, field)


class MinuendFieldPrep(FieldPrep):
    """被减处理"""
    def __init__(self, subtrahend, field=None):
        super().__init__(lambda ins, x, f: subtrahend - x, lambda ins, x, f: subtrahend - int(x), field)


"""
复杂字段名(多用于ArrayField)
:param name: 字段名称
:param index: 下标
:param attr: 下一层的属性
:param offsets {level: 偏移字段名}
"""
CAttr = DataClass("CAttr", ("attrs", "offsets"))

COMLEX_ATTR_MAP = {}

def test_comlex_attr(text):
    """
    检查字段名是否是能构造CAttr的字符串
    若是，返回对应的CAttr实例，否则返回None
    """
    it = COMLEX_ATTR_MAP.get(text, None)
    if it is None:
        if text.find('.') is not -1:
            attrs = []
            offsets = None
            args = text.split('.')
            i = 0
            for arg in args:
                if arg.find('+') is not -1:
                    arg, offset = arg.split('+')
                    arg = int(arg)
                    if offsets is None:
                        offsets = {}
                    offsets[i] = offset
                elif arg.isdigit():
                    arg = int(arg)
                attrs.append(arg)
                i += 1

            it = CAttr(attrs, offsets)
            COMLEX_ATTR_MAP[text] = it
    return it
