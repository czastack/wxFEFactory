from gba.rom import RomRW

class FeRomRW(RomRW):
    __slots__ = ()

    FONT_POINTER = 0x06E0
    POINTER_START_POINTER = 0x06DC