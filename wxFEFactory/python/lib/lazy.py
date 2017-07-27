from functools import partial


def lazy(func, type_=property):
    name = '_' + func.__name__
    def _deco(self):
        val = getattr(self, name, None)
        if val is None:
            val = func(self)
            setattr(self, name, val)
        return val
    return type_(_deco) if type_ else _deco


def classlazy(func, type_=property):
    name = '_' + func.__name__
    def _deco(self):
        val = getattr(self.__class__, name, None)
        if val is None:
            val = func(self)
            setattr(self.__class__, name, val)
        return val
    return type_(_deco) if type_ else _deco


lazymethod = partial(lazy, type_=None)
lazyclassmethod = partial(lazy, type_=classmethod)
