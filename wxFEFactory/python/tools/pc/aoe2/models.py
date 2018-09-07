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
    SIZE = 0
    current = FloatField(0x2C, label='当前')
    total = FloatField(0x10, label='剩余')
    max = FloatField(0x80, label='上限')


class Player(Model):
    SIZE = 0
    id = Field(0x9C, label='玩家ID')
    resources = ModelPtrField(0xA8, ResourceManager)


class UnitType(Model):
    hp_max = WordField(0x2A, label="HP上限")
    view = FloatField(0x2C, label="视野")
    shipload = ByteField(0x30, label="Shipload")
    collision = FloatField(0x34, label="碰撞")
    move_speed = FloatField(0xC8, label="移动速度")
    search = FloatField(0x104, label="搜索")
    work_efficiency = FloatField(0x108, label="工作效率")
    short_def = WordField((0x128, 2), label="近战防御")  # 近战防御指针(+2=近战防御)
    atk = WordField((0x130, 6), label="对人攻击力")  # 攻击力指针？(+6=攻击)
    atk2 = WordField((0x130, 10), label="对建筑攻击力")
    atk3 = WordField((0x130, 14), label="攻击力3")
    range_max = FloatField(0x138, label="最大射程")
    damage_radius = FloatField(0x13C, label="攻击范围")
    damage_type = Field(0x140, label="伤害方式")
    atk_spped = FloatField(0x144, label="攻击硬直")  # 越小攻速越快(>0)
    range_min = FloatField(0x15C, label="最小射程")
    base_def = WordField(0x160, label="基础防御")
    base_atk = WordField(0x162, label="基础攻击")
    range_base = FloatField(0x164, label="基础射程")
    construction_time = WordField(0x182, label="建造时间")

    def far_def_addr(self, field):
        """获取远程防御地址"""
        # 在近战防御基地址开始，往后对齐4字节检查数值3，3的后两个字节就是远程防御地址
        addr = self.handler.read_addr(self.addr + 0x128) + 4
        for i in range(3):
            if self.handler.read16(addr) == 3:
                return addr + 2
            addr += 4

    far_def = WordField(far_def_addr, label="远程防御")


class Unit(Model):
    SIZE = 0
    type = ModelPtrField(8, UnitType)
    player = ModelPtrField(0xC, Player)
    hp = FloatField(0x30, label='HP')
    ptr_unknow1 = Field(0x18, label='不明指针')
    selected = ByteField(0x36, label='选中状态')
    resource = FloatField(0x44, label='资源')
    ptr_unknow2 = Field(0x6C, label='不明指针2')
    player_class = WordField((0xC, 0x9C), label='Player Class')
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
