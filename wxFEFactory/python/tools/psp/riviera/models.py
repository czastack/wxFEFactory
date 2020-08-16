from lib.hack.models import Model, Field, SignedField, ByteField, WordField, ArrayField, ModelField


class ItemSlot(Model):
    SIZE = 4
    item = ByteField(0)
    count = ByteField(1)
    value = WordField(0)


class Character(Model):
    SIZE = 0xA0

    hpmax = WordField(0x0126ACB4, label="HP上限")
    resist = WordField(0x0126ACB6, label="RESIST")
    str = ByteField(0x0126ACB8, label="STR")
    mgc = ByteField(0x0126ACB9, label="MGC")
    agl = ByteField(0x0126ACBA, label="AGL")
    vit = ByteField(0x0126ACBB, label="VIT")
    hp_heal = ByteField(0x0126ACBD, label="HP回复%")
    resistance = ArrayField(0x0126ACBE, 5, SignedField(0, size=1), label="抗性")
    adaptive = ByteField(0x0126ACC3, label="全抗性")
    skills = Field(0x0126ACD0, bytes, 0x48)


# class CharacterBattle(Model):
#     SIZE = 0x58
#     hp = WordField(0x0126ACB4)


class Global(Model):
    tp = ByteField(0x0126C341, label="TP")
    favors = ArrayField(0x0126C314, 8, ByteField(0))  # 好感度
    member_num = ByteField(0x0126AC98, label="队伍人数")
    members = ArrayField(0x0126AC99, 5, ByteField(0), label="队员")
    item_num = ByteField(0x0126C34F, label="道具数量")
    items = ArrayField(0x0126B076, 16, ModelField(0, ItemSlot))
    kill_slot = WordField(0x012E24F2, label="必杀槽")
    rage = WordField(0x012E24FC, label="RAGE")
    battle_time = ByteField(0x012E2506, label="战斗时间")
    # character_battles = ArrayField(0, 6, ModelField(0, CharacterBattle))  # 战斗中人物信息
    # event_items = ArrayField(0x0126A009, 10, WordField(0))  # 事件道具
