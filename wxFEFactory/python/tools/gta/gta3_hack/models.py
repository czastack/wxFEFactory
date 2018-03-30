from lib.hack.model import Model, Field, ByteField, WordField, CoordField, ManagedModelPtrField
from ..gta_base.models import Physicle, WeaponSet, Pool
from ..gta3_base.models import BaseBlip, GTA3Player, GTA3Vehicle
from . import address
import math


class Entity(Physicle):
    coord = CoordField(0x34)
    speed = CoordField(0x78)
    weight = Field(0xc0, float)
    model_id = Field(0x5c, int, 1)


class Vehicle(Entity, GTA3Vehicle):
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
            yield Player(self.handler.read32(self.addr + offset), self.context)
            offset += 4

    @property
    def driver(self):
        addr = self.handler.read32(self.addr + 0x1a4)
        if addr:
            return Player(addr, self.context)

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


class Player(Entity, GTA3Player):
    SIZE = 0x5f0

    hp = Field(0x2c0, float)
    ap = Field(0x2c4, float)
    rotation = Field(0x2dc, float)
    # stamina = Field(0x600, float)
    isInVehicle = Field(0x314, bool, 1)
    cur_weapon = Field(0x504, int)
    vehicle = ManagedModelPtrField(0x310, Vehicle)
    collidingCar = ManagedModelPtrField(0x34c, Vehicle)
    cur_weapon_slop = Field(0x498, int, 1)
    wanted_ptr = Field(0x53c)

    @property
    def weapons(self):
        return WeaponSet(self.addr + 0x35c, self.handler, 13)

    @property
    def cur_weapon(self):
        return self.weapons[self.cur_weapon_slop]

    @property
    def wanted_level(self):
        return self.handler.read32(self.wanted_ptr + 0x18)

    @wanted_level.setter
    def wanted_level(self, value):
        value = int(value)
        if value < 0 or value > 6:
            return print('wanted_level must between 0 and 6')
        wanted_ptr = self.wanted_ptr
        self.handler.write32(wanted_ptr + 0x18, value)
        self.handler.write32(wanted_ptr, (0, 60, 220, 420, 820, 1620, 3220)[value])


class Marker(BaseBlip):
    SIZE = 48

    color = Field(0)
    blipType = Field(4)
    entity_handle = Field(8)
    coord = CoordField(20)
    index = WordField(3)
    bright = ByteField(34)
    active = ByteField(35)
    sprite = ByteField(44)
