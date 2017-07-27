import os
import json

class Configurable:
    """
    virtual getConfigFile() -> str
    """

    def __init__(self):
        self.config_changed = False

    def setConfig(self, key, value):
        self.config[key] = value
        self.config_changed = True

    def loadConfig(self):
        try:
            with open(self.getConfigFile()) as file:
                self.config = json.load(file)
        except FileNotFoundError:
            self.config = {}

    def writeConfig(self):
        if self.config_changed:
            with open(self.getConfigFile(), 'w') as file:
                self.config = json.dump(self.config, file)


class HistoryList(list):
    __slots__ = ('_index', 'maxsize')

    def __init__(self, data=None, maxsize=-1):
        if data:
            super().__init__(data)
        self._index = 0
        self.maxsize = maxsize

    def prev(self):
        if self:
            if self._index == 0:
                self._index = len(self)
            self._index -= 1
            return self[self._index]

    def next(self):
        if self:
            self._index += 1
            if self._index == len(self):
                self._index = 0
            return self[self._index]

    def append(self, e):
        try:
            i = self.index(e)
            self.append(self.pop(i))
        except ValueError:
            if self.maxsize is not -1 and self.maxsize == len(self):
                self.pop(0)
            super().append(e)
        self._index = 0


def fuzzyfinder(input, collection, accessor=lambda x: x):
    """
    模糊匹配
    Args:
        input (str): A partial string which is typically entered by a user.
        collection (iterable): A collection of strings which will be filtered
                               based on the `input`.
    Returns:
        suggestions (generator): A generator object that produces a list of
            suggestions narrowed down from `collection` using the `input`.
    """
    suggestions = []
    input = str(input) if not isinstance(input, str) else input
    pat = '.*?'.join(map(re.escape, input))
    regex = re.compile(pat)
    for item in collection:
        r = regex.search(accessor(item))
        if r:
            suggestions.append((len(r.group()), r.start(), accessor(item), item))

    return (z[-1] for z in sorted(suggestions))