from lib.hack.models import Model, Field, ByteField, ArrayField, ModelField, ModelPtrField, ToggleField
from ..models import ItemSlot, BaseGlobal


class Character(Model):
    SIZE = 0xA8
    prof = Field(0x44)
    level = ByteField(0x6A)
    level_limit = ByteField(0x63)
    exp = ByteField(0x6B)
    no = ByteField(0x41)  # 头像、身份？
    moved = ByteField(0x9C)
    posx = ByteField(0x6E)
    posy = ByteField(0x6F)
    hpmax = ByteField(0x50)  # TODO
    hp = ByteField(0x6C)
    power = ByteField(0x51)
    magic = ByteField(0x52)
    skill = ByteField(0x53)
    speed = ByteField(0x54)
    lucky = ByteField(0x55)
    defense = ByteField(0x56)
    magicdef = ByteField(0x57)
    move_add = ByteField(0x6D)
    items = ArrayField(0x70, 5, ModelField(0, ItemSlot))
    proficiency = ArrayField(0x84, 6, ByteField(0))  # 武器熟练度(剑, 枪, 斧, 弓, 书, 杖) (00: -, 01: E, 1F: D, 4C: C, 88: B)


class Config(Model):
    money = Field(0x0190)
    difficulty = ByteField(0x01A5)
    character_gender = False


class ItemInfo(Model):
    SIZE = 0x3C
    name_ptr = Field(0x04)  # 名称指针
    desc_ptr = Field(0x08)  # 介绍文本指针
    icon = ByteField(0x0C)  # 图标序号
    type = ByteField(0x10)  # 类型 0: 剑, 枪, 斧, 弓, 魔, 杖, 龙石, 弩车
    level = ByteField(0x12)  # 要求熟练度 00: -, 01: E, 1F: D, 4C: C, 88: B
    power = ByteField(0x15)  # 威力
    hit = ByteField(0x16)  # 命中
    kill = ByteField(0x17)  # 必杀
    weight = ByteField(0x18)  # 重量
    range_min = ByteField(0x19)  # 最小射程
    range_max = ByteField(0x1A)  # 最大射程
    move_add = ByteField(0x1B)  # 属性增加效果
    hp_add = ByteField(0x1C)
    power_add = ByteField(0x1D)
    magic_add = ByteField(0x1E)
    skill_add = ByteField(0x1F)
    speed_add = ByteField(0x20)
    lucky_add = ByteField(0x21)
    defense_add = ByteField(0x22)
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
    character_addr = Field(0x021986F4)
    curx = ByteField(0x02273BD4)  # 0x02272EA4  # TODO
    cury = ByteField(0x02273BD5)  # 0x02272EA5  # TODO
    # characters = ArrayField(0x202be48, 0xff, ModelField(0, Character))
    train_items = ArrayField(0x021986D0, 100, ModelField(0, ItemSlot))  # 运输队
    ourturn = ToggleField(0x021A9674, enable=0xE2812000, disable=0xE2812001)
    control_enemy = ToggleField(0x021B1830, enable=0xE1500000, disable=0xE1510000)
    upgrade_max = ToggleField(0x0203C474, enable=0xE1A09005, disable=0xB2899001)
    upgrade_all = ToggleField(0x0203C44C, enable=0xE1A00000, disable=0xAA000009)
    lv1_can_transfer = ToggleField(0x02049EE0, enable=0x00000001, disable=0xE350000A)
    can_train = ToggleField(0x021C6F7C, enable=0xE3A00002, disable=0xEBF9D152)
    can_visit = ToggleField(0x021ECB14, enable=0xE3A00002, disable=0xEBF98B4C)  # TODO
    can_holddown = ToggleField(0x021C6E0C, enable=0xEBF9A61E, disable=0xEBF9D1AE)
    use_enemy_prof = ToggleField(0x021D4CEC, enable=0xEA000022, disable=0x1A000022)
    infinite_refine = ToggleField(0x02052618, size=2, enable=0, disable=0x0A01)
    item_consume = ToggleField(0x0203CDD0, size=2, enable=0x0000, disable=0x0001)
    enemy_item_drop = ToggleField(0x021D3114, size=8, enable=0xE3500000E1D006B0, disable=0xE3500020E5D10003)
    exp_rate = Field(0x021CFACC)
    pro_rate = Field(0x021CFC78)
    config = ModelPtrField(0x02198120, Config, 4)
    _iteminfos = ArrayField(0x022494E0, 0xff, ModelField(0, ItemInfo))

    difficulty = ByteField(0x0227E6E5)  # 0201FF8C E3A00000
    always_level_up = ToggleField(0x021CFAC4, enable=0xE3A02064, disable=0xE5D1206B)

    @property
    def _offset(self):
        return self.handler.read32(0x021BD44C) - 0x022BEAA0

    @property
    def iteminfos(self):
        self.field('_iteminfos').offset = self.handler.read32(0x0227A748 + self._offset)
        return self._iteminfos
