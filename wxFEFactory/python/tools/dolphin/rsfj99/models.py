from lib.hack.model import Model, Field


class Ram(Model):
    level = Field(0x00E464FC, size=1) # 等级
    hp = Field(0x00E464D8) # 生命
    max_hp = Field(0x00E464DC) # 最大生命
    money = Field(0x00E464F0) # 金钱
    power = Field(0x00E46500, size=2) # 力
    stamina = Field(0x00E46502, size=2) # 体力
    energy = Field(0x00E464F8) # 气力
    soul = Field(0x00E464F4) # 魂
    exp = Field(0x00E464EC) # 经验

    potion = 0x00D850FC # 回复道具 (19个普通回复药+44个料理, 值为数量)
    consumer = 0x00D85110 # 消费道具 (8个, 值为数量)
    food = 0x00D85118 # 食材 (10个, 值为数量)
    decorator = 0x00D85122 # 装饰1 (25个, 值为1)
    book = 0x00D8513B # 书物 (37个, 值为1)
    blade = 0x00D8518D # 刀 (108个可装备刀+BOSS鬼助/百姬不可装备刀, 值为1)
    decorator2 = 0x00D851FF # 装饰2 (30个, 值为1)
