from lib.hack.models import Model, Field, ByteField, WordField, BitsField, ArrayField, ModelField


PERSON_ATTRS = (
    (0x049F, "拳"),
    (0x04A3, "脚"),
    (0x04A7, "棍"),
    (0x04AB, "投掷"),
    (0x04AF, "敏捷"),
    (0x04B3, "防御"),
    (0x04B7, "力量"),
    (0x04BB, "体力"),
    (0x04BF, "生命"),
    (0x04C3, "生命上限"),
)


class Global(Model):
    growth_points = ByteField(0x008B)
    scene = ByteField(0x0042)
    _money_1p = Field(0x04C7, size=3)
    _money_2p = Field(0x04CA, size=3)

    @property
    def money_1p(self):
        return "%X0" % self._money_1p

    @money_1p.setter
    def money_1p(self, value):
        self._money_1p = int(str(int(value) // 10), 16)

    @property
    def money_2p(self):
        return "%X0" % self._money_2p

    @money_2p.setter
    def money_2p(self, value):
        self._money_2p = int(str(int(value) // 10), 16)


class Person(Model):
    _locals = locals()

    for addr, name in PERSON_ATTRS:
        _locals[name] = ByteField(addr)

    del _locals


class ItemHolder(Model):
    SIZE = 8
    items = ArrayField(0x064D, 8, BitsField(0, 1, 0, 7))
