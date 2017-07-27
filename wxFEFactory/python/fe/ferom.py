from gba.rom import RomRW
from lib.lazy import lazy
from . import config
from .fedict import FeDict, CtrlCode
import os

ctrltable = (
    CtrlCode(0x0100, "br"),
    CtrlCode(0x0200, "br2")
)

class FeRomRW(RomRW):
    __slots__ = ()

    FONT_POINTER = 0x06E0
    TEXT_TABLE_POINTER = 0x06DC

    def __init__(self, path, mode=None):
        RomRW.__init__(self, path, mode=mode)

        code = self.getRomCode()
        if code not in config.romcode:
            print(f'{self.name}不是火纹的rom, code={code}')
            self.close()
        else:
            self.key = config.romcode[code]
        self._dict = None

    def openDict(self, path=None):
        # 码表路径，默认放在本文件夹下面
        if path is None:
            path = config.dictmap[self.key]
            path = os.path.join(os.path.dirname(__file__), path)

        self._dict_path = path

        huffstart = self.read32(self.FONT_POINTER)
        huffsize = self.read32(self.TEXT_TABLE_POINTER) - huffstart
        self._dict = FeDict((self.name, huffstart & self.addrmask, huffsize), path, None, ctrltable)

    @lazy
    def text_table_start(self):
        return self.read32(self.TEXT_TABLE_POINTER) + 4

    def getTextEntryPtr(self, i):
        """
        读取文本指针表项的值（地址）
        i从0开始
        """
        return self.read32(self.text_table_start + i * 4)

    def getTextEntryText(self, i):
        """
        读取文本指针表项的内容（文本）
        i从0开始
        """
        return self.readText(self.getTextEntryPtr(i))

    @property
    def dict_path(self):
        return getattr(self, '_dict_path', None)

    def __iter__(self):
        return self

    def __next__(self):
        return self._file.read(1)[0]

    def __getitem__(self, i):
        pass

    def __setitem__(self, i):
        pass

    def readText(self, addr):
        if self._dict is None:
            self.openDict()
        return self._dict.decodeHaffuman(self.pos(addr))