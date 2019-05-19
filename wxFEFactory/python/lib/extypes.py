import types
import weakref


list_tuple = (list, tuple)


def is_list_tuple(obj):
    return isinstance(obj, list_tuple)


def astr(text):
    """确保是字符串类型"""
    return text if isinstance(text, str) else str(text)


class Map(dict):
    __slots__ = ()

    def __getattr__(self, name):
        return self.get(name, None)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        del self[name]


class Dict:
    """
    usage:
        data = Dict({'a': 1})
        print(data.a)  # get 1
    """
    __slots__ = ('_data',)

    def __init__(self, obj=None):
        self._attr('_data', obj)

    def _attr(self, name, value):
        object.__setattr__(self, name, value)

    def __getattr__(self, name):
        return self._data.get(name, getattr(self._data, name, None))

    def __setattr__(self, name, value):
        self._data[name] = value

    def __str__(self):
        return self._data.__str__()

    def __iter__(self):
        return self._data.__iter__()

    def __getitem__(self, key):
        if isinstance(key, tuple):
            return (self._data[k] for k in key)
        elif isinstance(key, list):
            return [self._data[k] for k in key]
        return self._data[key]

    def __setitem__(self, key, value):
        if is_list_tuple(key):
            if is_list_tuple(value):
                val = iter(value).__next__
            else:
                def val():
                    return value
            for k in key:
                self._data[k] = val()
        else:
            self._data[key] = value

    def __delattr__(self, name):
        del self._data[name]

    def __repr__(self):
        return __class__.__name__ + '(' + self.__str__() + ')'

    def __and__(self, keys):
        if is_list_tuple(key):
            return __class__({key: self.__getattr__(key) for key in keys})


class Dicts:
    """
    接收字典列表
    datas = Dict([{'a': 1}, {'a': 2}])
    for data in datas:
        print(data.a)
    """
    __slots__ = ('_ref', 'data')

    def __init__(self, array):
        if is_list_tuple(array):
            self._ref = None
            self.data = array
        else:
            raise TypeError('array must be a list or tuple')

    def __iter__(self):
        if not self._ref:
            self._ref = Dict()

        for item in self.data:
            self._ref.__init__(item)
            yield self._ref


class INum:
    def __init__(self, i):
        self.i = i

    def __pos__(self):
        self.i += 1
        return self.i

    def __neg__(self):
        self.i -= 1
        return self.i

    def __int__(self):
        return self.i

    __index__ = __int__


class WeakBinder:
    def __init__(self, obj):
        self.ref = weakref.proxy(obj)

    def __getattr__(self, name):
        attr = getattr(self.ref.__class__, name, None)
        if isinstance(attr, types.FunctionType):
            method = types.MethodType(attr, self.ref)
            setattr(self, name, method)
            return method
        return getattr(self.ref, name)


def weakmethod(method):
    if isinstance(method, types.MethodType):
        method = types.MethodType(method.__func__, weakref.proxy(method.__self__))
    return method


class classproperty:
    def __init__(self, method):
        self.method = method

    def __get__(self, instance, owner):
        return self.method(owner)


class _DataClass:
    __slots__ = ()
    default = None

    def __init__(self, *args, **kwargs):
        self._set_data(args, kwargs)

    def set_data(self, *args, **kwargs):
        self._set_data(args, kwargs)

    def _set_data(self, args, kwargs):
        for field, arg in zip(self.__slots__, args):
            setattr(self, field, arg)
        for field in kwargs:
            setattr(self, field, kwargs[field])

    def to_dict(self):
        return {field: getattr(self, field) for field in self.__slots__}

    def to_tuple(self):
        return tuple(self)

    def clone(self):
        return self.__class__(self)

    def __iter__(self):
        return (getattr(self, field) for field in self.__slots__)

    def __getitem__(self, i):
        return getattr(self, self.__slots__[i], self.default)

    def __setitem__(self, i, value):
        return setattr(self, self.__slots__[i], value)

    def __str__(self):
        return str(self.to_tuple())

    def __repr__(self):
        return self.__class__.__name__ + self.__str__()

    def __getattr__(self, name):
        if self.defaults:
            return self.defaults.get(name, self.default)
        return self.default


def DataClass(name, fields, default=None, defaults=None, attrs=None, bases=None):
    """ 直接构造数据类
    :param bases: 父类元组或None"""
    the_attrs = {'fields': fields, 'default': default, 'defaults': defaults}
    if attrs:
        attrs.update(the_attrs)
        the_attrs = attrs
    return DataClassMeta.__new__(DataClassMeta, name, bases, the_attrs)


class DataClassMeta(type):
    def __new__(class_, name, bases, attrs):
        fields = attrs.pop('fields')

        the_bases = (_DataClass,)
        if bases:
            # 处理继承
            dataclass_base = False
            base_slots = []
            base_defaults = {}
            defaults = attrs.pop('defaults', None)
            for base in bases:
                if issubclass(base, _DataClass):
                    dataclass_base = True
                    base_slots.extend(base.__slots__)
                    if base.defaults:
                        base_defaults.update(base.defaults)
            if defaults:
                base_defaults.update(defaults)
            attrs['defaults'] = base_defaults
            base_slots.extend(fields)
            slots = base_slots

            if dataclass_base:
                if dataclass_base:
                    the_bases = bases
                else:
                    the_bases = bases + the_bases
        else:
            slots = tuple(fields)
        attrs['__slots__'] = slots
        return super().__new__(class_, name, the_bases, attrs)
