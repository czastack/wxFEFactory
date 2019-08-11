from lib.hack import utils


class AssemblyGroup:
    """节点组合"""
    def __init__(self, *nodes):
        self.nodes = nodes

    def generate(self, owner, context):
        buff = bytearray()
        for node in self.nodes:
            if isinstance(node, bytes):
                buff.extend(node)
                context.addr += len(node)
            elif isinstance(node, AssemblyNode):
                data = node.generate(owner, context)
                buff.extend(data)
                context.addr += len(data)
        return bytes(buff)


class AssemblyNode:
    """汇编节点"""
    @staticmethod
    def offsetof(target, addr, size):
        """计算偏移
        :param size: 指令长度
        """
        diff = target - addr - size
        if abs(diff) < 0x7FFFFFFF:
            return utils.u32(diff).to_bytes(4, 'little')

    def get_target(self, owner):
        """获取目标符号(变量地址)"""
        target = self.target
        if isinstance(self.target, str):
            target = owner.get_variable(target).addr
        return target

    def generate(self, owner, context):
        return b''


class Variable(AssemblyNode):
    """写入变量地址"""
    def __init__(self, key):
        self.key = key

    def generate(self, owner, context):
        size = 4 if owner.is32process else 8
        addr = owner.get_variable(self.key).addr
        if addr >= (1 << (size << 3)):
            raise ValueError('变量%s长度超过%d字节' % (self.key, size))
        return addr.to_bytes(size, 'little')


class Cmp(AssemblyNode):
    """比较节点"""
    def __init__(self, target, value):
        if value > 0xFF:
            raise ValueError("暂时只支持8位立即数的值")
        self.target = target
        self.value = value

    def generate(self, owner, context):
        target = self.get_target(owner)
        if owner.is32process:
            return b'\x83\x3D' + target.to_bytes(4, 'little') + self.value.to_bytes(1, 'little')
        else:
            offset = self.offsetof(target, context.addr, 7)
            if offset:
                return b'\x83\x3D' + offset + self.value.to_bytes(1, 'little')
            else:
                if target > 0xFFFFFFFF:
                    raise ValueError("cmp 83 3C 25 不支持64位地址" + hex(target))
                return b'\x83\x3C\x25' + target.to_bytes(4, 'little') + self.value.to_bytes(1, 'little')


class Dec(AssemblyNode):
    """自减节点"""
    def __init__(self, target):
        self.target = target

    def generate(self, owner, context):
        target = self.get_target(owner)
        offset = self.offsetof(target, context.addr, 6)
        if offset:
            return b'\xFF\x0D' + offset
        else:
            if target > 0xFFFFFFFF:
                raise ValueError("dec FF 0C 25 不支持64位地址")
            return b'\xFF\x0C\x25' + target.to_bytes(4, 'little')


class IfInt64(AssemblyNode):
    """条件分支节点"""
    def __init__(self, target, true_node, false_node):
        self.target = target
        self.true_node = true_node
        self.false_node = false_node

    def generate(self, owner, context):
        target = self.get_target(owner)
        return (self.true_node if target > 0xFFFFFFFF else self.false_node).generate(owner, context)


class MemRead(AssemblyNode):
    """从内存读取值"""
    def __init__(self, addr=0, offset=0, size=4):
        self.addr = addr
        self.offset = offset
        self.size = size

    def generate(self, owner, context):
        addr = (self.addr or context.original_addr) + self.offset
        return owner.handler.read(addr, bytes, self.size)


class Offset(AssemblyNode):
    """计算偏移地址"""
    def __init__(self, target, size=4):
        self.target = target
        self.size = size

    def generate(self, owner, context):
        target = self.get_target(owner)
        return self.offsetof(target, context.addr, self.size)


class Origin(AssemblyNode):
    """查找的原始值"""
    def generate(self, owner, context):
        return context.original


ORIGIN = Origin()


def insert_before(data):
    return AssemblyGroup(data, ORIGIN)


def insert_after(data):
    return AssemblyGroup(ORIGIN, data)
