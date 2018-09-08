from .configurable import Configurable


class ConfigGroup:
    GROUPS = []

    def __init__(self, owner):
        if not isinstance(owner, Configurable):
            raise TypeError('owner must be Configurable object')
        self.owner = owner
        self.children = []
        parent = self.active_group()
        if parent:
            parent.append_child(self)

    def append_child(self, child):
        self.children.append(child)

    @classmethod
    def active_group(cls):
        return cls.GROUPS[-1] if len(cls.GROUPS) else None

    def __enter__(self):
        self.GROUPS.append(self)
        return self

    def __exit__(self, *args):
        if self.GROUPS.pop() is not self:
            raise ValueError('GROUPS层次校验失败')
        for field in self.children:
            field.render()
            field.read()
            help_text = getattr(field, 'help', None)
            if help_text is not None:
                field.set_help()

    def read(self, _=None):
        for field in self.children:
            field.read()

    def write(self, _=None):
        for field in self.children:
            field.write()