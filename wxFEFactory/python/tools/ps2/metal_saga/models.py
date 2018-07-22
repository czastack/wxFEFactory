from lib.hack.models import Model, LookAfterModel, Field, ByteField, WordField, BitsField, ArrayField, ModelField, ToggleField, ModelPtrField


class StaticItem(Model):
    SIZE = 0x80
    name = Field(0x0, bytes, 0x10, label="名称")
    desc = WordField(0x18) # 说明偏移(+00826AE0)
    weight = WordField(0x34, label="重量")
    load = WordField(0x38, label="载重")
    atk = WordField(0x40, label="攻击")
    defense = WordField(0x48, label="C装置防御+")
    strength = WordField(0x4C, label="强度") # 防具防御力


class ItemInfo(LookAfterModel):
    SIZE = 0x30
    prev = ModelPtrField(0x0, 'self', 4, label="上一指针")
    next = ModelPtrField(0x4, 'self', 4, label="下一指针")
    item = WordField(0x8, label="种类")
    attr1 = ByteField(0x14, label="弹药数/C装置程序")
    status = ByteField(0x18, label="状态") # 1:小破, 2:大破, 4:改
    atk_addition = BitsField(0x1A, 1, 0, 4, label="攻击改造级别")
    str_addition = BitsField(0x1A, 1, 4, 4, label="强度改造级别")

    def set_field(self, name, value):
        if self.addr is 0:
            print("目标为空，无法设置")
        else:
            return super().set_field(name, value)


class Items:
    def __init__(self, head, length):
        self.head = head
        self.length = length

    def __getitem__(self, index):
        if index >= self.length:
            raise IndexError('list index out of range')
        while index < 0:
            index += self.length
        item = self.head
        i = 0
        while item.addr and i < self.length:
            if i == index:
                return item
            item = item.next
            i += 1


class Person(Model):
    SIZE = 0x0240
    name = Field(0x007F8690, bytes, 24, label="名称")
    prof = WordField(0x007F86BC, label="职业")
    level = ByteField(0x007F86C4, label="等级")
    exp = Field(0x007F86E4, label="经验")
    hpmax = WordField(0x007F86C8, label="HP最大值")
    hp = WordField(0x007F86CC, label="HP")
    atk = WordField(0x007F86D0, label="攻击")
    defense = WordField(0x007F86D4, label="防御")
    drive = ByteField(0x007F86DC, label="运转")
    title = ByteField(0x007F86EC, label="称号")
    # status = ByteField(0x007F86C0, label="状态") # 1:正常, 2:死亡 (除1外车会消失?)
    skills = ArrayField(0x007F86F4, 6, WordField(0)) # 技能
    equips = ArrayField(0x007F8744, 6, ModelPtrField(0, ItemInfo)) # 武器,头部,躯干,手臂,脚部,胸甲
    # unkown_ptr = Field(0x007F86B8)


class PersonGrow(Model):
    """角色成长值"""
    SIZE = 0x30
    hp_init = Field(0x003A7DD0, label="HP初始值")
    hp_grow = Field(0x003A7DD4, label="HP上升值")
    atk_init = Field(0x003A7DD8, label="攻击力初始值")
    atk_grow = Field(0x003A7DDC, label="攻击力上升值")
    def_init = Field(0x003A7DE0, label="防御力初始值")
    def_grow = Field(0x003A7DE4, label="防御力上升值")
    drive_init = Field(0x003A7DF0, label="运转力初始值")
    drive_grow = Field(0x003A7DF4, label="运转力上升值")


class Chariot(Model):
    SIZE = 0x100
    name = Field(0x009305C0, bytes, 24, label="名称")
    sp = WordField(0x009305F4, label="装甲")
    equiped_ptrs = ArrayField(0x009305F0, 10, Field(0)) # 装备着的装备指针, 底盘, C装置, 引擎, ?, ?, ?, ?, ?, ?, 副炮
    equip_count = ByteField(0x00930654, label="装备数量")
    first_equip = ModelPtrField(0x00930658, ItemInfo, 4) # 第一个装备指针
    # chassis = ByteField(0x7E830E, label="底盘")
    # defense = ByteField(0x7E830F, label="底盘防御")
    # weight = ByteField(0x7E8312, label="底盘重量")
    # bullet = ByteField(0x7E8314, label="弹舱")
    # hole_type = ArrayField(0x7E8325, 3, ByteField(0)) # 炮穴类型
    # items = ArrayField(0x7E8332, 8, BitsField(0, 1, 0, 7))
    # equips = ArrayField(0x7E833A, 8, ModelField(0, ItemInfo))
    # special_bullets = ArrayField(0x03003DE1, 8, ByteField(0)) # 特殊炮弹
    # special_bullets_count = ArrayField(0x03003E39, 8, ByteField(0)) # 特殊炮弹
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

    @property
    def equips(self):
        return Items(self.first_equip, 10)


class Enemy(Model):
    SIZE = 12
    hp = WordField(0x7EABDE, label="HP")


class Global(Model):
    money = Field(0x007D0A64, label="金钱")
    battlein = ByteField(0x7E0685, label="不遇敌率")
    posx = ByteField(0x0358)
    posy = ByteField(0x035c)
    offx = ByteField(0x0062)
    offy = ByteField(0x0063)
    no_battle = ToggleField(0x7E0685, size=1, enableData=0xFF, disableData=0x00, label="不遇敌")

    # wanted_status = ArrayField(0x7E910F, 16, ByteField(0)) # 0=未击破, 63=未领奖金, E3=已领奖金

    # 敌人情况
    enemys = ArrayField(0, 10, ModelField(0, Enemy))

    first_item = ModelPtrField(0x007D10A8, ItemInfo, 4) # 道具1
    static_items = ArrayField(0x007FC8D0, 0x041A, ModelField(0, StaticItem))

    battle_count = Field(0x007D0AA8, label="战斗回数")
    win_count = Field(0x007D0AAC, label="胜利回数")
    die_count = Field(0x007D0AB0, label="全灭回数")
    escape_count = Field(0x007D0AB4, label="逃亡回数")

    def iter_items(self):
        item = self.first_item
        i = 0
        while item.addr:
            yield item
            item = item.next
            i += 1
            if i >= 64:
                raise StopIteration

    @property
    def items(self):
        return Items(self.first_item, 64)
