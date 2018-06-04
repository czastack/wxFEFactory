from lib.hack.model import Model, Field, ByteField, WordField, ArrayField, ModelField


# 76C5-01-01敌方HP(1当1)
# 76E5-01-01敌方HP(1当256)
# 7705-01-01敌方HP上限(1当1)
# 7725-01-01敌方HP上限(1当256)
# 00C0 00CB 光标X
# 00C1 00CC 光标Y


ENEMY_ATTRS = (

)


class Global(Model):
    money = WordField(0x743A)
    exp = WordField(0x74EF)


class Person(Model):
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



#0 741A-01-FF超合金Z(加1点防卫)
#0 741B-01-FF磁性涂料(加1点速度)
#0 741C-01-FF传感器(加1点强度)
#0 741D-01-FFC装甲(加5点HP)
#0 741E-01-FF超合金W(加3点防卫)
#0 741F-01-FF助推器(加1点移动)
#0 7420-01-FF喷气机翼(将部队变为空军)
#0 7421-01-FF传感器Ⅱ(加3点强度)
#0 7422-01-FFM合金(加3点速度)
#0 7423-01-FF电子盾(加10点HP)
#0 7424-01-FF米诺夫粒子(一回降低全敌50%命中率)
#0 7425-01-FF正义(补充20点精神)
#0 7426-01-FF医治(补充100点精神)
#0 7427-01-FF维修(全体补充1~150点HP)
#0 7428-01-FF斗志(一回合攻击力翻一倍)
#0 7429-01-FF疾风(一回合加3格移动力)
#0 742A-01-FF勇气(补充100点HP)
#0 742B-01-FF愤怒(对单人造成1~200伤害)
#0 742C-01-FF瞄准(一回合增加单人10%命中率)
#0 742D-01-FF根基(加经验1~255)
#0 742E-01-FF地雷(直接升到50级)
#0 742F-01-FF探雷器(效果不明)
#0 7430-01-FFG零件(用于刚达变形)
#0 7431-01-FF非尔卡(效果不明)