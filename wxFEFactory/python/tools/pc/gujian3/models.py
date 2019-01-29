from lib.hack.models import Model, Field, Fields, ByteField, WordField, FloatField, CoordField


class Global(Model):
    energy = FloatField(0xAE4, label="体力 f 3.39")
    vigour = FloatField(0xAB4, label="元气 f 5.23")
    health = Field(0xA98, label="元精 4 2346")
    skill = Field(0xB18, label="战意技 4 1000 截风100")
    atk = Field(0xB88, label="攻击 9999")
    defense = Field(0xBB8, label="防御")
    critical_buff = Field(0xBE8, label="爆击伤害加成 999")
    critical = Field(0xBF0, label="暴击率")
    attr_wood = Field(0xC10, label="木属性")
    attr_fire = Field(0xC30, label="火属性")
    attr_earth = Field(0xC50, label="土属性")
    attr_metal = Field(0xC70, label="金属性")
    attr_water = Field(0xC90, label="水属性")
    # Field(0x6D0, label="防守移动 防守0 正常1")
    # Field(0x8A8, label="攻击方式 普通攻击 10001")


class Movement(Model):
    coord = CoordField(0, label='坐标')
    air_time = FloatField(-0x14, label='空中滞留时间')  # 初始30, 减慢为15
    jump_height = FloatField(-0x18, label='跳跃高度')
    move_speed_mult = FloatField(-0x38, label='移动速度倍数')
