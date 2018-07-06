from lib.hack.models import Model, Field, ByteField, WordField


class ItemSlot(Model):
    SIZE = 0x2
    item = ByteField(0)
    count = ByteField(1)
    value = WordField(0)


class BaseGlobal(Model):
    random = Field(0x03000000, size=8) # 乱数