from lib.hack.model import Model, Field, ByteField, ShortField, ArrayField, ModelField, OffsetsField
from ..febase.models import BasePerson, ItemSlot, BaseGlobal


class Person(BasePerson):
    SIZE = 0x48
    prof = Field(0x44)
    level = ByteField(0x5A)
    exp = ByteField(0x5B)
    no = ByteField(0x41) # 头像、身份？
    moved = ByteField(0x94)
    posx = ByteField(0x5E)
    posy = ByteField(0x5F)
    hpmax = ByteField(0x50)
    hp = ByteField(0x5C)
    power = ByteField(0x51)
    skill = ByteField(0x53)
    speed = ByteField(0x54)
    defensive = ByteField(0x56)
    magicdef = ByteField(0x52)
    lucky = ByteField(0x55)
    # physical_add = ByteField(26)
    # together = ByteField(27) # 同行人物序号
    move_add = ByteField(0x5D)
    items = ArrayField(0x60, 5, ModelField(0, ItemSlot))
    proficiency = ArrayField(0x74, 6, ByteField(0)) # 武器熟练度(剑, 枪, 斧, 弓, 书, 杖) (E级:01 D级:1F C级:47 B级:79 A级:B5 S级:FB)
    # status = ByteField(48) # 状态种类
    # status_turn = ByteField(49) # 状态持续回合数
    # support = ArrayField(50, 10, ByteField(0)) # 支援等级


class Global(BaseGlobal):
    money = OffsetsField((0x021BD44C, 0x0194))
    # chapter = ByteField(0x0202BCFA)
    # turns = ShortField(0x0202BCFC)
    # extra_flag = ShortField(0x02024F72) # 附加项
    person_addr = Field(0x021BED30)
    # curx = ShortField(0x0202bcc0)
    # cury = ShortField(0x0202bcc2)
    # persons = ArrayField(0x202be48, 0xff, ModelField(0, Person))
    # train_items = ArrayField(0x0203A818, 100, ModelField(0, ItemSlot)) # 运输队
