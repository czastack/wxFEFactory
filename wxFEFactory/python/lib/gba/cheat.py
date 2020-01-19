import re

# import xml.etree.ElementTree as ET

# Gameshark code types:
#
# NNNNNNNN 001DC0DE - ID code for the game (game 4 character name) from ROM
# DEADFACE XXXXXXXX - changes decryption seeds
# 0AAAAAAA 000000YY - 8-bit constant write
# 1AAAAAAA 0000YYYY - 16-bit constant write
# 2AAAAAAA YYYYYYYY - 32-bit constant write
# 3AAAAAAA YYYYYYYY - ??
# 6AAAAAAA 0000YYYY - 16-bit ROM Patch (address >> 1)
# 6AAAAAAA 1000YYYY - 16-bit ROM Patch ? (address >> 1)
# 6AAAAAAA 2000YYYY - 16-bit ROM Patch ? (address >> 1)
# 8A1AAAAA 000000YY - 8-bit button write
# 8A2AAAAA 0000YYYY - 16-bit button write
# 8A3AAAAA YYYYYYYY - 32-bit button write
# 80F00000 0000YYYY - button slow motion
# DAAAAAAA 0000YYYY - if address contains 16-bit value enable next code
# FAAAAAAA 0000YYYY - Master code function
#
# CodeBreaker codes types:
#
# 0000AAAA 000Y - Game CRC (Y are flags: 8 - CRC, 2 - DI)
# 1AAAAAAA YYYY - Master Code function (store address at ((YYYY << 0x16)
#                 + 0x08000100))
# 2AAAAAAA YYYY - 16-bit or
# 3AAAAAAA YYYY - 8-bit constant write
# 4AAAAAAA YYYY - Slide code
# XXXXCCCC IIII   (C is count and I is address increment, X is value increment.)
# 5AAAAAAA CCCC - Super code (Write bytes to address, CCCC is count)
# BBBBBBBB BBBB
# 6AAAAAAA YYYY - 16-bit and
# 7AAAAAAA YYYY - if address contains 16-bit value enable next code
# 8AAAAAAA YYYY - 16-bit constant write
# 9AAAAAAA YYYY - change decryption (when first code only?)
# AAAAAAAA YYYY - if address does not contain 16-bit value enable next code
# BAAAAAAA YYYY - if 16-bit < YYYY
# CAAAAAAA YYYY - if 16-bit > YYYY
# D0000020 YYYY - if button keys equal value enable next code
# EAAAAAAA YYYY - increase value stored in address
#
# 以 4, 7, A, B, C, D 开头的CB码是两行代码的开头。


UNKNOWN_CODE = -1
INT_8_BIT_WRITE = 0
INT_16_BIT_WRITE = 1
INT_32_BIT_WRITE = 2
GSA_16_BIT_ROM_PATCH = 3
GSA_8_BIT_GS_WRITE = 4
GSA_16_BIT_GS_WRITE = 5
GSA_32_BIT_GS_WRITE = 6
CBA_IF_KEYS_PRESSED = 7
CBA_IF_TRUE = 8
CBA_SLIDE_CODE = 9  # CB压缩码
CBA_IF_FALSE = 10
CBA_AND = 11
GSA_8_BIT_GS_WRITE2 = 12
GSA_16_BIT_GS_WRITE2 = 13
GSA_32_BIT_GS_WRITE2 = 14
GSA_16_BIT_ROM_PATCH2 = 15
GSA_8_BIT_SLIDE = 16
GSA_16_BIT_SLIDE = 17
GSA_32_BIT_SLIDE = 18
GSA_8_BIT_IF_TRUE = 19
GSA_32_BIT_IF_TRUE = 20
GSA_8_BIT_IF_FALSE = 21
GSA_32_BIT_IF_FALSE = 22
GSA_8_BIT_FILL = 23
GSA_16_BIT_FILL = 24
GSA_8_BIT_IF_TRUE2 = 25
GSA_16_BIT_IF_TRUE2 = 26
GSA_32_BIT_IF_TRUE2 = 27
GSA_8_BIT_IF_FALSE2 = 28
GSA_16_BIT_IF_FALSE2 = 29
GSA_32_BIT_IF_FALSE2 = 30
GSA_SLOWDOWN = 31
CBA_ADD = 32
CBA_OR = 33
CBA_LT = 34  # 小于
CBA_GT = 35  # 大于
CBA_SUPER = 36

TYPE_CB = 0
TYPE_V1 = 1
TYPE_V3 = 2


MASK_8 = 0x000000FF
MASK_16 = 0x0000FFFF
MASK_28 = 0x0FFFFFFF
MASK_32 = 0xFFFFFFFF
ROLLINGSEED = 0xC6EF3720
SEED_INCREMENT = 0x9E3779B9
SEEDS_V1 = (0x09F4FBBD, 0x9681884A, 0x352027E9, 0xF3DEE5A7)
SEEDS_V3 = (0x7AA9648F, 0x7FAE6994, 0xC0EFAAD5, 0x42712C57)

REG_GS = re.compile("(?i)\\b([0-9a-f]{8}) ?([0-9a-f]{8})\\b$")  # Gameshark
REG_CB = re.compile("(?i)([0-9a-f]{8}) ([0-9a-f]{4})$")
REG_RAW = re.compile("(?i)(0[23][0-9a-f]{6})[ :]([0-9a-f]{1,8})$")

TYPE_8BIT = {
    INT_8_BIT_WRITE, GSA_8_BIT_GS_WRITE, GSA_8_BIT_GS_WRITE2, GSA_8_BIT_SLIDE, GSA_8_BIT_IF_TRUE,
    GSA_8_BIT_IF_FALSE, GSA_8_BIT_FILL, GSA_8_BIT_IF_TRUE2, GSA_8_BIT_IF_FALSE2, GSA_SLOWDOWN
}
TYPE_16BIT = {
    INT_16_BIT_WRITE, GSA_16_BIT_ROM_PATCH, GSA_16_BIT_GS_WRITE, CBA_IF_KEYS_PRESSED, CBA_IF_TRUE,
    CBA_SLIDE_CODE, CBA_IF_FALSE, CBA_AND, GSA_16_BIT_GS_WRITE2, GSA_16_BIT_ROM_PATCH2, GSA_16_BIT_SLIDE,
    GSA_16_BIT_FILL, GSA_16_BIT_IF_TRUE2, GSA_16_BIT_IF_FALSE2, CBA_ADD, CBA_OR, CBA_LT, CBA_GT, CBA_SUPER
}
TYPE_32BIT = {
    INT_32_BIT_WRITE, GSA_32_BIT_GS_WRITE, GSA_32_BIT_GS_WRITE2, GSA_32_BIT_SLIDE,
    GSA_32_BIT_IF_TRUE, GSA_32_BIT_IF_FALSE, GSA_32_BIT_IF_TRUE2, GSA_32_BIT_IF_FALSE2
}

CB_TYPE = {
    INT_8_BIT_WRITE: 0x3,
    INT_16_BIT_WRITE: 0x8,
    CBA_SLIDE_CODE: 0x4,
    CBA_OR: 0x2,
    CBA_SUPER: 0x5,
    CBA_AND: 0x6,
    CBA_IF_TRUE: 0x7,
    CBA_IF_FALSE: 0xA,
    CBA_LT: 0xB,
    CBA_GT: 0xC,
    CBA_IF_KEYS_PRESSED: 0xD,
    CBA_ADD: 0xE,
}

GSV3_TYPE = {
    GSA_8_BIT_FILL: 0x00,
    GSA_16_BIT_FILL: 0x01,
    INT_32_BIT_WRITE: 0x02,
    GSA_8_BIT_IF_TRUE: 0x04,
    CBA_IF_TRUE: 0x05,
    GSA_32_BIT_IF_TRUE: 0x06,
    GSA_8_BIT_IF_FALSE: 0x08,
    CBA_IF_FALSE: 0x09,
    GSA_32_BIT_IF_FALSE: 0x0a,
    GSA_8_BIT_IF_TRUE2: 0x24,
    GSA_16_BIT_IF_TRUE2: 0x25,
    GSA_32_BIT_IF_TRUE2: 0x26,
    GSA_8_BIT_IF_FALSE2: 0x28,
    GSA_16_BIT_IF_FALSE2: 0x29,
    GSA_32_BIT_IF_FALSE2: 0x2a,
    GSA_SLOWDOWN: 0x04,
    GSA_8_BIT_GS_WRITE2: 0x08,
    GSA_16_BIT_GS_WRITE2: 0x09,
    GSA_32_BIT_GS_WRITE2: 0x0a,
    GSA_16_BIT_ROM_PATCH2: 0x0c,
    GSA_8_BIT_SLIDE: 0x40,
    GSA_16_BIT_SLIDE: 0x41,
    GSA_32_BIT_SLIDE: 0x42,
}


def get_bit(type):
    if type in TYPE_8BIT:
        return 8
    elif type in TYPE_16BIT:
        return 16
    elif type in TYPE_32BIT:
        return 32
    return 0


def get_bit_mask(bit):
    if bit == 8:
        return MASK_8
    elif bit == 16:
        return MASK_16
    elif bit == 32:
        return MASK_32
    return -1


def get_type_mask(type):
    return get_bit_mask(get_bit(type))


def get_type_size(type):
    return get_bit(type) >> 3


def high4(num):
    return (num >> 28) & 0xF


def gsdecode(address, value, isv3):
    """GS解码"""
    rollingseed = ROLLINGSEED
    increment = SEED_INCREMENT
    seeds = SEEDS_V3 if isv3 else SEEDS_V1
    bitsleft = 32

    while bitsleft > 0:
        s1 = (address << 4 & MASK_32) + seeds[2]
        s2 = (address + rollingseed)
        s3 = s1 ^ s2
        s4 = (address >> 5) + seeds[3]
        value = (value - (s3 ^ s4)) & MASK_32

        t1 = (value << 4 & MASK_32) + seeds[0]
        t2 = value + rollingseed
        t3 = t1 ^ t2
        t4 = (value >> 5) + seeds[1]
        address = (address - (t3 ^ t4)) & MASK_32

        rollingseed = (rollingseed - increment) & MASK_32
        bitsleft -= 1

    return address, value


def gsencode(address, value, isv3):
    """GS编码"""
    rollingseed = 0
    increment = SEED_INCREMENT
    seeds = SEEDS_V3 if isv3 else SEEDS_V1
    bitsleft = 32

    while bitsleft > 0:
        rollingseed = (rollingseed + increment) & MASK_32

        t1 = (value << 4 & MASK_32) + seeds[0]
        t2 = value + rollingseed
        t3 = t1 ^ t2
        t4 = (value >> 5) + seeds[1]
        address = (address + (t3 ^ t4)) & MASK_32

        s1 = (address << 4 & MASK_32) + seeds[2]
        s2 = address + rollingseed
        s3 = s1 ^ s2
        s4 = (address >> 5) + seeds[3]
        value = (value + (s3 ^ s4)) & MASK_32

        bitsleft -= 1

    return address, value


def gsencode_string(address, value, isv3):
    address, value = gsencode(address, value, isv3)
    address = "%08X" % address
    value = "%08X" % value
    if isv3:
        return address + " " + value
    return address + value


def rawstr2gs(code, isv3):
    """原始代码转GS代码
    :param code: 一条代码字符串
    :param isv3: 是否是v3版本
    """
    address = int(code[:8], 16)
    value = int(code[9:17], 16)
    return gsencode_string(address, value, isv3)


def cb_string(address, value):
    return "%08X %04X" % (address, value)


def decode(src, code):
    """解析金手指"""
    match = REG_CB.match(src)

    if match:
        codeType = TYPE_CB
        address = int(match.group(1), 16)
        value = int(match.group(2), 16)
        if code.wait_second:
            code.addrInc = value
            code.dataSize = address & MASK_16
            code.valueInc = (address >> 16) & MASK_16
            code.wait_second = False
            return

        head = high4(address)
        address &= MASK_28
        codeFunc = 0
        for f, h in CB_TYPE.items():
            if h is head:
                codeFunc = f
                break
        else:
            raise ValueError("不支持的CB头", head)
        if CBA_SLIDE_CODE is CBA_SLIDE_CODE:
            wait_second = True
        return
    match = REG_GS.match(src)
    if match:
        isv3 = src[8] == ' '
        address = int(match.group(1), 16)
        value = int(match.group(2), 16)
        address, value = gsdecode(address, value, isv3)
        # 如果是ID识别码
        if value == 0x1DC0DE:
            return
        if isv3:
            codeType = TYPE_V3
            if code.wait_second:
                # 处理双行代码的第二条
                if GSA_8_BIT_GS_WRITE2 <= code.func <= GSA_16_BIT_ROM_PATCH2:
                    code.value = address
                elif GSA_8_BIT_SLIDE <= code.func <= GSA_32_BIT_SLIDE:
                    code.value = address
                    code.addrInc = value & MASK_16
                    value >>= 16
                    code.dataSize = value & MASK_8
                    value >>= 8
                    code.valueInc = value & MASK_8
                code.wait_second = False
                return
            v3type = (address >> 25) & 0x7F
            address = (address & 0x00F00000) << 4 | (address & 0x0003FFFF)
            if v3type == 0x00:
                if address == 0:
                    # 对于特殊代码 地址其实是第一行的数值
                    v3type = (value >> 25) & 0x7F
                    address = (value & 0x00F00000) << 4 | (value & 0x0003FFFF)
                    if v3type == 0x04:
                        codeFunc = GSA_SLOWDOWN
                    elif 0x08 <= v3type <= 0x0a:
                        if v3type == 0x08:
                            codeFunc = GSA_8_BIT_GS_WRITE2
                        elif v3type == 0x09:
                            codeFunc = GSA_16_BIT_GS_WRITE2
                        else:
                            codeFunc = GSA_32_BIT_GS_WRITE2
                        code.wait_second = True
                        value = 0
                    elif 0x0c <= v3type <= 0x0f:
                        codeFunc = GSA_16_BIT_ROM_PATCH2
                        address = 0x08000000 | ((value & 0x00FFFFFF) << 1)
                        code.wait_second = True
                        value = 0
                    elif 0x40 <= v3type <= 0x42:
                        if v3type == 0x40:
                            codeFunc = GSA_8_BIT_SLIDE
                        elif v3type == 0x41:
                            codeFunc = GSA_16_BIT_SLIDE
                        else:
                            codeFunc = GSA_32_BIT_SLIDE
                        code.wait_second = True
                        value = 0
                else:
                    codeFunc = GSA_8_BIT_FILL
                    code.dataSize = value >> 8
                    value &= MASK_8
            elif v3type == 0x01:
                codeFunc = GSA_16_BIT_FILL
                code.dataSize = value >> 16
                value &= MASK_16
            else:
                for f, t in GSV3_TYPE.items():
                    if t is v3type:
                        codeFunc = f
                        break
        else:
            # v1/v2
            codeType = TYPE_V1
            v1type = high4(address)
            if v1type == 0:
                # 8位ram写入
                codeFunc = INT_8_BIT_WRITE
            elif v1type == 1:
                # 16位ram写入
                codeFunc = INT_16_BIT_WRITE
            elif v1type == 2:
                # 32位ram写入
                codeFunc = INT_32_BIT_WRITE
            elif v1type == 6:
                # 16位rom patch (补丁) GSA_16_BIT_ROM_PATCH
                address <<= 1
                subtype = high4(address)
                if subtype == 0x0C:
                    codeFunc = GSA_16_BIT_ROM_PATCH
                    address &= MASK_28
                # UNKNOWN_CODE
            elif v1type == 8:
                subtype = (address >> 20) & 0xF
                if 1 <= subtype <= 3:
                    if subtype == 1:
                        codeFunc = GSA_8_BIT_GS_WRITE
                    elif subtype == 2:
                        codeFunc = GSA_16_BIT_GS_WRITE
                    else:
                        codeFunc = GSA_32_BIT_GS_WRITE
                elif subtype == 15:
                    codeFunc = GSA_SLOWDOWN
                    value &= 0xFF00
            elif v1type == 0x0D:
                if address != 0xDEADFACE:
                    codeFunc = CBA_IF_TRUE
                    address &= MASK_28

    code.address = address
    code.value = value
    code.type = codeType
    code.func = codeFunc


def encode(code):
    """生成作弊码"""
    func = code.func
    if code.type is TYPE_CB:
        address2 = 0
        value2 = 0
        code.address = (code.address & MASK_28) | (CB_TYPE.get(func, 0) << 28)
        if func is INT_32_BIT_WRITE:
            address2 = code.address + 2
            value2 = code.value >> 16
        elif func is CBA_SLIDE_CODE:
            address2 = (code.valueInc << 16) | code.dataSize
            value2 = code.addrInc
        code.value &= MASK_16
        code.set_text(cb_string(code.address, code.value))
        if address2:
            code.add_line(cb_string(address2, value2))
    elif code.type is TYPE_V3:
        # raw 地址 -> v3 地址
        # 把第2个数右移一个变成 0x00AAAAAAA
        # 类型乘2作为前两个字母 0xTTAAAAAAA
        if func != GSA_16_BIT_ROM_PATCH2:
            code.address = ((code.address & 0x000FFFFF) | ((code.address >> 4) & 0x00F00000)
                | (GSV3_TYPE.get(func, 0) << 25))
        code.value &= get_type_mask(func)
        if GSA_8_BIT_FILL <= func <= GSA_16_BIT_FILL:
            code.value = code.value | ((code.dataSize - 1) << get_bit(type))
            code.set_gs(True)
        elif func in {
                INT_32_BIT_WRITE, GSA_8_BIT_IF_TRUE, CBA_IF_TRUE,
                GSA_32_BIT_IF_TRUE, GSA_8_BIT_IF_FALSE, CBA_IF_FALSE, GSA_32_BIT_IF_FALSE,
                GSA_8_BIT_IF_TRUE2, GSA_16_BIT_IF_TRUE2, GSA_32_BIT_IF_TRUE2,
                GSA_8_BIT_IF_FALSE2, GSA_16_BIT_IF_FALSE2, GSA_32_BIT_IF_FALSE2}:
            code.set_gs(True)
        elif GSA_8_BIT_GS_WRITE2 <= func <= GSA_32_BIT_GS_WRITE2:
            code.set_text(gsencode_string(0, code.address, True))
            code.add_line(gsencode_string(code.value, 0, True))
        elif func is GSA_16_BIT_ROM_PATCH2:
            code.address = ((code.address & 0x00FFFFFF) >> 1) | (GSV3_TYPE.get(func, 0) << 25)
            code.set_text(gsencode_string(0, code.address, True))
            code.add_line(gsencode_string(code.value, 0, True))
        elif GSA_8_BIT_SLIDE <= func <= GSA_32_BIT_SLIDE:
            # Example:
            # raw=02001234:12345678
            # data=10; Value Inc=1; Address Inc=2
            # unencrypted:
            # 00000000 80201234
            # 12345678 010A0002
            # args0 data, args1 value inc, args2 address inc
            value2 = (code.valueInc << 24) | (code.dataSize << 16) | code.addrInc
            code.set_text(gsencode_string(0, code.address, True))
            code.add_line(gsencode_string(code.value, value2, True))
    elif code.type is TYPE_V1:
        code.address &= MASK_28
        code.value &= get_type_mask(func)
        if INT_8_BIT_WRITE <= func <= INT_32_BIT_WRITE:
            code.address |= (get_bit(func) & 0xf0) << 24
            code.set_gs(False)
        elif func is GSA_16_BIT_ROM_PATCH:
            code.address = (code.address >> 1) | 0x64000000
            code.set_gs(False)
        elif GSA_8_BIT_GS_WRITE <= func <= GSA_32_BIT_GS_WRITE:
            code.address = code.address & 0x0F0FFFFF | 0x80000000 | (((get_bit(func) & 0xf0) + 0x10) << 16)
            code.set_gs(False)
        elif func is CBA_IF_TRUE:
            code.address |= 0xD << 28
            code.set_gs(False)


class CheatCode:
    def __init__(self, address=0, value=0, type=0, func=0):
        self.address = address
        self.value = value
        self.type = type
        self.func = func
        self.buffer = []
        self.batch_mode = False
        self.wait_second = False

    def clear(self):
        self.buffer.clear()

    def set_text(self, text):
        if self.batch_mode and len(self.buffer):
            self.add_line(text)
        else:
            self.clear()
            self.buffer.append(text)

    def get_text(self):
        return ''.join(self.buffer)

    def add_line(self, text):
        self.buffer.append('\n')
        self.buffer.append(text)

    def set_gs(self, isv3):
        self.set_text(gsencode_string(self.address, self.value, isv3))

    def set_cb(self):
        self.set_text(cb_string(self.address, self.value))

    def from_string(self, text):
        decode(text, self)
        return self


if __name__ == '__main__':
    code = CheatCode()
    code.from_string("0146DCEA3E32A31D")
    print("%08X %08X" % (code.address, code.value))
