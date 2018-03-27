from lib.hack.model import Model, Field, ByteField, ShortField, ArrayField, ModelField


class Person(Model):
    punch = ByteField(0)
    foot = ByteField(1)
    arms = ByteField(2)
    defense = ByteField(3)
    strong = ByteField(7)
    attack = ByteField(4)
    agile = ByteField(5)
    jump = ByteField(6)
    stamina = ByteField(8)
    hp = ByteField(10)
    hpmax = ByteField(12)
    money = Field(64)
    items = ArrayField(68, 12, ShortField(0))
    skills = ArrayField(92, 12, ShortField(0))
    skillkeys = ArrayField(116, 12, ShortField(0))


class Global(Model):
    partner_count = Field(0x02018AB5) # 我方人数
    enemy_count = Field(0x02018AB6) # 敌方人数