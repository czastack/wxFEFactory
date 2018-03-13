from lib.hack.model import Model, Field, ByteField, ArrayField, ModelField, OffsetsField, ModelPtrField
from ..febase.models import BasePerson, ItemSlot, BaseGlobal


class Person(BasePerson):
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
    skill = ByteField(0x53)
    speed = ByteField(0x54)
    defensive = ByteField(0x56)
    magicdef = ByteField(0x52)
    lucky = ByteField(0x55)
    # physical_add = ByteField(26)
    # together = ByteField(27) # 同行人物序号
    move_add = ByteField(0x5D)
    items = ArrayField(0x60, 5, ModelField(0, ItemSlot))
    proficiency = ArrayField(0x74, 6, ByteField(0)) # 武器熟练度(剑, 枪, 斧, 弓, 书, 杖) (E级:01 D级:1F C级:47 B级:79 A级:B5 S级:FB)
    # status = ByteField(48) # 状态种类
    # status_turn = ByteField(49) # 状态持续回合数
    # support = ArrayField(50, 10, ByteField(0)) # 支援等级


class Config(Model):
    difficulty = ByteField(0x01A9)
    character_gender = ByteField(0x0298)
    character_hair_style = ByteField(0x029D)
    character_hair_color = ByteField(0x029E)
    character_eye = ByteField(0x029F)
    character_cloth = ByteField(0x02A0)


class Global(BaseGlobal):
    money = OffsetsField((0x021BD44C, 0x0194))
    # chapter = ByteField(0x0202BCFA)
    # turns = ShortField(0x0202BCFC)
    person_addr = Field(0x021BED30)
    curx = ByteField(0x02272EA4)
    cury = ByteField(0x02272EA5)
    # persons = ArrayField(0x202be48, 0xff, ModelField(0, Person))
    # train_items = ArrayField(0x0203A818, 100, ModelField(0, ItemSlot)) # 运输队
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