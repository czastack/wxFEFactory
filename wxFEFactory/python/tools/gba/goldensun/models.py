from lib.hack.models import Model, Field, ByteField, WordField, ArrayField, ModelField


class Skill(Model):
    """精神力"""
    SIZE = 4
    _value = WordField(0)

    @property
    def value(self):
        return self._value & 0x7FFF

    @value.setter
    def value(self, value):
        self._value = value


class ItemSlot(Model):
    """
    第1字节为物品种类，有几个物品会用到第二个字节 (|1)
    第二字节表示物品种类*8, |2 表示装备状态
    """

    SIZE = 2
    _item = WordField(0)
    _item1 = ByteField(0)
    _count = ByteField(1)
    value = WordField(0)

    @property
    def item(self):
        return self._item & 0b0000000111111111

    @item.setter
    def item(self, value):
        self._item = (self._item & 0b1111111000000000) | (int(value) & 0b0000000111111111)

    @property
    def count(self):
        return ((self._count & 0b11111100) >> 3) + 1

    @count.setter
    def count(self, value):
        self._count = ((int(value) - 1) << 3) | (self._count & 0b11)


class BasePerson(Model):
    SIZE = 0x14C

    name = Field(0, bytes, 0xF)
    level = ByteField(0x0F)
    exp = Field(0x124)
    hpmax = WordField(0x34)
    epmax = WordField(0x36)
    hp = WordField(0x38)
    ep = WordField(0x3A)
    atk = WordField(0x3C)
    defense = WordField(0x3E)

    ground_power = WordField(0x48)
    ground_defense = WordField(0x4A)
    water_power = WordField(0x4C)
    water_defense = WordField(0x4E)
    fire_power = WordField(0x50)
    fire_defense = WordField(0x52)
    wind_power = WordField(0x54)
    wind_defense = WordField(0x56)

    speed = WordField(0x40)
    lucky = ByteField(0x42)
    skills = ArrayField(0x58, 32, ModelField(0, Skill))
    items = ArrayField(0xD8, 15, ModelField(0, ItemSlot))
    # djinni1 = Field(0xF8)  # 精灵
    # djinni2 = Field(0x108)
    # djinni3 = Field(0x118)
    # djinni4 = Field(0x11C)
    djinni_ground = Field(0xF8)  # 地精灵
    djinni_water = Field(0xFC)  # 水精灵
    djinni_fire = Field(0x100)  # 火精灵
    djinni_wind = Field(0x104)  # 风精灵
    djinni_ground_on = Field(0x108)  # 地精灵附身状态
    djinni_water_on = Field(0x10C)  # 地精灵附身状态
    djinni_fire_on = Field(0x110)  # 地精灵附身状态
    djinni_wind_on = Field(0x114)  # 地精灵附身状态
    djinni_ground_count = ByteField(0x118)  # 拥有的精灵数
    djinni_water_count = ByteField(0x119)
    djinni_fire_count = ByteField(0x11A)
    djinni_wind_count = ByteField(0x11B)
    djinni_ground_on_count = Field(0x11C)  # 精灵附身数
    djinni_water_on_count = Field(0x11D)
    djinni_fire_on_count = Field(0x11E)
    djinni_wind_on_count = Field(0x11F)


class BaseGlobal(Model):

    @property
    def town_pos(self):
        return (self.town_x, self.town_y)

    @town_pos.setter
    def town_pos(self, value):
        self.town_x, self.town_y = value

    @property
    def map_pos(self):
        return (self.map_x, self.map_y)

    @map_pos.setter
    def map_pos(self, value):
        self.map_x, self.map_y = value
