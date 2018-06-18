from lib.hack.model import Model, Field, ByteField, WordField


class ItemInfo(Model):
    SIZE = 2
    item = ByteField(0)
    count = ByteField(1)


class ItemInfo2(Model):
    SIZE = 4
    item = WordField(0)
    count = ByteField(2)


class BaseGlobal(Model):
    pass