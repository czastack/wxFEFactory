from lib.hack.model import Model, Field, ByteField, ShortField, ArrayField, ModelField


class Person(Model):
    SIZE = 0x18

    # name = Field(0, bytes, 0xF)
    exp = Field(0x0, size=3)
    level = ByteField(0x13A)
    hp = ShortField(0x112)
    hpmax = ShortField(0x114)
    atk = ShortField(0x116)
    defensive = ShortField(0x118)
    power = ByteField(0x13B)
    intelli = ByteField(0x13C)
    stamina = ByteField(0x13D)
    speed = ByteField(0x13E)
    battle = ByteField(0x13F)
    drive = ByteField(0x140)
    fix = ByteField(0x141)
    # 装备、道具代码0x80以上表示装备状态
    equips = ArrayField(0x162, 8, ByteField(0))
    items = ArrayField(0x18A, 8, ByteField(0))

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

    sp = ShortField(0x0)
    equips = ArrayField(0x219, 8, ByteField(0))
    items = ArrayField(0x271, 8, ByteField(0))
    bullet = ByteField(0x3D4)
    defensive = ByteField(0x3D2)
    weight = ShortField(0x3D7)
    special_bullets = ArrayField(0x169, 8, ByteField(0)) # 特殊炮弹
    special_bullets_count = ArrayField(0x1C1, 8, ByteField(0)) # 特殊炮弹

    def __getattr__(self, name):
        if name.startswith('equips.'):
            index = int(name[7:])
            return self.equips[index] & 0x7F
        elif name.startswith('items.'):
            index = int(name[6:]) & 0x7F
            return self.items[index]
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