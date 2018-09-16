from lib.hack import utils


class AssemblyCodes:
    def __init__(self, *nodes):
        self.nodes = nodes

    def generate(self, owener, addr):
        buff = bytearray()
        for node in self.nodes:
            if isinstance(node, bytes):
                buff.extend(node)
                addr += len(node)
            elif isinstance(node, AssemblyCode):
                data = node.generate(owener, addr)
                buff.extend(data)
                addr += len(data)
        return bytes(buff)


class AssemblyCode:
    @staticmethod
    def offset(target, addr, size):
        """计算偏移
        :param size: 指令长度
        """
        diff = target - addr - size
        if abs(diff) < 0x7FFFFFFF:
            utils.u32(diff).to_bytes(4, 'little')


class Variable(AssemblyCode):
    def __init__(self, key, size=4):
        self.key = key
        self.size = size

    def generate(self, owener, addr):
        variable = owener.get_variable(self.key)
        if variable >= (1 << (self.size << 3)):
            raise ValueError('变量%s长度超过%d字节' % (self.key, self.size))
        return variable.to_bytes(self.size, 'little')


class Cmp(AssemblyCode):
    def __init__(self, target, value):
        if value > 0xFF:
            raise ValueError("暂时只支持8位立即数的值")
        self.target = target
        self.value = value

    def generate(self, owener, addr):
        target = self.target
        if isinstance(self.target, str):
            target = owener.get_variable(target)
        offset = self.offset(target, addr, 7)
        if offset:
            return b'\x83\x3D' + offset + self.value.to_bytes(1, 'little')
        else:
            if target > 0xFFFFFFFF:
                raise ValueError("cmp 83 3C 25 不支持64位地址")
            return b'\x83\x3C\x25' + target.to_bytes(4, 'little') + self.value.to_bytes(1, 'little')


class Dec(AssemblyCode):
    def __init__(self, target):
        self.target = target

    def generate(self, owener, addr):
        target = self.target
        if isinstance(self.target, str):
            target = owener.register_variable(target)
        offset = self.offset(target, addr, 6)
        if offset:
            return b'\xFF\x0D' + offset
        else:
            if target > 0xFFFFFFFF:
                raise ValueError("dec FF 0C 25 不支持64位地址")
            return b'\xFF\x0C\x25' + target.to_bytes(4, 'little')
