from functools import partial


def lazy(func, type_=property, indict=False):
    name = '_' + func.__name__
    def _deco(self):
        value = getattr(self, name, None) if not indict else self.__dict__.get(name, None)
        if value is None:
            value = func(self)
            setattr(self, name, value)
        return value
    return type_(_deco) if type_ else _deco


def classlazy(func, type_=property, indict=False):
    name = '_' + func.__name__
    def _deco(self):
        value = getattr(self, name, None) if not indict else self.__dict__.get(name, None)
        if value is None:
            value = func(self)
            setattr(self.__class__, name, value)
        return value
    return type_(_deco) if type_ else _deco


lazymethod = partial(lazy, type_=None)
lazyclassmethod = partial(lazy, type_=classmethod)
lazyclassmethod_indict = partial(lazy, type_=classmethod, indict=True)