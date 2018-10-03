from lib.hack.models import Model, Field, ByteField, WordField, ArrayField, ModelField, ToggleField, ToggleFields
from ..models import ItemSlot, BaseGlobal


class Person(Model):
    SIZE = 0x48
    prof = Field(4)
    level = ByteField(8)
    exp = ByteField(9)
    no = ByteField(11)
    moved = ByteField(12)
    posx = ByteField(16)
    posy = ByteField(17)
    hpmax = ByteField(18)
    hp = ByteField(19)
    power = ByteField(20)
    skill = ByteField(21)
    speed = ByteField(22)
    defense = ByteField(23)
    magicdef = ByteField(24)
    lucky = ByteField(25)
    physical_add = ByteField(26)
    together = ByteField(27)  # 同行人物序号
    move_add = ByteField(29)
    items = ArrayField(30, 5, ModelField(0, ItemSlot))
    proficiency = ArrayField(40, 8, ByteField(0))  # 武器熟练度(剑、枪、斧、弓、杖、理、光、暗 E级:01 D级:1F C级:47 B级:79 A级:B5 S级:FB)
    status = ByteField(48)  # 状态种类
    status_turn = ByteField(49)  # 状态持续回合数
    support = ArrayField(50, 10, ByteField(0))  # 支援等级


class Global(BaseGlobal):
    money = Field(0x0202BCF4)
    chapter = ByteField(0x0202BCFA)
    turns = WordField(0x0202BCFC)
    extra_flag = WordField(0x02024F72)  # 附加项
    person_addr = Field(0x02003c08)
    curx = WordField(0x0202bcc0)
    cury = WordField(0x0202bcc2)
    persons = ArrayField(0x202be48, 0xff, ModelField(0, Person))
    train_items = ArrayField(0x0203A818, 100, ModelField(0, ItemSlot))  # 运输队

    # # Hack code EN
    # inf_move = ToggleFields(
    #     ToggleField(0x080183A8, size=2, enable=0x2000, disable=0x2002),
    #     ToggleField(0x08018750, size=2, enable=0x2100, disable=0x2102),
    #     ToggleField(0x0801D2BC, size=2, enable=0x2100, disable=0x2140),
    #     ToggleField(0x080320DE, size=2, enable=0x2100, disable=0x2140)
    # )  # 无限行动
    # item_count_keep = ToggleField(0x08016B0A, size=2, enable=0x46C0, disable=0x1812)  # 武器耐久度不减
    # proficiency_max = ToggleField(0x0802C280, size=2, enable=0x22FB, disable=0x1C02)  # 武器熟练度最大
    # ability_up_1 = ToggleField(0x0802B9BC, size=2, enable=0x2001, disable=0x1C20)  # 全能力成长1点
    # ability_up_2 = ToggleField(0x0802B9BC, size=2, enable=0x2002, disable=0x1C20)  # 全能力成长2点
    # got_100exp = ToggleField(0x0802C58C, size=2, enable=0x2164, disable=0x1809)  # 战后升级
    # support_quickly = ToggleField(0x080282C2, size=2, enable=0x7039, disable=0x7038)  # 好感度快速提升

    # Hack code ZH
    inf_move = ToggleFields(
        ToggleField(0x080183A8, size=2, enable=0x2000, disable=0x2002),
        ToggleField(0x08018464, size=2, enable=0x2100, disable=0x2102),
        ToggleField(0x0801CF20, size=2, enable=0x2100, disable=0x2140),
        ToggleField(0x0803202A, size=2, enable=0x2100, disable=0x2140)
    )  # 无限行动
    item_count_keep = ToggleField(0x080168B2, size=2, enable=0x46C0, disable=0x1812)  # 武器耐久度不减
    proficiency_max = ToggleField(0x0802C1C8, size=2, enable=0x22FB, disable=0x1C02)  # 武器熟练度最大
    ability_up_1 = ToggleField(0x0802B904, size=2, enable=0x2001, disable=0x1C20)  # 全能力成长1点
    ability_up_2 = ToggleField(0x0802B904, size=2, enable=0x2002, disable=0x1C20)  # 全能力成长2点
    got_100exp = ToggleField(0x0802C4C4, size=2, enable=0x2164, disable=0x1809)  # 战后升级
    support_quickly = ToggleField(0x08028256, size=2, enable=0x7039, disable=0x7038)  # 好感度快速提升
