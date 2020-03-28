from lib.hack.models import (
    Model, Field, ByteField, WordField, FloatField, ArrayField, ModelField, ModelPtrField, CoordField, ToggleField
)


class Progress(Model):
    """游戏统计数据"""
    play_count = Field(0x4, label="游戏局数")
    slot_2 = Field(0x8, label="Slot 2")
    finish_count = Field(0xC, label="通关数")
    most_gold_obtained_at_once = Field(0x10, label="单局最多金币获得数")
    most_cells_obtained_at_once = Field(0x14, label="单局最多细胞获得数")
    teleportations_used = Field(0x18, label="传送次数")
    total_gold_acquired = Field(0x1C, label="金币获得数")
    total_gold_spent = Field(0x20, label="金币花费数")
    cells_acquired = Field(0x24, label="细胞获得数")
    cells_spent = Field(0x28, label="细胞花费数")
    health_flasks_used = Field(0x2C, label="药瓶使用数")
    curses_survived = Field(0x30, label="诅咒消除数")
    slot_13 = Field(0x34, label="Slot 13")
    slot_14 = Field(0x38, label="Slot 14")
    weapon_blueprints = Field(0x3C, label="武器图纸数")
    skill_blueprints = Field(0x40, label="技能图纸数")
    mutation_blueprints = Field(0x44, label="变异图纸数")
    normal_chests_opened = Field(0x48, label="普通宝箱开启数")
    cursed_chests_opened = Field(0x4C, label="诅咒宝箱开启数")
    secret_portals_opened = Field(0x50, label="秘密区域开启数")
    challenges_completed = Field(0x54, label="挑战完成数")
    challenges_failed = Field(0x58, label="挑战失败数")
    slot_22 = Field(0x5C, label="Slot 22")
    untouchable_doors_completed = Field(0x60, label="无伤击杀门完成数")
    untouchable_doors_failed = Field(0x64, label="无伤击杀门失败数")
    timed_door_challenges_completed = Field(0x68, label="限时门通过数")
    timed_door_challenges_failed = Field(0x6C, label="限时门失败数")
    slot_27 = Field(0x70, label="Slot 27")
    deaths_by_trap = Field(0x74, label="陷阱死亡数")
    killed_in_a_challenge_room = Field(0x78, label="挑战门死亡数")
    deaths_by_falling = Field(0x7C, label="跌落死亡数")
    deaths_by_infection = Field(0x80, label="反弹死亡数")
    deaths_by_suicide = Field(0x84, label="自杀死亡数")
    cells_lost = Field(0x88, label="细胞丢失数")


class Upgrade(object):
    """卷轴升级"""
    tactics = Field(0x4, label="战术升级")
    brutality = Field(0x8, label="暴虐升级")
    survival = Field(0xC, label="生存升级")


class RunStats(Model):
    """运行时游戏数据"""
    time = Field(0x20, type=float, size=8, label="时间")
    gold = Field(0x2C, label="金币")
    nohit_kill = Field(0x48, label="无伤击杀数")
    nohit_kill_max = Field(0x4C, label="最大无伤击杀数")

    tactics_upgrades = Field((0x18, 0x4), label="战术升级")
    brutality_upgrades = Field((0x18, 0x8), label="暴虐升级")
    survival_upgrades = Field((0x18, 0xC), label="生存升级")



class InventoryItem(Model):
    """物品"""
    level = Field(0xC, label="等级")
    reforged_times = Field((0x10, 4), label="锻造次数")  # (level - 1 = 升级到S级)


class Weapon(InventoryItem):
    """武器"""
    ammo = Field(0x18, label="弹药")


# class WeaponInfo(Model):
#     """武器"""
#     weapon_data = ModelPtrField(8, Weapon)  # 武器数据
#     continuous_count = Field(0x20, label="连续挥动次数")


class Skill(Model):
    """技能"""
    cooldown = Field((0x10, 0x78), float, 8, label="冷却")
    cooldown_max = Field((0x10, 0x80), float, 8, label="最大冷却")


class Player(Model):
    """玩家数据"""
    hp = Field(0xE8, label='HP')
    hpmax = Field(0xEC, label='HP上限')
    tactics = ByteField(0x110, label='战术等级')
    brutality = ByteField(0x114, label='暴虐等级')
    survival = ByteField(0x118, label='生存等级')
    cell = Field(0x340, label='细胞')
    coord_x = Field(0x4C, label='X坐标')
    coord_y = Field(0x50, label='Y坐标')
    curse_kill = Field(0x2C4, label='诅咒剩余击杀')
    reset_mutations = Field(0x2C8, label='重置变异')
    max_height = Field(0x2D0, label='最大高度')
    health_flask = Field(0x310, label='药瓶')
    forgotten_sepulcher_darkness = FloatField(0x34C, label='遗忘墓穴黑暗')
    # 计时器
    # Roll 4
    # Stunned 9
    # Freeze 23
    # Force Field 27
    # Liposuction 37
    # Electric? 41
    # Invisibility 42
    # Dashing 62
    timer = ArrayField((0x140, 8), 100, Field(0, float, 8))
    # 武器槽
    inventory = ArrayField((0x300, 0x4, 0x334, 0x4, 0x8, 0x10), 50, ModelPtrField(0, InventoryItem))
    primary_weapon = ModelPtrField((0x300, 8), Weapon)
    # primary_weapon_info = ModelPtrField(0x300, WeaponInfo)
    primary_weapon = ModelPtrField((0x300, 8), Weapon)
    secondary_weapon = ModelPtrField((0x304, 8), Weapon)
    left_skill = ModelPtrField((0x320, 8, 0x10), Skill)
    right_skill = ModelPtrField((0x320, 8, 0x14), Skill)

    form_fields = (
        'hp', 'hpmax', 'tactics', 'brutality', 'survival', 'cell', 'coord_x', 'coord_y',
        'curse_kill', 'reset_mutations', 'max_height', 'health_flask', 'forgotten_sepulcher_darkness',
    )


class Manager(Model):
    player = ModelPtrField(0x64, Player)
    progress = ModelPtrField((0x58, 0x28), Progress)
    runstats = ModelPtrField(0x5C, RunStats)
