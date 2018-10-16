from lib.hack.models import (
    Model, Field, ByteField, WordField, FloatField, ArrayField, ModelField, ModelPtrField, CoordField
)


class Value(Model):
    """数值"""
    value = FloatField(0x6C, label='数量')
    scaled_maximum = FloatField(0x58, label='缩放最大值')
    base_maximum = FloatField(0x5C, label='最大值')

    def value_max(self):
        self.set_with('value', 'scaled_maximum')


class WeaponAmmo(Value):
    """武器管理器"""
    regen_rate = FloatField(0x84, label='回复速度')


class Weapon(Model):
    display_level = Field(0x1E0, label='显示等级')
    specification_level = Field(0x1E4, label='作用等级')
    actual_level = Field(0xE3C, label='武器实际等级')
    item_actual_level = Field(0x8B4, label='物品实际等级')
    calculated_damage = FloatField(0x8E8, label='计算伤害')
    base_damage = FloatField(0x8EC, label='基本伤害')
    calculated_accuracy = FloatField(0x8D4, label='计算精准率')
    base_accuracy = FloatField(0x8D8, label='基本精准率')
    calculated_fire_rate = FloatField(0x8C0, label='计算开火率')
    base_fire_rate = FloatField(0x8C4, label='基本开火率')
    calculated_projectile_speed = FloatField(0xEB4, label='计算子弹速')
    base_projectile_speed = FloatField(0xEB8, label='基本子弹速')
    calculated_reload_speed = FloatField(0xA30, label='计算换弹速')
    base_reload_speed = FloatField(0xA34, label='基本换弹速')
    calculated_burst_length = Field(0xAFC, label='计算爆发长度')  # 0: Auto
    base_burst_length = Field(0xB00, label='基本爆发长度')
    calculated_projectiles_per_shot = Field(0xDB8, label='计算射击子弹数')
    base_projectiles_per_shot = Field(0xDBC, label='基本射击子弹数')
    calculated_bullets_used = Field(0x9DC, label='计算使用子弹')
    base_bullets_used = Field(0x9E0, label='基本使用子弹')
    calculated_extra_shot_chance = Field(0xD28, label='计算额外射击机会')
    base_extra_shot_chance = Field(0xD2C, label='基本额外射击机会')
    magazine_size = Field(0xA0C, label='弹药库容量')
    current_bullets = Field(0xA28, label='当前子弹')
    clip_ammo = Field(0x9D4, label='弹夹子弹')
    item_price = Field(0x1D0, label='物品价格')
    item_quantity = Field(0x1D8, label='物品数量')
    item_state = Field(0x224, label='物品状态')  # Favorited, Crossed, Equipped, ect

    def set_level(self, level):
        """设置等级"""
        self.display_level = self.specification_level = level
        if self.actual_level:
            self.actual_level = level
        elif self.item_actual_level:
            self.item_actual_level = level


class VehicleManager(Model):
    boost = ModelPtrField((0x37C, 0x188), Value, label='推进剂')
    health = ModelPtrField((0x37C, 0x18C), Value, label='血量')


class ShieldHealth(Value):
    """护甲和生命"""
    regen_rate = FloatField(0x98, label='回复速度')
    status = Field(0x104, label='切换')  # Normal: 5, God: 6


class Experience(Value):
    """经验值"""
    multiplier = FloatField(0x118, label='经验倍数')


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
    level = Field(0x258, label='等级')
    exp_next_level = Field(0x25C, label='到下级经验值')
    skill_points = Field(0x274, label='技能点数')
    head = Field(0x55C, label='头像')
    skin = Field(0x56C, label='皮肤')


class SecondWind(Model):
    """原地复活"""
    multiplier = FloatField(0x650, label='生命倍数')
    fight_time_multiplier = FloatField(0x434, label='时间倍数')


class PlayerConfig(Model):
    """玩家属性"""
    player_model_scale = FloatField(0x78, label='角色模型大小')
    player_visibility = ByteField(0xBF, label='角色能见度')
    move_speed_mult = FloatField(0x310, label='移动速度倍数')
    current_weapon = ModelPtrField(0x470, Weapon)
    second_wind = ModelPtrField((0x6A4, 0x68), SecondWind)
    hit_ricochet_chance = FloatField(0x948, label='击飞')
    miss_ricochet_chance = FloatField(0x9AC, label='避开击飞')
    ignore_fatal_damage_chance = FloatField(0x9E8, label='免受致命伤')
    coord = CoordField(0x60, label='坐标')
    move_vector = CoordField(0x104, label='坐标')


class SkillItem(Model):
    SIZE = 0x24
    status = Field(0x0)


class SkillManager(Model):
    main_skill = Field(0x1C, label='主技能状态')
    main_skill_duration = FloatField((0, 0x74), label='主技能持续时间')
    skills = ArrayField(0x40, 33, ModelField(0, SkillItem))


class TeamConfig(Model):
    """团队属性"""
    skill_mgr = ModelPtrField((0xB74, 0x58), SkillManager, label='技能')
    main_skill_cooldown_timer = FloatField((0xB64, 0x6C), label='主技能冷却时间')
    main_skill_cooldown_mult = FloatField((0xB64, 0x60), label='主技能冷却倍数')
    damage_heals_self = FloatField(0xBF4)
    team_ammo_regen = FloatField(0xE58, label='团队弹药回复')
    explosives_heal_allies = FloatField(0xF90)
    bullets_heal_allies = FloatField(0xF54)
    badass_tokens = FloatField(0x1664, label='坏小子徽章')
    team_kill_skill_timer_mult = FloatField(0x18A4)

    mullets_resistance = FloatField(0x4A0, label='普通抗性')
    mhysical_resistance = FloatField(0x580, label='物理抗性')
    melee_resistance = FloatField(0x4C8, label='近战抗性')
    mxplosive_resistance = FloatField(0x5A8, label='爆炸抗性')
    mhock_resistance = FloatField(0x5D0, label='闪电抗性')
    morrosive_resistance = FloatField(0x5F8, label='腐蚀抗性')
    mire_resistance = FloatField(0x620, label='火焰抗性')
    mlag_resistance = FloatField(0x648, label='紫渣抗性')
    elemental_resistance = FloatField(0x4B4, label='元素抗性')
    erenades_resistance = FloatField(0x4DC, label='手榴弹/枪桶抗性')
    rockets_resistance = FloatField(0x4F0, label='火箭炮抗性')
    chock_time = FloatField(0x464, label='闪电时间')
    corrosive_time = FloatField(0x478, label='腐蚀时间')
    cire_time = FloatField(0x450, label='火焰时间')
    melee_damage = FloatField(0x374, label='近战伤害')
    physical_damage = FloatField(0x57C, label='物理伤害')
    explosive_damage = FloatField(0x554, label='爆炸伤害')
    shock_damage = FloatField(0x540, label='闪电伤害')
    corrosive_damage = FloatField(0x568, label='腐蚀伤害')
    fire_damage = FloatField(0x52C, label='火焰伤害')
    slag_damage = FloatField(0x590, label='紫渣伤害')


class SystemConfig(Model):
    """系统属性"""
    time_scale_multiplier = FloatField(0x328, label='时间流逝倍数')
    gravity = FloatField(0x3A0, label='重力')


class PhysicsConfig(Model):
    """物理属性"""
    move_speed = FloatField(0x2A8, label='移动速度')
    jump_height = FloatField(0x2EC, label='跳跃高度')
    friction = FloatField(0x2D8, label='摩擦力')
    viewing_height = FloatField(0x350, label='可视高度')


class PlayerManager(Model):
    player_config = ModelPtrField(0xA4, PlayerConfig)
    physics_config = ModelPtrField(0xDC, PhysicsConfig)
    bank_size = Field((0x210, 0x40), label='仓库空间')
    weapon_deck_size = Field(0x1BC, label='武器装备空间')
    backpack_size = Field(0x1B8, label='背包大小')
    backpack_used_space = Field(0x1D8, label='背包已用空间')


class Manager(Model):
    system_config = ModelPtrField((0xC, 0xA4), SystemConfig)
    character = ModelPtrField(0x24, Character)
    team_config = ModelPtrField((0x2C, 0xA4), TeamConfig)
    player_mgr = ModelPtrField(0x30, PlayerManager)
    weapon_ammos = ArrayField((0x2C, 0x188), 7, ModelPtrField(0, WeaponAmmo), cachable=True)
    vehicle_mgrs = ArrayField((0x10, 0x358), 2, ModelPtrField(0, VehicleManager), cachable=True)


# class PlayerManager(Model):
#     current_weapon = ModelPtrField(0x470, Weapon)


class Global(Model):
    mgr = ModelPtrField(0x01EEE798, Manager)
    # player_mgr = ModelPtrField(0x01EEF510, PlayerManager)
