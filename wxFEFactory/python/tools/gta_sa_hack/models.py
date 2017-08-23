from lib.hack.model import Model, Field, CoordsField
from lib.lazy import lazy
import math


def distance(p1, p2):
    """求三围空间两点坐标"""
    return math.sqrt(
          abs(round(p1[0], 6) - round(p2[0], 6)) ** 2
        + abs(round(p1[1], 6) - round(p2[1], 6)) ** 2
        + abs(round(p1[2], 6) - round(p2[2], 6)) ** 2
    )


class Pos(Model):
    grad = CoordsField(0)
    coord = CoordsField(0x30)


class SAObject(Model):
    SPECIAL_BP = 2
    SPECIAL_FP = 3
    SPECIAL_DP = 6
    SPECIAL_EP = 7

    special = Field(0x42, int, 1) # bit coded for BP DP EP FP (Prevent from Explosion, Collision, Bullet, Fire)
    speed = CoordsField(0x44)

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


class Player(SAObject):
    hp = Field(0x540, float)
    maxhp = Field(0x544, float)
    ap = Field(0x548, float)
    cur_rotation = Field(0x558, float)
    rotation = Field(0x55c, float)
    cur_weapon_slop = Field(0x718, int, 1)
    weight = Field(0x8c, float)
    # stamina = Field(0x600, float)
    # isInVehicle = Field(0x5f4, bool, 1)

    @property
    def lastCar(self):
        ptr = self.handler.read32(self.addr + 0x58c)
        return Vehicle(ptr, self.handler) if ptr else None

    @property
    def carStandOn(self):
        ptr = self.handler.read32(self.addr + 0x584)
        return Vehicle(ptr, self.handler) if ptr else None

    @lazy
    def weapons(self):
        return WeaponSet(self.addr + 0x5a0, self.handler)

    @property
    def cur_weapon(self):
        return self.weapons[self.cur_weapon_slop]

    def distance(self, obj):
        return distance(self.coord, obj if hasattr(obj, '__iter__') else obj.coord)


class Vehicle(SAObject):
    hp = Field(0x4c0, float)
    weight = Field(0x8c, float)
    numPassengers = Field(0x484, int, 1)
    maxPassengers = Field(0x488, int, 1)
    dirt = Field(0x4b0, float) # 0.0~15.0
    _tranler = Field(0x4c8, int)
    door_status = Field(0x4f8, int)

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

    def distance(self, obj):
        return distance(self.coord, obj if hasattr(obj, '__iter__') else obj.coord)

    @property
    def trailer(self):
        ptr = self._tranler
        return Vehicle(ptr, self.handler) if ptr else None

    def lockDoor(self):
        self.door_status = 2

    def unlockDoor(self):
        self.door_status = 1

    def repair(self):
        self.hp = 1000
        self.handler.write32(self.addr + 0x5b4, 0)

    def flip(self):
        grad = self.grad
        grad[0] = -grad[0]
        grad[1] = -grad[1]
        

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
    SIZE = 28

    id = Field(0x0, int) # 武器id
    state = Field(0x4, int)
    ammo_clip = Field(0x8, int) # 弹夹数
    ammo = Field(0xC, int) # 弹药数

    def set(self, other):
        if isinstance(other, WeaponItem):
            self.id = other.id
            self.ammo = other.ammo
        elif isinstance(other, (tuple, list)):
            self.id, self.ammo = other


# 有弹药数的武器分组
SLOT_HAS_AMMO = [2, 3, 4, 5, 6, 7, 8, 9]

WEAPON_NONE = ( 0, -1, "无" )

WEAPON_LIST = [
    [
        # (id, model, name)
        WEAPON_NONE,
        ( 1, 331, "指节套环" ),
    ],
    [
        WEAPON_NONE,
        ( 2, 333, "高尔夫杆" ),
        ( 3, 334, "警棍" ),
        ( 4, 335, "小刀" ),
        ( 5, 336, "棒球棍" ),
        ( 6, 337, "铁铲" ),
        ( 7, 338, "武士刀" ),
        ( 8, 339, "桌球棍" ),
        ( 9, 341, "电锯" ),
    ],
    [
        WEAPON_NONE,
        ( 22, 346, "手枪" ),
        ( 23, 347, "消音手枪" ),
        ( 24, 348, "沙漠之鹰" ),
    ],
    [
        WEAPON_NONE,
        ( 25, 349, "霰弹枪" ),
        ( 26, 350, "短管霰弹枪" ),
        ( 27, 351, "SPAZ12" ),
    ],
    [
        WEAPON_NONE,
        ( 28, 352, "乌兹" ),
        ( 29, 353, "MP5" ),
        ( 32, 372, "Tech9" ),
    ],
    [
        WEAPON_NONE,
        ( 30, 355, "AK47" ),
        ( 31, 356, "M4" ),
    ],
    [
        WEAPON_NONE,
        ( 33, 357, "打猎步枪" ),
        ( 34, 358, "狙击步枪" ),
    ],
    [
        WEAPON_NONE,
        ( 35, 359, "火箭发射器" ),
        ( 36, 360, "热感应RPG" ),
        ( 37, 361, "火焰发射器" ),
        ( 38, 362, "机枪" ),
    ],
    [
        WEAPON_NONE,
        ( 16, 342, "手榴弹" ),
        ( 17, 343, "催泪弹" ),
        ( 18, 344, "燃烧瓶" ),
        ( 39, 363, "遥控炸药包" ),
    ],
    [
        WEAPON_NONE,
        ( 41, 365, "喷雾器" ),
        ( 42, 366, "灭火器" ),
        ( 43, 367, "照相机" ),
    ],
    [
        WEAPON_NONE,
        ( 10, 321, "Dildo 1" ),
        ( 11, 322, "Dildo 2" ),
        ( 12, 323, "Vibe 1" ),
        ( 13, 324, "Vibe 2" ),
        ( 14, 325, "鲜花" ),
        ( 15, 326, "藤条" ),
    ],
    [
        WEAPON_NONE,
        ( 44, 368, "夜视镜" ),
        ( 45, 369, "热能感应器" ),
        ( 46, 371, "降落伞" ),
    ],
    [
        WEAPON_NONE,
        ( 40, 364, "Detonator" ),
    ],
]
