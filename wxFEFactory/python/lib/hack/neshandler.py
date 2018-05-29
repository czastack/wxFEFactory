from .handler import MemHandler
import struct


class VirtuaNesHandler(MemHandler):
    CLASS_NAME = 'VirtuaNESwndclass'
    WINDOW_NAME = 'VirtuaNES'

    RAM = 0x59E3B0 # size=0x2000
    WRAM = 0x57C398 # size=0x20000
    # DRAM = 0x5692EC # size=0xa000
    # XRAM = 0x59C398 # size=0x2000
    # ERAM = 0x573320 # size=0x8000
    # CRAM = 0x5612EC # size=0x8000
    # VRAM = 0x57B360 # size=0x1000
    # SPRAM = 0x5A0424 # size=0x100
    # PROM = 0x57C364 # ptr
    # VROM = 0x5A0420 # ptr
    BANKS = 0x57B340

    def attach(self):
        return self.attachByWindowName(self.CLASS_NAME, None)

    def prepareAddr(self, addr, size=4):
        if self._raw_addr:
            return addr

        if 0x0000 <= addr <= 0x1FFF:
            return self.RAM + addr
        elif 0x6000 <= addr <= 0x7FFF:
            return self.WRAM + (addr - 0x6000)
        elif 0x8000 <= addr <= 0xFFFF:
            return self.rawRead(self.BANKS + ((addr >> 13) << 2), int, 4) + (addr & 0x1FFF)
        return False


class NestopiaHandler(MemHandler):
    CLASS_NAME = 'Nestopia'
    WINDOW_NAME = CLASS_NAME

    def attach(self):
        succeed = self.attachByWindowName(self.CLASS_NAME, None)
        self.ram = 0
        self.wram = 0
        self.roms = None

        if succeed:
            with self.raw_env():
                pMsgHandler = self.readPtr(self.readPtr(self.base + 0x1b1334)) + 4
                size = self.readPtr(pMsgHandler + 8) # msgHandler 列表数量
                if size > 0x1000:
                    return False
                start = self.readPtr(pMsgHandler)
                for i in range(size):
                    if self.read32(start) == 0x0218: # WM_POWERBROADCAST
                        pMain = self.readPtr(start + 4)
                        pEmulator = self.readPtr(pMain)
                        pMachine = self.readPtr(pEmulator)
                        pCpu = pMachine + 48
                        self.ram = pCpu + 104
                        pBoard = self.readPtr(pCpu + 2664 + (12 * 0x6000))
                        self.wram = self.readPtr(pBoard + 80)
                        self.roms = struct.unpack('4L', self.read(pBoard + 4, bytes, 16))
                        break

                    start += 12
                else:
                    # succeed = False
                    pass

        return succeed

    def prepareAddr(self, addr, size=4):
        if self._raw_addr:
            return addr

        if 0x0000 < addr < 0x1FFF and self.ram:
            return self.ram + addr
        elif 0x6000 < addr < 0x7FFF and self.wram:
            return self.wram + (addr - 0x6000)
        elif 0x8000 <= addr <= 0xFFFF and self.roms:
            return self.roms[(addr >> 13) - 4] + (addr & 0x1FFF)
        return False