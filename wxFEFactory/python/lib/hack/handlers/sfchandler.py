from .handler import MemHandler
from ..models import Model, Field, ByteField, QWordField, StringField
import struct


class Memory64(Model):
    ADDR = 0x1405D9270

    RAM = QWordField(40)
    ROM = QWordField(48)
    SRAM = QWordField(56)
    VRAM = QWordField(64)
    FillRAM = QWordField(72)

    ROMFilename = StringField(73849, 100, encoding='utf-8')
    ROMName = StringField(74110, 23, encoding='utf-8')
    RawROMName = StringField(74133, 23, encoding='utf-8')
    ROMId = StringField(74156, 5, encoding='utf-8')
    CompanyId = Field(74164)
    ROMRegion = ByteField(74168)
    ROMSpeed = ByteField(74169)
    ROMType = ByteField(74170)
    ROMSize = ByteField(74171)
    ROMChecksum = Field(74172)
    HiROM = ByteField(74220)
    LoROM = ByteField(74221)


class Memory32(Model):
    ADDR = 0x007832A0

    RAM = Field(36)
    ROM = Field(40)
    SRAM = Field(44)
    VRAM = Field(48)
    FillRAM = Field(52)

    ROMFilename = StringField(41037, 100, encoding='utf-8')
    ROMName = StringField(41298, 23, encoding='utf-8')
    RawROMName = StringField(41321, 23, encoding='utf-8')
    ROMId = StringField(41344, 5, encoding='utf-8')
    CompanyId = Field(41352)
    ROMRegion = ByteField(41356)
    ROMSpeed = ByteField(41357)
    ROMType = ByteField(41358)
    ROMSize = ByteField(41359)
    ROMChecksum = Field(41360)
    HiROM = ByteField(41408)
    LoROM = ByteField(41409)


class Snes9xHandler(MemHandler):
    CLASS_NAME = 'Snes9X: WndClass'
    WINDOW_NAME = 'Snes9X'

    def attach(self):
        succeed = self.attach_window(self.CLASS_NAME, None)
        if succeed:
            Memory = Memory32 if self.is32process else Memory64
            with self.raw_env():
                self.memory = Memory(Memory.ADDR, self).datasnap(('RAM', 'ROM', 'ROMFilename', 'HiROM', 'LoROM'))
        return succeed

    def address_map(self, addr, size=4):
        if self._raw_addr:
            return addr

        bank = (addr >> 16) & 0xFF
        addr &= 0xFFFF

        if 0 <= bank <= 0x3F:
            if addr <= 0x1FFF:
                return self.memory.RAM + addr
            elif 0x8000 <= addr <= 0xFFFF:
                return self.memory.ROM + (addr - 0x8000)
        elif bank == 0x7E or bank == 0x7F:
            return self.memory.RAM + ((bank - 0x7E << 16) | addr)
        elif bank == 0xFE or bank == 0xFF:
            return self.memory.ROM + ((bank - 0xFE << 16) | addr)
        return False