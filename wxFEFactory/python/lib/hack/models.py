from lib.utils import float32, Accumulator
from lib.extypes import DataClass, classproperty
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

    @classproperty
    def field_names(cls):
        field_names = getattr(cls, '_field_names', None)
        if field_names is None:
            field_names = cls._field_names = tuple(name for name, value in cls.__dict__.items()
                if isinstance(value, FieldType))
        return field_names

    @classproperty
    def fields(cls):
        fields = getattr(cls, '_fields', None)
        if fields is None:
            fields = cls._fields = tuple(cls.field(name) for name in cls.field_names)
        return fields

    @property
    def addr_hex(self):
        return ("%08X" if self.addr < 0x100000000 else "%016X") % self.addr

    def next(self):
        self.addr += self.SIZE
        return self

    def to_bytes(self):
        return self.handler.read(self.addr, bytes, self.SIZE)

    def to_hex_str(self):
        from . import utils
        return utils.bytes_beautify(self.to_bytes())

    def hex(self):
        return self.to_bytes().hex()

    def fromhex(self, hexstr):
        return self.handler.write(self.addr, bytes.fromhex(hexstr), self.SIZE)

    def clone(self):
        return self.__class__(self.addr, self.handler)

    def addrof(self, field):
        if isinstance(field, str):
            temp = self.field(field)
            if temp is None:
                def func(item, attr, is_int):
                    if is_int:
                        return item.addr_at(attr)
                    else:
                        return item & attr

                result = self.handle_comlex_attr(field, func)
                if result is not COMLEX_ATTR_NONE:
                    return result
            else:
                field = temp

        if field:
            return field.get_addr(self)

    def offsetof(self, field):
        if isinstance(field, str):
            field = self.field(field)
            if field is None:
                return

        if isinstance(field, FieldType):
            return field.offset
        else:
            raise TypeError('expected a Field object, got ' + str(field))

    def set_with(self, nameto, namefrom):
        setattr(self, nameto, getattr(self, namefrom))
        return self

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
        def func(item, attr, is_int):
            if is_int:
                try:
                    item = item[attr]
                except IndexError:
                    item = 0
            else:
                item = getattr(item, attr)
            return item

        result = self.handle_comlex_attr(name, func)
        if result is not COMLEX_ATTR_NONE:
            return result
        raise AttributeError("'{}' object has no attribute '{}'".format(self.__class__.__name__, name))

    def __setattr__(self, name, value):
        def func(item, attr, is_int):
            if is_int:
                item[attr] = value
            else:
                if item is not None:
                    setattr(item, attr, value)
                else:
                    print("目标为空，无法设置")

            return True

        if self.handle_comlex_attr(name, func) is COMLEX_ATTR_NONE:
            super().__setattr__(name, value)

    def handle_comlex_attr(self, name, func, out_range_warn=False):
        """func(item, attr, is_int) 最后一项的处理"""
        data = test_comlex_attr(name)
        if data is not None:
            item = self
            prev = None  # 取offset的对象
            i = 0
            last = len(data.attrs) - 1
            result = None
            for attr in data.attrs:
                is_last = i == last
                if isinstance(attr, str) and attr.startswith('$'):
                    # 动态attr
                    if attr.startswith('$$'):
                        attr = getattr(item, attr[2:])
                    else:
                        attr = getattr(self, attr[1:])
                if isinstance(attr, int):
                    offset = data.offsets and data.offsets.get(i, None)
                    if offset is not None:
                        attr += getattr(prev, offset)
                    try:
                        if is_last:
                            result = func(item, attr, True)
                        else:
                            item = item[attr]
                    except IndexError:
                        if out_range_warn:
                            print("下标{}超过限制，长度为{}".format(attr, item.length))
                        break
                else:
                    if is_last:
                        result = func(item, attr, False)
                    else:
                        prev = item
                        item = getattr(item, attr)
                        if item is None or item is 0:
                            break
                i += 1
            return result
        return COMLEX_ATTR_NONE

    def datasnap(self, fields=None):
        data = SimpleNamespace()
        for name in (fields if fields else self.field_names):
            setattr(data, name, getattr(self, name))
        return data


class ManagedModel(Model):
    def __init__(self, addr, context):
        super().__init__(addr, context.handler)
        self.context = context

    def clone(self):
        return self.__class__(self.addr, self.context)


class LookAfterModel(Model):
    """带字段拦截功能的Model"""
    own_fields = ()

    def __init_subclass__(cls):
        fields = []
        for name, value in cls.__dict__.items():
            if isinstance(value, FieldType):
                fields.append(name)
        cls.own_fields = tuple(fields)

    def __getattribute__(self, name):
        if name != 'own_fields' and name in self.own_fields:
            result = self.get_field(name)
            if result is not None:
                return result
        return object.__getattribute__(self, name)

    def __setattr__(self, name, value):
        if name in self.own_fields:
            if self.set_field(name, value) is False:
                return
        object.__setattr__(self, name, value)

    def get_field(self, nam):
        pass

    def set_field(self, name, value):
        pass


class FieldType:
    """最基本的字段类型"""
    def __init__(self, label):
        self.label = label

    def get_addr(self, instance):
        offset = self.offset
        if isinstance(offset, int):
            return instance.addr + offset
        elif isinstance(offset, tuple):
            if len(offset) == 2:
                return instance.handler.read_ptr(instance.addr + offset[0]) + offset[1]
            return instance.handler.read_last_addr(instance.addr + offset[0], offset[1:])
        elif callable(offset):
            return offset(instance, self)


class Field(FieldType):
    def __init__(self, offset, type=int, size=4, label=None):
        self.offset = offset
        self.type = type
        self.size = size
        super().__init__(label)

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        ret = instance.handler.read(self.get_addr(instance), self.type, self.size)
        if self.type is float:
            ret = float32(ret)
        return ret

    def __set__(self, instance, value):
        if not isinstance(value, self.type):
            value = self.type(value)
        if self.type is int and value < 0:
            value &= (1 << (self.size << 3)) - 1
        instance.handler.write(self.get_addr(instance), value, self.size)

    def __str__(self):
        return "{}(offset={}, size={})".format(self.__class__.__name__,
            hex(self.offset) if isinstance(self.offset, int) and self.offset > 0xFF else self.offset, self.size)

    __repr__ = __str__


class Fields(FieldType):
    """同步控制多个地址的值"""
    def __init__(self, *args, label=None):
        self.fields = args
        super().__init__(label)

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return self.fields[0].__get__(instance, owner)

    def __set__(self, instance, value):
        for field in self.fields:
            field.__set__(instance, value)


class Cachable:
    """可缓存对象"""
    key = None

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
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
        if instance is None:
            return self
        if self.size is 0:
            # 对于ProcessHandler，根据目标进程获取指针大小
            self.size = instance.handler.ptr_size
        return instance.handler.read_uint(self.get_addr(instance), self.size)


class ByteField(Field):
    __init__ = partialmethod(Field.__init__, size=1)


class WordField(Field):
    __init__ = partialmethod(Field.__init__, size=2)


class QWordField(Field):
    __init__ = partialmethod(Field.__init__, size=8)


class FloatField(Field):
    __init__ = partialmethod(Field.__init__, type=float)


DWordField = Field
U8Field = ByteField
U16Field = WordField
U32Field = DWordField
U64Field = QWordField


class SignedField(Field):
    """有符号字段"""
    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return instance.handler.read_int(self.get_addr(instance), self.type, self.size)

    def __set__(self, instance, value):
        if not isinstance(value, self.type):
            value = self.type(value)
        instance.handler.write_int(self.get_addr(instance), value, self.size)


class ToggleField(Field):
    """开关字段"""
    # 几种情况: 1. data在Widget中, get, set使用真实值; 2. data在Field中，get, set使用布尔值
    def __init__(self, *args, enable=None, disable=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.enable = enable
        self.disable = disable
        self.type = type(enable)
        if self.type is bytes:
            self.size = len(enable)

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        value = super().__get__(instance, owner)
        if self.enable is not None:
            return value == self.enable
        return value

    def __set__(self, instance, value):
        if value is True:
            value = self.enable
        elif value is False:
            value = self.disable
        super().__set__(instance, value)


class ToggleFields(FieldType):
    """同步控制多个ToggleField"""
    def __init__(self, *args, label=None):
        self.fields = args
        super().__init__(label)

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
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
        self.mask = (1 << bitlen) - 1
        super().__init__(offset, int, size, label)

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        value = super().__get__(instance)
        return (value >> self.bitoffset) & self.mask

    def __set__(self, instance, value):
        old = super().__get__(instance)
        value = (old & (~(self.mask << self.bitoffset) & 0xFFFFFFFFFFFFFFFF)
            | ((int(value) & self.mask) << self.bitoffset))
        super().__set__(instance, value)

    @classmethod
    def create(cls, offset, size, bits):
        bitoffset = Accumulator()
        return (cls(offset, size, bitoffset.add(bit), bit) for bit in bits)


class ModelPtrField(Cachable, PtrField):
    """模型指针字段"""
    def __init__(self, offset, modelClass, size=0, label=None):
        super().__init__(offset, size=size, label=label)
        self.modelClass = modelClass

    def create_cache(self, instance):
        if self.modelClass == 'self':
            self.modelClass = type(instance)
        return self.modelClass(PtrField.__get__(self, instance, None), instance.handler)

    def update_cache(self, instance, cache):
        cache.addr = PtrField.__get__(self, instance, None)

    def __set__(self, instance, value):
        if isinstance(value, Model):
            value = value.addr
        super().__set__(instance, value)


class ManagedModelPtrField(ModelPtrField):
    """托管模型指针字段"""
    def create_cache(self, instance):
        return self.modelClass(super().__get__(instance, owner), instance.context)


class ModelField(Cachable, Field):
    """模型字段"""
    def __init__(self, offset, modelClass, size=0, label=None):
        super().__init__(offset, None, size or getattr(modelClass, 'SIZE', 0), label)
        self.modelClass = modelClass

    def create_cache(self, instance):
        return self.modelClass(self.get_addr(instance), instance.handler)

    def update_cache(self, instance, cache):
        cache.addr = self.get_addr(instance)

    def __set__(self, instance, value):
        if isinstance(value, self.modelClass):
            instance.handler.write(self.get_addr(instance), value.to_bytes())
        elif isinstance(value, bytes):
            if len(value) != self.size:
                raise ValueError("value size {} not match Model size {}".format(len(value), self.size))
            instance.handler.write(self.get_addr(instance), value)
        else:
            raise ValueError("can't set attribute, except bytes or Model object")


class ManagedModelField(ModelField):
    """托管模型字段"""
    def create_cache(self, instance):
        return self.modelClass(self.get_addr(instance), instance.context)


class CoordField(Cachable, FieldType):
    field_size = 4
    length = 3

    def __init__(self, offset, type=float, length=length, field_size=field_size, label=None):
        self.offset = offset
        self.type = type
        self.field_size = field_size
        self.length = length
        self.size = self.length * field_size
        super().__init__(label)

    def create_cache(self, instance):
        return CoordData(self, instance)

    def __set__(self, instance, value):
        if isinstance(value, CoordData) and value.addr == self.get_addr(instance):
            print('The value is a copy of this CoordData')
        elif isinstance(value, bytes):
            instance.handler.write(self.get_addr(instance), value)
        else:
            it = iter(value)
            for i in range(self.length):
                item = next(it)
                if item is None or item == '':
                    continue
                instance.handler.write(self.get_addr(instance) + i * self.field_size, self.type(item))


class CoordData:
    def __init__(self, owner, instance):
        self.owner = owner
        self.instance = instance
        self._pos = 0

    @property
    def addr(self):
        return self.instance.addr + self.owner.offset

    def values(self):
        addr = self.addr
        return [self.instance.handler.read(addr + i * self.owner.field_size, self.owner.type)
            for i in range(self.owner.length)]

    def set(self, value):
        it = iter(value)
        for i in range(self.owner.length):
            item = next(it)
            if item is None or item == '':
                continue
            self[i] = item

    def to_bytes(self):
        return self.instance.handler.read(self.addr, bytes, self.owner.size)

    def __getitem__(self, i):
        return self.instance.handler.read(self.addr + i * self.owner.field_size, self.owner.type)

    def __setitem__(self, i, value):
        return self.instance.handler.write(self.addr + i * self.owner.field_size, self.owner.type(value))

    def __iadd__(self, value):
        if hasattr(value, '__iter__'):
            for i, it in enumerate(value):
                self[i] += it
        else:
            for i in range(self.len):
                self[i] += value
        return self

    def __imul__(self, value):
        if hasattr(value, '__iter__'):
            for i, it in enumerate(value):
                self[i] *= it
        else:
            for i in range(self.len):
                self[i] *= value
        return self

    def __iter__(self):
        self._pos = 0
        return self

    def __next__(self):
        if self._pos < self.owner.length:
            ret = self[self._pos]
            self._pos += 1
            return ret
        raise StopIteration

    def __str__(self):
        return str(self.values())

    def __repr__(self):
        return self.__class__.__name__ + str(tuple(self.values()))

    class Item:
        def __init__(self, i):
            self.i = i

        def __get__(self, instance, ownner=None):
            return instance[self.i]

        def __set__(self, instance, value):
            instance[self.i] = value

    x = Item(0)
    y = Item(1)
    z = Item(2)


class ArrayField(Cachable, Field):
    itemkeys = None

    def __init__(self, offset, length, field, cachable=False, label=None):
        self.length = length
        self.field = field
        self.cachable = cachable and isinstance(field, Cachable)
        super().__init__(offset, field, length * field.size, label)

    def __set_name__(self, owner, name):
        super().__set_name__(owner, name)
        if self.cachable:
            # itemkeys: 元素可缓存时(itemkeys不为None)，itemkeys是元素对应的key
            self.itemkeys = tuple("%s_%d" % (self.key, i) for i in range(self.length))

    def create_cache(self, instance):
        return ArrayData(self, instance)

    def __set__(self, instance, value):
        if isinstance(value, bytes):
            instance.handler.write(self.get_addr(instance), value)
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
    def __init__(self, owner, instance):
        self.owner = owner
        self.instance = instance
        if owner.field.size is 0:
            """传入了延迟设置size的field"""
            owner.field.__get__(instance)

    def __len__(self):
        return self.owner.length

    def get_field(self, i):
        if i >= self.owner.length:
            raise IndexError("array index out of range")
        field = self.owner.field
        offset = self.owner.offset
        if isinstance(offset, tuple):
            field.offset = offset[0:-1] + ((offset[-1] + field.size * i),)
        else:
            field.offset = offset + field.size * i
        if self.owner.itemkeys:
            field.key = self.owner.itemkeys[i]
        return field

    def __getitem__(self, i):
        return self.get_field(i).__get__(self.instance)

    def __setitem__(self, i, value):
        return self.get_field(i).__set__(self.instance, value)

    def __iter__(self):
        self._pos = 0
        return self

    def __next__(self):
        if self._pos < self.owner.length:
            ret = self[self._pos]
            self._pos += 1
            return ret
        raise StopIteration

    @property
    def addr(self):
        return self.owner.get_addr(self.instance)

    @property
    def length(self):
        return self.owner.length

    @property
    def size(self):
        return self.owner.length * self.owner.field.size

    def fill(self, value):
        if isinstance(value, int) and isinstance(self.owner.field, Field) and self.owner.field.type is int:
            data = value.to_bytes(self.owner.field.size, 'little') * self.owner.length
            self.instance.handler.write(self.addr, data)
        else:
            for i in range(self.owner.length):
                self[i] = value

    def addr_at(self, i):
        if i < 0:
            i += self.owner.length

        if i < 0 or i >= self.owner.length:
            raise IndexError

        return self.addr + self.owner.field.size * i

    def to_bytes(self):
        return self.instance.handler.read(self.addr, bytes, self.size)


class StringField(Field):
    def __init__(self, offset, size=0, label=None, encoding='gbk'):
        super().__init__(offset, bytes, size or 64, label)
        self.encoding = encoding

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        ret = instance.handler.read(self.get_addr(instance), self.type, self.size)
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
COMLEX_ATTR_NONE = object()


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
