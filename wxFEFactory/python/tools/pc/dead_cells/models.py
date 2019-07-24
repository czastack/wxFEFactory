from lib.hack.models import (
    Model, Field, ByteField, WordField, FloatField, ArrayField, ModelField, ModelPtrField, CoordField, ToggleField
)


class Player(Model):
    hp = Field(0xE8, label='HP')
    hpmax = Field(0xEC, label='HP上限')
    red_tier = ByteField(0x114, label='暴虐')
    purple_tier = ByteField(0x110, label='战术')
    green_tier = ByteField(0x118, label='生存')
    cell = Field(0x33C, label='细胞')


class Game(Model):
    time = Field(0x28, type=float, size=8, label="时间")
    gold = Field(0x34, label="金币")
    kill = Field(0x50, label="无伤击杀数")


class HlHandle(Model):
    player = ModelPtrField((0x18, 0x64), Player)
    game = ModelPtrField((0x18, 0x5C), Game)
