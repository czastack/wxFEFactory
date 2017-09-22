from lib.hack.model import Model, Field, OffsetsField, CoordsField
from lib.lazy import lazy
from ..gta_base.models import Physicle, WeaponSet, Pool
from . import address
import math


class Entity(Physicle):
    pass


class Player(Entity):
    SIZE = 0x6d8

    hp = Field(0x354, float)
    ap = Field(0x358, float)
    rotation = Field(0x378, float)
    coord = CoordsField(0x34)
    speed = CoordsField(0x70)
    weight = Field(0xB8, float)
    stamina = Field(0x600, float)
    isInVehicle = Field(0x3AC, bool, 1)
    cur_weapon = Field(0x504, int)
    crouch = Field(0x150, bool)
    isOnGround = Field(0x150, bool)
    modelid = Field(0xe8, int, 1)
    fastShoot = Field(0x141, int, 1)
    wanted_level = OffsetsField((0x5f4, 0x20), int, 1)

    @lazy
    def weapons(self):
        return WeaponSet(self.addr + 0x408, self.handler, 11)

    @property
    def lastCar(self):
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
    roll = CoordsField(0x04)
    dir = CoordsField(0x14)
    coord = CoordsField(0x34)
    speed = CoordsField(0x70)
    turn = CoordsField(0x7C)
    weight = Field(0xB8, float)
    color1 = Field(0x30, int, 1)
    color2 = Field(0x31, int, 1)
    modelid = Field(0x5c, int, 1)
    primaryColor = Field(0x1a0, int, 1)
    secondaryColor = Field(0x1a1, int, 1)
    numPassengers = Field(0x1cc, int, 1)
    maxPassengers = Field(0x1d0, int, 1)

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