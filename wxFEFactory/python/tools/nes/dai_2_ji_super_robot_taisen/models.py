from lib.hack.models import Model, Field, ByteField, WordField, ArrayField, ModelField


# 76C5-01-01敌方HP(1当1)
# 76E5-01-01敌方HP(1当256)
# 7705-01-01敌方HP上限(1当1)
# 7725-01-01敌方HP上限(1当256)
# 00C0 00CB 光标X
# 00C1 00CC 光标Y


class Char(Model):
    @property
    def hp(self):
        return (self.hp_high << 8) | self.hp_low

    @hp.setter
    def hp(self, value):
        value = int(value)
        self.hp_low = value & 0xFF
        self.hp_high = (value >> 8) & 0xFF

    @property
    def hpmax(self):
        return (self.hpmax_high << 8) | self.hpmax_low

    @hpmax.setter
    def hpmax(self, value):
        value = int(value)
        self.hpmax_low = value & 0xFF
        self.hpmax_high = (value >> 8) & 0xFF


class Person(Char):
    ability = ByteField(0x73D7)
    spiritual_type = ByteField(0x7537)
    robot = ByteField(0x7557)
    map_y = ByteField(0x7597)
    map_x = ByteField(0x75B7)
    map_avatar = ByteField(0x75D7)
    weapon_1 = ByteField(0x75F7)
    weapon_2 = ByteField(0x7617)
    mobile = ByteField(0x7637)
    strength = ByteField(0x7657)
    defense = ByteField(0x7677)
    speed = ByteField(0x7697)
    hp_low = ByteField(0x76B7)
    hp_high = ByteField(0x76D7)
    hpmax_low = ByteField(0x76F7)
    hpmax_high = ByteField(0x7717)
    move = ByteField(0x7737)
    spiritual = ByteField(0x7822)
    spiritual_max = ByteField(0x782D)


# class Enemy(Char):
#     hp_low = ByteField(0x76C5)
#     hp_high = ByteField(0x76E5)
#     hpmax_low = ByteField(0x7705)
#     hpmax_high = ByteField(0x7725)


# class Weapon(Model):
#     SIZE = 6

#     AtkField = AddFieldPrep(80)
#     RangeField = AddFieldPrep(1)

#     range_max = RangeField(0)
#     hit = ByteField(1)
#     range_min = RangeField(2)
#     atk_air = AtkField(3)
#     atk_land = AtkField(4)
#     atk_sea = AtkField(5)


class Global(Model):
    money = WordField(0x743A)
    exp = WordField(0x74EF)
    items = ArrayField(0x741A, 24, ByteField(0))
    # weapons = ArrayField(0xB29D, 188, ModelField(0, Weapon))
