import types
import weakref


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
        print(data.a) # get 1
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
        if isinstance(key, (list, tuple)):
            if isinstance(value, (list, tuple)):
                val = iter(value).__next__
            else:
                val = lambda: value
            for k in key:
                self._data[k] = val()
        else:
            self._data[key] = value

    def __delattr__(self, name):
        del self._data[name]

    def __repr__(self):
        return __class__.__name__ + '(' + self.__str__() + ')'

    def __and__(self, keys):
        if isinstance(key, (list, tuple)):
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
        if isinstance(array, (list, tuple)):
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
    __slots__ = ('ref',)

    def __init__(self, obj):
        self.ref = weakref.proxy(obj)

    def __getattr__(self, name):
        attr = getattr(self.ref.__class__, name, None)
        if isinstance(attr, types.FunctionType):
            return types.MethodType(attr, self.ref)
        return getattr(self.ref, name)


def weakmethod(method):
    if isinstance(method, types.MethodType):
        method = types.MethodType(method.__func__, weakref.proxy(method.__self__))
    return method


class BaseDataClass:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        for field, arg in zip(self.__slots__, args):
            setattr(self, field, arg)
        for field in kwargs:
            setattr(self, field, kwargs[field])

    set_data = __init__

    def to_dict(self):
        return {field: getattr(self, field) for field in self.__slots__}

    def to_tuple(self):
        return tuple(getattr(self, field) for field in self.__slots__)

    def __str__(self):
        return str(self.to_tuple())

    def __repr__(self):
        return self.__class__.__name__ + self.__str__()

    def __getattr__(self, name):
        return self.default


def DataClass(name, fields, default=None):
    return type(name, (BaseDataClass,), {'__slots__': tuple(fields), 'default': default})