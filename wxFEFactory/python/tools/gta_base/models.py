from lib.hack.model import Model, Field


def distance(p1, p2):
    """求三围空间两点坐标"""
    return math.sqrt(
          abs(round(p1[0], 6) - round(p2[0], 6)) ** 2
        + abs(round(p1[1], 6) - round(p2[1], 6)) ** 2
        + abs(round(p1[2], 6) - round(p2[2], 6)) ** 2
    )


class Physicle(Model):
    def distance(self, obj):
        return distance(self.coord, obj if hasattr(obj, '__iter__') else obj.coord)


class WeaponSet(Model):
    def __init__(self, addr, handler, size=13, item_size=24):
        super().__init__(addr, handler)
        self.size = size
        self.item_size = item_size

    def __getitem__(self, i):
        if i < 0 or i >= self.size:
            print("not available i")
            return
        return WeaponItem(self.addr + i * self.item_size, self.handler)

    def __setitem__(self, i, item):
        if i < 0 or i >= self.size:
            print("not available i")
            return
        self[i].set(item)


class WeaponItem(Model):
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