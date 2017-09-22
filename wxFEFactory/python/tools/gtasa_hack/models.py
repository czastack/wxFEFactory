from lib.hack.model import Model, Field, CoordsField
from lib.lazy import lazy
from .data import VEHICLE_LIST
from ..gta_base.models import Physicle, WeaponSet, Pool
from . import address
import math


class Pos(Model):
    grad = CoordsField(0)
    looking = CoordsField(0x10)
    coord = CoordsField(0x30)


class Entity(Physicle):
    SPECIAL_BP = 2
    SPECIAL_FP = 3
    SPECIAL_DP = 6
    SPECIAL_EP = 7

    special = Field(0x42, int, 1) # bit coded for BP DP EP FP (Prevent from Explosion, Collision, Bullet, Fire)
    speed = CoordsField(0x44)
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
    def lastCar(self):
        ptr = self.handler.read32(self.addr + 0x58c)
        return Vehicle(ptr, self.handler) if ptr else None

    @property
    def carStandOn(self):
        ptr = self.handler.read32(self.addr + 0x584)
        return Vehicle(ptr, self.handler) if ptr else None

    @property
    def isInVehicle(self):
        return self._isInVehicle == 50

    @lazy
    def weapons(self):
        return WeaponSet(self.addr + 0x5a0, self.handler, 13, 28)

    @property
    def cur_weapon(self):
        return self.weapons[self.cur_weapon_slop]


class Vehicle(Entity):
    SIZE = 0xa18

    hp = Field(0x4c0, float)
    numPassengers = Field(0x484, int, 1)
    maxPassengers = Field(0x488, int, 1)
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

    def lockDoor(self):
        self.door_status = 2

    def unlockDoor(self):
        self.door_status = 1

    def flip(self):
        grad = self.grad
        grad[0] = -grad[0]
        grad[1] = -grad[1]


class Object(Entity):
    SIZE = 0x19c


class Marker(Model):
    SIZE = 40

    MARKER_TYPE_CAR = 1
    MARKER_TYPE_CHAR = 2
    MARKER_TYPE_OBJECT = 3
    MARKER_TYPE_COORDS = 4
    MARKER_TYPE_CONTACT = 5

    color = Field(0)
    poolIndex = Field(4, int)
    coord = CoordsField(8)
    _blip = Field(38, int, 1)

    @property
    def blipType(self):
        return self._blip >> 2

    @property
    def entity(self):
        blipType = self.blipType
        if blipType is __class__.MARKER_TYPE_CAR:
            return Pool(address.VEHICLE_POOL, self.handler, Vehicle)[self.poolIndex >> 8]
        elif blipType is __class__.MARKER_TYPE_CHAR:
            return Pool(address.PED_POOL, self.handler, Player)[self.poolIndex >> 8]
        elif blipType is __class__.MARKER_TYPE_OBJECT:
            pass