from gba.dictionary import Dictionary
import ctypes


class CTreeNode(ctypes.Structure):
    _fields_ = [("left", ctypes.c_ushort), ("right", ctypes.c_ushort)]

LP_CNODE = ctypes.POINTER(CTreeNode)


class TreeNode:
    __slots__ = ('left', 'right', 'parent')

    def __init__(self, parent=None):
        self.parent = parent

    def isLeaf(self):
        return self.right is None

    @property
    def value(self):
        return self.left


class HaffumanDictionary(Dictionary):
    __slots__ = ('tree', 'leafmap')

    def __init__(self, huffmandata, codetable, lowrange=None, ctrltable=None):
        """
        :param huffmandata: 包含哈夫曼树的顺序存储数据 (file, start, size)
        """
        super().__init__(codetable, lowrange, ctrltable)
        self.buildtree(*huffmandata)
        

    def buildtree(self, file, start, size):
        # 生成哈夫曼树
        buff = ctypes.create_string_buffer(size)
        with open(file, 'rb') as f:
            f.seek(start)
            f.readinto(buff)

        nodes = ctypes.cast(buff, LP_CNODE)
        leafmap = {}

        def rparse(node, index):
            # ph(index)
            cnode = nodes[index]
            if cnode.right == 0xFFFF:
                node.right = None
                # rom哈夫曼树中字码是大端存储的
                node.left = ((cnode.left & 0xFF00) >> 8) | ((cnode.left & 0xFF) << 8)
                leafmap[node.left] = node
                return

            node.left = TreeNode(node)
            node.right = TreeNode(node)
            rparse(node.left, cnode.left)
            rparse(node.right, cnode.right)

        root = TreeNode()
        rparse(root, (size >> 2) - 1)

        self.tree = root
        self.leafmap = leafmap

    def decodeHaffuman(self, data):
        currentByte = 0
        bit = 0
        code = 0
        result = []
        it = iter(data)

        while True:
            node = self.tree
            break_continue = False

            while node:
                bit -= 1
                if bit < 0:
                    currentByte = next(it)
                    bit = 7

                if (currentByte & 1) is 0:
                    node = node.left
                else:
                    node = node.right
                currentByte >>= 1
                if node.isLeaf():
                    code = node.value
                    if (code & 0xFF00) is not 0:
                        result.append(code)
                        break_continue = True
                    break
                
            if not break_continue and (code & 0xFF) is 0:
                break

        return ''.join(self.getChar(code) for code in result)

    def encodeHaffuman(self, text, buf=None, null=True):
        """
        :param null: 把\0添加到结尾
        """
        result = bytearray() if buf is None else buf
        byte = 0
        bit  = 0
        # 因哈夫曼值从根结点开始，先从叶结点往上，写入逆序的比特流，再用huffmanBit控制比特位逆转
        huffmanBit = 0
        if null:
            text += '\0'
        for ch in text:
            node = self.leafmap.get(self.getCode(ch), None)
            if node is None:
                raise ValueError("码表中没有这个字：" + ch)

            parent = node.parent
            huffmanCode = 0

            while parent:
                if node is parent.right:
                    huffmanCode |= 1 << huffmanBit
                huffmanBit += 1
                node = parent
                parent = node.parent

            while True:
                huffmanBit -= 1
                byte |= ((huffmanCode >> huffmanBit) & 1) << bit
                bit += 1
                if bit is 8:
                    bit = 0
                    result.append(byte)
                    byte = 0
                if huffmanBit is 0:
                    break

        if bit < 8:
            result.append(byte)

        return result


if __name__ == '__main__' or __name__ == 'builtins':
    workdir = 'E:/GBA/fe8/'
    di = HaffumanDictionary((workdir + 'font.bin', 0, 0x52B4), workdir + 'fe8dict.txt') 
    # print(di.encodeHaffuman('铁剑'))
    print(di.decodeHaffuman(b'\x93\xe4\x93\xbf\x01'))

