from lib.hack.models import (
    Model, Field, Fields, ByteField, WordField, ArrayField, ModelField, ModelPtrField, CoordField, ToggleField
)


class IngameItem(Model):
    """游戏中个人物品"""
    SIZE = 0x1C
    enabled = ToggleField(4, size=1, enable=1, disable=0, label="激活")
    slot = ByteField(5, label="槽位")
    type = WordField(6, label="种类")
    quantity = WordField(0x0A, label="数量/武器弹药")
    double_quantity = WordField(0x0C, label="双枪弹药")
    max_quantity = WordField(0x10, label="最大数量/武器弹药")
    model = Field(0x18, label="模型")


class Character(Model):
    """角色"""
    id = Field((0x010C, 0x16), bytes, 6)
    health = WordField(0x0F10, label="生命值")
    health_max = WordField(0x0F12, label="生命值上限")
    invincible = ToggleField(0x0FC4, enable=0, disable=1, label="无敌")
    stamina = Field(0x3B00, float, label="体力")
    stamina_max = Field(0x3B04, float, label="体力上限")
    coord = CoordField(0x50, label="坐标")
    moving_speed = Field(0x54, float, label="移动速度")
    cur_item = ByteField(0x46D8)  # 当前使用的物品序号(只读)
    items = ArrayField(0x46E0, 24, ModelField(0, IngameItem))  # 水平武器: 0~6, 药丸: 7, 垂直武器: 8~12 其他物品: 15~23
    rapid_fire = Field(0x4F4C, float, label="快速开火")
    fix_weapon_switch = Field(0x46D0, float)  # 竖行武器切换至横行武器时的修正？
    is_wet = Field(0x2E34, label="是否湿了")


class SavedItem(Model):
    SIZE = 4
    type = WordField(0, label="种类")
    quantity = WordField(2, label="数量/武器弹药")


class SavedItems(Model):
    SIZE = 0x70
    items = ArrayField(0x10, 24, ModelField(0, SavedItem))


class SavedItemManager(Model):
    # 0x3CE4 * *(_DWORD *)(dword_17C345C + 0x20)
    saved_items0 = ArrayField(0x5E8, 8, ModelField(0, SavedItems))
    saved_items = ArrayField(0x20D8, 8, ModelField(0, SavedItems))
    saved_items2 = ArrayField(0x35E4, 8, ModelField(0, SavedItems))


class SavedItems2(Model):
    SIZE = 0x60
    items = ArrayField(0x4, 24, ModelField(0, SavedItem))


class SavedItemManager2(Model):
    SIZE = 40
    saved_items = ArrayField(0, 24, ModelPtrField(0, SavedItems2))


class CharacterStruct(Model):
    chars = ArrayField(0x24, 8, ModelPtrField(0, Character))
    chars_count = Field(0x44, label="角色数量")


class CharacterConfig(Model):
    saved_item_manager = ModelField(0x3F798, SavedItemManager)


class Enemy(Character):
    """敌人"""
    pass


class EnemyItem(Model):
    """敌人"""
    enemy = ModelPtrField(0, Enemy)


class EnemyData(Model):
    count = Field(0x30, label="敌人数量")
    enemy_items = ArrayField(0x3C, 10, ModelPtrField(0, EnemyItem))


class SkillPoints(Model):
    skill_points = Field(0x588, label="技能点数")


class Global(Model):
    character_struct = ModelPtrField(0x013C4428, CharacterStruct)
    character_config = ModelPtrField(0x013C345C, CharacterConfig)
    enemy_data = ModelPtrField(0x13C33CC, EnemyData)
    char_skills = ArrayField((0x013C3414, 1832), 8, ArrayField(0, 3, Field(0)))
    saved_item_manager2 = ModelField(0x1388D58, SavedItemManager2)
