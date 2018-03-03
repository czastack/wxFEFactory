from lib.hack.model import Model, Field, ByteField, ArrayField, ModelField


class ItemSlot(Model):
    SIZE = 0x28
    item = Field(0)
    count = ByteField(4)


class Person(Model):
    SIZE = 0x3F0
    belong = ByteField(0x8D)
    level = ByteField(0x8E)
    exp = ByteField(0x8F)
    hp = ByteField(0xA4) # 当前hp
    physical_add = ByteField(0xA5)
    move_add = ByteField(0xA6)
    hp_add = ByteField(0xA9) # hp增加值(最大hp=hp初始值+hp增加值)
    power_add = ByteField(0xAA)
    magic_add = ByteField(0xAB)
    skill_add = ByteField(0xAC)
    speed_add = ByteField(0xAD)
    lucky_add = ByteField(0xAE)
    defensive_add = ByteField(0xAF)
    magicdef_add = ByteField(0xB0)
    items = ArrayField(0x150, 6, ModelField(0, ItemSlot))


class Ram(Model):
    persons = ArrayField(0x00930C00, 0xff, ModelField(0, Person))
    # decorator2 = ArrayField(0x00D851FF, 30, Field(0, size=1)) # 装饰2 (30个, 值为1)
    turn = Field(0x003AE34A, size=2) # 回合数
    money1 = Field(0x003AE350)
    money2 = Field(0x003AE354)
    money3 = Field(0x003AE358)
    exp1 = Field(0x003AE35C, type_=float)
    exp2 = Field(0x003AE360, type_=float)
    exp3 = Field(0x003AE364, type_=float)