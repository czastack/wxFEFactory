from functools import partial


class classlazy:
    def __init__(self, getter):
        self.name = '_' + getter.__name__
        self.getter = getter

    def __get__(self, instance, owner=None):
        owner = owner or instance.__class__
        value = getattr(owner, self.name, None)
        if value is None:
            value = self.getter(instance or owner)
            setattr(owner, self.name, value)
        return value


def cachable(func):
    cache = {}

    def _deco(value):
        result = cache.get(value, None)
        if result is None:
            result = cache[value] = func(value)
        return result

    return _deco


def lazy(func, type_=property, indict=False):
    name = '_' + func.__name__

    def _deco(self):
        value = self.__dict__.get(name, None) if indict else getattr(self, name, None)
        if value is None:
            value = func(self)
            setattr(self, name, value)
        return value
    return type_(_deco) if type_ else _deco


lazymethod = partial(lazy, type_=None)
lazyclassmethod = partial(lazy, type_=classmethod)
