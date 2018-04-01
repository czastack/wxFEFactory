from functools import partial


class FileRW:
    __slots__ = ('_file', 'addrmask')

    MODE = 'rb'

    def __init__(self, path, addrmask=-1, mode=None):
        self._file = open(path, mode or self.MODE)
        self.addrmask = addrmask

    def close(self):
        self._file.close()

    __del__ = close

    def __getattr__(self, name):
        try:
            return getattr(self._file, name)
        except AttributeError:
            raise

    def pos(self, offset):
        if self.addrmask != -1:
            offset &= self.addrmask
        self._file.seek(offset)
        return self

    def rawRead(self, size):
        return self._file.read(size)

    def read(self, addr, type, size=1):
        return self.pos(addr).rawRead(size)

    def readUint(self, pos, size, signed=False):
        if pos is not None:
            self.pos(pos)
        return int.from_bytes(self._file.read(size), byteorder='little', signed=signed)

    def writeUint(self, pos, value, size, signed=False):
        if value is None:
            value = pos
        elif pos is not None:
            self.pos(pos)
        return self._file.write(value.to_bytes(size, byteorder='little', signed=signed))

    def readInt(self, addr, size=4):
        return self.readUint(addr, size, signed=True)

    def writeInt(self, addr, data, size=4):
        return self.writeUint(addr, data, size, signed=True)

    def read8(self, pos=None):
        return self.readUint(pos, 1)

    def read16(self, pos=None):
        return self.readUint(pos, 2)

    def read32(self, pos=None):
        return self.readUint(pos, 4)

    def rawWrite(self, data):
        return self._file.write(data)

    def write(self, addr, data, size=0):
        if size:
            data = data[:size]
        return self.pos(addr).rawWrite(data)

    def write8(self, pos, value=None):
        return self.writeUint(pos, value, 1)

    def write16(self, pos, value=None):
        return self.writeUint(pos, value, 2)

    def write32(self, pos, value=None):
        return self.writeUint(pos, value, 4)

    def patchFile(self, addr, file, offset=0, size=-1):
        with open(file, 'rb') as f:
            if offset:
                f.seek(offset)
            self.write(addr, f.read(size))