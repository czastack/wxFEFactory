from lib.hack.model import Model, Field, ByteField, WordField, ArrayField, ModelField, CAttr


class PersonChariot(Model):
    SIZE = 0

    @classmethod
    def _init_fields(cls):
        fields = []
        for key, value in cls.__dict__.items():
            if isinstance(value, Field):
                fields.append(value)
                value.origin_offset = value.offset
        cls.fields = fields

    def set_index(self, i):
        if not hasattr(self, 'fields'):
            self._init_fields()

        for field in self.fields:
            field.offset = field.origin_offset + field.size * i
            if isinstance(field, ArrayField):
                data = field.__get__(self, self.__class__)
                data.addr = self.addr + field.offset
                data.offset = field.offset


class Person(PersonChariot):
    # name = Field(0, bytes, 0xF)
    exp = Field(0x64C9, size=3)
    level = ByteField(0x647E)
    hp = WordField(0x6466)
    hpmax = WordField(0x6460)
    atk = WordField(0x646C)
    defensive = WordField(0x6472)
    strength = ByteField(0x6481)
    intelli = ByteField(0x6484)
    stamina = ByteField(0x648A)
    speed = ByteField(0x6487)
    battle = ByteField(0x648d)
    fix = ByteField(0x6490)
    drive = ByteField(0x6493)
    # 装备、道具代码0x80以上表示装备状态
    equips = ArrayField(0x6496, 8, ByteField(0))
    items = ArrayField(0x64AE, 8, ByteField(0))


class ChariotEquip(Model):
    SIZE = 11
    type = ByteField(0)


class Chariot(PersonChariot):
    sp = WordField(0x64E8)
    items = ArrayField(0x65CF, 8, ByteField(0))
    equips = ArrayField(0x6627, 8, ModelField(0, ChariotEquip))
    bullet = ByteField(0x0300404C)
    defensive = ByteField(0x0300404A)
    weight = WordField(0x0300404F)
    special_bullets = ArrayField(0x03003DE1, 8, ByteField(0)) # 特殊炮弹
    special_bullets_count = ArrayField(0x03003E39, 8, ByteField(0)) # 特殊炮弹
    main_bullets_count = ByteField(0x6535) # 主炮数量

    def set_index(self, i):
        super().set_index(i)
        field = self.field('equips')
        field.offset = field.origin_offset + i
        self.equips.addr = self.addr + field.offset
        self.equips.offset = field.offset


class Global(Model):
    money = Field(0x645D, size=3)
    battlein = ByteField(0x043F)
    posx = ByteField(0x0358)
    posy = ByteField(0x035c)
    offx = ByteField(0x0062)
    offy = ByteField(0x0063)
    storage = ArrayField(0x03004106, 100, WordField(0))
    undead = ByteField(0x647B)