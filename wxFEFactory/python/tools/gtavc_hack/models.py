from lib.hack.model import Model, Field, CoordField
from ..gta_base.models import Physicle, WeaponSet, Pool
from ..gta3_base.models import BaseBlip
import math


class Entity(Physicle):
    coord = CoordField(0x34)
    speed = CoordField(0x70)
    weight = Field(0xB8, float)


class Player(Entity):
    SIZE = 0x6d8

    hp = Field(0x354, float)
    ap = Field(0x358, float)
    rotation = Field(0x378, float)
    stamina = Field(0x600, float)
    isInVehicle = Field(0x3AC, bool, 1)
    cur_weapon = Field(0x504, int, 1)
    crouch = Field(0x150, bool)
    isOnGround = Field(0x150, bool)
    model_id = Field(0xe8, int, 1)
    fastShoot = Field(0x141, int, 1)
    wanted_ptr = Field(0x5f4)

    @property
    def wanted_level(self):
        return self.handler.read32(self.wanted_ptr + 0x20)

    @wanted_level.setter
    def wanted_level(self, value):
        value = int(value)
        if value < 0 or value > 6:
            return print('wanted_level must between 1 and 6')
        wanted_ptr = self.wanted_ptr
        self.handler.write32(wanted_ptr + 0x20, value)
        self.handler.write32(wanted_ptr, (0, 200, 570, 1220, 2420, 4820)[value])

    @property
    def weapons(self):
        weaponset = getattr(self, '_weaponset', None)
        if not weaponset:
            weaponset = self._weaponset = WeaponSet(self.addr + 0x408, self.handler, 11)
        else:
            weaponset.addr = self.addr + 0x408
        return weaponset

    @property
    def vehicle(self):
        ptr = self.handler.read32(self.addr + 0x3a8)
        return Vehicle(ptr, self.handler) if ptr else None

    @property
    def nearPersons(self):
        offset = 0x56c
        for i in range(10):
            yield Player(self.handler.read32(self.addr + offset), self.handler)
            offset += 4


class Vehicle(Entity):
    SIZE = 0x5dc

    hp = Field(0x204, float)
    roll = CoordField(0x04)
    dir = CoordField(0x14)
    turn = CoordField(0x7C)
    color1 = Field(0x30, int, 1)
    color2 = Field(0x31, int, 1)
    model_id = Field(0x5c, int, 1)
    primaryColor = Field(0x1a0, int, 1)
    secondaryColor = Field(0x1a1, int, 1)
    num_passengers = Field(0x1cc, int, 1)
    max_passengers = Field(0x1d0, int, 1)
    door_status = Field(0x230, int, 1)

    @property
    def passengers(self):
        offset = 0x1ac
        for i in range(4):
            yield Player(self.handler.read32(self.addr + offset), self.handler)
            offset += 4

    @property
    def driver(self):
        addr = self.handler.read32(self.addr + 0x1a8)
        if addr:
            return Player(addr, self.handler)

    def stop(self):
        self.speed = (0, 0, 0)

    def flip(self):
        self.dir[0] = -self.dir[0]
        self.dir[1] = -self.dir[1]

    def lock_door(self):
        self.door_status = 2

    def unlock_door(self):
        self.door_status = 1


class Marker(BaseBlip):
    SIZE = 56

    color = Field(0)
    blipType = Field(4)
    entity_handle = Field(8)
    coord = CoordField(24)
    index = Field(36, size=2)
    bright = Field(38, size=1)
    active = Field(39, size=1)
    sprite = Field(52, size=1)