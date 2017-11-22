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


class NativeModel:
    P = 'L'

    def __init__(self, handle, mgr):
        self.handle = handle
        self.mgr = mgr

    @property
    def native_context(self):
        return self.mgr.native_context

    @property
    def native_call(self):
        return self.mgr.native_call

    @property
    def native_call_vector(self):
        return self.mgr.native_call_vector

    @property
    def script_call(self):
        return self.mgr.script_call

    def getter(name, ret_type=int, ret_size=4):
        def getter(self):
            return self.native_call(name, self.P, self.handle, ret_type=ret_type, ret_size=ret_size)
        return getter

    def getter_ptr(name, ret_type=int, ret_size=4):
        def getter(self):
            self.native_call(name, self.P * 2, self.handle, self.native_context.get_temp_addr())
            return self.native_context.get_temp_value(type=ret_type, size=ret_size)
        return getter

    def setter(name, type_=int, default=None):
        if type_ is int:
            s = None
        elif type_ is float:
            s = 'f'
        elif type_ is bool:
            s = '?'
        else:
            raise ValueError('not support type: ' + type_.__name__)
        if default is not None:
            def setter(self, value=default):
                self.native_call(name, self.P + (s or self.P), self.handle, type_(value))
        else:
            def setter(self, value):
                self.native_call(name, self.P + (s or self.P), self.handle, type_(value))
        return setter

    @staticmethod
    def make_handle(arg):
        if isinstance(arg, int):
            return arg
        return arg.handle

    builders = (getter, getter_ptr, setter)


class NativeModel64(NativeModel):
    P = 'Q'