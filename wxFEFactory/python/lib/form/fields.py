import ctypes
from lib.ui import wx

u8 = ctypes.c_ubyte
u16 = ctypes.c_ushort
u32 = ctypes.c_ulong

CTYPE_MAP = {
    1: u8,
    2: u16,
    4: u32,
}


class Field:
    __slots__ = ('name', 'label', 'size')

    def __init__(self, name, label, size):
        self.name = name
        self.label = label
        self.size = size

    @property
    def CTYPE(self):
        return CTYPE_MAP[self.size]

    def __repr__(self):
        return '%s("%s", "%s", %s)' % (self.__class__.__name__, self.name, self.label, self.size)


class Group(Field):
    __slots__ = ('children',)

    def __init__(self, name, label, children):
        super().__init__(name, label, 0)
        self.children = children

    def create_property(self, pg):
        pg.add_category(self.label)
        for field in self.children:
            field.create_property(pg)


class Int(Field):
    def create_property(self, pg):
        pg.add_int_property(self.label, self.name)


class Uint(Field):
    def create_property(self, pg):
        pg.add_hex_property(self.label, self.name)


class Text(Field):
    def create_property(self, pg):
        pg.add_string_property(self.label, self.name)


class SimpleSelect(Field):
    __slots__ = ('options',)

    def __init__(self, name, label, size, options=None):
        super().__init__(name, label, size)
        self.options = options

    def create_property(self, pg):
        pg.add_enum_property(self.label, self.name, None, self.options, None)


class FlagSelect(Field):
    __slots__ = ('options',)

    def __init__(self, name, label, size, options):
        super().__init__(name, label, size)
        self.options = options

    def create_property(self, pg):
        pg.add_flags_property(self.label, self.name, None, self.options)


class Bytes(Field):
    def create_property(self, pg):
        pg.add_hex_property(self.label, self.name)
