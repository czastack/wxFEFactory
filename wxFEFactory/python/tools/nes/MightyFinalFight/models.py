from lib.hack.model import Model, Field, ByteField, WordField, ArrayField, Fields


class Global(Model):
    player = ByteField(0x0034)
    hp = ByteField(0x003A)
    life = ByteField(0x003E)
    play_level = ByteField(0x0022) # 关卡
    invincible = WordField(0x0069) # 无敌时间
    level = ByteField(0x006B)
    _exp = WordField(0x006C)
    enemy = Fields(WordField(0x032C), WordField(0x033C))
    enemy_hp = Field(0x0496, size=8) # 敌人hp, 每字节代表一个敌人
    tool_count = ByteField(0x00A9)

    @property
    def exp(self):
        return "%X" % self._exp

    @exp.setter
    def exp(self, value):
        self._exp = int(str(value), 16)

    @property
    def maxhp(self):
        return 64 + self.level * 8