from lib.hack.models import Model, Field, ByteField, WordField, ArrayField, ModelField


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
    items = ArrayField(68, 12, WordField(0))
    skills = ArrayField(92, 12, WordField(0))
    skillkeys = ArrayField(116, 12, WordField(0))
