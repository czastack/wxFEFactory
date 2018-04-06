from lib.hack.model import Model, Field, ByteField, WordField, ArrayField, ModelField
from ..models import ItemSlot, BasePerson, BaseGlobal


class Person(BasePerson):
    pass


class Global(BaseGlobal):
    time = Field(0x02041C9C)
    money = Field(0x02000250)
    get_money = Field(0x0203059C)
    get_exp = Field(0x020305A0)
    battlein = WordField(0x02000498)

    # 城镇中坐标
    town_x = WordField(0x02030EC6)
    town_y = WordField(0x02030ECE)
    # 世界地图中坐标
    map_x = WordField(0x02030DB6)
    map_y = WordField(0x02030DAE)
