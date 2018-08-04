from lib.hack.models import (
    Model, Field, Fields, ByteField, WordField, ArrayField, ModelPtrField, CoordField, ToggleField
)


class Global(Model):
    pass


class Player(Model):
    hp = WordField(0x1364, label="HP")
    hpmax = WordField(0x1366, label="最大HP")
    moving_coord = CoordField(0x2AD0, label="移动坐标")
    melee_coord = CoordField(0x2E10, label="坐标")
    idle = Field(0x10E0)
    target = Field(0x2DA4, label="目标")
    ai = Field(0x2DA8, label="AI")
    attack_reaction = Field(0x1358)
    invincible = ToggleField(0x135C, label="无敌", enableData=0, disableData=1)
    merce_kill_counter = Field(0x25BC)


class CharacterStruct(Model):
    players = ArrayField(0x24, 4, ModelPtrField(0, Player))
    players_count = Field(0x34, label="角色数量")
