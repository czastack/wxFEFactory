from lib.hack.models import Model, Field, ByteField, WordField, FloatField, ArrayField, ModelField, ModelPtrField


class WeaponManager(Model):
    """武器管理器"""
    ammo = FloatField(0x6C, label='弹药')


class ShieldHealth(Model):
    """护甲和生命"""
    value = FloatField(0x6C, label='数量')
    scaled_maximum = FloatField(0x58, label='缩放最大值')
    base_maximum = FloatField(0x5C, label='最大值')
    regen_rate = FloatField(0x98, label='回复速度')
    status = Field(0x104, label='切换')  # Normal: 5, God: 6


class Experience(Model):
    """经验值"""
    value = FloatField(0x6C, label='数量')
    scaled_maximum = FloatField(0x58, label='缩放最大值')
    base_maximum = FloatField(0x5C, label='最大值')
    multiplier = FloatField(0x118, label='经验倍数')
    to_next_level = Field(0x25C, label='到下级经验值')


class Character(Model):
    """角色"""
    health = ModelPtrField(0x3AC, ShieldHealth, label='护甲')
    shield = ModelPtrField(0x3B8, ShieldHealth, label='生命')
    money = Field(0x2A0, label='钱')
    eridium = Field(0x2B4, label='铱元素块')
    seraph_crystals = Field(0x2C8, label='炽天使水晶')
    torgue_tokens = Field(0x2F0, label='托格币')
    experience = ModelPtrField((0xA4, 0xB58), Experience)
    melee_overide_cooldown = FloatField((0xA4, 0xB70, 0x6C))
    head = Field(0x55C, label='头像')
    skin = Field(0x56C, label='皮肤')


class SecondWind(Model):
    """恢复元气"""
    multiplier = FloatField(0x650, label='倍数')
    fight_time_multiplier = FloatField(0x434, label='倍数')


class PlayerConfig(Model):
    """玩家属性"""
    player_model_scale = FloatField(0x78, label='角色模型大小')
    player_visibility = FloatField(0xBF, label='角色能见度')
    second_wind = ModelPtrField((0x6A4, 0x68), SecondWind)
    hit_ricochet_chance = FloatField(0x948, label='击飞')
    miss_ricochet_chance = FloatField(0x9AC, label='避开击飞')
    ignore_fatal_damage_chance = FloatField(0x9E8, label='免受致命伤')


class TeamConfig(Model):
    """团队属性"""
    team_ammo_regen = FloatField(0xE58, label='团队弹药回复')
    team_kill_skill_timer_mult = FloatField(0x18A4)
    explosives_heal_allies = FloatField(0xF90)
    bullets_heal_allies = FloatField(0xF54)
    damage_heals_self = FloatField(0xBF4)


class Manager(Model):
    time_scale_multiplier = FloatField((0xC, 0xA4, 0x328), label='时间流逝倍数')
    character = ModelPtrField(0x24, Character)
    team_config = ModelPtrField((0x2C, 0xA4), TeamConfig)
    player_config = ModelPtrField((0x30, 0xA4), PlayerConfig)
    weapon_mgrs = ArrayField((0x2C, 0x188), 7, ModelPtrField(0, WeaponManager), cachable=True)


class Global(Model):
    mgr = ModelPtrField(0x01EEE798, Manager)
