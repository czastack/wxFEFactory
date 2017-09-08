from lib.hack.model import Model, Field


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