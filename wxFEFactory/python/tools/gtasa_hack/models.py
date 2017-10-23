from lib.hack.model import Model, Field, CoordField
from lib.lazy import lazy
from .data import VEHICLE_LIST
from ..gta_base.models import Physicle, WeaponSet, Pool
from ..gta_base.models import ManagedModel
from . import address
import math


class Pos(Model):
    grad = CoordField(0)
    looking = CoordField(0x10)
    coord = CoordField(0x30)


class Entity(Physicle):
    SPECIAL_BP = 2
    SPECIAL_FP = 3
    SPECIAL_DP = 6
    SPECIAL_EP = 7

    special = Field(0x42, int, 1) # bit coded for BP DP EP FP (Prevent from Explosion, Collision, Bullet, Fire)
    speed = CoordField(0x44)
    model_id = Field(0x22, int, 2)
    weight = Field(0x8c, float)

    @property
    def pos(self):
        return Pos(self.handler.read32(self.addr + 0x14), self.handler)

    @property
    def coord(self):
        return self.pos.coord

    @coord.setter
    def coord(self, val):
        self.pos.coord = val

    def stop(self):
        self.speed = (0, 0, 0)

    def setSpecial(self, on, bitindex):
        if on:
            self.special |= 1 << bitindex
        else:
            self.special &= ~(1 << 1)


class Player(Entity):
    SIZE = 0x7c4

    hp = Field(0x540, float)
    maxhp = Field(0x544, float)
    ap = Field(0x548, float)
    cur_rotation = Field(0x558, float)
    rotation = Field(0x55c, float)
    cur_weapon_slop = Field(0x718, int, 1)
    _isInVehicle = Field(0x530, int, 1)

    @property
    def vehicle(self):
        ptr = self.handler.read32(self.addr + 0x58c)
        return Vehicle(ptr, self.handler) if ptr else None

    @property
    def vehicle_on(self):
        """当前玩家站在其上的载具"""
        ptr = self.handler.read32(self.addr + 0x584)
        return Vehicle(ptr, self.handler) if ptr else None

    @property
    def isInVehicle(self):
        return self._isInVehicle == 50

    @property
    def weapons(self):
        weaponset = getattr(self, '_weaponset', None)
        if not weaponset:
            weaponset = self._weaponset = WeaponSet(self.addr + 0x5a0, self.handler, 13, 28)
        else:
            weaponset.addr = self.addr + 0x5a0
        return weaponset

    @property
    def cur_weapon(self):
        return self.weapons[self.cur_weapon_slop]


class Vehicle(Entity):
    SIZE = 0xa18

    hp = Field(0x4c0, float)
    num_passengers = Field(0x484, int, 1)
    max_passengers = Field(0x488, int, 1)
    dirt = Field(0x4b0, float) # 0.0~15.0
    _tranler = Field(0x4c8, int)
    door_status = Field(0x4f8, int)

    body_color = Field(0x434, int, 1)
    stripe_color = Field(0x435, int, 1)
    body2_color = Field(0x436, int, 1)
    stripe2_color = Field(0x437, int, 1)

    @property
    def name(self):
        model_id = self.model_id
        try:
            item = next(filter(lambda x: x[1] == model_id, VEHICLE_LIST))
            return item[0]
        except:
            return None

    @property
    def grad(self):
        return self.pos.grad

    @grad.setter
    def grad(self, val):
        self.pos.grad = val

    @property
    def passengers(self):
        offset = 0x460
        for i in range(9):
            yield Player(self.handler.read32(self.addr + offset), self.handler)
            offset += 4

    @property
    def driver(self):
        addr = self.handler.read32(self.addr + 0x460)
        if addr:
            return Player(addr, self.handler)

    @property
    def trailer(self):
        ptr = self._tranler
        return Vehicle(ptr, self.handler) if ptr else None

    def lock_door(self):
        self.door_status = 2

    def unlock_door(self):
        self.door_status = 1

    def flip(self):
        grad = self.grad
        grad[0] = -grad[0]
        grad[1] = -grad[1]


class Object(Entity):
    SIZE = 0x19c


class Marker(ManagedModel):
    SIZE = 40

    MARKER_TYPE_CAR = 1
    MARKER_TYPE_PED = 2
    MARKER_TYPE_OBJECT = 3
    MARKER_TYPE_COORDS = 4
    MARKER_TYPE_CONTACT = 5
    AVAILABLE_TYPE = (MARKER_TYPE_CAR, MARKER_TYPE_PED)

    color = Field(0)
    entity_handle = Field(4, int)
    coord = CoordField(8)
    sprite = Field(36, int, 1)
    flags1 = Field(37, int, 1)
    flags2 = Field(38, int, 1)

    @property
    def bright(self):
        return self.flags1 & 1

    @property
    def blipType(self):
        return self.flags2 >> 2

    @property
    def entity(self):
        blipType = self.blipType
        index = self.entity_handle >> 8
        if blipType is __class__.MARKER_TYPE_CAR:
            return self.mgr.vehicle_pool[index]
        elif blipType is __class__.MARKER_TYPE_PED:
            return self.mgr.ped_pool[index]
        elif blipType is __class__.MARKER_TYPE_OBJECT:
            return self.mgr.object_pool[index]