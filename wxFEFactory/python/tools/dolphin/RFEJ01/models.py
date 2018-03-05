from lib.hack.model import Model, Field, ByteField, ArrayField, ModelField


class ItemSlot(Model):
    SIZE = 0x28
    item = Field(0)
    count = ByteField(4)


class SkillSlot(Model):
    SIZE = 8
    skill = Field(0, size=2)


class Person(Model):
    SIZE = 0x3F0
    prof = Field(0x02, size=2) # 职业
    camp = Field(0x04, size=4) # 阵营？0x8064CDFC = 晓之团
    no = ByteField(0x0C) # 角色编号
    belong = ByteField(0x0D) # 所属
    level = ByteField(0x0E)
    exp = ByteField(0x0F)
    posx = ByteField(0x12) # 横坐标(左上角开始)
    posy = ByteField(0x13) # 纵坐标
    moved = ByteField(0x1F) # 1表示已经移动，0表示可以行动
    hp = ByteField(0x24) # 当前hp
    physical_add = ByteField(0x25)
    move_add = ByteField(0x26)
    hp_add = ByteField(0x29) # hp增加值(最大hp=hp初始值+hp增加值)
    power_add = ByteField(0x2A)
    magic_add = ByteField(0x2B)
    skill_add = ByteField(0x2C)
    speed_add = ByteField(0x2D)
    lucky_add = ByteField(0x2E)
    defensive_add = ByteField(0x2F)
    magicdef_add = ByteField(0x30)
    skills = Field(0x3E, size=2)
    items = ArrayField(0xCC, 7, ModelField(0, ItemSlot))
    proficiency = ArrayField(0x01E4, 12, Field(0, size=2)) # 24个字节 武器熟练度(剑、枪、斧、弓、短剑、打、炎、雷、风、光、暗、杖)
    support = ArrayField(0x210, 72, ByteField(0)) # 72个字节 C级=32, B级=64, A级=96


class Ram(Model):
    # 4.0.2: 9: 0x00914EC0 
    # 5.x 9: 0x00930C80
    persons = ArrayField(0x00912B50, 0xff, ModelField(0, Person))
    turn = Field(0x003AE34A, size=2) # 回合数
    money1 = Field(0x003AE350)
    money2 = Field(0x003AE354)
    money3 = Field(0x003AE358)
    exp1 = Field(0x003AE35C, type_=float)
    exp2 = Field(0x003AE360, type_=float)
    exp3 = Field(0x003AE364, type_=float)
    pedid = ByteField(0x003AC8FC) # 当前人物编号
    curx = Field(0x003C88B1, size=2) # 当前光标x坐标
    cury = Field(0x003C88B3, size=2) # 当前光标y坐标