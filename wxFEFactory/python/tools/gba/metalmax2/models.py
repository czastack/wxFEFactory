from lib.hack.model import Model, Field, ByteField, WordField, ArrayField, ModelField, CAttr


class Person(Model):
    SIZE = 24

    # name = Field(0, bytes, 0xF)
    exp = Field(0x0, size=3)
    level = ByteField(0x03003D69)
    hp = WordField(0x03003D41)
    hpmax = WordField(0x03003D43)
    atk = WordField(0x03003D45)
    defensive = WordField(0x03003D47)
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
        data = self.test_comlex_attr(name)
        if data:
            if data.name == 'equips':
                return self.equips[data.index] & 0x7F
            elif data.name == 'items':
                return self.items[data.index] & 0x7F
        return super().__getattr__(name)

    def __setattr__(self, name, value):
        data = self.test_comlex_attr(name)
        if data:
            if data.name == 'equips':
                self.equips[data.index] = 0x80 | value
                return
        
        super().__setattr__(name, value)


class Chariot(Model):
    SIZE = 8

    sp = WordField(0x03003C78)
    items = ArrayField(0x03003E91, 8, ByteField(0))
    equips = ArrayField(0x03003EE9, 8, ByteField(0))
    bullet = ByteField(0x0300404C)
    defensive = ByteField(0x0300404A)
    weight = WordField(0x0300404F)
    special_bullets = ArrayField(0x03003DE1, 8, ByteField(0)) # 特殊炮弹
    special_bullets_count = ArrayField(0x03003E39, 8, ByteField(0)) # 特殊炮弹

    def __getattr__(self, name):
        data = self.test_comlex_attr(name)
        if data:
            if data.name == 'equips':
                return self.equips[data.index] & 0x7F
            elif data.name == 'items':
                return self.items[data.index] & 0x7F
        return super().__getattr__(name)

    def __setattr__(self, name, value):
        data = self.test_comlex_attr(name)
        if data:
            if data.name == 'equips':
                self.equips[data.index] = 0x80 | value
                return
        
        super().__setattr__(name, value)


class Global(Model):
    money = Field(0x03003C6E)
    battlein = ByteField(0x03003244)
    posx = ByteField(0x030042FA)
    posy = ByteField(0x030042FB)
    storage = ArrayField(0x03004106, 100, WordField(0))
    storage_page = 1
    storage_page_lenth = 10

    @property
    def storage_offset(self):
        return (self.storage_page - 1) * self.storage_page_lenth