from lib.hack.models import Model, Field, ByteField, WordField, BitsField, ArrayField, ModelField, ToggleField


class Person(Model):
    SIZE = 0x0100
    name = Field(0x7E8000, bytes, 5, label="名称")
    title = ByteField(0x7E8005, label="称号")
    level = ByteField(0x7E8006, label="等级")
    exp = Field(0x7E8013, label="经验")
    hp = WordField(0x7E800C, label="HP")
    hpmax = WordField(0x7E800A, label="HP最大值")
    atk = WordField(0x7E8039, label="攻击")
    defensive = WordField(0x7E803B, label="防御")
    battle = ByteField(0x7E8007, label="战斗LV")
    drive = ByteField(0x7E8008, label="驾驶LV")
    fix = ByteField(0x7E8009, label="修理LV")
    strength = ByteField(0x7E800E, label="腕力")
    intelli = ByteField(0x7E800F, label="知力")
    stamina = ByteField(0x7E8010, label="体力")
    speed = ByteField(0x7E8011, label="速度")
    status = ByteField(0x7E8017, label="状态")
    items = ArrayField(0x7E801A, 12, ByteField(0)) # 0x80以上表示装备状态
    equips = ArrayField(0x7E8026, 8, BitsField(0, 1, 0, 7))
    equips_raw = Field(0x7E8026, size=8)

    def equip_all(self):
        self.equips_raw |= 0x8080808080808080


class ChariotEquip(Model):
    SIZE = 8
    equip = ByteField(0, label="种类")
    defensive = ByteField(1, label="守备力")
    weight = BitsField(2, 2, bitoffset=0, bitlen=12, label="重量")
    status = BitsField(3, 1, bitoffset=4, bitlen=4, label="状态") # flag 2=损坏 4=大破 8=装备
    attr1 = WordField(4, label="攻击力/命中率/积载力")
    attr2 = ByteField(6, label="弹药数/回避率")
    ammo = ByteField(7, label="弹舱")


class Chariot(Model):
    SIZE = 0x100
    name = Field(0x7E8300, bytes, 10, label="名称")
    sp = WordField(0x7E8328, label="装甲")
    chassis = ByteField(0x7E830E, label="底盘")
    defensive = ByteField(0x7E830F, label="底盘防御")
    weight = ByteField(0x7E8312, label="底盘重量")
    bullet = ByteField(0x7E8314, label="弹舱")
    hole_type = ArrayField(0x7E8325, 3, ByteField(0)) # 炮穴类型
    items = ArrayField(0x7E8332, 8, BitsField(0, 1, 0, 7))
    equips = ArrayField(0x7E833A, 8, ModelField(0, ChariotEquip))
    special_bullets = ArrayField(0x03003DE1, 8, ByteField(0)) # 特殊炮弹
    special_bullets_count = ArrayField(0x03003E39, 8, ByteField(0)) # 特殊炮弹
    position = Field(0x7E8389, size=7, label="地图位置")
    # mapid = WordField(0x7E8389, label="所在地图")
    posx = WordField(0x7E838B, label="横坐标")
    posy = WordField(0x7E838D, label="纵坐标")
    # img = ByteField(0x7E838F, label="地图形象")

    @classmethod
    def item_type(self, id):
        if 0x00 <= id < 0x4A:
            return 'weapon'
        elif 0x4A <= id < 0x5E:
            return 'control'
        elif 0x5E <= id < 0x7F:
            return 'engine'


class Enemy(Model):
    SIZE = 12
    hp = WordField(0x7EABDE, label="HP")


class Global(Model):
    money = Field(0x7E9102, label="金钱")
    battlein = ByteField(0x7E0685, label="不遇敌率")
    posx = ByteField(0x0358)
    posy = ByteField(0x035c)
    offx = ByteField(0x0062)
    offy = ByteField(0x0063)
    no_battle = ToggleField(0x7E0685, size=1, enableData=0xFF, disableData=0x00, label="不遇敌")

    after_exp = WordField(0x7E4170, label="战后经验")
    bs_flag = WordField(0x7E4170, label="BS全功能") # 0x3FFF
    town_flag = WordField(0x7E8E28, label="村庄全开") # 0xFFFF
    map_flag = Field(0x7E8E40, type=bytes, size=32, label="村庄全开")
    chariot_flag = ByteField(0x7E8E02, label="战车情报全开") # 0xFF
    iteminfo_flag = Field(0x7E8E80, type=bytes, size=52, label="道具情报全开")
    hunting_count = ArrayField(0x7E911F, 5, Field(0)) # 怪物猎杀数量
    this_week_kill = ByteField(0x7E912F, label="本周目标击破数")
    medal_flag = WordField(0x7E8018, label="全勋章获得") # 0xFFFF

    wanted_status = ArrayField(0x7E910F, 16, ByteField(0)) # 0=未击破, 63=未领奖金, E3=已领奖金
    parter_flag = ArrayField(0x7E9106, 3, ByteField(0))
    parter_count = ByteField(0x7E9168) # 1=加入, FF=离队
    auto_battle = ToggleField(0x7E8017, size=1, enableData=0x40, disableData=0x00, label="自动战斗")

    # 敌人情况
    enemys = ArrayField(0, 10, ModelField(0, Enemy))
