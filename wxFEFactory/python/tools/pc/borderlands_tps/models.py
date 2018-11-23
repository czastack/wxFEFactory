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
    """弹药"""
    regen_rate = FloatField(0x84, label='回复速度')
    status = Field(0x108, label='切换')  # Normal: 5, Infinite: 6


class Weapon(Model):
    display_level = Field(0x1DC, label='显示等级')
    specification_level = Field(0x1E0, label='作用等级')
    actual_level = Field(0xE84, label='武器实际等级')
    item_actual_level = Field(0x8AC, label='物品实际等级')
    calculated_damage = FloatField(0x8E0, label='计算伤害')
    base_damage = FloatField(0x8E4, label='基本伤害')
    calculated_accuracy = FloatField(0x8CC, label='计算偏移率')
    base_accuracy = FloatField(0x8D0, label='基本偏移率')
    calculated_fire_rate = FloatField(0x8B8, label='计算射击延迟')
    base_fire_rate = FloatField(0x8BC, label='基本射击延迟')
    calculated_projectile_speed = FloatField(0xD74, label='计算子弹速')
    base_projectile_speed = FloatField(0xD78, label='基本子弹速')
    calculated_swap_speed = FloatField(0x940, label='计算切换速')
    base_swap_speed = FloatField(0x944, label='基本切换速')
    calculated_reload_speed = FloatField(0xA2C, label='计算换弹速')
    base_reload_speed = FloatField(0xA30, label='基本换弹速')
    calculated_burst_length = Field(0xB38, label='计算爆发长度')  # 0: Auto
    base_burst_length = Field(0xB3C, label='基本爆发长度')
    calculated_projectiles_per_shot = Field(0xDF0, label='计算射击子弹数')
    base_projectiles_per_shot = Field(0xDF4, label='基本射击子弹数')
    calculated_bullets_used = Field(0x9D8, label='计算使用子弹')
    base_bullets_used = Field(0x9DC, label='基本使用子弹')
    calculated_extra_shot_chance = Field(0x404, label='计算额外射击机会')
    base_extra_shot_chance = Field(0x408, label='基本额外射击机会')
    magazine_size = Field(0xA04, label='弹药库容量')
    current_bullets = Field(0xA24, label='当前子弹')
    clip_ammo = Field(0x9D0, label='弹夹子弹')
    item_price = Field(0x1CC, label='物品价格')
    item_quantity = Field(0x1D4, label='物品数量')
    item_state = Field(0x21C, label='物品状态')  # Favorited, Crossed, Equipped, ect

    # type_definition = Field(0xE78, label='类别')
    # balance_definition = Field(0xE7C, label='平衡')
    # manufacturer = Field(0xE80, label='制造商')
    # body = Field(0xE88, label='枪身')
    # grip = Field(0xE8C, label='握把')
    # barrel = Field(0xE90, label='枪管')
    # sight = Field(0xE94, label='准镜')
    # stock = Field(0xE98, label='枪托')
    # elemental = Field(0xE9C, label='元素')
    # accessory1 = Field(0xEA0, label='配件1')
    # accessory2 = Field(0xEA4, label='配件2')
    # material = Field(0xEA8, label='材料')

    def set_level(self, level):
        """设置等级"""
        self.display_level = self.specification_level = level
        if self.actual_level:
            self.actual_level = level
        elif self.item_actual_level:
            self.item_actual_level = level


class VehicleManager(Model):
    boost = ModelPtrField((0x38C, 0x188), Value, label='推进剂')
    health = ModelPtrField(0x394, Value, label='血量')
    scale = FloatField(0x78, label='缩放')
    coord = CoordField(0x60, label='坐标')


class ShieldHealth(Value):
    """护甲和生命"""
    regen_rate = FloatField(0x98, label='回复速度')
    status = Field(0x108, label='切换')  # Normal: 5, God: 6


class Experience(Value):
    """经验值"""
    multiplier = FloatField(0x144, label='经验倍数')


class Character(Model):
    """角色"""
    health = ModelPtrField(0x3B8, ShieldHealth, label='护甲')
    shield = ModelPtrField(0x3C4, ShieldHealth, label='生命')
    oxygen = ModelPtrField(0x3D0, ShieldHealth, label='氧气')
    money = Field(0x2AC, label='钱')
    moon_shards = Field(0x2C0, label='月亮石')
    shift_coins = Field(0x310, label='ShiftCoins')
    experience = ModelPtrField((0xA4, 0xC4C), Experience)
    melee_overide_cooldown = ModelPtrField((0xA4, 0xC64), Value)
    level = Field(0x258, label='等级')
    exp_next_level = Field(0x268, label='到下级经验值')
    skill_points = Field(0x280, label='技能点数')
    head = Field(0x574, label='头像')
    skin = Field(0x584, label='皮肤')


class PlayerConfig(Model):
    """玩家属性"""
    player_model_scale = FloatField(0x78, label='角色模型大小')
    time_scale_multiplier = FloatField(0x328, label='时间流逝倍数')
    gravity = FloatField(0x3A0, label='重力')  # confirm
    player_visibility = ByteField(0xBF, label='角色能见度')
    player_allegiance = Field(0x518, label='角色忠诚')
    move_speed_mult = FloatField(0x320, label='移动速度倍数')
    current_weapon = ModelPtrField(0x480, Weapon)
    hit_ricochet_chance = FloatField(0xA1C, label='击飞')
    miss_ricochet_chance = FloatField(0xA80, label='避开击飞')
    ignore_fatal_damage_chance = FloatField(0xABC, label='免受致命伤')
    bullet_reflect_chance = FloatField(0xA44, label='子弹反弹次数')
    coord = CoordField(0x60, label='坐标')
    move_vector = CoordField(0x104, label='移动向量')

    ffyl_time_mult = FloatField(0xBDC, label='原地复活时间倍数')
    ffyl_Health_mult = FloatField(0xBDC, label='原地复活生命倍数')
    current_vehicle = ModelPtrField(0x450, VehicleManager)
    # wall_detection = ByteField(0xBF, label='墙壁检测')
    # butt_slam_force = FloatField(0x12A4, label='原地复活生命倍数')
    # movement_acceleration_rate = FloatField(0x2D8, label='移动加速度倍数')


class SkillItem(Model):
    SIZE = 0x24
    status = Field(0x0)


class SkillManager(Model):
    ability_status = Field(0x1C, label='主技能状态')
    ability_duration = FloatField((0, 0x74), label='主技能持续时间')
    skills = ArrayField(0x40, 33, ModelField(0, SkillItem))


class AbilityCooldown(Value):
    mult = FloatField(0x70, label='冷却倍数')


class TeamConfig(Model):
    """团队属性"""
    moxxi_drink_duration = FloatField(0x10BC, label='莫西饮酒时长')
    skill_mgr = ModelPtrField((0xC98, 0x58), SkillManager, label='技能')
    ability_cooldown = ModelPtrField(0xC58, AbilityCooldown, label='主技能冷却')
    damage_heals_self = FloatField(0xD54)
    team_ammo_regen = FloatField(0xFE0, label='团队弹药回复')
    explosives_heal_allies = FloatField(0x114C)
    bullets_heal_allies = FloatField(0x1110)
    badass_tokens = FloatField(0x182C, label='坏小子徽章')
    badass_bonuses = ArrayField((0x183C, 0), 14, Field(0))  # 坏小子加成效果
    team_kill_skill_timer_mult = FloatField(0x1A7C)
    damage_taken_mult = FloatField(0x590, label='伤害倍数?')

    shock_time = FloatField(0x4A0, label='闪电时间')
    corrosive_time = FloatField(0x4B4, label='腐蚀时间')
    fire_time = FloatField(0x48C, label='火焰时间')
    frost_time = FloatField(0x4DC, label='冰冻时间')
    melee_damage = FloatField(0x374, label='近战伤害')
    physical_damage = FloatField(0x608, label='物理伤害')
    explosive_damage = FloatField(0x5E0, label='爆炸伤害')
    shock_damage = FloatField(0x5CC, label='闪电伤害')
    corrosive_damage = FloatField(0x5F4, label='腐蚀伤害')
    fire_damage = FloatField(0x5B8, label='火焰伤害')
    frost_damage = FloatField(0x630, label='冰冻伤害')


# class SystemConfig(Model):
#     """系统属性"""
#     time_scale_multiplier = FloatField(0x328, label='时间流逝倍数')
#     gravity = FloatField(0x3A0, label='重力')  # confirm


class PhysicsConfig(Model):
    """物理属性"""
    move_speed = FloatField(0x2A8, label='移动速度')
    jump_height = FloatField(0x2EC, label='跳跃高度')
    friction = FloatField(0x2D8, label='摩擦力')
    viewing_height = FloatField(0x360, label='可视高度')


class PlayerManager(Model):
    player_config = ModelPtrField(0xA4, PlayerConfig)
    physics_config = ModelPtrField(0xDC, PhysicsConfig)
    bank_size = Field((0x230, 0x40), label='仓库空间')
    weapon_deck_size = Field(0x1DC, label='武器装备空间')
    backpack_size = Field(0x1D8, label='背包大小')
    backpack_used_space = Field(0x1F8, label='背包已用空间')


class Manager(Model):
    # system_config = ModelPtrField((0xC, 0xA4), SystemConfig)
    character = ModelPtrField(0x24, Character)
    team_config = ModelPtrField((0x2C, 0xA4), TeamConfig)
    player_mgr = ModelPtrField(0x30, PlayerManager)
    weapon_ammos = ArrayField((0x2C, 0x188), 8, ModelPtrField(0, WeaponAmmo), cachable=True)
    vehicle_mgrs = ArrayField((0x10, 0x378), 4, ModelPtrField(0, VehicleManager), cachable=True)


class Global(Model):
    mgr = ModelPtrField(0x01CFA848, Manager)
