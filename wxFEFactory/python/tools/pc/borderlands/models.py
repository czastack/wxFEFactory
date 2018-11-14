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
    real_magazine_size = FloatField(0x3B0, label='计算弹夹容量')
    base_magazine_size = FloatField(0x3B4, label='基本弹夹容量')
    current_ammo = FloatField(0x3CC, label='当前弹药')
    total_ammo = FloatField(0x390, label='总弹药数')
    # all_ammo = ModelPtrField(0x3BC, Value, label='包含弹夹的总弹药数')
    calculated_damage = FloatField(0x2BC, label='计算伤害')
    base_damage = FloatField(0x2C0, label='基本伤害')
    calculated_accuracy = FloatField(0x2A8, label='计算偏移率')
    base_accuracy = FloatField(0x2AC, label='基本偏移率')
    calculated_fire_rate = FloatField(0x294, label='计算射击延迟')
    base_fire_rate = FloatField(0x298, label='基本射击延迟')
    calculated_bullets_used = Field(0x398, label='计算使用子弹')
    base_bullets_used = Field(0x39C, label='基本使用子弹')
    item_price = Field(0x21C, label='物品价格')


class WeaponProf(Model):
    SIZE = 0x2C
    level = Field(0, label='等级')
    exp = Field(4, label='经验')


class MovementManager(Model):
    base_move_speed = FloatField(0x2D0, label='基本移动速度')
    current_move_speed = FloatField(0x2CC, label='当前移动速度')
    current_jump_height = FloatField(0x300, label='当前跳跃高度')
    base_jump_height = FloatField(0x304, label='基本跳跃高度')
    rriction = FloatField(0x2FC, label='摩擦力')
    coord = CoordField(0x5C, label='坐标')
    move_vector = CoordField(0x124, label='移动向量')


class AnotherManager(Model):
    weapon_profs = ArrayField((0xF0, 0x508), 7, ModelField(0, WeaponProf))
    movement_mgr = ModelPtrField(0x70, MovementManager)


class PhysicsManager(Model):
    movement_mgr = ModelPtrField((0, 0x28, 0x5A0), MovementManager)
    view_height = FloatField((0x10, 0x28, 0x360), label='可视高度')


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


class Vehicle(Model):
    boost = ModelPtrField((0x390, 0x1DC), Value, label='推进剂')
    health = ModelPtrField(0x398, Value, label='血量')


# class VehicleManager(Model):
#     vehicle_1 = ModelPtrField(0, Vehicle)
#     vehicle_2 = ModelPtrField(0x18, Vehicle)


class PlayerManager(Model):
    character_config = ModelPtrField((0xA8, 0x14), CharacterConfig)
    character = ModelPtrField(0x2AC, Character)


class Manager(Model):
    play_mgr = ModelPtrField(0x24, PlayerManager)


class Global(Model):
    mgr = ModelPtrField(0x01BF3C90, Manager)
    another_mgr = ModelPtrField((0x01C2AF2C, 8), AnotherManager)
    physics_mgr = ModelPtrField(0x01BF3C9C, PhysicsManager)
    vehicle_mgr = ModelPtrField((0x01BF0164, 0), Vehicle)
    current_weapon_ammo = ModelPtrField((0x01BF3CCC, 0, 0x28, 0x38C), Value, label='当前武器子弹总数')
