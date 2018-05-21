from .handler import MemHandler
import struct


class VirtuaNesHandler(MemHandler):
    CLASS_NAME = 'VirtuaNESwndclass'
    WINDOW_NAME = 'VirtuaNES'

    RAM = 0x59E3B0 # size=0x2000
    WRAM = 0x57C398 # size=0x20000
    DRAM = 0x5692EC # size=0xa000
    XRAM = 0x59C398 # size=0x2000
    ERAM = 0x573320 # size=0x8000
    CRAM = 0x5612EC # size=0x8000
    VRAM = 0x57B360 # size=0x1000
    SPRAM = 0x5A0424 # size=0x100
    PROM = 0x57C364 # ptr
    VROM = 0x5A0420 # ptr

    def attach(self):
        succeed = self.attachByWindowName(self.CLASS_NAME, None)
        return succeed

    def prepareAddr(self, addr, size=4):
        if self._raw_addr:
            return addr

        if 0x0000 < addr < 0x1FFF:
            return self.RAM + addr
        elif 0x6000 < addr < 0x7FFF:
            return self.WRAM + (addr - 0x6000)
        return False