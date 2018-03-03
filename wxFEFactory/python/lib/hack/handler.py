from fefactory_api.emuhacker import ProcessHandler
import struct


class BigendHandler(ProcessHandler):
    """大端处理器"""
    def read(self, addr, type, size):
        if type is int:
            return self.readUint(addr, size if size else self.ptr_size)
        elif type is float:
            data = ProcessHandler.read(self, addr, bytes, size if size else 4)
            return struct.unpack('>f', data)[0]
        elif type is bool:
            return bool(self.read8(addr))
        else:
            return ProcessHandler.read(self, addr, type, size)

    def write(self, addr, data, size):
        _type = type(data)
        if _type is int:
            return self.writeUint(addr, data, size if size else self.ptr_size)
        elif _type is float:
            return ProcessHandler.write(self, addr, struct.pack('>f', data), size if size else 4)
        elif _type is bool:
            return self.write8(addr, data)
        else:
            return ProcessHandler.write(self, addr, data, size)

    def readUint(self, addr, size):
        return int.from_bytes(ProcessHandler.read(self, addr, bytes, size), 'big')

    def writeUint(self, addr, data, size):
        return ProcessHandler.write(self, addr, data.to_bytes(size, 'big'), size)

    def read16(self, addr):
        return self.readUint(addr, 2)

    def read32(self, addr):
        return self.readUint(addr, 4)

    def read64(self, addr):
        return self.readUint(addr, 8)

    def write16(self, addr, data):
        return self.writeUint(addr, data, 2)

    def write32(self, addr, data):
        return self.writeUint(addr, data, 4)

    def write64(self, addr, data):
        return self.writeUint(addr, data, 8)

    def readFloat(self, addr):
        return self.read(addr, float, 4)

    def writeFloat(self, addr, data):
        return self.write(addr, float(data), 4)
