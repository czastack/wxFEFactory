# from lib.hack.model import Model, Field, CoordField, ModelField
# from lib.lazy import lazy
from lib.utils import normalFloat
from ..gta_base.models import Physicle, Pool
import math


# class Pos(Model):
#     grad = CoordField(0)
#     looking = CoordField(0x10)
#     coord = CoordField(0x30)


# class Entity(Physicle):
#     # speed = CoordField(0x78)
#     # weight = Field(0xc0, float)
#     modelid = Field(0x2e, int, 2)

#     @property
#     def pos(self):
#         return Pos(self.handler.read32(self.addr + 0x20), self.handler)

#     @property
#     def coord(self):
#         return self.pos.coord

#     @coord.setter
#     def coord(self, value):
#         self.pos.coord = value

# class Vehicle(Entity):
#     SIZE = 0x5a8

#     hp = Field(0x200, float)
#     roll = CoordField(0x04)
#     dir = CoordField(0x14)
#     numPassengers = Field(0x1c8, int, 1)
#     maxPassengers = Field(0x1cc, int, 1)
#     door_status = Field(0x224, int, 1)
#     flags = Field(0x1f5, int, 1)
#     primaryColor = Field(0x19c, int, 1)
#     secondaryColor = Field(0x19d, int, 1)
#     type = Field(0x284, int, 4)

#     @property
#     def passengers(self):
#         offset = 0x1a8
#         for i in range(4):
#             yield Player(self.handler.read32(self.addr + offset), self.handler)
#             offset += 4

#     @property
#     def driver(self):
#         addr = self.handler.read32(self.addr + 0x1a4)
#         if addr:
#             return Player(addr, self.handler)

#     def stop(self):
#         self.speed = (0, 0, 0)

#     def flip(self):
#         self.coord[2] += 0.05
#         self.dir[0] = -self.dir[0]
#         self.dir[1] = -self.dir[1]

#     def lock_door(self):
#         self.door_status = 2

#     def unlock_door(self):
#         self.door_status = 1

#     def ignoreDamage(self, ignore=True):
#         if ignore:
#             self.flags |= 4
#         else:
#             self.flags &= (~4 & 0xFFFFFFFF)


# class Player(Entity):
#     SIZE = 0xf00

#     hp = Field(0x1f0, float)
#     ap = Field(0x2c4, float)
#     rotation = Field(0x2dc, float)
#     # stamina = Field(0x600, float)
#     isInVehicle = Field(0x314, bool, 1)
#     cur_weapon = Field(0x504, int)
#     vehicle = ModelField(0x310, Vehicle)
#     collidingCar = ModelField(0x34c, Vehicle)
#     cur_weapon_slop = Field(0x498, int, 1)

#     @lazy
#     def weapons(self):
#         return WeaponSet(self.addr + 0x35c, self.handler, 13)

#     @property
#     def cur_weapon(self):
#         return self.weapons[self.cur_weapon_slop]


class IVEntity(Physicle):
    pass


class CoordData:
    def __init__(self, obj, values):
        self.obj = obj
        self._values = list(values)

    def values(self):
        return list(self._values)

    def __getitem__(self, i):
        return self._values[i]

    def __setitem__(self, i, value):
        self._values[i] = value
        self.obj.coord = self

    def __iter__(self):
        self._pos = 0
        return self

    def __next__(self):
        if self._pos < 3:
            ret = self[self._pos]
            self._pos += 1
            return ret
        raise StopIteration

    def __str__(self):
        return __class__.name + str(self._values)


class Player(IVEntity):
    def __init__(self, index, native_call, native_context):
        self.index = index
        self.native_call = native_call
        self.native_context = native_context

    def getter(name, ret_type=int, ret_size=4):
        def getter(self):
            return self.native_call(name, 'L', self.index, ret_type=ret_type, ret_size=4)
        return getter

    def getter_ptr(name, ret_type=int, ret_size=4):
        def getter(self):
            self.native_call(name, 'LL', self.index, self.native_context.get_temp_addr())
            return self.native_context.get_temp_value(type=ret_type, size=ret_size)
        return getter

    def setter(name, ret_type=int):
        if ret_type is int:
            s = 'L'
        elif ret_type is float:
            s = 'f'
        elif ret_type is bool:
            s = '?'
        else:
            raise ValueError('ret_type not support')
        def setter(self, value):
            self.native_call(name, 'L' + s, self.index, value)
        return setter

    hp = property(getter_ptr('GET_CHAR_HEALTH'), setter('SET_CHAR_HEALTH'))
    set_max_health = setter('SET_CHAR_MAX_HEALTH')
    ap = property(getter_ptr('GET_CHAR_ARMOUR'), setter('SET_CHAR_ARMOUR'))
    money = property(getter('GET_CHAR_MONEY'), setter('SET_CHAR_MONEY'))
    gravity = property(getter('GET_CHAR_GRAVITY', float), setter('SET_CHAR_GRAVITY', float))
    set_invincible = setter('SET_CHAR_INVINCIBLE', bool)
    wanted_level = property(getter_ptr('STORE_WANTED_LEVEL'), setter('ALTER_WANTED_LEVEL'))
    isInVehicle = property(getter('IS_CHAR_IN_ANY_CAR', bool, 1))
    # 不会从摩托车上摔下来
    keep_bike = property(
        getter('GET_CHAR_CAN_BE_KNOCKED_OFF_BIKE', bool),
        setter('SET_CHAR_CAN_BE_KNOCKED_OFF_BIKE', bool)
    )

    @property
    def coord(self):
        ctx = self.native_context
        self.native_call('GET_CHAR_COORDINATES', 'L3L', self.index, ctx.get_temp_addr(1), ctx.get_temp_addr(2), ctx.get_temp_addr(3))
        values = (
            normalFloat(ctx.get_temp_value(1, float)),
            normalFloat(ctx.get_temp_value(2, float)),
            normalFloat(ctx.get_temp_value(3, float))
        )
        return CoordData(self, values)

    @coord.setter
    def coord(self, value):
        self.native_call('SET_CHAR_COORDINATES', 'L3f', self.index, *value)

    get_vehicle_addr = getter_ptr('GET_CAR_CHAR_IS_USING')

    @property
    def vehicle(self):
        addr = self.get_vehicle_addr()
        if addr:
            return Vehicle(addr, self.native_call, self.native_context)

    def give_weapon(self, weapon, ammo):
        # M4 15
        # 狙击步枪 16
        # 火箭发射器 18
        # 机枪 20
        self.native_call('GIVE_WEAPON_TO_CHAR', 'L3L', self.index, weapon, ammo, 0)

    def get_weapon_in_slot(self, slot):
        ctx = self.native_context
        self.native_call('GET_CHAR_WEAPON_IN_SLOT', 'L3L', self.index, ctx.get_temp_addr(1), ctx.get_temp_addr(2), ctx.get_temp_addr(3))
        return (
            ctx.get_temp_value(1), # weapon_type
            ctx.get_temp_value(2), # ammo
        )

    def remove_all_weapons(self):
        self.native_call('REMOVE_ALL_CHAR_WEAPONS', None)
        
    def set_char_ammo(self, weapon, ammo):
         self.native_call('SET_CHAR_AMMO', 'L2L', self.index, weapon, ammo)


class Vehicle(IVEntity):
    pass