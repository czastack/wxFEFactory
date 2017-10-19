def astr(text):
    """确保是字符串类型"""
    return text if isinstance(text, str) else str(text)

def list_re(li, fn):
    """列表元素映射"""
    for i in range(len(li)):
        li[i] = fn(li[i])

def list_find(li, fn):
    """列表查找第一个匹配的元素"""
    for x in li:
        if fn(x):
            return x;

def puts(dst, src, keys=None):
    """
    更新dict全部或指定字段
    dst: 模板dict, src: 来源dict
    """
    for key in keys or src:
        dst[key] = src[key]


def append_or(dic, key, value):
    if key in dic:
        dic[key].append(value)
    else:
        dic[key] = [value]

def make_tuple(*args):
    return args

def make_list(*args):
    return list(args)


class Map(dict):
    __slots__ = ()

    def __getattr__(self, name):
        return self[name] if name in self else None

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        del self[name]

    __puts__ = puts


class Dict:
    """
    usage:
        data = Dict({'a': 1})
        print(data.a) # get 1
    """
    __slots__ = ('_data',)

    def __init__(self, obj = None):
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

    puts = puts


class Dicts:
    """
    接收字典列表
    datas = Dict([{'a': 1}, {'a': 2}])
    for data in datas:
        print(data.a)
    """
    __slots__ = ('__ref', 'data')

    def __init__(self, array):
        if isinstance(key, (list, tuple)):
            self.__ref = None
            self.data = array
        else:
            raise TypeError('array must be a list or tuple')

    def __iter__(self):
        if not self.__ref:
            self.__ref = Dict()
        
        for item in self.data:
            self.__ref.__init__(item)
            yield self.__ref


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