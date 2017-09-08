from lib.hack.model import Model, Field, OffsetsField, CoordsField
from ..gta_base.models import WeaponSet
from lib.lazy import lazy
import math


def distance(p1, p2):
    """求三围空间两点坐标"""
    return math.sqrt(
          abs(round(p1[0], 6) - round(p2[0], 6)) ** 2
        + abs(round(p1[1], 6) - round(p2[1], 6)) ** 2
        + abs(round(p1[2], 6) - round(p2[2], 6)) ** 2
    )


class Player(Model):
    SIZE = 0xdb0

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

    def distance(self, obj):
        return distance(self.coord, obj if hasattr(obj, '__iter__') else obj.coord)


class Vehicle(Model):
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

    def distance(self, obj):
        return distance(self.coord, obj if hasattr(obj, '__iter__') else obj.coord)

    def stop(self):
        self.speed = (0, 0, 0)

    def flip(self):
        self.dir[0] = -self.dir[0]
        self.dir[1] = -self.dir[1]
