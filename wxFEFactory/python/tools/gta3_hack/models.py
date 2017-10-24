from lib.hack.model import Model, Field, CoordField, ModelField
from ..gta_base.models import Physicle, WeaponSet, Pool
from ..gta3_base.models import BaseBlip
from . import address
import math


class Entity(Physicle):
    coord = CoordField(0x34)
    speed = CoordField(0x78)
    weight = Field(0xc0, float)
    model_id = Field(0x5c, int, 1)


class Vehicle(Entity):
    SIZE = 0x5a8

    hp = Field(0x200, float)
    roll = CoordField(0x04)
    dir = CoordField(0x14)
    num_passengers = Field(0x1c8, int, 1)
    max_passengers = Field(0x1cc, int, 1)
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

    def lock_door(self):
        self.door_status = 2

    def unlock_door(self):
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
    vehicle = ModelField(0x310, Vehicle)
    collidingCar = ModelField(0x34c, Vehicle)
    cur_weapon_slop = Field(0x498, int, 1)

    @property
    def weapons(self):
        return WeaponSet(self.addr + 0x35c, self.handler, 13)

    @property
    def cur_weapon(self):
        return self.weapons[self.cur_weapon_slop]


class Marker(BaseBlip):
    SIZE = 48

    color = Field(0)
    blipType = Field(4)
    entity_handle = Field(8)
    coord = CoordField(20)
    index = Field(32, size=2)
    bright = Field(34, size=1)
    active = Field(35, size=1)
    sprite = Field(44, size=1)
