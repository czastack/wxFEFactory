from lib.hack.models import Model, Field, ByteField, ArrayField, ModelField, ModelPtrField, ToggleField, ToggleFields
from ..models import ItemSlot, BaseGlobal


class Person(Model):
    SIZE = 0xA8
    prof = Field(0x44)
    level = ByteField(0x6A)
    level_limit = ByteField(0x63)
    exp = ByteField(0x6B)
    no = ByteField(0x41)  # 头像、身份？
    moved = ByteField(0x9C)
    posx = ByteField(0x6E)
    posy = ByteField(0x6F)
    hpmax = ByteField(0x50)
    hp = ByteField(0x6C)
    power = ByteField(0x51)
    magic = ByteField(0x52)
    skill = ByteField(0x53)
    speed = ByteField(0x54)
    lucky = ByteField(0x55)
    defense = ByteField(0x56)
    magicdef = ByteField(0x57)
    move_add = ByteField(0x6D)
    items = ArrayField(0x70, 5, ModelField(0, ItemSlot))
    proficiency = ArrayField(0x84, 6, ByteField(0))  # 武器熟练度(剑, 枪, 斧, 弓, 书, 杖) (00: -, 01: E, 1F: D, 4C: C, 88: B)


class Config(Model):
    money = Field(0x0190)
    difficulty = ByteField(0x01A5)
    character_gender = False


class ItemInfo(Model):
    SIZE = 0x3C
    name_ptr = Field(0x04)  # 名称指针
    desc_ptr = Field(0x08)  # 介绍文本指针
    icon = ByteField(0x0C)  # 图标序号
    type = ByteField(0x10)  # 类型 0: 剑, 枪, 斧, 弓, 魔, 杖, 龙石, 弩车
    level = ByteField(0x12)  # 要求熟练度 00: -, 01: E, 1F: D, 4C: C, 88: B
    power = ByteField(0x15)  # 威力
    hit = ByteField(0x16)  # 命中
    kill = ByteField(0x17)  # 必杀
    weight = ByteField(0x18)  # 重量
    range_min = ByteField(0x19)  # 最小射程
    range_max = ByteField(0x1A)  # 最大射程
    move_add = ByteField(0x1B)  # 属性增加效果
    hp_add = ByteField(0x1C)
    power_add = ByteField(0x1D)
    magic_add = ByteField(0x1E)
    skill_add = ByteField(0x1F)
    speed_add = ByteField(0x20)
    lucky_add = ByteField(0x21)
    defense_add = ByteField(0x22)
    magicdef_add = ByteField(0x23)
    attr1 = ByteField(0x24)
    attr2 = ByteField(0x25)
    attr3 = ByteField(0x26)
    attr4 = ByteField(0x27)
    attr5 = ByteField(0x28)
    attr6 = ByteField(0x29)
    attr7 = ByteField(0x2A)
    attr8 = ByteField(0x2B)
    attr9 = ByteField(0x2C)
    attr10 = ByteField(0x2D)
    attr11 = ByteField(0x2E)
    attr12 = ByteField(0x2F)


COMMON_FIELDS = {
    'control_enemy': ToggleField(enable=0xE1500000, disable=0xE1520001, label="可以操作敌人"),
    'inf_move': ToggleField(enable=0xE1500000, disable=0xE3100001, label="无限行动"),
    'exchange_enemy': ToggleField(enable=0xE1500000, disable=0xE1510002, label="可以和敌人换物品"),
    'anyone_bag': ToggleFields(
        ToggleField(enable=0xE1A00000, disable=0xA000004),
        ToggleField(enable=0xE1A00000, disable=0xA000004),
        label="任何人可使用行囊"),
    'quick_info': ToggleField(enable=0xE35000FF, disable=0xE3100001, label="快速显示信息"),
    'custom_exp': ToggleField(enable=0xE3A0003C, disable=0xC3A00064, label="自定义获取经验值"),

    'growth_rate_add': ToggleField(enable=0xEA000000A3A060FFE35600FFE2866064,
        disable=0xA3A060FFE35600FF, size=16, label="成长率XX%加算(最大255%)"),

    'add_all_attr': ToggleField(enable=0xE3A00001, disable=0xEB01A8F8, label="成长率1%以上升级后能力值必定+1"),

    'break_keep': ToggleField(enable=0xE12FFF1E, disable=0xE92D4010, label="中断存档不消失"),
    'item_keep': ToggleField(enable=0xE1A00000, disable=0xEB08F683, label="道具使用不减"),
    'first_turn_withdraw': ToggleField(enable=0xE3500001, disable=0xE3500003, label="第一回合可撤退"),
    'no_battle_3d': ToggleField(enable=0xEA00003F, disable=0xDA00003F, label="3D迷宫接触敌人不战斗"),
    'well_no_driy': ToggleFields(
        ToggleField(enable=0xEA000000, disable=0xA3A00001),
        ToggleField(enable=0xEA000000, disable=0xA3A00001),
        label="圣井不会干涸"),
}


VERSION_SPECIFIC = {
    '1.0': {
        'control_enemy': 0x002F9584,
        'inf_move': 0x002F9590,
        'exchange_enemy': 0x00333C4C,
        'anyone_bag': (0x0031C5B0, 0x0031C9D8),
        'quick_info': 0x0039BF2C,
        'custom_exp': 0x004509EC,
        'growth_rate_add': 0x00356A58,
        'add_all_attr': 0x00356B84,
        'break_keep': 0x003BA3F0,
        'item_keep': 0x001D7024,
        'first_turn_withdraw': 0x0044D968,
        'no_battle_3d': 0x0017ED4C,
        'well_no_driy': (0x0042CE6C, 0x0042CC80),
    },
    '1.1': {
        'control_enemy': 0x002FA18C,
        'inf_move': 0x002FA198,
        'exchange_enemy': 0x00334948,
        'anyone_bag': (0x0031D2AC, 0x0031D6D4),
        'quick_info': 0x0039C93C,
        'custom_exp': 0x0045127C,
        'growth_rate_add': 0x00357468,
        'add_all_attr': 0x00357594,
        'break_keep': 0x003BAE00,
        'item_keep': 0x001D7C30,
        'first_turn_withdraw': 0x0044E1F8,
        'no_battle_3d': 0x0017FE6C,
        'well_no_driy': (0x0042D6FC, 0x0042D510),
    }
}


def bind_fields(data, version):
    source = VERSION_SPECIFIC[version]
    for key, field in COMMON_FIELDS.items():
        data[key] = field.replace(offset=source[key])
    return data


class BaseGlobalEchos(BaseGlobal):
    pass


class Global_1_0(BaseGlobalEchos):
    bind_fields(locals(), '1.0')


class Global_1_1(BaseGlobalEchos):
    bind_fields(locals(), '1.1')


SPECIFIC_GLOBALS = {
    '1.0': Global_1_0,
    '1.1': Global_1_1,
}
