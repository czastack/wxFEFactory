from lib.hack.models import Model, Field, ByteField, WordField, ArrayField, ModelField, ToggleField, ToggleFields
from ..models import ItemSlot, BaseGlobal


class Person(Model):
    SIZE = 0x48
    prof = Field(4)
    level = ByteField(8)
    exp = ByteField(9)
    no = ByteField(11)
    moved = ByteField(12)
    posx = ByteField(14)
    posy = ByteField(15)
    hpmax = ByteField(16)
    hp = ByteField(17)
    power = ByteField(18)
    skill = ByteField(19)
    speed = ByteField(20)
    defense = ByteField(21)
    magicdef = ByteField(22)
    lucky = ByteField(23)
    physical_add = ByteField(24)
    move_add = ByteField(26)
    together = ByteField(27)  # 同行人物序号
    items = ArrayField(28, 5, ModelField(0, ItemSlot))
    proficiency = ArrayField(38, 8, ByteField(0))  # 武器熟练度(剑、枪、斧、弓、杖、理、光、暗 E级:01 D级:1F C级:47 B级:79 A级:B5 S级:FB)
    status = ByteField(46)  # 状态种类
    status_turn = ByteField(47)  # 状态持续回合数
    support = ArrayField(48, 10, ByteField(0))  # 支援等级


class Global(BaseGlobal):
    money = Field(0x0202AA50)
    turns = WordField(0x0202AA58)
    chapter = ByteField(0x0202AA56)
    person_addr = Field(0x02003114)
    curx = WordField(0x0202AA1C)
    cury = WordField(0x0202AA1E)
    persons = ArrayField(0x202AB78, 0xff, ModelField(0, Person))
    train_items = ArrayField(0x02039430, 100, ModelField(0, ItemSlot))  # 运输队
    # Hack code
    inf_move = ToggleFields(
        ToggleField(0x08017B80, size=2, enable=0x2000, disable=0x2002),
        ToggleField(0x08017EEA, size=2, enable=0x2100, disable=0x2102),
        ToggleField(0x0801B976, size=2, enable=0x2000, disable=0x2040),
        ToggleField(0x0802A0C8, size=2, enable=0x2000, disable=0x2040)
    )  # 无限行动
    item_count_keep = ToggleField(0x08016940, size=2, enable=0x46C0, disable=0x1812)  # 武器耐久度不减
    proficiency_max = ToggleField(0x080256CC, size=2, enable=0x22FB, disable=0x1C02)  # 武器熟练度最大
    ability_up_1 = ToggleField(0x080250CC, size=2, enable=0x2001, disable=0x1C20)  # 全能力成长1点
    ability_up_2 = ToggleField(0x080250CC, size=2, enable=0x2002, disable=0x1C20)  # 全能力成长2点
    got_100exp = ToggleField(0x080258D0, size=2, enable=0x2464, disable=0x1824)  # 战后升级
    # got_100exp = ToggleFields(
    #     ToggleField(0x080258BA, size=2, enable=0x2064, disable=0x2001),
    #     ToggleField(0x080258D0, size=2, enable=0x2464, disable=0x1824),
    #     ToggleField(0x08025994, size=2, enable=0x46C0, disable=0xDD00),
    #     ToggleField(0x080259C6, size=2, enable=0x2064, disable=0x200A)
    #     ToggleField(0x080259CC, size=2, enable=0x3064, disable=0x300A)
    # )
    support_quickly = ToggleField(0x08022B72, size=2, enable=0x7039, disable=0x7038)  # 好感度快速提升
