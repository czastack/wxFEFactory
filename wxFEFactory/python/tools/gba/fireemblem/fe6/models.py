from lib.hack.model import Model, Field, ByteField, WordField, ArrayField, ModelField
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
    defensive = ByteField(21)
    magicdef = ByteField(22)
    lucky = ByteField(23)
    physical_add = ByteField(24)
    move_add = ByteField(26)
    together = ByteField(27) # 同行人物序号
    items = ArrayField(28, 5, ModelField(0, ItemSlot))
    proficiency = ArrayField(38, 8, ByteField(0)) # 武器熟练度(剑、枪、斧、弓、杖、理、光、暗) (E级:01 D级:1F C级:47 B级:79 A级:B5 S级:FB)
    status = ByteField(46) # 状态种类
    status_turn = ByteField(47) # 状态持续回合数
    support = ArrayField(48, 10, ByteField(0)) # 支援等级


class Global(BaseGlobal):
    money = Field(0x0202AA50)
    turns = WordField(0x0202AA58)
    chapter = ByteField(0x0202AA56)
    person_addr = Field(0x02003114)
    curx = WordField(0x0202AA1C)
    cury = WordField(0x0202AA1E)
    persons = ArrayField(0x202AB78, 0xff, ModelField(0, Person))
    train_items = ArrayField(0x02039430, 100, ModelField(0, ItemSlot)) # 运输队
