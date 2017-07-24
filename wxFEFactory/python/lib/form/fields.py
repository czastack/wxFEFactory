import ctypes

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

    def createProperty(self, pg):
        pg.addCategory(self.label)
        for field in self.children:
            field.createProperty(pg)


class Int(Field):
    def createProperty(self, pg):
        pg.addIntProperty(self.label, self.name)


class Uint(Field):
    def createProperty(self, pg):
        pg.addHexProperty(self.label, self.name)


class Text(Field):
    def createProperty(self, pg):
        pg.addStringProperty(self.label, self.name)


class SimpleSelect(Field):
    __slots__ = ('options',)

    def __init__(self, name, label, size, options=None):
        super().__init__(name, label, size)
        self.options = options

    def createProperty(self, pg):
        pg.addEnumProperty(self.label, self.name, None, self.options, None)


class FlagSelect(Field):
    __slots__ = ('options',)

    def __init__(self, name, label, size, options):
        super().__init__(name, label, size)
        self.options = options

    def createProperty(self, pg):
        pg.addFlagsProperty(self.label, self.name, None, self.options)


class Bytes(Field):
    def createProperty(self, pg):
        pg.addHexProperty(self.label, self.name)
