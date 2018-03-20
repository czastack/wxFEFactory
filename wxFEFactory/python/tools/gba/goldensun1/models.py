from lib.hack.model import Model, Field, ByteField, ShortField, ArrayField, ModelField


class ItemSlot(Model):
    """
    第1字节为物品种类，有几个物品会用到第二个字节 (|1)
    第二字节表示物品种类*8, |2 表示装备状态
    """

    SIZE = 2
    _item = ShortField(0)
    _item1 = ByteField(0)
    _count = ByteField(1)
    value = ShortField(0)

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
        self._count = ((int(value) - 1) << 3 ) | (self._count & 0b11)


class Person(Model):
    SIZE = 0x14C

    skills_page = 1
    skills_page_length = 5

    name = Field(0, bytes, 0xF)
    level = ByteField(0x0F)
    exp = Field(0x124)
    hp = ShortField(0x34)
    ep = ShortField(0x36)
    hpmax = ShortField(0x38)
    epmax = ShortField(0x3A)
    atk = ShortField(0x3C)
    defensive = ShortField(0x3E)
    speed = ShortField(0x40)
    lucky = ByteField(0x42)
    skills = ArrayField(0x58, 32, Field(0))
    items = ArrayField(0xD8, 15, ModelField(0, ItemSlot))
    elf1 = ByteField(0xF8) # 精灵
    elf2 = ByteField(0x108)
    elf3 = ByteField(0x118)
    elf4 = ByteField(0x11C)


    def __getattr__(self, name):
        if name.startswith('items.'):
            index = int(name[6:])
            return self.items[index].item
        elif name.startswith('items_count.'):
            index = int(name[12:])
            return self.items[index].count
        elif name.startswith('skills.'):
            index = int(name[7:]) + self.skills_offset
            if index < self.field('skills').length:
                return self.skills[index]
            return 0

    def __setattr__(self, name, value):
        if name.startswith('items.'):
            index = int(name[6:])
            self.items[index].item = value
        elif name.startswith('items_count.'):
            index = int(name[12:])
            self.items[index].count = value
        elif name.startswith('skills.'):
            index = int(name[7:]) + self.skills_offset
            if index < self.field('skills').length:
                self.skills[index] = value
        else:
            super().__setattr__(name, value)

    @property
    def skills_offset(self):
        return (self.skills_page - 1) * self.skills_page_length


class Global(Model):
    time = Field(0x02041C9C)
    money = Field(0x02000250)
    get_money = Field(0x0203057C)
    get_exp = Field(0x02030580)
    battlein = ShortField(0x0200047A)

    # 城镇中坐标
    town_x = ShortField(0x02030EC6)
    town_y = ShortField(0x02030ECE)
    # 世界地图中坐标
    map_x = ShortField(0x02030DB6)
    map_y = ShortField(0x02030DAE)

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