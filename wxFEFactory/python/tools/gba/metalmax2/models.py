from lib.hack.model import Model, Field, ByteField, ShortField, ArrayField, ModelField


class Person(Model):
    SIZE = 24

    # name = Field(0, bytes, 0xF)
    exp = Field(0x0, size=3)
    level = ByteField(0x03003D69)
    hp = ShortField(0x03003D41)
    hpmax = ShortField(0x03003D43)
    atk = ShortField(0x03003D45)
    defensive = ShortField(0x03003D47)
    power = ByteField(0x03003D6A)
    intelli = ByteField(0x03003D6B)
    stamina = ByteField(0x03003D6C)
    speed = ByteField(0x03003D6D)
    battle = ByteField(0x03003D6E)
    drive = ByteField(0x03003D6F)
    fix = ByteField(0x03003D70)
    # 装备、道具代码0x80以上表示装备状态
    equips = ArrayField(0x03003D91, 8, ByteField(0))
    items = ArrayField(0x03003DB9, 8, ByteField(0))

    def __getattr__(self, name):
        if name.startswith('equips.'):
            index = int(name[7:])
            return self.equips[index] & 0x7F
        elif name.startswith('items.'):
            index = int(name[6:]) & 0x7F
            return self.items[index]

    def __setattr__(self, name, value):
        if name.startswith('equips.'):
            index = int(name[7:])
            self.equips[index] = 0x80 | value
        elif name.startswith('items.'):
            index = int(name[6:])
            self.items[index] = value
        else:
            super().__setattr__(name, value)


class Chariot(Model):
    SIZE = 8

    sp = ShortField(0x03003C78)
    items = ArrayField(0x03003E91, 8, ByteField(0))
    equips = ArrayField(0x03003EE9, 8, ByteField(0))
    bullet = ByteField(0x0300404C)
    defensive = ByteField(0x0300404A)
    weight = ShortField(0x0300404F)
    special_bullets = ArrayField(0x03003DE1, 8, ByteField(0)) # 特殊炮弹
    special_bullets_count = ArrayField(0x03003E39, 8, ByteField(0)) # 特殊炮弹

    def __getattr__(self, name):
        if name.startswith('equips.'):
            index = int(name[7:])
            return self.equips[index] & 0x7F
        elif name.startswith('items.'):
            index = int(name[6:])
            return self.items[index] & 0x7F
        elif name.startswith('special_bullets.'):
            index = int(name[16:])
            return self.special_bullets[index]
        elif name.startswith('special_bullets_count.'):
            index = int(name[22:])
            return self.special_bullets_count[index]

    def __setattr__(self, name, value):
        if name.startswith('equips.'):
            index = int(name[7:])
            self.equips[index] = 0x80 | value
        elif name.startswith('items.'):
            index = int(name[6:])
            self.items[index] = value
        elif name.startswith('special_bullets.'):
            index = int(name[16:])
            self.special_bullets[index] = value
        elif name.startswith('special_bullets_count.'):
            index = int(name[22:])
            self.special_bullets_count[index] = value
        else:
            super().__setattr__(name, value)


class Global(Model):
    money = Field(0x03003C6E)
    battlein = ByteField(0x03003244)
    posx = ByteField(0x030042FA)
    posy = ByteField(0x030042FB)
    storage = ArrayField(0x03004106, 100, ShortField(0))
    storage_page = 1
    page_lenth = 10

    def __getattr__(self, name):
        if name.startswith('storage.'):
            index = int(name[8:]) + self.storage_offset
            return self.storage[index]

    def __setattr__(self, name, value):
        if name.startswith('storage.'):
            index = int(name[8:]) + self.storage_offset
            self.storage[index] = value
        else:
            super().__setattr__(name, value)

    @property
    def storage_offset(self):
        return (self.storage_page - 1) * self.page_lenth