from lib.hack.model import Model, Field
import math


def distance(p1, p2):
    """求三围空间两点坐标"""
    return math.sqrt(
          abs(round(p1[0], 6) - round(p2[0], 6)) ** 2
        + abs(round(p1[1], 6) - round(p2[1], 6)) ** 2
        + abs(round(p1[2], 6) - round(p2[2], 6)) ** 2
    )


class ManagedModel(Model):
    def __init__(self, addr, mgr):
        super().__init__(addr, mgr.handler)
        self.mgr = mgr


class Physicle(Model):
    def distance(self, obj):
        return distance(self.coord, obj if hasattr(obj, '__iter__') else obj.coord)

    def stop(self):
        self.speed = (0, 0, 0)

    def get_offset_coord_m(self, offset):
        """手动获取偏移后的坐标"""
        coord = self.coord.values()
        coord[0] += offset[0]
        coord[1] += offset[1]
        coord[2] += offset[2]
        return coord

    get_offset_coord = get_offset_coord_m


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


class Pool(Model):
    _start = Field(0)
    _size = Field(8)

    def __init__(self, ptr, handler, item_class=None):
        super().__init__(handler.read32(ptr), handler)
        self.item_class = item_class
        self._i = 0
        self.start = self._start
        self.size = self._size

    def __getitem__(self, i):
        if self.item_class:
            return self.item_class(self.addr_at(i), self.handler)

    def addr_at(self, i):
        return self.start + i * self.item_class.SIZE

    def __iter__(self):
        self._i = 0
        return self

    def __next__(self):
        if self._i == self.size:
            raise StopIteration

        item = self[self._i]
        self._i += 1
        return item