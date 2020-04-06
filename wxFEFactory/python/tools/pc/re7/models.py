from lib.hack.models import (
    Model, Field, Fields, ByteField, WordField, FloatField, ArrayField, ModelField, ModelPtrField,
    CoordField, BytesField, ToggleField, UnicodeField
)


class Character(Model):
    """角色"""
    health_max = FloatField(0x20, label="最大HP")
    health = FloatField(0x24, label="HP")



class PositionStruct(Model):
    """位置数据"""
    coord = CoordField((0x18, 0x30), label="坐标")


class BagItem(Model):
    """背包物品"""
    name = UnicodeField((0x28, 0x80, 0x24), size=64, label="物品名称")
    quantity = Field((0x28, 0x88), label="数量")


class BoxItem(Model):
    """物品箱物品"""
    name = UnicodeField((0x20, 0x24), size=64, label="物品名称")
    quantity = Field(0x28, label="数量")


class Manager(Model):
    character = ModelPtrField((0x58, 0x28, 0x28, 0x70), Character)
    bag_items = ArrayField((0x60, 0x20, 0x30), 20, ModelPtrField(0, BagItem))
    box_items = ArrayField((0x58, 0x68, 0x60, 0x30), 20, ModelPtrField(0, BoxItem))


class Global(Model):
    manager = ModelPtrField(0x081E4148, Manager)


class CodexGlobal(Model):
    # character = ModelPtrField((0x07088EA0, 0x50), CharacterDataStruct)
    pass


SPECIFIC_GLOBALS = {
    'steam': Global,
    'codex': CodexGlobal,
}
