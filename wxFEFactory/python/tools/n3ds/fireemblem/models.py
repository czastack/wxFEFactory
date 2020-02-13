from lib.hack.models import Model, Field, ByteField, WordField


class ItemSlot(Model):
    SIZE = 4
    item = WordField(0)
    count = ByteField(2)
    status = ByteField(3)  # 0x10=装备中
    value = Field(0)


class BaseGlobal(Model):
    pass
