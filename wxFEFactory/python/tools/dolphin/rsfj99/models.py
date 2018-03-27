from lib.hack.model import Model, Field, ArrayField


class Global(Model):
    level = Field(0x00E464FC, size=1) # 等级
    hp = Field(0x00E464D8) # 生命
    max_hp = Field(0x00E464DC) # 最大生命
    money = Field(0x00E464F0) # 金钱
    power = Field(0x00E46500, size=2) # 力
    stamina = Field(0x00E46502, size=2) # 体力
    energy = Field(0x00E464F8) # 气力
    soul = Field(0x00E464F4) # 魂
    exp = Field(0x00E464EC) # 经验

    potion = ArrayField(0x00D850FD, 19, Field(0, size=1)) # 回复道具 (19个, 值为数量)
    consumer = ArrayField(0x00D85110, 8, Field(0, size=1)) # 消费道具 (8个, 值为数量)
    food_material = ArrayField(0x00D85118, 10, Field(0, size=1)) # 食材 (10个, 值为数量)
    decorator = ArrayField(0x00D85122, 25, Field(0, size=1)) # 装饰1 (25个, 值为1)
    book = ArrayField(0x00D8513B, 37, Field(0, size=1)) # 书物 (37个, 值为1)
    food = ArrayField(0x00D85160, 44, Field(0, size=1)) # 料理 (出现在回复道具栏，44个, 值为数量)
    blade = ArrayField(0x00D8518D, 108, Field(0, size=1)) # 刀 (108个可装备刀+6把BOSS鬼助/百姬不可装备刀, 值为1)
    decorator2 = ArrayField(0x00D851FF, 30, Field(0, size=1)) # 装饰2 (30个, 值为1)