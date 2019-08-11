from lib.hack.models import (
    Model, Field, ByteField, WordField, FloatField, ArrayField, ModelField, ModelPtrField, CoordField, ToggleField
)


class Game(Model):
    """运行时游戏数据"""
    money = Field(0x197C4C0, label="金钱")
    exp = Field(0x1984670, label="经验")


class Player(Model):
    """玩家数据"""
    hp = Field(0xE8, label='HP')
    hpmax = Field(0xEC, label='HP上限')
