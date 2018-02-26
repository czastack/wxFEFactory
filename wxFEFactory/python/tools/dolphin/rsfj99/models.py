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

    potion = 0x00E0609D # 回复道具
    consumer = 0x00E060B0 # 消费道具
    blade = 0x00E06159 # 刀具
    decorator = 0x00E060C2 # 装饰
    food = 0x00E060B8 # 食物
    book = 0x00E060DB # 书物