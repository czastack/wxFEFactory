from lib.hack.models import (
    Model, Field, FloatField, ByteField, WordField, ArrayField, ModelField, ModelPtrField, CoordField, ToggleField,
    FieldPrep
)


class ResourceManager(Model):
    SIZE = 12
    food = FloatField(0, label='食物')
    wood = FloatField(4, label='木材')
    rock = FloatField(8, label='石材')
    gold = FloatField(12, label='黄金')


class PopulationManager(Model):
    current = FloatField(0x2C, label='当前')
    total = FloatField(0x10, label='剩余')
    max = FloatField(0x80, label='上限')


class Player(Model):
    id = Field(0x9C, label='玩家ID')
    resources = ModelPtrField(0xA8, ResourceManager)


class AtkDefItem(Model):
    SIZE = 4
    type = WordField(0, label="类型")
    value = WordField(2, label="值")


class AtkDefItems(Model):
    SIZE = 24
    items = ArrayField(0, 6, ModelField(0, AtkDefItem))


class UnitType(Model):
    # type = ByteField(0x4, label="类型") # 类型
    # dll_name = WordField(0xC, label="语言DLL:名称")
    # dll_hint = WordField(0xE, label="语言DLL:创建提示")
    # id1 = WordField(0x10, label="ID 1")
    # id2 = WordField(0x12, label="ID 2")
    # id3 = WordField(0x14, label="ID 3")
    # type2 = WordField(0x16, label="类别")
    # fn_str = ModelPtrField(0x18, StringField(0), 'fn名称指针')
    # name_str = ModelPtrField(0x20, StringField(0), '名称指针')
    # dll_help = Field(0xA8, label="语言DLL:帮助说明")
    # dll_hot_text = Field(0xAC, label="语言DLL:热键文字")
    # dll_hot_text_ = Field(0xB0, label="热键文字")
    hp_max = WordField(0x2A, label="HP上限")
    view = FloatField(0x2C, label="视野")
    shipload = ByteField(0x30, label="Shipload")
    collision = FloatField(0x34, label="碰撞")
    move_speed = FloatField(0xC8, label="移动速度")
    search = FloatField(0x104, label="搜索")
    work_efficiency = FloatField(0x108, label="工作效率")
    def_items = ModelPtrField(0x128, AtkDefItems)  # 防御列表
    atk_items = ModelPtrField(0x130, AtkDefItems)  # 攻击列表
    range_max = FloatField(0x138, label="最大射程")
    damage_radius = FloatField(0x13C, label="攻击范围")
    damage_type = Field(0x140, label="伤害方式")
    atk_interval = FloatField(0x144, label="攻击间隔")  # 越小攻速越快(>0)
    atk_interval2 = FloatField(0x168, label="攻击间隔2")
    range_min = FloatField(0x15C, label="最小射程")
    base_def = WordField(0x160, label="显示的防御")
    base_atk = WordField(0x162, label="显示的攻击")
    range_base = FloatField(0x164, label="显示的射程")
    construction_time = WordField(0x182, label="建造时间")
    thrown_object = WordField(0x148, label="抛掷物单位")
    addition_thrown_object = WordField(0x1AC, label="附加抛掷物单位")
    min_thrown_object_count = WordField(0x19C, label="最小附加弹药数")
    thrown_object_area = CoordField(0x1A0, label="抛掷物产生区域")


class Unit(Model):
    type = ModelPtrField(8, UnitType)
    player = ModelPtrField(0xC, Player)
    hp = FloatField(0x30, label='HP')
    ptr_unknow1 = Field(0x18, label='不明指针')
    selected = ByteField(0x36, label='选中状态')
    resource = FloatField(0x44, label='资源')
    ptr_unknow2 = Field(0x6C, label='不明指针2')
    construction_progress = FloatField(0x1FC, label="建造进度")


class PlayerManager(Model):
    population_mgr = ModelPtrField((0x4C, 0x4, 0xA8), PopulationManager)

    v2 = Field(0x4C)
    v3 = WordField(0x94)

    @property
    def adv_selected_unit(self):
        addr = self.handler.read32(self.v2 + 4 * self.v3)
        addr = self.handler.read32(addr + 0x01C0)
        return Unit(addr, self.handler)


class Global(Model):
    player = ModelPtrField((0x00295794, 0xFC), Player)
    player_mgr = ModelPtrField((0x003912A0, 0x424), PlayerManager)
    selected_units = ArrayField(0x002B71A0, 30, ModelPtrField(0, Unit))
