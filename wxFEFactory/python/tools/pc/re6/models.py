from lib.hack.models import (
    Model, Field, Fields, ByteField, WordField, ArrayField, ModelField, ModelPtrField, CoordField, ToggleField
)


class IngameItem(Model):
    """游戏中个人物品"""
    SIZE = 28
    enabled = ToggleField(0, size=1, enableData=1, disableData=0, label="激活")
    type = WordField(2, label="种类")
    quantity = WordField(6, label="数量/武器弹药")
    max_quantity = WordField(12, label="最大数量/武器弹药")
    model = Field(20, label="模型")


class CharacterConfigItem(Model):
    SIZE = 112
    model = Field(0)
    weapon_ability = ArrayField(16, 7, Field(0))
    skills = ArrayField(0x0728, 3, Field(0))


class CharacterConfig(Model):
    chars = ArrayField(0x42d7c, 7, ModelField(0, CharacterConfigItem))


class Character(Model):
    """角色"""
    health = WordField(0x0F10, label="生命值")
    health_max = WordField(0x0F12, label="生命值上限")
    invincible = ToggleField(0x0FC4, enableData=0, disableData=1, label="无敌")
    melee = Field(0x3B00, float, label="体术值")
    melee_max = Field(0x3B04, float, label="体术值上限")
    coord = CoordField(0x50, label="坐标")
    moving_speed = Field(0x54, float, label="移动速度")
    cur_item = ByteField(0x46D8)  # 当前使用的物品序号(只读)
    items = ArrayField(0x46E4, 24, ModelField(0, IngameItem))  # 水平武器: 0~6, 药丸: 7, 垂直武器: 8~12 其他物品: 15~23
    rapid_fire = Field(0x4F4C, float, label="快速开火")
    fix_weapon_switch = Field(0x46D0, float)  # 竖行武器切换至横行武器时的修正？
    is_wet = Field(0x2E34, label="是否湿了")


class CharacterStruct(Model):
    chars = ArrayField(0x24, 4, ModelPtrField(0, Character))
    chars_count = Field(0x44, label="角色数量")


class Money(Model):
    money = Field(0x01C0, label="金钱")


class Global(Model):
    character_struct = ModelPtrField(0x013C4428, CharacterStruct)
    character_config = ModelPtrField(0x013C345C, CharacterConfig)
