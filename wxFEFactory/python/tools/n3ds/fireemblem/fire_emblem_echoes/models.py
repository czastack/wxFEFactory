import struct
from lib.hack.models import Model, Field, ByteField, ArrayField, ModelField, ToggleField, ToggleFields
from lib.hack.utils import pack_dwords
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
    'control_enemy': (
        ToggleField(enable=0xE1500000, disable=0xE1520001, label="可以操作敌人"),
        0x002F9584,  # 1.0
        0x002FA18C,  # 1.1
    ),
    'inf_move': (
        ToggleField(enable=0xE1500000, disable=0xE3100001, label="无限行动"),
        0x002F9590,
        0x002FA198,
    ),
    'exchange_enemy': (
        ToggleField(enable=0xE1500000, disable=0xE1510002, label="可以和敌人换物品"),
        0x00333C4C,
        0x00334948,
    ),
    'anyone_bag': (
        ToggleFields(
            ToggleField(enable=0xE1A00000, disable=0xA000004),
            ToggleField(enable=0xE1A00000, disable=0xA000004),
            label="任何人可使用行囊"
        ),
        (0x0031C5B0, 0x0031C9D8),
        (0x0031D2AC, 0x0031D6D4),
    ),
    'quick_info': (
        ToggleField(enable=0xE35000FF, disable=0xE3100001, label="快速显示信息"),
        0x0039BF2C,
        0x0039C93C,
    ),
    'custom_exp': (
        ToggleField(enable=0xE3A0003C, disable=0xC3A00064, label="自定义获取经验值"),
        0x004509EC,
        0x0045127C,
    ),

    'growth_rate_add': (
        ToggleField(
            enable=0xEA000000A3A060FFE35600FFE2866064,
            disable=0xE3560000AA000001A3A060FFE35600FF, size=16, label="成长率XX%加算(最大255%)"
        ),
        0x00356A58,
        0x00357468,
    ),

    'growth_rate_add_value': (
        ByteField(label="成长率加算"),
        0x00356A58,
        0x00357468,
    ),

    'add_all_attr': (
        ToggleField(enable=0xE3A00001, disable=0xEB01A8F8, label="成长率1%以上升级后能力值必定+1"),
        0x00356B84,
        0x00357594,
    ),

    'break_keep': (
        ToggleField(enable=0xE12FFF1E, disable=0xE92D4010, label="中断存档不消失"),
        0x003BA3F0,
        0x003BAE00,
    ),
    'item_keep': (
        ToggleField(enable=0xE1A00000, disable=0xEB08F683, label="道具使用不减"),
        0x001D7024,
        0x001D7C30,
    ),
    'inf_mila': (
        ToggleField(enable=0x13A00001, disable=0x15900008, label="无限使用米拉齿轮"),
        0x00434C0C,
        0x0043549C,
    ),
    'no_battle_3d': (
        ToggleField(enable=0xEA00003F, disable=0xDA00003F, label="3D迷宫接触敌人不战斗"),
        0x0017ED4C,
        0x0017FE6C,
    ),
    'first_turn_withdraw': (
        ToggleField(enable=0xE3500001, disable=0xE3500003, label="第一回合可撤退"),
        0x0044D968,
        0x0044E1F8,
    ),
    'well_no_driy': (
        ToggleFields(
            ToggleField(enable=0xEA000000, disable=0xA3A00001),
            ToggleField(enable=0xEA000000, disable=0xA3A00001),
            label="圣井不会干涸"
        ),
        (0x0042CE6C, 0x0042CC80),
        (0x0042D6FC, 0x0042D510),
    ),
    'support_talk_now': (
        ToggleFields(
            ToggleField(enable=0xE3A00006, disable=0xE5D00054),
            ToggleField(enable=0xE1500000E5C40019E2400001, disable=0xE1510000E2400001E1D411D9, size=12),
            label="立即发生支援对话"
        ),
        (0x001F7E18, 0x001F7E30),
        (0x001F8A24, 0x001F8A3C),
    ),
    'inf_hp': (
        ToggleFields(
            ToggleField(
                enable=pack_dwords(0xE1A00004, 0xE3550000, 0x112FFF1E, 0xE59640CC, 0xE3540000, 0x012FFF1E, 0xE5D44008,
                                   0xE3540000, 0x13540003, 0x112FFF1E, 0xE3A050FF, 0xE59640C4, 0xE5C4503C, 0xE2800064,
                                   0xE35000FF, 0xA3A000FF, 0xE5C600E3, 0xE5C60404, 0xE12FFF1E),
                disable=b'\x00' * 76),
            ToggleField(disable=0xE1A00004),
            label="HP无限"),
        (0x005279D0, {'offset': 0x004523B4, 'enable': 0xEB035585}),
        (0x005282D0, {'offset': 0x00452C9C, 'enable': 0xEB03558B}),
    ),
    'range_100': (
        ToggleFields(
            ToggleField(disable=0xE1A06002),
            ToggleField(disable=0xE1A00004),
            ToggleField(
                enable=pack_dwords(0xE1A00004, 0xE59740CC, 0xE5D44008, 0xE3540000, 0x03A00064, 0xE12FFF1E, 0xE59060CC,
                                   0xE5D66008, 0xE3560000, 0x03A05001, 0x028EEF5E, 0x11A06002, 0xE12FFF1E),
                disable=b'\x00' * 52),
            label="攻击射程100"),
        (
            {'offset': 0x004537C4, 'enable': 0xEB0350D3},
            {'offset': 0x00453DF4, 'enable': 0xEB034F41},
            0x00527B00
        ),
        (
            {'offset': 0x004540AC, 'enable': 0xEB0350D9},
            {'offset': 0x004546DC, 'enable': 0xEB034F47},
            0x00528400
        ),
    ),
    'move_max': (
        ToggleFields(
            ToggleField(
                enable=pack_dwords(0xE59640CC, 0xE3540000, 0x08BD8070, 0xE5D44008, 0xE3540000,
                                   0x13540003, 0x18BD8070, 0xE3A04032, 0xE5C640DF, 0xE8BD8070),
                disable=b'\x00' * 40),
            ToggleField(disable=0xE8BD8070),
            label="移动力最大"),
        (
            0x00527B40,
            {'offset': 0x004523B8, 'enable': 0xEA0355E0},
        ),
        (
            0x00528440,
            {'offset': 0x00452CA0, 'enable': 0xEA0355E6},
        ),
    ),
    'all_weapon_equipment': (
        ToggleField(enable=0xE12FFF1EE3A00001, disable=0xE1A04000E92D40F0, size=8, label="可装备全武器"),
        0x0045077C,
        0x0045100C,
    ),
    'all_support_a': (
        ToggleFields(
            ToggleField(
                enable=pack_dwords(0xE92D4002, 0xE59F1008, 0xE5801018, 0xE1D001D8, 0xE8BD8002, 0x63626203),
                disable=b'\x00' * 24),
            ToggleField(disable=0xE8BD8070),
            label="全支援A"),
        (
            0x00527C00,
            {'offset': 0x003A30C4, 'enable': 0xEB0612CD, 'disable': 0xE1D001D8},
        ),
        (
            0x00528500,
            {'offset': 0x003A3AD4, 'enable': 0xEB061289, 'disable': 0xE1D001D8},
        ),
    ),
    'all_attr_max_99': (
        ToggleField(
            enable=pack_dwords(0xE3A0C063, 0xE5C0C03C, 0xE59600C8, 0xE0804005, 0xE5D4402C, 0xE084400C, 0xEA000002),
            disable=pack_dwords(0xE5D0C03C, 0xE59600C8, 0xE0804005, 0xE5D4402C, 0xE084400C, 0xE35400FF, 0xA3A040FF),
            label="全能力上限99"),
        0x00452290,
        0x00452B78,
    ),
}


def bind_fields(data, version):
    """绑定字段"""
    index = version + 1
    for key, value in COMMON_FIELDS.items():
        data[key] = value[0].replace(value[index])
    return data


class BaseGlobalEchos(BaseGlobal):
    pass


class Global_1_0(BaseGlobalEchos):
    """version 1.0"""
    bind_fields(locals(), 0)

    all_class_selectable = ToggleFields(
        ToggleField(
            0x00527A40,
            enable=pack_dwords(0xE59F0014, 0xE5900000, 0xE2800C06, 0xE28000CC, 0xE0800385, 0xE0800285,
                               0xE12FFF1E, 0x0066013C),
            disable=b'\x00' * 32),
        ToggleField(0x001D1020, enable=0xE58D0024E59FA178E3A00049, disable=0xDA000023C59FA178E3500000, size=12),
        ToggleField(0x001D1050, enable=0xEB0D5A7A, disable=0xEB0A1CF8),
        ToggleField(0x001D108C, enable=0xE3A00000, disable=0xEB0A1C6F),
        ToggleField(0x001FBB48, enable=0xE3A00001, disable=0xE3A00000),
        ToggleField(0x001FBB58, enable=0xEA000036, disable=0x0A000036),
        label="转职全职业可选",
    )


class Global_1_1(BaseGlobalEchos):
    """version 1.1"""
    bind_fields(locals(), 1)

    all_class_selectable = ToggleFields(
        ToggleField(
            0x00528340,
            enable=pack_dwords(0xE59F0020, 0xE5908000, 0xE7980105, 0xE3500000, 0x112FFF1E, 0xE2855001,
                               0xE355006F, 0x1AFFFFF9, 0xE5980000, 0xE12FFF1E, 0x0066114C),
            disable=b'\x00' * 44),
        ToggleField(0x001D1BC0, enable=0xE58D0024E59FA178E3A0006F, disable=0xDA000023C59FA178E3500000, size=12),
        ToggleField(0x001D1BF0, enable=0xEB0D59D2, disable=0xEB0A1C4A),
        ToggleField(0x001D1C2C, enable=0xE3A00000, disable=0xEB0A1C6F),
        ToggleField(0x001FC8B0, enable=0xE3A00001, disable=0xE3A00000),
        ToggleField(0x001FC8C0, enable=0xEA000036, disable=0x0A000036),
        label="转职全职业可选",
    )


SPECIFIC_GLOBALS = {
    '1.0': Global_1_0,
    '1.1': Global_1_1,
}
