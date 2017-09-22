from lib.hack.model import Model, Field, CoordsField, ModelField
from lib.lazy import lazy
from ..gta_base.models import Physicle, WeaponSet, Pool
from . import address
import math


class Entity(Physicle):
    coord = CoordsField(0x34)
    speed = CoordsField(0x78)
    weight = Field(0xc0, float)
    modelid = Field(0x5c, int, 1)


class Vehicle(Entity):
    SIZE = 0x5a8

    hp = Field(0x200, float)
    roll = CoordsField(0x04)
    dir = CoordsField(0x14)
    numPassengers = Field(0x1c8, int, 1)
    maxPassengers = Field(0x1cc, int, 1)
    door_status = Field(0x224, int, 1)
    flags = Field(0x1f5, int, 1)
    primaryColor = Field(0x19c, int, 1)
    secondaryColor = Field(0x19d, int, 1)
    type = Field(0x284, int, 4)

    @property
    def passengers(self):
        offset = 0x1a8
        for i in range(4):
            yield Player(self.handler.read32(self.addr + offset), self.handler)
            offset += 4

    @property
    def driver(self):
        addr = self.handler.read32(self.addr + 0x1a4)
        if addr:
            return Player(addr, self.handler)

    def stop(self):
        self.speed = (0, 0, 0)

    def flip(self):
        self.coord[2] += 0.05
        self.dir[0] = -self.dir[0]
        self.dir[1] = -self.dir[1]

    def lockDoor(self):
        self.door_status = 2

    def unlockDoor(self):
        self.door_status = 1

    def ignoreDamage(self, ignore=True):
        if ignore:
            self.flags |= 4
        else:
            self.flags &= (~4 & 0xFFFFFFFF)


class Player(Entity):
    SIZE = 0x5f0

    hp = Field(0x2c0, float)
    ap = Field(0x2c4, float)
    rotation = Field(0x2dc, float)
    # stamina = Field(0x600, float)
    isInVehicle = Field(0x314, bool, 1)
    cur_weapon = Field(0x504, int)
    lastCar = ModelField(0x310, Vehicle)
    collidingCar = ModelField(0x34c, Vehicle)
    cur_weapon_slop = Field(0x498, int, 1)

    @lazy
    def weapons(self):
        return WeaponSet(self.addr + 0x35c, self.handler, 13)

    @property
    def cur_weapon(self):
        return self.weapons[self.cur_weapon_slop]


class Marker(Model):
    SIZE = 56

    MARKER_TYPE_CAR = 1
    MARKER_TYPE_PED = 2
    MARKER_TYPE_OBJECT = 3

    color = Field(0)
    blipType = Field(4)
    poolIndex = Field(8)
    coord = CoordsField(12)

    @property
    def entity(self):
        blipType = self.blipType
        if blipType is __class__.MARKER_TYPE_CAR:
            return Pool(address.VEHICLE_POOL, self.handler, Vehicle)[self.poolIndex >> 8]
        elif blipType is __class__.MARKER_TYPE_PED:
            return Pool(address.PED_POOL, self.handler, Player)[self.poolIndex >> 8]
        elif blipType is __class__.MARKER_TYPE_OBJECT:
            pass