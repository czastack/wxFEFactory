from lib.hack.models import (
    Model, Field, Fields, ByteField, WordField, ArrayField, ModelField, ModelPtrField, CoordField, ToggleField
)


class Global(Model):
    pass


class SlotItem(Model):
    """游戏中物品"""
    SIZE = 0x30
    type = Field(0, label="种类")
    ammo = Field(4, label="数量/武器弹药")
    ammo_max = Field(8, label="最大数量/武器弹药")
    slot = Field(0x14, label="槽位")
    status = Field(0x18, label="状态")  # 01: 装备中, 02:未装备


class SavedItem(Model):
    """存档中的个人物品"""
    SIZE = 0x2C
    type = WordField(0x0)
    quantity = Field(0x4)
    max_quantity = Field(0x8)
    reload_speed = Field(0x1C)
    fire_power = Field(0x1E)
    capacity = Field(0x1F)
    piercing = Field(0x21)
    scope = Field(0x22)
    critical = Field(0x23)
    attack_range = Field(0x24)


class InventoryTreasureItem(Model):
    """物品箱/宝物箱物品"""
    SIZE = 0x48
    type = WordField(0)
    quantity = WordField(2)


class SavedItemHolder(Model):
    SIZE = 0x420
    """存档中的每个角色物品栏"""
    items = ArrayField(0, 9, ModelField(0, SavedItem))


class InventoryTreasureItemHolder(Model):
    SIZE = 0x1e60
    inventory_items = ArrayField(0x1C38, 54, ModelField(0, InventoryTreasureItem))
    treasure_items = ArrayField(0x2B68, 54, ModelField(0, InventoryTreasureItem))


class Player(Model):
    hp = WordField(0x1364, label="HP")
    hpmax = WordField(0x1366, label="最大HP")
    moving_coord = CoordField(0x2AD0, label="移动坐标")
    melee_coord = CoordField(0x2E10, label="坐标")
    idle = Field(0x10E0)
    target = Field(0x2DA4, label="目标")
    ai = Field(0x2DA8, label="AI")
    attack_reaction = Field(0x1358)
    invincible = ToggleField(0x135C, label="无敌", enableData=0, disableData=1)
    merce_kill_counter = Field(0x25BC)
    slot_items = ArrayField(0x21A8, 24, ModelField(0, SlotItem))


class CharacterStruct(Model):
    players = ArrayField(0x24, 4, ModelPtrField(0, Player))
    players_count = Field(0x34, label="角色数量")
    saved_items = ArrayField(0x714D0, 4, ModelField(0, SavedItemHolder))
    inventory_treasure = ModelPtrField(0x168F0, InventoryTreasureItemHolder)


class Inventory(Model):
    pass


class Money(Model):
    money = Field(0x01C0, label="金钱")
