from lib.hack.models import (
    Model, Field, Fields, ByteField, WordField, ArrayField, ModelField, ModelPtrField, CoordField, ToggleField
)


class SavedItem(Model):
    """整理界面个人物品"""
    SIZE = 0x2C
    type = WordField(0x0, label="种类")
    quantity = Field(0x4, label="数量/武器弹药")
    max_quantity = Field(0x8, label="最大数量/武器弹药")
    fire_power = WordField(0x1C, label="火力升级")
    reload_speed = ByteField(0x1E, label="装弹速度升级")
    capacity = ByteField(0x1F, label="容量升级")
    critical = ByteField(0x21, label="爆头率升级")
    attack_range = ByteField(0x21, label="攻击范围升级")
    piercing = ByteField(0x22, label="贯穿伤害升级")
    scope = ByteField(0x24, label="瞄准镜升级")
    model = Field(0x28, label="模型")


class IngameItem(SavedItem):
    """游戏中物品"""
    SIZE = 0x30
    slot = Field(0x14, label="槽位")
    status = Field(0x18, label="状态")  # 01: 装备中, 02:未装备


class InventoryTreasureItem(Model):
    """物品箱/宝物箱物品"""
    SIZE = 0x48
    type = WordField(0, label="种类")
    quantity = WordField(2, label="数量/武器弹药")


class SavedItemHolder(Model):
    SIZE = 0x420
    """整理界面每个角色物品栏"""
    items = ArrayField(0, 9, ModelField(0, SavedItem))


class InventoryTreasureItemHolder(Model):
    SIZE = 0x1e60
    inventory_items = ArrayField(0x1C38, 54, ModelField(0, InventoryTreasureItem))
    treasure_items = ArrayField(0x2B68, 54, ModelField(0, InventoryTreasureItem))


class Character(Model):
    health = WordField(0x1364, label="HP")
    health_max = WordField(0x1366, label="最大HP")
    coord = CoordField(0x30, label="坐标")
    # idle = Field(0x10E0)
    # target = Field(0x2DA4, label="目标")
    # ai = Field(0x2DA8, label="AI")
    # attack_reaction = Field(0x1358)
    # merce_kill_counter = Field(0x25BC)
    invincible = ToggleField(0x135C, label="无敌", enableData=0, disableData=1)
    items = ArrayField(0x21A8, 24, ModelField(0, IngameItem))


class CharacterStruct(Model):
    chars = ArrayField(0x24, 4, ModelPtrField(0, Character))
    chars_count = Field(0x34, label="角色数量")
    saved_items = ArrayField(0x714D0, 4, ModelField(0, SavedItemHolder))
    inventory_treasure_holder = ModelPtrField(0x168F0, InventoryTreasureItemHolder)


class Inventory(Model):
    pass


class Money(Model):
    money = Field(0x01C0, label="金钱")


class Global(Model):
    character_struct = ModelPtrField(0x00DA2A5C, CharacterStruct)
    money = ModelPtrField(0x00DA23D8, Money)
