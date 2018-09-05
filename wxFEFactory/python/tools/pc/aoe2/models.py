from lib.hack.models import (
    Model, Field, FloatField, ByteField, WordField, ArrayField, ModelField, ModelPtrField, CoordField, ToggleField
)


class ResourceManager(Model):
    SIZE = 12
    food = FloatField(0, label='食物')
    wood = FloatField(4, label='木材')
    rock = FloatField(8, label='石材')
    gold = FloatField(12, label='黄金')


class PopulationManager(Model):
    SIZE = 0
    current = FloatField(0x2C, label='当前')
    total = FloatField(0x10, label='剩余')
    max = FloatField(0x80, label='上限')


class UnitType(Model):
    hp_max = WordField(0x2A, label="HP上限")
    view = FloatField(0x2C, label="视野")
    collision = FloatField(0x34, label="碰撞")
    move_speed = FloatField(0xC8, label="移动速度")
    search = FloatField(0x104, label="搜索")
    work_efficiency = FloatField(0x108, label="工作效率")
    short_defense = WordField((0x128, 2), label="近战防御")  # 近战防御指针？(+2=近战防御)
    far_defense = WordField((0x128, 6), label="远程防御")  # 近战防御指针？(+6=远程防御 错的)
    atk = WordField((0x130, 6), label="攻击力")  # 攻击力指针？(+6=攻击)
    range_max = FloatField(0x138, label="最大射程")
    damage_radius = FloatField(0x13C, label="攻击范围")
    damage_type = Field(0x140, label="伤害方式")
    atk_spped = FloatField(0x144, label="攻击速度")
    range_min = FloatField(0x15C, label="最小射程")


class Unit(Model):
    SIZE = 0
    type = ModelPtrField(8, UnitType)
    hp = FloatField(0x30, label='HP')
    ptr_unknow1 = Field(0x18, label='不明指针')
    selected = ByteField(0x36, label='选中状态')
    ptr_unknow2 = Field(0x6C, label='不明指针2')


class Global(Model):
    resources = ModelPtrField((0x00295794, 0xFC, 0xA8), ResourceManager)
    population_mgr = ModelPtrField((0x003912A0, 0x424, 0x4C, 0x4, 0xA8), PopulationManager)
    select_units = ArrayField(0x002B71A0, 30, ModelPtrField(0, Unit))
