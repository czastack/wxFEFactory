import abc
import os
from lib.gba.rom import BaseRomRW, RomProxyRW, RomHandler
from lib.lazy import lazy
from . import config
from .fedict import FeDict, CtrlCode

# 控制码表
ctrl_table = (
    CtrlCode(0x0000, "End"),              # 结束
    CtrlCode(0x0100, "br"),               # 换行
    CtrlCode(0x0200, "br2"),              # 换2行
    CtrlCode(0x0300, "A"),                # 提示按A键继续
    CtrlCode(0x0400, "P1"),               # 短暂停顿
    CtrlCode(0x0500, "P2"),               # 比上一个代码停顿时间长
    CtrlCode(0x0600, "P3"),               # 比上一个代码停顿时间长
    CtrlCode(0x0700, "P4"),               # 比上一个代码停顿时间长
    CtrlCode(0x0800, "OpenFarLeft"),      # 确定头像等在屏幕中的位置（最左边）
    CtrlCode(0x0900, "OpenMidLeft"),      # 确定头像等在屏幕中的位置（中间偏左）
    CtrlCode(0x0a00, "OpenLeft"),         # 确定头像等在屏幕中的位置（左边）
    CtrlCode(0x0b00, "OpenRight"),        # 确定头像等在屏幕中的位置（右边）
    CtrlCode(0x0c00, "OpenMidRight"),     # 确定头像等在屏幕中的位置（中间偏右）
    CtrlCode(0x0d00, "OpenFarRight"),     # 确定头像等在屏幕中的位置（最右边）
    CtrlCode(0x0e00, "OpenFarFarLeft"),   # 确定头像等在屏幕中的位置（最最左边以至于超出屏幕范围）
    CtrlCode(0x0f00, "OpenFarFarRight"),  # 确定头像等在屏幕中的位置（最最右边以至于超出屏幕范围）
    CtrlCode(0x1000, "LoadFace"),         # 载入XX号头像
    CtrlCode(0x1100, "ClearFace"),        # 清除头像
    CtrlCode(0x1400, "CloseSpeechFast"),  # 快速关闭语言框
    CtrlCode(0x1500, "CloseSpeechSlow"),  # 缓慢关闭语言框
    CtrlCode(0x1600, "ToggleMouthMove"),  # 开始/结束伴随人物口型变化
    CtrlCode(0x1700, "ToggleSmile"),      # 开始/结束伴随人物微笑
    CtrlCode(0x1800, "Yes"),              # 给出选择支（默认是）
    CtrlCode(0x1900, "No"),               # 给出选择支（默认否）
    CtrlCode(0x1a00, "Buy/Sell"),         # 提示是否买卖物品
    CtrlCode(0x1c00, "SendToBack"),
    CtrlCode(0x1f00, "P0"),

    CtrlCode(0x1b00, "ShopContinue"),     # fe8特有 提示是否继续在商店逗留
    CtrlCode(0x1d00, "FastPrint"),        # fe8特有

    CtrlCode(0x1200, "NormalPrint"),      # fe6特有
    CtrlCode(0x1300, "FastPrint"),        # fe6特有

    # 最低位为1的一般都会带有换行行为，名称以Br结尾区分
    CtrlCode(0x0201, "br3"),
    CtrlCode(0x0301, "ABr"),
    CtrlCode(0x0401, "P1Br"),
    CtrlCode(0x0501, "P2Br"),
    CtrlCode(0x0601, "P3Br"),
    CtrlCode(0x0701, "P4Br"),
    CtrlCode(0x0801, "OpenFarLeftBr"),
    CtrlCode(0x0901, "OpenMidLeftBr"),
    CtrlCode(0x0a01, "OpenLeftBr"),
    CtrlCode(0x0b01, "OpenRightBr"),
    CtrlCode(0x0c01, "OpenMidRightBr"),
    CtrlCode(0x0d01, "OpenFarRightBr"),
    CtrlCode(0x0e01, "OpenFarFarLeftBr"),
    CtrlCode(0x0f01, "OpenFarFarRightBr"),
    CtrlCode(0x1101, "ClearFaceBr"),
    CtrlCode(0x1401, "CloseSpeechFastBr"),
    CtrlCode(0x1501, "CloseSpeechSlowBr"),
    CtrlCode(0x1601, "ToggleMouthMoveBr"),
    CtrlCode(0x1701, "ToggleSmileBr"),
    CtrlCode(0x1a01, "Buy/SellBr"),
    CtrlCode(0x1b01, "ShopContinueBr"),
    CtrlCode(0x1c01, "SendToBackBr"),

    CtrlCode(0x80000400, "LoadOverworldFaces"),    # 在世界地图载入XX号头像
    CtrlCode(0x80000500, "G"),                     # 显示玩家持有金钱数额
    CtrlCode(0x80000a00, "MoveFarLeft"),           # 移动头像至最左
    CtrlCode(0x80000b00, "MoveMidLeft"),           # 移动头像至偏左
    CtrlCode(0x80000c00, "MoveLeft"),              # 移动头像至左
    CtrlCode(0x80000d00, "MoveRight"),             # 移动头像至右
    CtrlCode(0x80000e00, "MoveMidRight"),          # 移动头像至偏右
    CtrlCode(0x80000f00, "MoveFarRight"),          # 移动头像至最右
    CtrlCode(0x80001000, "MoveFarFarLeft"),        # 移动头像至最最左以至于超出屏幕范围
    CtrlCode(0x80001100, "MoveFarFarRight"),       # 移动头像至最最右以至于超出屏幕范围
    CtrlCode(0x80001600, "EnableBlinking"),        # 眨眼
    CtrlCode(0x80001800, "DelayBlinking"),
    CtrlCode(0x80001900, "PauseBlinking"),
    CtrlCode(0x80001b00, "DisableBlinking"),       # 停止眨眼
    CtrlCode(0x80001c00, "OpenEyes"),              # 睁眼
    CtrlCode(0x80001d00, "CloseEyes"),             # 闭眼
    CtrlCode(0x80001e00, "HalfCloseEyes"),         # 半闭眼
    CtrlCode(0x80001f00, "Wink"),                  # 眨眼一下
    CtrlCode(0x80002000, "Tact"),                  # 显示玩家姓名
    CtrlCode(0x80002100, "ToggleRed"),             # 开始/结束红色文本
    CtrlCode(0x80002200, "Item"),                  # 显示载入的物品名称
    CtrlCode(0x80002300, "SetName"),               # 用于CG画面时的对话，显示说话者姓名
    CtrlCode(0x80002500, "ToggleColorInvert"),     # 开始/结束语言框反色

    CtrlCode(0x80001700, "Unknow80001700"),        # 似乎是fe8特有

    # 最低位为1的一般都会带有换行行为，名称以Br结尾区分
    CtrlCode(0x80000401, "LoadOverworldFacesBr"),  # 在世界地图载入XX号头像
    CtrlCode(0x80000501, "GBr"),                   # 显示玩家持有金钱数额后换行
    CtrlCode(0x80000a01, "MoveFarLeftBr"),         # 移动头像至最左
    CtrlCode(0x80000b01, "MoveMidLeftBr"),         # 移动头像至偏左
    CtrlCode(0x80000c01, "MoveLeftBr"),            # 移动头像至左
    CtrlCode(0x80000d01, "MoveRightBr"),           # 移动头像至右
    CtrlCode(0x80000e01, "MoveMidRightBr"),        # 移动头像至偏右
    CtrlCode(0x80000f01, "MoveFarRightBr"),        # 移动头像至最右
    CtrlCode(0x80001001, "MoveFarFarLeftBr"),      # 移动头像至最最左以至于超出屏幕范围
    CtrlCode(0x80001101, "MoveFarFarRightBr"),     # 移动头像至最最右以至于超出屏幕范围
    CtrlCode(0x80001601, "EnableBlinkingBr"),      # 眨眼
    CtrlCode(0x80001801, "DelayBlinkingBr"),
    CtrlCode(0x80001901, "PauseBlinkingBr"),
    CtrlCode(0x80001b01, "DisableBlinkingBr"),     # 停止眨眼
    CtrlCode(0x80001c01, "OpenEyesBr"),            # 睁眼
    CtrlCode(0x80001d01, "CloseEyesBr"),           # 闭眼
    CtrlCode(0x80001e01, "HalfCloseEyesBr"),       # 半闭眼
    CtrlCode(0x80001f01, "WinkBr"),                # 眨眼一下
    CtrlCode(0x80002001, "TactBr"),                # 显示玩家姓名
    CtrlCode(0x80002101, "ToggleRedBr"),           # 开始/结束红色文本
    CtrlCode(0x80002201, "ItemBr"),                # 显示载入的物品名称
    CtrlCode(0x80002301, "SetNameBr"),             # 用于CG画面时的对话，显示说话者姓名
    CtrlCode(0x80002501, "ToggleColorInvertBr"),   # 开始/结束语言框反色

    # 接在0x1000后时表示头像序号
    # FE7 0201~bd01, df, e0, e4 -> faceid
    # 这里的0xF000只是占位
    CtrlCode(0xF000, "Face%d"),

    # 未知控制码
    CtrlCode(0x1001, "{Unknow1001}"),
    CtrlCode(0x2300, "{Unknow2300}"),
    CtrlCode(0x3000, "{Unknow3000}"),
    CtrlCode(0x3000, "{Unknow3000}"),
    CtrlCode(0x3000, "{Unknow3000}"),
    CtrlCode(0x3001, "{Unknow3001}"),
    CtrlCode(0x4D00, "{Unknow4D00}"),
)


class FeRomHandler(RomHandler):
    FONT_POINTER = 0x06E0
    TEXT_TABLE_POINTER = 0x06DC

    @abc.abstractmethod
    def pos(self, pos):
        pass

    def __init__(self):
        code = self.get_rom_code()
        title = self.get_rom_title()
        if code not in config.romcode:
            print('{}不是火纹的rom, code={}'.format(title, code))
            self.close()
        else:
            self.key = config.romcode[code]
        self._dict = None

    def open_dict(self, path=None):
        # 码表路径，默认放在本文件夹下面
        if path is None:
            path = config.dictmap[self.key]
            path = os.path.join(os.path.dirname(__file__), path)

        self._dict_path = path

        huffstart = self.read32(self.FONT_POINTER)
        huffsize = self.read32(self.TEXT_TABLE_POINTER) - huffstart
        self._dict = FeDict(self.read(huffstart, bytes, huffsize),
            path, (0x8180, 0x9f00), ctrl_table)

    @lazy
    def text_table_start(self):
        return self.read32(self.TEXT_TABLE_POINTER) + 4

    def get_text_entry_ptr(self, i):
        """
        读取文本指针表项的值（地址）
        i从0开始
        """
        return self.read32(self.text_table_start + i * 4)

    def get_text_entry_text(self, i):
        """
        读取文本指针表项的内容（文本）
        i从0开始
        """
        return self.read_text(self.get_text_entry_ptr(i))

    @property
    def dict_path(self):
        return getattr(self, '_dict_path', None)

    @property
    def dict(self):
        if not self._dict:
            self.open_dict()
        return self._dict

    def __iter__(self):
        return self

    def __next__(self):
        return self.raw_read(1)[0]

    def read_text(self, addr, codebuff=None):
        """
        从rom中读取文本，遇结束符00结束
        :param codebuff: 用于返回原始字码 byte数组
        """
        if addr >> 28 == 8:
            # 打过补丁的处理
            text = self.dict.decode_it(self.pos(addr), codebuff)
        else:
            # print("%04X" % addr)
            text = self.dict.decode_haffuman_text(self.pos(addr), codebuff)
        return text

    def write_text(self, addr, text):
        huffbytes = self.dict.encode_haffuman(text)
        self.write(addr, huffbytes)

    def write_text_codes(self, addr, codes):
        huffbytes = self.dict.encode_haffuman_code(codes)
        self.write(addr, huffbytes)


class FeRomRW(BaseRomRW, FeRomHandler):
    def __init__(self, path, mode=None):
        BaseRomRW.__init__(self, path, mode=mode)
        FeRomHandler.__init__(self)


class FeEmuRW(RomProxyRW, FeRomHandler):
    def __init__(self, emu):
        RomProxyRW.__init__(self, emu)
        FeRomHandler.__init__(self)
        self._pos = 0

    def pos(self, pos):
        self._pos = pos
        return self

    def __iter__(self):
        return self

    def __next__(self):
        ret = self.read8(self._pos)
        self._pos += 1
        return ret
