from .handler import MemHandler
from ..models import Model, Field, ByteField, QWordField, StringField
import struct


class Memory64(Model):
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


class Snes9xHandler(MemHandler):
    CLASS_NAME = 'Snes9X: WndClass'
    WINDOW_NAME = 'Snes9X'

    MEMORY_ADDR = 0x1405D9270

    def attach(self):
        succeed = self.attachByWindowName(self.CLASS_NAME, None)
        if succeed:
            with self.raw_env():
                self.memory = Memory64(self.MEMORY_ADDR, self).datasnap(('RAM', 'ROM', 'SRAM', 'VRAM', 'ROMFilename'))
        return succeed

    def prepareAddr(self, addr, size=4):
        if self._raw_addr:
            return addr

        if 0x0000 <= addr <= 0xFFFF:
            return self.memory.RAM + addr
        return False