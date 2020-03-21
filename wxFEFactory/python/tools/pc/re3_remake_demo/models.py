from lib.hack.models import (
    Model, Field, Fields, ByteField, WordField, FloatField, ArrayField, ModelField, ModelPtrField,
    CoordField, BytesField, ToggleField
)
from .datasets import INVENTORY_OPTIONS, AMMO_MAP


class Character(Model):
    """角色"""
    data = Field(0x54, label="数据")
    health = Field((0x2C0, 0x58), label="HP")
    invincible = ToggleField((0x2C0, 0x5C), label="无敌", enable=0, disable=1)
    # health_max = WordField(0x1366, label="最大HP")
    action = Field((0x108, 0x54), label="动作")
    weapon_state = Field((0x128, 0x58))
    speed = FloatField((0x130, 0x50), label="速度")


class CharacterStruct(Model):
    char = ModelPtrField(0x50, Character)


class CharacterDataStruct_1(object):
    SIZE = 24
    character_code = Field(16)


class CharacterDataStruct(Model):
    # Leon: (48, 16), Claire: (72, 16)
    chars_data = ArrayField((0x50, 0x18, 0x30), 4, ModelField(0, CharacterDataStruct_1))


class PositionStruct(Model):
    """位置数据"""
    coord = CoordField((0x18, 0x30), label="坐标")


class InventoryItemInfo(Model):
    """仓库物品信息"""
    SIZE = 240
    item_code = Field(0x10, label="物品编码")
    weapon_code = Field(0x14, label="武器编码")
    ammo_code = Field(0x1C, label="子弹编码")
    count = Field(0x20, label="数量")

    @property
    def choice(self):
        """物品种类序号"""
        self_weapon = self.weapon_code
        self_item = self.item_code
        i = 0
        for item, weapon, _ in INVENTORY_OPTIONS:
            if (self_weapon == 0xFFFFFFFF and self_item == item) or (self_weapon and self_weapon == weapon):
                break
            i += 1
        else:
            i = -1
        return i

    @choice.setter
    def choice(self, value):
        item, weapon, _ = INVENTORY_OPTIONS[value]
        self.item_code = item
        self.weapon_code = 0xFFFFFFFF if weapon == -1 else weapon
        self.ammo_code = AMMO_MAP.get(weapon, 0)


class InventoryItem(Model):
    """仓库物品"""
    info = ModelField((0x18, 0x10, 0), InventoryItemInfo)
    data = BytesField((0x18, 0), 240)


class Inventory(Model):
    """物品栏"""
    capcity = Field(0x90, label="背包容量")
    items = ArrayField((0x98, 0x10, 0x20), 20, ModelPtrField(0, InventoryItem))


class Global(Model):
    character_data = ModelPtrField((0x070A6080, 0x50), CharacterDataStruct)
    character_struct = ModelPtrField(0x070A7CD0, CharacterStruct)
    # char_array = 0x062C730C
    position_struct = ModelPtrField(0x070973C8, PositionStruct)
    inventory = ModelPtrField((0x08DCB6C0, 0x50), Inventory)
    camera_dist = Field((0x070A87D8, 0x98, 0x160, 0x34), label="摄像机参数")
    save_count = Field((0x070A8860, 0x198, 0x24), label="保存次数")


class CodexGlobal(Model):
    character_data = ModelPtrField((0x07088EA0, 0x50), CharacterDataStruct)
    character_struct = ModelPtrField(0x0708A678, CharacterStruct)
    # char_array = 0x062B2386
    position_struct = ModelPtrField(0x070B0D98, PositionStruct)
    inventory = ModelPtrField((0x070B0840, 0x50), Inventory)
    camera_dist = Field((0x07081988, 0x98, 0x160, 0x34), label="摄像机参数")
    save_count = Field((0x07081A90, 0x198, 0x24), label="保存次数")


SPECIFIC_GLOBALS = {
    'steam': Global,
    'codex': CodexGlobal,
}
