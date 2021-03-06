from lib.hack.models import Model, Field, ByteField, WordField, BitsField, ArrayField, ModelField


class Person(Model):
    SIZE = 8

    # name = Field(0, bytes, 0xF)
    exp = Field(0x0, size=3, label="经验")
    level = ByteField(0x03003D69, label="等级")
    hp = WordField(0x03003D41, label="HP")
    hpmax = WordField(0x03003D43, label="HP上限")
    atk = WordField(0x03003D45, label="攻击")
    defense = WordField(0x03003D47, label="守备")
    power = ByteField(0x03003D6A, label="腕力")
    intelli = ByteField(0x03003D6B, label="知力")
    stamina = ByteField(0x03003D6C, label="体力")
    speed = ByteField(0x03003D6D, label="速度")
    battle = ByteField(0x03003D6E, label="战斗")
    drive = ByteField(0x03003D6F, label="驾驶")
    fix = ByteField(0x03003D70, label="修理")
    # 装备、道具代码0x80以上表示装备状态
    equips = ArrayField(0x03003D91, 8, BitsField(0, 1, 0, 7))
    items = ArrayField(0x03003DB9, 8, BitsField(0, 1, 0, 7))


class Chariot(Model):
    SIZE = 8

    sp = WordField(0x03003C78, label="装甲片")
    items = ArrayField(0x03003E91, 8, BitsField(0, 1, 0, 7))
    equips = ArrayField(0x03003EE9, 8, BitsField(0, 1, 0, 7))
    bullet = ByteField(0x0300404C, label="弹仓容量")
    defense = ByteField(0x0300404A, label="守备力")
    weight = WordField(0x0300404F, label="底盘重量")
    special_bullets = ArrayField(0x03003DE1, 8, ByteField(0))  # 特殊炮弹
    special_bullets_count = ArrayField(0x03003E39, 8, ByteField(0))  # 特殊炮弹


class Global(Model):
    money = Field(0x03003C6E, label="金钱")
    battlein = ByteField(0x03003244, label="遇敌率")
    posx = ByteField(0x030042FA)
    posy = ByteField(0x030042FB)
    storage = ArrayField(0x03004106, 100, WordField(0))
