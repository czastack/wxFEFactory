from lib.hack.model import Model, Field, CoordsField, ModelField
from lib.lazy import lazy
import math


def distance(p1, p2):
    """求三围空间两点坐标"""
    return math.sqrt(
          abs(round(p1[0], 6) - round(p2[0], 6)) ** 2
        + abs(round(p1[1], 6) - round(p2[1], 6)) ** 2
        + abs(round(p1[2], 6) - round(p2[2], 6)) ** 2
    )


class Entity(Model):
    coord = CoordsField(0x34)
    speed = CoordsField(0x78)
    weight = Field(0xc0, float)
    modelid = Field(0x5c, int, 1)

    def distance(self, obj):
        return distance(self.coord, obj if hasattr(obj, '__iter__') else obj.coord)


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
        return Player(self.handler.read32(self.addr + 0x1a4), self.handler)

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
    SIZE = 0xbe0

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
        return WeaponSet(self.addr + 0x35c, self.handler)

    @property
    def cur_weapon(self):
        return self.weapons[self.cur_weapon_slop]


class WeaponSet(Model):

    def __getitem__(self, i):
        if i < 0 or i > 12:
            print("not available i")
            return
        return WeaponItem(self.addr + i * WeaponItem.SIZE, self.handler)

    def __setitem__(self, i, item):
        if i < 0 or i > 12:
            print("not available i")
            return
        self[i].set(item)


class WeaponItem(Model):
    SIZE = 24

    id = Field(0) # 武器id
    state = Field(0x4, int)
    ammo_clip = Field(0x8, int) # 弹夹数
    ammo = Field(0xC, int) # 弹药数

    def set(self, other):
        if isinstance(other, WeaponItem):
            self.id = other.id
            self.ammo = other.ammo
        elif isinstance(other, (tuple, list)):
            self.id, self.ammo = other