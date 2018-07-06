from lib.hack.models import Model, Field, ByteField, WordField, ArrayField


class Global(Model):
    level = ByteField(0x00E464FC) # 等级
    hp = Field(0x00E464D8) # 生命
    max_hp = Field(0x00E464DC) # 最大生命
    money = Field(0x00E464F0) # 金钱
    power = WordField(0x00E46500) # 力
    stamina = WordField(0x00E46502) # 体力
    energy = Field(0x00E464F8) # 气力
    soul = Field(0x00E464F4) # 魂
    exp = Field(0x00E464EC) # 经验

    potion = ArrayField(0x00D850FD, 19, ByteField(0)) # 回复道具 (19个, 值为数量)
    consumer = ArrayField(0x00D85110, 8, ByteField(0)) # 消费道具 (8个, 值为数量)
    food_material = ArrayField(0x00D85118, 10, ByteField(0)) # 食材 (10个, 值为数量)
    decorator = ArrayField(0x00D85122, 25, ByteField(0)) # 装饰1 (25个, 值为1)
    book = ArrayField(0x00D8513B, 37, ByteField(0)) # 书物 (37个, 值为1)
    food = ArrayField(0x00D85160, 44, ByteField(0)) # 料理 (出现在回复道具栏，44个, 值为数量)
    blade = ArrayField(0x00D8518D, 108, ByteField(0)) # 刀 (108个可装备刀+6把BOSS鬼助/百姬不可装备刀, 值为1)
    decorator2 = ArrayField(0x00D851FF, 30, ByteField(0)) # 装饰2 (30个, 值为1)