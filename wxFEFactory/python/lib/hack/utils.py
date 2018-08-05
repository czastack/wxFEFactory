from lib.utils import split_label_value


class BaseItemProvider:
    def __init__(self):
        self._choices = None
        self._values = None

    @property
    def choices(self):
        if self._choices is None:
            self.generate()
        return self._choices

    @property
    def values(self):
        if self._values is None:
            self.generate()
        return self._values


class ItemProvider(BaseItemProvider):
    """截取部分items提供器"""
    def __init__(self, datas, start, end, can_empty=True):
        super().__init__()
        self.datas = datas
        self.start = start
        self.end = end
        self.can_empty = can_empty

    def generate(self):
        choices = self.datas[self.start:self.end]
        values = tuple(range(self.start, self.end))
        if self.can_empty:
            if isinstance(self.datas, list):
                choices.insert(0, "无")
                values.insert(0, 0)
            elif isinstance(self.datas, tuple):
                choices = ("无",) + choices
                values = (0,) + values
        self._choices = choices
        self._values = values
        del self.datas, self.start, self.end, self.can_empty

    def __add__(self, items):
        return ItemProviders(self, items)


class ItemProviders(BaseItemProvider):
    """多个ItemProvider组合"""
    def __init__(self, *args):
        self.elems = list(args)
        super().__init__()

    def generate(self):
        choices = []
        values = []
        for elem in self.elems:
            choices.extend(elem.choices)
            values.extend(elem.values)
        self._choices = tuple(choices)
        self._values = tuple(values)
        del self.elems

    def __add__(self, items):
        self.elems.append(items)
        return self


class OptionProvider(BaseItemProvider):
    """分隔labels, values提供器"""
    def __init__(self, datas):
        super().__init__()
        self.datas = datas

    def generate(self):
        self._choices, self._values = split_label_value(self.datas)


def strhex(n, size=0):
    """
    :param size: 字节数
    """
    if size is 0:
        for x in (0x8, 0x10, 0x20, 0x40, 0x80):
            if n < (1 << x):
                break
        size = x >> 3
    return "%0*X" % ((size << 1), n)
