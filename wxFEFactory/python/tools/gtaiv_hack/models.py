# from lib.hack.model import Model, Field, CoordField, ModelField
# from lib.lazy import lazy
from lib.utils import normalFloat
from lib.lazy import lazy
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
    def __init__(self, index, native_call, native_context):
        self.index = index
        self.native_call = native_call
        self.native_context = native_context


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
    SIZE = 0xf00

    def __init__(self, index, ped_index, native_call, native_context):
        super().__init__(index, native_call, native_context)
        self.ped_index = ped_index

    def player_getter(name, ret_type=int, ret_size=4):
        def getter(self):
            return self.native_call(name, 'L', self.index, ret_type=ret_type, ret_size=ret_size)
        return getter

    def player_getter_ptr(name, ret_type=int, ret_size=4):
        def getter(self):
            self.native_call(name, 'LL', self.index, self.native_context.get_temp_addr())
            return self.native_context.get_temp_value(type=ret_type, size=ret_size)
        return getter

    def player_setter(name, type_=int):
        if type_ is int:
            s = 'L'
        elif type_ is float:
            s = 'f'
        elif type_ is bool:
            s = '?'
        else:
            raise ValueError('not support type: ' + type_.__name__)
        def setter(self, value):
            self.native_call(name, 'L' + s, self.index, value)
        return setter

    def getter(name, ret_type=int, ret_size=4):
        def getter(self):
            return self.native_call(name, 'L', self.ped_index, ret_type=ret_type, ret_size=ret_size)
        return getter

    def getter_ptr(name, ret_type=int, ret_size=4):
        def getter(self):
            self.native_call(name, 'LL', self.ped_index, self.native_context.get_temp_addr())
            return self.native_context.get_temp_value(type=ret_type, size=ret_size)
        return getter

    def setter(name, type_=int):
        if type_ is int:
            s = 'L'
        elif type_ is float:
            s = 'f'
        elif type_ is bool:
            s = '?'
        else:
            raise ValueError('not support type: ' + type_.__name__)
        def setter(self, value):
            self.native_call(name, 'L' + s, self.ped_index, value)
        return setter

    hp = property(getter_ptr('GET_CHAR_HEALTH'), setter('SET_CHAR_HEALTH'))
    set_max_health = setter('SET_CHAR_MAX_HEALTH')
    ap = property(getter_ptr('GET_CHAR_ARMOUR'), setter('SET_CHAR_ARMOUR'))
    money = property(player_getter_ptr('STORE_SCORE'))

    @money.setter
    def money(self, value):
        value = int(value)
        if value < 0:
            value = 0
        else:
            value -= self.money
        self.native_call('ADD_SCORE', 'LL', self.index, value)

    gravity = property(getter('GET_CHAR_GRAVITY', float), setter('SET_CHAR_GRAVITY', float))
    set_invincible = setter('SET_CHAR_INVINCIBLE', bool)

    wanted_level = property(player_getter_ptr('STORE_WANTED_LEVEL'))

    @wanted_level.setter
    def wanted_level(self, level):
        level = int(level)
        if level > 0:
            self.native_call('ALTER_WANTED_LEVEL', 'LL', self.index, level)
        else:
            self.native_call('CLEAR_WANTED_LEVEL', 'L', self.index)
        self.native_call('APPLY_WANTED_LEVEL_CHANGE_NOW', 'L', self.index)

    isInVehicle = property(getter('IS_CHAR_IN_ANY_CAR', bool, 1))
    # 不会从摩托车上摔下来
    keep_bike = property(
        getter('GET_CHAR_CAN_BE_KNOCKED_OFF_BIKE', bool),
        setter('SET_CHAR_CAN_BE_KNOCKED_OFF_BIKE', bool)
    )

    @property
    def coord(self):
        ctx = self.native_context
        self.native_call('GET_CHAR_COORDINATES', 'L3L', self.ped_index, ctx.get_temp_addr(1), ctx.get_temp_addr(2), ctx.get_temp_addr(3))
        values = (
            normalFloat(ctx.get_temp_value(1, float)),
            normalFloat(ctx.get_temp_value(2, float)),
            normalFloat(ctx.get_temp_value(3, float))
        )
        return CoordData(self, values)

    @coord.setter
    def coord(self, value):
        self.native_call('SET_CHAR_COORDINATES', 'L3f', self.ped_index, *value)

    get_vehicle_addr = getter_ptr('GET_CAR_CHAR_IS_USING')

    @property
    def vehicle(self):
        addr = self.get_vehicle_addr()
        if addr:
            return Vehicle(addr, self.native_call, self.native_context)

    # ----------------------------------------------------------------------
    # 武器相关
    # ----------------------------------------------------------------------
    def give_weapon(self, weapon, ammo):
        # M4 15
        # 狙击步枪 16
        # 火箭发射器 18
        # 机枪 20
        # WEAPON_UNARMED = 0
        # WEAPON_BASEBALLBAT = 1
        # WEAPON_POOLCUE = 2
        # WEAPON_KNIFE = 3
        # WEAPON_GRENADE = 4
        # WEAPON_MOLOTOV = 5
        # WEAPON_ROCKET = 6
        # WEAPON_PISTOL = 7
        # WEAPON_UNUSED0 = 8
        # WEAPON_DEAGLE = 9
        # WEAPON_SHOTGUN = 10
        # WEAPON_BARETTA = 11
        # WEAPON_MICRO_UZI = 12
        # WEAPON_MP5 = 13
        # WEAPON_AK47 = 14
        # WEAPON_M4 = 15
        # WEAPON_SNIPERRIFLE = 16
        # WEAPON_M40A1 = 17
        # WEAPON_RLAUNCHER = 18
        # WEAPON_FTHROWER = 19
        # WEAPON_MINIGUN = 20
        # WEAPON_EPISODIC_1 = 21
        # WEAPON_EPISODIC_2 = 22
        # WEAPON_EPISODIC_3 = 23
        # WEAPON_EPISODIC_4 = 24
        # WEAPON_EPISODIC_5 = 25
        # WEAPON_EPISODIC_6 = 26
        # WEAPON_EPISODIC_7 = 27
        # WEAPON_EPISODIC_8 = 28
        # WEAPON_EPISODIC_9 = 29
        # WEAPON_EPISODIC_10 = 30
        # WEAPON_EPISODIC_11 = 31
        # WEAPON_EPISODIC_12 = 32
        # WEAPON_EPISODIC_13 = 33
        # WEAPON_EPISODIC_14 = 34
        # WEAPON_EPISODIC_15 = 35
        # WEAPON_EPISODIC_16 = 36
        # WEAPON_EPISODIC_17 = 37
        # WEAPON_EPISODIC_18 = 38
        # WEAPON_EPISODIC_19 = 39
        # WEAPON_EPISODIC_20 = 40
        # WEAPON_EPISODIC_21 = 41
        # WEAPON_EPISODIC_22 = 42
        # WEAPON_EPISODIC_23 = 43
        # WEAPON_EPISODIC_24 = 44
        # WEAPON_CAMERA = 45
        # WEAPON_OBJECT = 46
        # WEAPON_WEAPONTYPE_LAST_WEAPONTYPE = 47
        # WEAPON_ARMOUR = 48
        # WEAPON_RAMMEDBYCAR = 49
        # WEAPON_RUNOVERBYCAR = 50
        # WEAPON_EXPLOSION = 51
        # WEAPON_UZI_DRIVEBY = 52
        # WEAPON_DROWNING = 53
        # WEAPON_FALL = 54
        # WEAPON_UNIDENTIFIED = 55
        # WEAPON_ANYMELEE = 56
        # WEAPON_ANYWEAPON = 57
        self.native_call('GIVE_WEAPON_TO_CHAR', 'L3L', self.ped_index, weapon, ammo, 0)

    def get_weapon_in_slot(self, slot):
        """
        WEAPON_SLOT_UNARMED = 0
        WEAPON_SLOT_MELEE = 1
        WEAPON_SLOT_HANDGUN = 2
        WEAPON_SLOT_SHOTGUN = 3
        WEAPON_SLOT_SMG = 4
        WEAPON_SLOT_RIFLE = 5
        WEAPON_SLOT_SNIPER = 6
        WEAPON_SLOT_HEAVY = 7
        WEAPON_SLOT_THROWN = 8
        WEAPON_SLOT_SPECIAL = 9
        WEAPON_SLOT_GIFT = 10
        WEAPON_SLOT_PARACHUTE = 11
        WEAPON_SLOT_DETONATORUNKNOWN = 12
        """
        ctx = self.native_context
        self.native_call('GET_CHAR_WEAPON_IN_SLOT', 'L4L', self.ped_index, slot, ctx.get_temp_addr(1), ctx.get_temp_addr(2), ctx.get_temp_addr(3))
        return (
            ctx.get_temp_value(1), # weapon_type
            ctx.get_temp_value(2), # ammo
        )

    def remove_all_weapons(self):
        self.native_call('REMOVE_ALL_CHAR_WEAPONS', None)
        
    def get_char_ammo(self, weapon):
        ctx = self.native_context
        self.native_call('GET_AMMO_IN_CHAR_WEAPON', 'L2L', self.ped_index, weapon, ctx.get_temp_addr())
        return ctx.get_temp_value()
        
    def set_char_ammo(self, weapon, ammo):
        self.native_call('SET_CHAR_AMMO', 'L2L', self.ped_index, weapon, ammo)

    def get_max_ammo(self, weapon):
        ctx = self.native_context
        self.native_call('GET_MAX_AMMO', 'L2L', self.ped_index, weapon, ctx.get_temp_addr())
        return ctx.get_temp_value()

    def max_ammo(self):
        for i in range(1, 12):
            weapon, ammo = self.get_weapon_in_slot(i)
            if weapon:
                self.set_char_ammo(weapon, 9999)

    weapon = property(getter_ptr('GET_CURRENT_CHAR_WEAPON'))

    @weapon.setter
    def weapon(self, weapon):
        self.native_call('SET_CURRENT_CHAR_WEAPON', 'L2L', self.ped_index, weapon, 1)

    @lazy
    def weapons(self):
        return WeaponSet(self)


class WeaponSet:
    def __init__(self, ped, size=13):
        self.ped = ped
        self.size = size

    def __getitem__(self, i):
        if i < 0 or i >= self.size:
            print("not available i")
            return
        return WeaponItem(self.ped, i)

    def __setitem__(self, i, item):
        if i < 0 or i >= self.size:
            print("not available i")
            return
        self[i].set(item)


class WeaponItem:
    def __init__(self, ped, slot):
        self.ped = ped
        self.slot = slot

    @property
    def data(self):
        return self.ped.get_weapon_in_slot(self.slot)

    @property
    def id(self):
        return self.data[0]

    @property
    def ammo(self):
        return self.data[1]

    @ammo.setter
    def ammo(self, ammo):
        self.ped.set_char_ammo(self.id, ammo)

    def set(self, other):
        if isinstance(other, WeaponItem):
            # self.id = other.id
            self.ammo = other.ammo
        elif isinstance(other, (tuple, list)):
            _, self.ammo = other


class Vehicle(IVEntity):
    SIZE = 0x5a8
    pass