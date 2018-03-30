from lib.hack.model import Model, Field, ByteField, ArrayField, ModelField, OffsetsField, ModelPtrField
from ..febase.models import ItemSlot, BaseGlobal


class Person(Model):
    SIZE = 0xA0
    prof = Field(0x44)
    level = ByteField(0x5A)
    exp = ByteField(0x5B)
    no = ByteField(0x41) # 头像、身份？
    moved = ByteField(0x94)
    posx = ByteField(0x5E)
    posy = ByteField(0x5F)
    hpmax = ByteField(0x50)
    hp = ByteField(0x5C)
    power = ByteField(0x51)
    magic = ByteField(0x52)
    skill = ByteField(0x53)
    speed = ByteField(0x54)
    defensive = ByteField(0x56)
    magicdef = ByteField(0x52)
    lucky = ByteField(0x55)
    # physical_add = ByteField(26)
    # together = ByteField(27) # 同行人物序号
    move_add = ByteField(0x5D)
    items = ArrayField(0x60, 5, ModelField(0, ItemSlot))
    proficiency = ArrayField(0x74, 6, ByteField(0)) # 武器熟练度(剑, 枪, 斧, 弓, 书, 杖) (00: -, 01: E, 1F: D, 4C: C, 88: B)
    # status = ByteField(48) # 状态种类
    # status_turn = ByteField(49) # 状态持续回合数
    # support = ArrayField(50, 10, ByteField(0)) # 支援等级


class Config(Model):
    money = Field(0x0194)
    difficulty = ByteField(0x01A9)
    character_gender = ByteField(0x0298)
    character_hair_style = ByteField(0x029D)
    character_hair_color = ByteField(0x029E)
    character_eye = ByteField(0x029F)
    character_cloth = ByteField(0x02A0)


class ItemInfo(Model):
    SIZE = 0x3C
    name_ptr = Field(0x04) # 名称指针
    desc_ptr = Field(0x08) # 介绍文本指针
    icon = ByteField(0x0C) # 图标序号
    type = ByteField(0x10) # 类型 0: 剑, 枪, 斧, 弓, 魔, 杖, 龙石, 弩车
    level = ByteField(0x12) # 要求熟练度 00: -, 01: E, 1F: D, 4C: C, 88: B
    power = ByteField(0x15) # 威力
    hit = ByteField(0x16) # 命中
    kill = ByteField(0x17) # 必杀
    weight = ByteField(0x18) # 重量
    range_min = ByteField(0x19) # 最小射程
    range_max = ByteField(0x1A) # 最大射程
    move_add = ByteField(0x1B) # 属性增加效果
    hp_add = ByteField(0x1C)
    power_add = ByteField(0x1D)
    magic_add = ByteField(0x1E)
    skill_add = ByteField(0x1F)
    speed_add = ByteField(0x20)
    lucky_add = ByteField(0x21)
    defensive_add = ByteField(0x22)
    magicdef_add = ByteField(0x23)
    attr1 = ByteField(0x24)
    attr2 = ByteField(0x25)
    attr3 = ByteField(0x26)
    attr4 = ByteField(0x27)
    attr5 = ByteField(0x28)
    attr6 = ByteField(0x29)
    attr7 = ByteField(0x2A)
    attr8 = ByteField(0x2B)
    attr9 = ByteField(0x2C)
    attr10 = ByteField(0x2D)
    attr11 = ByteField(0x2E)
    attr12 = ByteField(0x2F)


class Global(BaseGlobal):
    # chapter = ByteField(0x0202BCFA)
    # turns = WordField(0x0202BCFC)
    person_addr = Field(0x021BED30)
    curx = ByteField(0x02273BD4) # 0x02272EA4
    cury = ByteField(0x02273BD5) # 0x02272EA5
    # persons = ArrayField(0x202be48, 0xff, ModelField(0, Person))
    train_items = ArrayField(0x022C7420, 100, ModelField(0, ItemSlot)) # 运输队
    ourturn = Field(0x021CC278)
    control_enemy = Field(0x021D5674)
    upgrade_max = Field(0x02050AC0)
    upgrade_all = Field(0x02050A98)
    lv1_can_transfer = Field(0x02049EE0)
    infinite_refine = ByteField(0x02069683)
    exp_rate = Field(0x021F4DA8)
    pro_rate = Field(0x021F4F5C)
    item_consume = Field(0x02051650)
    enemy_item_drop = Field(0x021F8CE0, size=8)
    can_train = Field(0x021EBE08)
    can_visit = Field(0x021ECB14)
    can_holddown = Field(0x021EBBD8)
    use_enemy_prof = Field(0x021D4CEC)
    config = ModelPtrField(0x021BD44C, Config, 4)
    # iteminfo_base = Field(0x0227A748)
    _iteminfos = ArrayField(0x022AA97C, 0xff, ModelField(0, ItemInfo))

    @property
    def _offset(self):
        return self.handler.read32(0x021BD44C) - 0x022BEAA0

    @property
    def iteminfos(self):
        self.field('_iteminfos').offset = self.handler.read32(0x0227A748 + self._offset)
        return self._iteminfos