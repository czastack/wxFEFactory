from lib.hack.model import Model, Field, ByteField, WordField, ArrayField, ModelField, ToggleField, ToggleFields
from ..models import ItemInfo, ItemInfo2, BaseGlobal


class Person(Model):
    SIZE = 0x70
    
    prof = ByteField(0x021A0BD8, label="职业")
    figure = ByteField(0x021A0BD9, label="形象")
    level = WordField(0x021A0BDC, label="等级")
    level_max = ByteField(0x021A0BDE, label="等级上限")
    exp = WordField(0x021A0BE0, label="经验")
    hp = WordField(0x021A0BE4, label="当前HP")
    hpmax = WordField(0x021A0BE6, label="最大HP")
    battle_level = WordField(0x021A0BEE, label="战斗等级")
    drive_level = WordField(0x021A0BF0, label="驾驶等级")
    power = WordField(0x021A0C26, label="腕力")
    strength = WordField(0x021A0BEA, label="体力")
    speed = WordField(0x021A0BEC, label="速度")
    spirit = ByteField(0x021A0BF4, label="男子气概")
    scar = WordField(0x021A0BF2, label="伤痕")
    weapon_1 = WordField(0x021A0BF6, label="武器1")
    weapon_2 = WordField(0x021A0BF8, label="武器2")
    weapon_3 = WordField(0x021A0BFA, label="武器3")
    equip_head = WordField(0x021A0BFC, label="头部装备")
    equip_body = WordField(0x021A0BFE, label="上身装备")
    equip_hand = WordField(0x021A0BF0, label="手部装备")
    equip_foot = WordField(0x021A0BF2, label="脚部装备")
    equip_orn = WordField(0x021A0BF4, label="装饰")
    skill_counts = ArrayField(0x021A0C06, 9, ModelField(0, ItemInfo)) # (技能, 次数)数组


class ChariotEquipInfo(Model):
    SIZE = 0x14

    equip = WordField(0, label="种类")
    chaneg = ByteField(5, label="超改次数")
    status = ByteField(6, label="损坏程度(>20:破损,>100:损坏)")
    ammo = ByteField(8, label="剩余弹药")
    star = ByteField(9, label="武器星级")
    defensive = WordField(10, label="守备力")
    attr1 = WordField(12, label="C装置命中率/武器攻击力/引擎载重(0.01t)")
    attr2 = WordField(14, label="C装置回避率/武器弹舱容量")
    weight = WordField(18, label="重量(0.01t)")


class ChariotItemInfo(ChariotEquipInfo):
    item = WordField(0, label="种类")


class Chariot(Model):
    SIZE = 0x256

    sp = WordField(0x21A1B9E, label="装甲")
    chassis = ModelField(0x021A1BA0, ChariotEquipInfo, label="底盘")
    equips = ArrayField(0x021A1BB4, 8, ModelField(0, ChariotEquipInfo), label="装备") # C装置,引擎,引擎2,洞1,洞2,洞3,洞4,洞5 # TODO
    items = ArrayField(0x021A1C54, 9, ModelField(0, ChariotItemInfo), label="道具")
    special_bullets = ArrayField(0x21A1DC6, 15, ModelField(0, ItemInfo), label="特殊炮弹") # TODO

    exportable_fields = ('equips', 'items', 'special_bullets')

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


class ChariotBattleStatus(Model):
    SIZE = 0xBC
    sp = WordField(0x021A61F0, label="装甲")
    spmax = WordField(0x021A61F2, label="最大装甲")


class BattleStatus(Model):
    SIZE = 0xB0
    status = Field(0x021A5EF0) # 角色状态
    hp = WordField(0x021A5FE2, label="HP")
    hpmax = WordField(0x021A5FE0, label="HP最大值")


class EnemyCase(Model):
    SIZE = 6
    race = WordField(0, label="种族") # TODO
    count = ByteField(2, label="数量") # TODO


class Enemy(Model):
    SIZE = 0xAE# ? 0xB0?

    race = WordField(0x021A63B6, label="种族") # TODO
    level = ByteField(0x021A63FE, label="等级") # TODO
    hp = Field(0x021A6400, label="HP") # TODO
    atk = WordField(0x021A6408, label="攻击") # TODO
    defensive = WordField(0x021AB622, label="防御") # TODO
    hit = WordField(0x021A640C, label="命中") # TODO
    avoid = WordField(0x021A640E, label="回避") # TODO
    speed = WordField(0x021A6410, label="速度") # TODO
    # exp = WordField(0x021A6414, label="EXP") # TODO
    # g = WordField(0x021A6416, label="G") # TODO
    # shine = WordField(0x021A6418, label="闪光") # TODO
    # 抗性(物火光电音气冷)
    resistance = ArrayField(0x021A641A, 7, WordField(0)) # TODO

    # class MonsterAtkPart(Model):
    #     SIZE = 6
    #     part = WordField(0, label="部件") # TODO
    #     arg1 = ByteField(2, label="参数1") # TODO
    #     arg1 = ByteField(3, label="参数2") # TODO
    #     arg1 = ByteField(4, label="参数3") # TODO
    # atk_parts = ArrayField(0x021B085C, 7, ModelField(0, MonsterAtkPart)) # TODO


class Global(BaseGlobal):
    persons = ArrayField(0, 15, ModelField(0, Person))
    chariots = ArrayField(0, 12, ModelField(0, Chariot))
    chariot_battle_status = ArrayField(0, 4, ModelField(0, ChariotBattleStatus))
    money = Field(0x0219F768, label="金钱")
    difficulty = ByteField(0x0219483D, label="难易度") # TODO
    stamp = WordField(0x0219F7BE, label="印章")
    game_turn = ByteField(0x021AA3E4, label="通关次数") # TODO
    exp = Field(0x021AAE90, label="经验") # TODO
    game_time = Field(0x022AC6FC, label="游戏时间")

    allfax = ToggleField(0x0219E90B, size=6, enableData=0xFFFFFFFFFFFF, label="传真全开") # TODO
    allmap = ToggleFields(
        # ToggleField(0x020ACE8A, enableData=0x20FF, size=2, disableData=0x7828),
        # ToggleField(0x020AC3F0, enableData=0x4770, size=2, disableData=0xD000),
        label="地图全开"
    )
    enemy_flash = ToggleFields(
        ToggleField(0x02087ADE, enableData=0x2109, size=2, disableData=0x718E),
        ToggleField(0x02087DBA, enableData=0x46C0, size=2, disableData=0xDA40),
        label="敌人闪光"
    )
    can_use_other_skill = ToggleFields(
        ToggleField(0x020753A4, enableData=0xE005, size=2, disableData=0xD105), # TODO
        ToggleField(0x02075628, enableData=0x4280, size=2, disableData=0x42A0), # TODO
        ToggleField(0x020E1F60, enableData=0x4280, size=2, disableData=0x4285), # TODO
        ToggleField(0x020DDB58, enableData=0x4280, size=2, disableData=0x2A02), # TODO
        label="可以使用其他副职业的特技"
    )
    must_critical_hit = ToggleFields(
        ToggleField(0x02000180, enableData=0x9800DB032807B500, size=8, disableData=0xBDAF1785CC47D6C6), # TODO
        ToggleField(0x02000188, enableData=0xF0D6BD009000380C, size=8, disableData=0x3AA28F402E0005E8), # TODO
        ToggleField(0x02000190, enableData=0xBD00F9BB, disableData=0x4B358143), # TODO
        ToggleField(0x020D6614, enableData=0xFDB4F729, disableData=0xFF78F7FF), # TODO
        label="必定会心一击"
    )

    quick_switch = ToggleField(0x0202460C, enableData=0x47702001, disableData=0x47702000, label="画面切换高速化")
    quick_move = ToggleField(0x021911FC, enableData=0x00001000, disableData=0x199, label="高速移动") # TODO
    must_winning = ToggleField(0x020442F0, enableData=0x2007E008, disableData=0x2007DD08, label="贩卖机绝对会中奖")
    tool_count_keep = ToggleField(0x0207681E, enableData=0x46C00049, disableData=0x54420049, label="消费道具用后不减") # TODO
    level_up_max = ToggleFields(
        ToggleField(0x0206FC64, enableData=0x1E482100, disableData=0x21001C18), # TODO
        ToggleField(0x020DF908, enableData=0xE0002000, disableData=0xF7F32064), # TODO
        label="等级上升时随机数值最大"
    )

    weight_zero = ToggleFields(
        ToggleField(0x02076A30, enableData=0x84C82000, disableData=0x18248CC8),
        ToggleField(0x02076A50, enableData=0x80022200, disableData=0x18248800),
        label="装甲除底盘外重量为0"
    )

    equip_limit_remove = ToggleFields(
        ToggleField(0x0207B9B2, size=2, enableData=0x46C0, disableData=0xD00A),
        ToggleField(0x02073AD0, size=2, enableData=0x46C0, disableData=0xD055),
        ToggleField(0x02073BA8, size=2, enableData=0x46C0, disableData=0xD003),
        ToggleField(0x02073C7E, size=2, enableData=0x46C0, disableData=0xD037),
        ToggleField(0x02073D16, size=2, enableData=0x46C0, disableData=0xD015),
        ToggleField(0x02073FD0, size=2, enableData=0x46C0, disableData=0xD005),
        ToggleField(0x0204E0EC, size=2, enableData=0x46C0, disableData=0xD030),
        label="装备限制解除"
    )

    without_material = ToggleFields(
        ToggleField(0x0204E9F0, enableData=0xE0141884, disableData=0x88601884), # TODO
        ToggleField(0x204EC04, enableData=0xE00AFCCF, disableData=0x8878FCCF), # TODO
        label="艺术家制作不需要素材",
    )

    twin_engines = ToggleField(0x02074648, enableData=0x77622201, disableData=0x1892D841, label="全车种双引擎") # TODO
    drop_item_three_star = ToggleField(0x020773B0, enableData=0x46C02003, disableData=0xFBB2F00F, label="敌人掉落的都是3星")
    no_battle = ToggleField(0x020BBE60, size=2, enableData=0x46C0, disableData=0x1C40, label="不遇敌")
    must_drop_item = ToggleField(0x020E0604, enableData=0x46C04281, disableData=0xDA304281, label="必定掉落道具") # TODO
    after_money = Field(0x021AAEA4, label="战后获得金钱") # TODO
    after_exp = Field(0x021AAE90, label="战后获得经验值") # TODO
    # 战后获得金钱倍数(2: 00C8, 4: 0190, 8: 0320, 16: 0640, 32: 0C80, 64: 1900, 128: 3200)
    after_money_rate = WordField(0x021A5CA8, label="战后获得金钱倍数")
    # 战后获得经验值倍数(2: 00C8, 4: 0190, 8: 0320, 16: 0640, 32: 0C80, 64: 1900, 128: 3200)
    after_exp_rate = WordField(0x021AAE4E, label="战后获得经验值倍数") # TODO
    ammo_keep = ToggleField(0x0208FA1C, enableData=0x46C0D302, disableData=0x1E52D302, label="车辆弹药不减")

    through_wall = ToggleField(0x020BE4C4, size=2, enableData=0x2000, disableData=0x1C28, label="穿墙")

    # 战斗必定先制
    must_first = ToggleField(0x02085A3E, size=6, enableData=0x46C070012102, disableData=0xD12A28027800, label="战斗必定先制") # TODO

    # 回复道具
    potions = ArrayField(0x0219F918, 27, ModelField(0, ItemInfo))
    # 战斗道具
    battle_items = ArrayField(0x0219F960, 46, ModelField(0, ItemInfo))
    # 道具
    humen_items = ArrayField(0x0219FC78, 222, ModelField(0, ItemInfo2))
    # 装备
    equips = ArrayField(0x0219FF6C, 373, ModelField(0, ItemInfo2))

    # 敌人分布
    enemy_case = ArrayField(0x021AAF40, 4, ModelField(0, EnemyCase)) # TODO
    # 敌人情况
    enemys = ArrayField(0, 10, ModelField(0, Enemy)) # TODO

    posx = WordField(0x0219120E, label="X坐标") # TODO
    posy = WordField(0x02191212, label="Y坐标") # TODO

    use_humen_weapon_1 = ToggleField(0x0208425C, enableData=0xE0012801, disableData=0xD12C2801, label="战车中也可以用人的武器v1")
    use_humen_weapon_2 = ToggleField(0x02085374, enableData=0xD00AE004, disableData=0xD00AD004, label="战车中也可以用人的武器v2")
    buy_chariot_item_three_star = ToggleField(0x02077378, enableData=0x72602003, disableData=0x7260D101, label="店内购入的车用品必定3星")
    can_buy_not_for_sale = ToggleField(0x0204E618, enableData=0x48B8E001, disableData=0x48B8D101, label="可以购入非卖的车用品")

    can_change_even_overweight = ToggleField(0x02043064, enableData=0x1EE4E000, disableData=0x1EE4D100, label="车身超过重量也可以改造")
    can_always_special_bullet = ToggleFields(
        ToggleField(0x0208EFEC, size=2, enableData=0x46C0, disableData=0xD111),
        ToggleField(0x0208EFFE, size=2, enableData=0xE007, disableData=0xD007),
        label="都能用特殊砲弾"
    )

    # 仓库第一件战车物品星级 0x21A0419
    # 好感度
    favorability = ArrayField(0x021AB52E, 12, ByteField(0))

    # 通缉名单状态03=击破 01=逃走
    wanted_status = ArrayField(0x021AB503, 26, ByteField(0))

    reward = Field(0x21AB4FE, size=3, label="获得赏金")
    fame = WordField(0x021AB501, label="有名度")

    skill_count_keep = ToggleFields(
        ToggleField(0x0208F070, size=2, enableData=0x46C0, disableData=0x1E40),
        ToggleField(0x0207C2B2, size=2, enableData=0x46C0, disableData=0x1E40),
        label="特技使用次数不减"
    )


    # 连射
    # 2212919C 00000000

    skill_count_keep = ToggleFields(
        ToggleField(0x020686F0, size=8, enableData=0x00C9314521F0E046, disableData=0xF009A9008B30E046),
        ToggleField(0x020686F8, size=8, enableData=0xA902688868081861, disableData=0xA90298019800FEAD),
        label="卡车回家系统可以移動到现在地"
    )
    can_go_wrong_place = ToggleField(0x0227E180, enableData=0x0169, disableData=0xFFFF)

    move_speed = WordField(0x020C2A58, label="移动速度")