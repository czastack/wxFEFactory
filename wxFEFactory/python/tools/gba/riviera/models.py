from lib.hack.models import Model, Field, SignedField, ByteField, WordField, ArrayField, ModelField


class ItemSlot(Model):
    SIZE = 4
    item = ByteField(0)
    count = ByteField(1)
    value = WordField(0)


class Person(Model):
    SIZE = 0xA0

    hp_max = WordField(0x020069F8, label="HP上限")
    resist = WordField(0x020069FA, label="RESIST")
    str = ByteField(0x020069FC, label="STR")
    mgc = ByteField(0x020069FD, label="MGC")
    agl = ByteField(0x020069FE, label="AGL")
    vit = ByteField(0x020069FF, label="VIT")
    hp_heal = ByteField(0x02006A01, label="HP回复%")
    resistance = ArrayField(0x02006A02, 5, SignedField(0, size=1), label="抗性")
    adaptive = ByteField(0x02006A07, label="全抗性")
    skills = Field(0x02006A18, bytes, 0x48)


class PersonBattle(Model):
    SIZE = 0x58
    hp = WordField(0x02002668)


class Global(Model):
    tp = ByteField(0x020091CF, label="TP")
    favors = ArrayField(0x020091A0, 8, ByteField(0))  # 好感度
    member_num = ByteField(0x020069DC, label="队伍人数")
    members = ArrayField(0x020069DD, 5, ByteField(0), label="队员")
    item_num = ByteField(0x020091DD, label="道具数量")
    items = ArrayField(0x02006DBC, 16, ModelField(0, ItemSlot))
    kill_slot = WordField(0x020028E2, label="必杀槽")
    rage = WordField(0x020028EC, label="RAGE")
    person_battles = ArrayField(0, 6, ModelField(0, PersonBattle))  # 战斗中人物信息
    event_items = ArrayField(0x02008170, 10, WordField(0))  # 事件道具
