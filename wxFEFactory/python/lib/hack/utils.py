
class ItemProvider:
    def __init__(self, datas, start, end, can_empty=True):
        self.datas = datas
        self.start = start
        self.end = end
        self.can_empty = can_empty
        self._choices = None
        self._values = None

    def generate(self):
        choices = self.datas[self.start:self.end]
        values = tuple(range(self.start, self.end))
        if self.can_empty:
            choices = ("无",) + choices
            values = (0,) + values
        self._choices = choices
        self._values = values
        del self.datas, self.start, self.end, self.can_empty
    
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
