from lib.hack.models import Model, Field, ByteField, WordField, ArrayField, ModelField


class ItemSlot(Model):
    SIZE = 4
    item = ByteField(0)
    count = ByteField(1)
    value = WordField(0)


class Person(Model):
    SIZE = 0xA0

    hpmax = WordField(0x20069F8)
    resist = WordField(0x20069FA)
    str = ByteField(0x20069FC)
    mgc = ByteField(0x20069FD)
    agl = ByteField(0x20069FE)
    vit = ByteField(0x20069FF)
    _resist = ByteField(0x2006A07)
    skills = Field(0x02006A18, bytes, 0x48)


class PersonBattle(Model):
    SIZE = 0x58
    hp = WordField(0x02002668)


class Global(Model):
    tp = ByteField(0x020091CF)
    favors = ArrayField(0x020091A0, 8, ByteField(0))  # 好感度
    member_num = ByteField(0x020069DC)
    members = ArrayField(0x020069DD, 5, ByteField(0))  # 好感度
    item_num = ByteField(0x020091DD)
    items = ArrayField(0x020069DD, 5, ByteField(0))  # 好感度
    items = ArrayField(0x02006DBC, 16, ModelField(0, ItemSlot))
    kill_slot = WordField(0x020028E2)
    rage = WordField(0x020028EC)
    person_battles = ArrayField(0, 6, ModelField(0, PersonBattle))  # 战斗中人物信息
    event_items = ArrayField(0x02008170, 10, WordField(0))  # 事件道具
