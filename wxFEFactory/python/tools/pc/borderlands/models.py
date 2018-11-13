from lib.hack.models import (
    Model, Field, ByteField, WordField, FloatField, ArrayField, ModelField, ModelPtrField, CoordField
)


class Value(Model):
    """数值"""
    value = FloatField(0x68, label='数量')
    scaled_maximum = FloatField(0x54, label='缩放最大值')
    base_maximum = FloatField(0x58, label='最大值')

    def value_max(self):
        self.set_with('value', 'scaled_maximum')


class WeaponAmmo(Value):
    """弹药"""
    SIZE = 4
    regen_rate = FloatField(0x80, label='回复速度')


class Weapon(Model):
    magazine_size = FloatField(0x3B0, label='弹药库容量')
    current_ammo = FloatField(0x3CC, label='当前弹药')
    total_ammo = FloatField(0x390, label='总弹药数')
    damage = FloatField(0x2BC, label='伤害')
    base_accuracy = FloatField(0x2A8, label='基本偏移率')
    calculated_accuracy = FloatField(0x2AC, label='计算偏移率')
    base_fire_rate = FloatField(0x294, label='基本射击延迟')
    calculated_fire_rate = FloatField(0x298, label='射击延迟')


class WeaponProf(Model):
    SIZE = 0x2C
    level = Field(0, label='等级')
    exp = Field(4, label='经验')


class AnotherManager(Model):
    weapon_profs = ArrayField((0xF0, 0x508), 7, ModelField(0, WeaponProf))
    move_speed = FloatField((0x70, 0x2CC), label='移动速度')


class ShieldHealth(Value):
    """护甲和生命"""
    regen_rate = FloatField(0x94, label='回复速度')
    status = Field(0x100, label='切换')  # Normal: 5, God: 6


class Character(Model):
    experience = ModelPtrField(0x1E4, Value, label='经验')
    ability_cooldown = ModelPtrField(0x1E8, Value, label='技能冷却')
    health = ModelPtrField(0x1F0, ShieldHealth, label='生命')
    shield = ModelPtrField(0x1F4, ShieldHealth, label='护盾')
    weapon_ammos = ArrayField(0x1F8, 8, ModelPtrField(0, WeaponAmmo), cachable=True)


class CharacterConfig(Model):
    level = Field(0x284, label='等级')
    exp_next_level = Field(0x288, label='下级所需经验')
    skill_points = Field(0x29C, label='技能点数')
    money = Field(0x2A4, label='金钱')


class PlayerManager(Model):
    character_config = ModelPtrField((0xA8, 0x14), CharacterConfig)
    character = ModelPtrField(0x2AC, Character)


class Manager(Model):
    play_mgr = ModelPtrField(0x24, PlayerManager)


class Global(Model):
    mgr = ModelPtrField(0x01BF3C90, Manager)
    another_mgr = ModelPtrField((0x01C2AF2C, 8), AnotherManager)
    current_weapon_ammo = ModelPtrField((0x01BF3CCC, 0, 0x28, 0x38C), Value, label='当前武器子弹总数')
