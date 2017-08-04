from gba.dictionary import Dictionary, CtrlCode
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


class FeDict(Dictionary):
    """
    火纹文本字典类 HaffumanDictionary
    """
    __slots__ = ('tree', 'leafmap')

    def __init__(self, huffmandata, codetable, lowrange=None, ctrltable=None):
        """
        :param huffmandata: 包含哈夫曼树的顺序存储数据 (file, start, size)
        """
        super().__init__(codetable, lowrange, ctrltable)
        self.buildtree(huffmandata)
        

    def buildtree(self, huffmandata):
        # 生成哈夫曼树
        buff = None

        if isinstance(huffmandata, (tuple, list)):
            file, start, size = huffmandata
            buff = ctypes.create_string_buffer(size)
            with open(file, 'rb') as f:
                f.seek(start)
                f.readinto(buff)
        elif isinstance(huffmandata, (bytes, bytearray)):
            size = len(huffmandata)
            buff = ctypes.create_string_buffer(size)
            buff.raw = huffmandata

        if buff is None:
            raise ValueError("生成哈夫曼树失败")

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

    def decodeHaffuman(self, data, result=None):
        """
        :param result: 返回解码后的code列表
        """
        curbyte = 0
        bit = 0
        code = 0
        it = iter(data)

        if result is None:
            result = []

        while True:
            node = self.tree
            break_continue = False

            while node:
                bit -= 1
                if bit < 0:
                    curbyte = next(it)
                    bit = 7

                if (curbyte & 1) is 0:
                    node = node.left
                else:
                    node = node.right
                curbyte >>= 1
                if node.isLeaf():
                    code = node.value
                    if (code & 0xFF00) is not 0:
                        result.append(code)
                        break_continue = True
                    break
                
            if not break_continue and (code & 0xFF) is 0:
                break

        text = []
        i = 0
        for code in result:
            word = self.getChar(code)
            if word is not None:
                text.append(word)
            elif self.ctrltable and code in self.ctrltable:
                word, i = self.ctrltable[code].decode(data, i)
                text.append(word)
            else:
                print("Error: %04X can't decode" % code)
            i += 1

        return ''.join(text)

        # return ''.join(self.getChar(code) for code in result)

    def encodeHaffuman(self, text, buf=None, null=True):
        """
        :param null: 把\0添加到结尾
        """
        codes = []
        for ch in text:
            code = self.getCode(ch)
            if code is 0x00:
                raise ValueError("码表中没有这个字：" + ch)
            codes.append(code)

        if null:
            codes.append(0x00)

        return self.encodeHaffumanCode(codes, buf)
            

    def encodeHaffumanCode(self, codes, buf=None):
        """
        codes 字码数组
        """
        result = bytearray() if buf is None else buf
        byte = 0
        bit  = 0
        # 因哈夫曼值从根结点开始，先从叶结点往上，写入逆序的比特流，再用huffmanBit控制比特位逆转
        huffmanBit = 0
        for code in codes:
            node = self.leafmap.get(code, None)
            if node is None:
                raise ValueError("哈夫曼树中没有这个编码：" + ("%04X" % code))

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

    @staticmethod
    def code_list_to_bytes(codes):
        result = bytearray(len(codes) * 2)
        i = 0
        for code in codes:
            # 火纹的每个字码写到rom中也一致（高低四位逆序）
            result[i] = (code >> 8) & 0xFF
            result[i + 1] = code & 0xFF
            i += 2
        return result

    @staticmethod
    def bytes_to_code_list(codebytes):
        codes = []
        for i in range(0, len(codebytes), 2):
            codes.append((codebytes[i] << 8) | codebytes[i + 1])
            i += 2
        return codes


if __name__ == '__main__' or __name__ == 'builtins':
    # workdir = 'E:/GBA/fe8/'
    # di = FeDict((workdir + 'font.bin', 0, 0x52B4), workdir + 'fe8dict.txt') 
    # print(di.encodeHaffuman('铁剑'))
    # print(di.decodeHaffuman(b'\x93\xe4\x93\xbf\x01'))

    # import os
    # di = FeDict((r'E:\GBA\rom\烈火之剑汉化版.gba', 0xbb5a80, 0x58ec), os.path.join(os.path.dirname(__file__), 'dict-fe7.txt'))
    # print(di.decodeHaffuman(b'\xCD\x1B'))
    pass

