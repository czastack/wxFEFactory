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

    def __init__(self, huffmandata, codetable, low_range=None, ctrltable=None, ctrl_low_range=None):
        """
        :param huffmandata: 包含哈夫曼树的顺序存储数据 (file, start, size)
        """
        super().__init__(codetable, low_range, ctrltable, ctrl_low_range)
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
        """ 哈夫曼字节流转字码列表
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
                        # 读到叶子结点
                        result.append(code)
                        break_continue = True
                    break
                
            if not break_continue and (code & 0xFF) is 0:
                break

        return result

    def decodeText(self, codes, codebytes=None):
        """字码列表转文本"""
        if codebytes is not None:
            codebytes.extend(self.codes_to_bytes(codes))

        it = iter(codes)
        text = []

        while True:
            try:
                code = next(it)
            except StopIteration:
                break
            if self.low_range[0] <= code < self.low_range[1]:
                word = self.getChar(code)
                if word is not None:
                    text.append(word)
                else:
                    print("Error: %04X can't decode" % code)
            else:
                if code == 0x8000:
                    code = code << 16 | next(it)

                if self.ctrltable and code in self.ctrltable:
                    word = self.ctrltable[code].decode_it(None)
                    text.append(word)

                    if code == 0x1000:
                        # 载入头像
                        try:
                            faceid = next(it) >> 8
                            # 这里没有判断范围，GBA三作都是2开始，后面几个id是离散的，每一作不一样
                            text.append('{Face%d}' % faceid)
                        except:
                            pass
                else:
                    print("Error: %04X can't decode" % code)
        return ''.join(text)

    def decodeHaffumanText(self, data, codebytes=None):
        """ 哈夫曼字节流转文本
        :param data: 哈夫曼字节流可迭代变量
        """
        codes = self.decodeHaffuman(data)
        return self.decodeText(codes, codebytes)

    def encodeText(self, text):
        """文本转字码列表，支持控制码"""
        codes = []
        length = len(text) - 1
        i = -1

        while i < length:
            i += 1
            ch = text[i]
            code = self.getCode(ch)
            if code is 0:
                if self.ctrltable and CtrlCode.FMT_START.startswith(ch):
                    con = False
                    for ctrlcode in self.ctrltable.values():
                        match = ctrlcode.encode_args(text, i)
                        if match:
                            code, args, i = match
                            i -= 1

                            if code == 0xF000 and args:
                                # 处理头像
                                code = args[0] << 8 | 1

                            elif code > 0xffff:
                                codes.append(code >> 16)
                                code &= 0xffff

                            codes.append(code)
                            con = True
                            break
                    if con:
                        continue
                print("warning: %s不在码表中" % ch)
                
            codes.append(code)

        return codes

    def encodeHaffuman(self, text, buf=None, null=True):
        """ 文本转哈夫曼字节数组
        :param null: 把\0添加到结尾
        :param buf: 可选的缓冲区（存放哈夫曼字节数据）
        """
        codes = self.encodeText(text)

        if null:
            codes.append(0x00)

        return self.encodeHaffumanCode(codes, buf)
            
    def encodeHaffumanCode(self, codes, buf=None):
        """ 文本转哈夫曼字节数组
        :param codes: 字码数组
        :param buf: 可选的缓冲区（存放哈夫曼字节数据）
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
    def codes_to_bytes(codes):
        """字码列表转bytes"""
        result = bytearray(len(codes) * 2)
        i = 0
        for code in codes:
            # 火纹的每个字码写到rom中也一致（高低四位逆序）
            result[i] = (code >> 8) & 0xFF
            result[i + 1] = code & 0xFF
            i += 2
        return result

    @staticmethod
    def bytes_to_codes(codebytes):
        """bytes转字码列表"""
        codes = []
        for i in range(0, len(codebytes), 2):
            codes.append((codebytes[i] << 8) | codebytes[i + 1])
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

