from lib.hack.models import Model, Field, ByteField, WordField, ArrayField, ModelField


PERSON_ATTRS = (
    (0x7A00, "体力当前值"),
    (0x7A04, "气力当前值"),
    (0x7A28, "体力最大值"),
    (0x7A2C, "气力最大值"),
    (0x7A08, "拳力"),
    (0x7A0C, "脚力"),
    (0x7A10, "武器"),
    (0x7A14, "投掷"),
    (0x7A18, "敏捷"),
    (0x7A1C, "防御"),
    (0x7A20, "力量"),
    (0x7A24, "跳跃"),
)


ENEMY_ATTRS = (
    (0x7A02, "A敌人的气力当前值"),
    (0x7A03, "A敌人的体力当前值"),
    (0x7A0B, "A敌人拳力"),
    (0x7A0F, "A敌人脚力"),
    (0x7A13, "A敌人武器"),
    (0x7A17, "A敌人投掷"),
    (0x7A1B, "A敌人敏捷"),
    (0x7A1F, "A敌人防御"),
    (0x7A23, "A敌人力量"),
    (0x7A27, "A敌人跳跃"),
    (0x7A06, "B敌人的气力当前值"),
    (0x7A07, "B敌人的体力当前值"),
    (0x7A0A, "B敌人拳力"),
    (0x7A0E, "B敌人脚力"),
    (0x7A12, "B敌人武器"),
    (0x7A16, "B敌人投掷"),
    (0x7A1A, "B敌人敏捷"),
    (0x7A1E, "B敌人防御"),
    (0x7A22, "B敌人力量"),
    (0x7A26, "B敌人跳跃"),
)


class Global(Model):
    growth_points = ByteField(0x008B)
    _money_1p = Field(0x7AE0, size=3)
    _money_2p = Field(0x7AE3, size=3)

    @property
    def money_1p(self):
        return "%X" % self._money_1p

    @money_1p.setter
    def money_1p(self, value):
        self._money_1p = int(str(value), 16)

    @property
    def money_2p(self):
        return "%X" % self._money_2p

    @money_2p.setter
    def money_2p(self, value):
        self._money_2p = int(str(value), 16)



class Person(Model):
    _locals = locals()

    for addr, name in PERSON_ATTRS:
        _locals[name] = ByteField(addr)

    del _locals


class ItemHolder(Model):
    SIZE = 16

    items = ArrayField(0x7AC0, 16, ByteField(0))

    def __getattr__(self, name):
        data = self.test_comlex_attr(name)
        if data:
            name = data.attrs[0]
            if name == 'items':
                return self.items[data.attrs[1]] & 0x7F
        return super().__getattr__(name)


class SkillHolder(Model):
    active_1 = ByteField(0x7AEB)
    active_2 = ByteField(0x7AEF)
    active_3 = ByteField(0x7B01)
    active_4 = ByteField(0x7B03)

    have_1 = ByteField(0x7C65)
    have_2 = ByteField(0x7C67)
    have_3 = ByteField(0x7C69)
    have_4 = ByteField(0x7C6B)


    # 技能激活flag 0x7AEB 0x7AEF 0x7B01 0x7B03
    # 技能拥有flag 0x7C65 0x7C67 0x7C69 0x7C6B