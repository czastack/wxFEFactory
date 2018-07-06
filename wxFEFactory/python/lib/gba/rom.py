from .file import FileRW

ROM_MASK = ~(1<<27)


class RomHandler:
    __slots__ = ()

    def getRomTitle(self):
        return self.read(0xA0, bytes, 12).decode()

    def getRomCode(self):
        return self.read(0xAC, bytes, 4).decode()


class BaseRomRW(FileRW):

    def __init__(self, path, addrmask=ROM_MASK, mode=None):
        FileRW.__init__(self, path, addrmask, mode)


class RomRW(BaseRomRW):
    pass


class RomProxyRW:
    ROM_START = 0x08000000

    def __init__(self, reader):
        self.reader = reader

    def address_map(self, addr):
        return addr | 0x08000000

    def read8(self, addr):
        return self.reader.read8(self.address_map(addr))

    def read16(self, addr):
        return self.reader.read16(self.address_map(addr))

    def read32(self, addr):
        return self.reader.read32(self.address_map(addr))

    def write8(self, addr, data):
        return self.reader.write8(self.address_map(addr), data)

    def write16(self, addr, data):
        return self.reader.write16(self.address_map(addr), data)

    def write32(self, addr, data):
        return self.reader.write32(self.address_map(addr), data)

    def read(self, addr, type, size):
        return self.reader.read(self.address_map(addr), type, size)

    def write(self, addr, data, size=0):
        return self.reader.write(self.address_map(addr), data)

    def add(self, addr, n):
        return self.reader.add(self.address_map(addr), n)
