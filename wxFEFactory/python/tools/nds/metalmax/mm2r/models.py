from lib.hack.model import Model, Field, ByteField, WordField, ArrayField, ModelField, OffsetsField, ModelPtrField, ToggleField, ToggleFields
from ..models import ItemInfo, ItemInfo2, BaseGlobal


class Person(Model):
    SIZE = 0xC4
    
    hp = WordField(0x02195DD8, label="当前HP")
    hpmax = WordField(0x02195DDA, label="最大HP")
    battle_level = WordField(0x02195DE2, label="战斗等级")
    drive_level = WordField(0x02195DE4, label="驾驶等级")
    power = WordField(0x02195DDC, label="腕力")
    strength = WordField(0x02195DDE, label="体力")
    speed = WordField(0x02195DE0, label="速度")
    spirit = WordField(0x02195DE8, label="男子气概")
    scar = WordField(0x02195DE6, label="伤痕")
    subprof = ByteField(0x02195DC8, label="副职业")
    figure = ByteField(0x02195DC9, label="形象")
    level_max = ByteField(0x02195DD0, label="等级上限")
    weapon_1 = ByteField(0x02195DEA, label="武器1")
    weapon_2 = ByteField(0x02195DEC, label="武器2")
    weapon_3 = ByteField(0x02195DEE, label="武器3")
    equip_head = ByteField(0x02195DF0, label="头部装备")
    equip_body = ByteField(0x02195DF2, label="上身装备")
    equip_hand = ByteField(0x02195DF4, label="手部装备")
    equip_foot = ByteField(0x02195DF6, label="脚部装备")
    equip_orn = ByteField(0x02195DF8, label="装饰")
    subprof_levels = ArrayField(0x02195E3A, 6, ByteField(0)) # 副职业等级(猎人、机械师、战士、护士、摔跤手、艺术家)


class ChariotEquipInfo(Model):
    SIZE = 0x14

    euip = WordField(0, label="种类")
    chaneg = ByteField(5, label="超改次数")
    ammo = ByteField(8, label="剩余弹药")
    level = ByteField(9, label="武器星级")
    defensive = WordField(10, label="守备力")
    hit = WordField(12, label="命中率(辅助)")
    atk = WordField(12, label="攻击力(武器)")
    avoid = WordField(14, label="回避率(辅助)")
    ammo_max = WordField(14, label="弹舱容量(武器)") # 00: 无限弹药
    weight = WordField(18, label="重量")


class ChariotItemInfo(ChariotEquipInfo):
    item = WordField(0, label="种类")


class Chariot(Model):
    SIZE = 0x25C

    chassis = WordField(0x02196D24, label="底盘")
    specital_bullet = ByteField(0x02196F40)
    specital_bullet_count = ByteField(0x02196F41)

    equips = ArrayField(0x02196D38, 8, ModelField(0, ChariotEquipInfo)) # C装置,引擎,C装置2/引擎2,洞1,洞2,洞3,洞4,洞5
    items = ArrayField(0x02196DD8, 9, ModelField(0, ChariotItemInfo))

    hole_type = ArrayField(0x02196D1F, 5, WordField(0))
    double_type = ByteField(0x02196D29, label="双持") # (0: 单引擎 单C装置, 1: 双引擎, 3: 双C装置)


class ChariotStatus(Model):
    SIZW = 0xBC
    sp = WordField(0x021AB3E4)
    spmax = WordField(0x021AB3E8)


class Global(BaseGlobal):
    # persons = ArrayField(0x202be48, 0xff, ModelField(0, Person))
    # train_items = ArrayField(0x022C7420, 100, ModelField(0, ItemSlot)) # 运输队
    money = Field(0x021947D8, label="金钱")
    exp = Field(0x021AAE90, label="经验")
    stamp = WordField(0x02194844, label="邮票")
    quick_switch = ToggleField(0x02027164, enableData=0x00002001, disableData=0x47702000, label="画面切换高速化")
    quick_move = ToggleField(0x021911FC, enableData=0x00001000, disableData=0x199, label="高速移动")
    must_winning = ToggleField(0x02042B54, enableData=0x46C04287, disableData=0xDD014287, label="贩卖机绝对会中奖")
    tool_count_keep = ToggleField(0x0206DD4C, enableData=0x2600B5F8, disableData=0x1C16B5F8, label="消费道具用后不减")
    level_up_max = ToggleFields(
        ToggleField(0x0206FC64, enableData=0x1E482100, disableData=0x21001C18),
        ToggleField(0x020DF908, enableData=0xE0002000, disableData=0xF7F32064),
        label="等级上升时随机数值最大"
    )
    game_time = Field(0x021295DC, label="游戏时间")

    weight_zero = ToggleFields(
        ToggleField(0x0206F37C, enableData=0x85482000, disableData=0x18248D48),
        ToggleField(0x0206F39C, enableData=0x80022200, disableData=0x18248800),
        label="装甲除底盘外重量为0"
    )

    equip_limit_remove = ToggleFields(
        ToggleField(0x02000120, enableData=0xF882F031, disableData=0xE5FCE69F),
        ToggleField(0x02000124, enableData=0x1E5B2300, disableData=0xBB92C9B8),
        ToggleField(0x02000128, enableData=0xBDF8802B, disableData=0xE28EAD90),
        ToggleField(0x0206E112, enableData=0xF805F792, disableData=0xF889F7C3),
        ToggleField(0x0206E16C, enableData=0xFFD8F791, disableData=0xF85CF7C3),
        label="装备限制解除"
    )

    without_material = ToggleFields(
        ToggleField(0x0204E9F0, enableData=0xE0141884, disableData=0x88601884),
        ToggleField(0x204EC04, enableData=0xE00AFCCF, disableData=0x8878FCCF),
        label="艺术家制作不需要素材",
    )

    twin_engines = ToggleField(0x02074648, enableData=0x77622201, disableData=0x1892D841, label="全车种双引擎")
    drop_item_three_star = ToggleField(0x0206FEB4, enableData=0x20030600, disableData=0x0E000600, label="敌人掉落的都是3星")
    no_battle = ToggleField(0x020AB298, enableData=0x0000E071, disableData=0xF7CDD371, label="不遇敌")
    must_drop_item = ToggleField(0x020E0604, enableData=0x46C04281, disableData=0xDA304281, label="必定掉落道具")
    after_money = Field(0x021AAEA4, label="战后获得金钱")
    after_exp = Field(0x021AAE90, label="战后获得经验值")
    # 战后获得金钱倍数(2: 00C8, 4: 0190, 8: 0320, 16: 0640, 32: 0C80, 64: 1900, 128: 3200)
    after_money_rate = WordField(0x21AAE4A, label="战后获得金钱倍数")
    # 战后获得经验值倍数(2: 00C8, 4: 0190, 8: 0320, 16: 0640, 32: 0C80, 64: 1900, 128: 3200)
    after_exp_rate = WordField(0x021AAE4E, label="战后获得经验值倍数")
    ammo_keep = ToggleField(0x020DDCDC, enableData=0x545346C0, disableData=0x54531E5B, label="车辆弹药不减")

    through_wall = ToggleFields(
        ToggleField(0x02034920, enableData=0xE1A00000, disableData=0xA3A00000),
        ToggleField(0x02034474, enableData=0xE1550001, disableData=0xB1550001),
        ToggleField(0x02034478, enableData=0xE1A05001, disableData=0xB1A05001),
        ToggleField(0x0203447C, enableData=0xE1A06000, disableData=0xB1A06000),
        ToggleField(0x020B24EE, size=2, enableData=0xE000, disableData=0xD100),
        label="穿墙"
    )

    # 战斗必定先制
    must_first = ToggleField(0x02085A3E, size=6, enableData=0x46C070012102, disableData=0xD12A28027800, label="战斗必定先制")

    # 回复道具
    potions = ArrayField(0x0219491C, 27, ModelField(0, ItemInfo))
    # 战斗道具
    battle_items = ArrayField(0x02194A3C, 46, ModelField(0, ItemInfo))
    # 道具
    humen_items = ArrayField(0x02194C78, 222, ModelField(0, ItemInfo2))
    # 装备
    equips = ArrayField(0x02194FF0, 373, ModelField(0, ItemInfo2))

    monster_1 = WordField(0x021AAF40, label="怪物1种类")
    monster_1_count = ByteField(0x021AAF42, label="怪物1种类")
    monster_2 = WordField(0x021AAF46, label="怪物1种类")
    monster_2_count = ByteField(0x021AAF48, label="怪物1种类")