from lib.hack.models import (
    Model, Field, ByteField, WordField, FloatField, ArrayField, ModelField, ModelPtrField, CoordField, ToggleField
)


class Progress(Model):
    """游戏统计数据"""
    play_count = Field(0x4, label="Total number of games")
    slot_2 = Field(0x8, label="Slot 2")
    finish_count = Field(0xC, label="Total number of games finished")
    most_gold_obtained_at_once = Field(0x10, label="Most Gold obtained at once")
    most_cells_obtained_at_once = Field(0x14, label="Most Cells obtained at once")
    teleportations_used = Field(0x18, label="Teleportations used")
    total_gold_acquired = Field(0x1C, label="Total gold acquired")
    total_gold_spent = Field(0x20, label="Total gold spent")
    cells_acquired = Field(0x24, label="Cells acquired")
    cells_spent = Field(0x28, label="Cells spent")
    health_flasks_used = Field(0x2C, label="Health flasks used")
    curses_survived = Field(0x30, label="Curses survived")
    slot_13 = Field(0x34, label="Slot 13")
    slot_14 = Field(0x38, label="Slot 14")
    weapon_blueprints = Field(0x3C, label="Weapon blueprints")
    skill_blueprints = Field(0x40, label="Skill blueprints")
    normal_chests_opened = Field(0x44, label="Normal chests opened")
    cursed_chests_opened = Field(0x48, label="Cursed chests opened")
    secret_portals_opened = Field(0x4C, label="Secret portals opened")
    challenges_completed = Field(0x50, label="Challenges completed")
    challenges_failed = Field(0x54, label="Challenges failed")
    slot_22 = Field(0x58, label="Slot 22")
    untouchable_doors_completed = Field(0x5C, label="Untouchable doors completed")
    untouchable_doors_failed = Field(0x60, label="Untouchable doors failed")
    timed_door_challenges_completed = Field(0x64, label="Timed door challenges completed")
    timed_door_challenges_failed = Field(0x68, label="Timed door challenges failed")
    slot_27 = Field(0x6C, label="Slot 27")
    deaths_by_trap = Field(0x70, label="Deaths by trap")
    killed_in_a_challenge_room = Field(0x74, label="Killed in a Challenge room")
    deaths_by_falling = Field(0x78, label="Deaths by falling")
    deaths_by_infection = Field(0x7C, label="Deaths by infection")
    deaths_by_suicide = Field(0x80, label="Deaths by suicide")
    cells_lost = Field(0x84, label="Cells lost")


class Game(Model):
    """运行时游戏数据"""
    time = Field(0x28, type=float, size=8, label="时 间")
    gold = Field(0x34, label="金币")
    nohit_kill = Field(0x50, label="无伤击杀数")
    nohit_kill_max = Field(0x54, label="最大无伤击杀数")

    tactics_upgrades = Field((0x20, 4), label="战术升级")
    brutality_upgrades = Field((0x20, 8), label="暴虐升级")
    survival_upgrades = Field((0x20, 0xC), label="生存升级")


class Weapon(Model):
    """武器"""
    level = Field(0xC, label="等级")
    reforged_times = Field((0x10, 4), label="锻造次数")  # (level - 1 = 升级到S级)
    ammo = Field(0x18, label="弹药")


class Skill(Model):
    """技能"""
    cooldown = Field((0x10, 0x78), float, 8, label="冷却")
    cooldown_max = Field((0x10, 0x80), float, 8, label="最大冷却")


class Player(Model):
    """玩家数据"""
    hp = Field(0xE8, label='HP')
    hpmax = Field(0xEC, label='HP上限')
    purple_tier = ByteField(0x110, label='战术等级')
    red_tier = ByteField(0x114, label='暴虐等级')
    green_tier = ByteField(0x118, label='生存等级')
    cell = Field(0x33C, label='细胞')
    coord_x = Field(0x4C, label='X坐标')
    coord_y = Field(0x50, label='Y坐标')
    curse_kill = Field(0x2C4, label='诅咒剩余击杀')
    health_flask = Field(0x310, label='药瓶')
    forgotten_sepulcher_darkness = FloatField(0x344, label='遗忘墓穴黑暗')
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
    weapon_slots = ArrayField((0x300, 0x4, 0x330, 0x4, 0x8, 0x10), 50, ModelPtrField(0, Weapon))
    primary_weapon = ModelPtrField((0x300, 8), Weapon)
    secondary_weapon = ModelPtrField((0x304, 8), Weapon)
    left_skill = ModelPtrField((0x320, 8, 0x10), Skill)
    right_skill = ModelPtrField((0x320, 8, 0x14), Skill)

    form_fields = (
        'hp', 'hpmax', 'purple_tier', 'red_tier', 'green_tier', 'cell', 'coord_x', 'coord_y',
        'curse_kill', 'health_flask', 'forgotten_sepulcher_darkness',
    )


class HlHandle(Model):
    player = ModelPtrField((0x18, 0x64), Player)
    progress = ModelPtrField((0x18, 0x58, 0x28), Progress)
    game = ModelPtrField((0x18, 0x5C), Game)
