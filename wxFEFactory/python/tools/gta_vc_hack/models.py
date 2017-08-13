from lib.hack.model import Model, Field, CoordsField
import math


def distance(p1, p2):
    """求三围空间两点坐标"""
    return math.sqrt(
          abs(round(p1[0], 6) - round(p2[0], 6)) ** 2
        + abs(round(p1[1], 6) - round(p2[1], 6)) ** 2
        + abs(round(p1[2], 6) - round(p2[2], 6)) ** 2
    )


class Player(Model):
    PLAYER1 = 0
    PLAYER2 = 1
    PLAYER3 = 2
    PLAYER4 = 3
    CIVMALE = 4
    CIVFEMALE = 5
    COP = 6
    GANG1 = 7
    GAMG2 = 8
    GANG3 = 9
    GANG4 = 10
    GANG5 = 11
    GANG6 = 12
    GANG7 = 13
    GANG8 = 14
    GANG9 = 15
    EMERGENCY = 16
    FIREMAN = 17
    CRIMINAL = 18
    SPECIAL = 1

    hp = Field(0x354, float)
    ap = Field(0x358, float)
    rotation = Field(0x378, float)
    coord = CoordsField(0x34)
    speed = CoordsField(0x70)
    weight = Field(0xB8, float)
    stamina = Field(0x600, float)
    isInVehicle = Field(0x5f4, bool, 1)
    cur_weapon = Field(0x504, int)
    crouch = Field(0x150, bool)
    isOnGround = Field(0x150, bool)
    modelid = Field(0xe8, int, 1)
    fastShoot = Field(0x141, int, 1)

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

    @property
    def wantedLevel(self):
        wanted_ptr = self.handler.read32(self.addr + 0x5f4)
        if wanted_ptr:
            return self.handler.read32(wanted_ptr + 0x20)

    @wantedLevel.setter
    def wantedLevel(self, val):
        wanted_ptr = self.handler.read32(self.addr + 0x5f4)
        if wanted_ptr:
            return self.handler.write(wanted_ptr + 0x20, val)

    def getWeapon(self, i):
        if i < 0 or i > 5:
            print("not available i")
            return
        return self.handler.read32(self.addr + 0x408 + i * 4)

    def setWeapon(self, i, weapon):
        if i < 0 or i > 5:
            print("not available i")
            return
        return self.handler.write32(self.addr + 0x408 + i * 4, weapon)

    def distance(self, obj):
        return distance(self.coord, obj if hasattr(obj, '__iter__') else obj.coord)


class Vehicle(Model):
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


class Weapon:
    NONE = 0
    BRASSKNUCKLE = 1
    SCREWDRIVER = 2
    GOLFCLUB = 3
    NITESTICK = 4
    KNIFECUR = 5
    BAT = 6
    HAMMER = 7
    CLEAVER = 8
    MACHETE = 9
    KATANA = 10
    CHNSAW = 11
    GRENADE = 12
    BOMB = 13
    TEARGAS = 14
    MOLOTOV = 15
    MISSILE = 16
    COLT45 = 17
    PYTHON = 18
    CHROMEGUN = 19
    SHOTGSPA = 20
    BUDDYSHOT = 21
    TEC9 = 22
    UZI = 23
    INGRAMS1 = 24
    MP5LGN = 25
    M4 = 26
    RUGER = 27
    SNIPER = 28
    LASER = 29
    ROCKETLA = 30
    FLAME = 31
    M60 = 32
    MINIGUN = 33
    DETONATOR = 34
    HELIGUN = 35
    CAMERA = 3