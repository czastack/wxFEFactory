from lib.hack.model import Model, Field, ByteField, WordField, ArrayField, ModelField, ToggleField, ToggleFields
from ..models import ItemInfo, ItemInfo2, BaseGlobal


class Person(Model):
    SIZE = 0xC4
    
    figure = ByteField(0x02195DC9, label="形象")
    level = WordField(0x02195DCE, label="等级")
    exp = WordField(0x02195DD4, label="经验")
    hp = WordField(0x02195DD8, label="当前HP")
    hpmax = WordField(0x02195DDA, label="最大HP")
    battle_level = WordField(0x02195DE2, label="战斗等级")
    drive_level = WordField(0x02195DE4, label="驾驶等级")
    power = WordField(0x02195E68, label="腕力")
    strength = WordField(0x02195DDE, label="体力")
    speed = WordField(0x02195E6C, label="速度")
    spirit = ByteField(0x02195DE8, label="男子气概")
    scar = WordField(0x02195DE6, label="伤痕")
    prof = ByteField(0x02195DC8, label="职业")
    level_max = ByteField(0x02195DD0, label="等级上限")
    weapon_1 = WordField(0x02195DEA, label="武器1")
    weapon_2 = WordField(0x02195DEC, label="武器2")
    weapon_3 = WordField(0x02195DEE, label="武器3")
    equip_head = WordField(0x02195DF0, label="头部装备")
    equip_body = WordField(0x02195DF2, label="上身装备")
    equip_hand = WordField(0x02195DF4, label="手部装备")
    equip_foot = WordField(0x02195DF6, label="脚部装备")
    equip_orn = WordField(0x02195DF8, label="装饰")
    skill_counts = ArrayField(0x02195DFB, 9, ByteField(0)) # 主职业技能剩余次数数组
    subskill_counts = ArrayField(0x02195E16, 9, ByteField(0)) # 副职业技能剩余次数数组
    subprof = ByteField(0x02195E39, label="副职业")
    subprof_levels = ArrayField(0x02195E3A, 6, ByteField(0)) # 副职业等级(猎人、机械师、战士、护士、摔跤手、艺术家)
    subprof_exps = ArrayField(0x02195E40, 6, Field(0)) # 副职业经验


class ChariotEquipInfo(Model):
    SIZE = 0x14

    equip = WordField(0, label="种类")
    chaneg = ByteField(5, label="超改次数")
    status = ByteField(6, label="损坏程度(>20:破损,>100:损坏)")
    ammo = ByteField(8, label="剩余弹药")
    level = ByteField(9, label="武器星级")
    defensive = WordField(10, label="守备力")
    attr1 = WordField(12, label="C装置命中率/武器攻击力/引擎载重(0.01t)")
    attr2 = WordField(14, label="C装置回避率/武器弹舱容量")
    weight = WordField(18, label="重量(0.01t)")


class ChariotItemInfo(ChariotEquipInfo):
    item = WordField(0, label="种类")


class Chariot(Model):
    SIZE = 0x25C

    sp = WordField(0x02196D1C, label="装甲")
    hole_type = ArrayField(0x02196D1F, 5, ByteField(0), label="炮穴类型")
    chassis = WordField(0x02196D24, label="底盘")
    double_type = ByteField(0x02196D29, label="双持") # (0: 单引擎 单C装置, 1: 双引擎, 3: 双C装置)
    equips = ArrayField(0x02196D38, 8, ModelField(0, ChariotEquipInfo), label="装备") # C装置,引擎,C装置2/引擎2,洞1,洞2,洞3,洞4,洞5
    items = ArrayField(0x02196DD8, 9, ModelField(0, ChariotItemInfo), label="道具")
    special_bullets = ArrayField(0x02196F40, 15, ModelField(0, ItemInfo), label="特殊炮弹")

    exportable_fields = ('hole_type', 'double_type', 'equips', 'items', 'special_bullets')

    def health(self):
        for equip in self.equips:
            equip.status = 0

    @classmethod
    def item_type(self, id):
        if 0x2F4 <= id < 0x341:
            return 'item'
        elif 0x341 <= id < 0x3BC:
            return 'engine'
        elif 0x3BC <= id < 0x3EF:
            return 'control'
        elif 0x3EF <= id < 0x543:
            return 'weapon'


class EnemyCase(Model):
    SIZE = 6
    race = WordField(0, label="种族")
    count = ByteField(2, label="数量")


class Enemy(Model):
    SIZE = 0xBC

    race = WordField(0x021AB5CE, label="种族")
    level = ByteField(0x021AB616, label="等级")
    hp = Field(0x021AB618, label="HP")
    atk = WordField(0x021AB620, label="攻击")
    defensive = WordField(0x021AB622, label="防御")
    hit = WordField(0x021AB624, label="命中")
    avoid = WordField(0x021AB626, label="回避")
    speed = WordField(0x021AB628, label="速度")
    # exp = WordField(0x021AB62C, label="EXP")
    # g = WordField(0x021AB62E, label="G")
    # shine = WordField(0x021AB630, label="闪光")
    # 抗性(物火光电音气冷)
    resistance = ArrayField(0x021AB632, 7, WordField(0))

    # class MonsterAtkPart(Model):
    #     SIZE = 6
    #     part = WordField(0, label="部件")
    #     arg1 = ByteField(2, label="参数1")
    #     arg1 = ByteField(3, label="参数2")
    #     arg1 = ByteField(4, label="参数3")
    # atk_parts = ArrayField(0x021AB644, 7, ModelField(0, MonsterAtkPart))


class Global(BaseGlobal):
    persons = ArrayField(0, 15, ModelField(0, Person))
    chariots = ArrayField(0, 12, ModelField(0, Chariot))
    money = Field(0x021947D8, label="金钱")
    difficulty = ByteField(0x0219483D, label="难易度")
    stamp = WordField(0x02194844, label="邮票")
    game_turn = ByteField(0x021AA3E4, label="通关次数")
    exp = Field(0x021AAE90, label="经验")
    game_time = Field(0x021295DC, label="游戏时间")
    quick_switch = ToggleField(0x02027164, enableData=0x00002001, disableData=0x47702000, label="画面切换高速化")
    quick_move = ToggleField(0x021911FC, enableData=0x00001000, disableData=0x199, label="高速移动")
    must_winning = ToggleField(0x02042B54, enableData=0x46C04287, disableData=0xDD014287, label="贩卖机绝对会中奖")
    tool_count_keep = ToggleField(0x0206DD4C, enableData=0x2600B5F8, disableData=0x1C16B5F8, label="消费道具用后不减")
    level_up_max = ToggleFields(
        ToggleField(0x0206FC64, enableData=0x1E482100, disableData=0x21001C18),
        ToggleField(0x020DF908, enableData=0xE0002000, disableData=0xF7F32064),
        label="等级上升时随机数值最大"
    )

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

    # 敌人分布
    enemy_case = ArrayField(0x021AAF40, 4, ModelField(0, EnemyCase))
    # 敌人情况
    enemys = ArrayField(0, 10, ModelField(0, Enemy))

    posx = WordField(0x0219120E, label="X坐标")
    posy = WordField(0x02191212, label="Y坐标")