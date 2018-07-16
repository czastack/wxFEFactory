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
    CPU_MEM_BANKS = 0x57B340
    PPU_MEM_BANKS = 0x5732EC

    def attach(self):
        return self.attach_window(self.CLASS_NAME, None)

    def address_map(self, addr):
        if self._raw_addr:
            return addr

        if 0x0000 <= addr <= 0x1FFF:
            return self.RAM + addr
        elif 0x6000 <= addr <= 0x7FFF:
            return self.WRAM + (addr - 0x6000)
        elif 0x8000 <= addr <= 0xFFFF:
            return self.cpu_mem_bank_addr(addr >> 13) + (addr & 0x1FFF)
        return False

    def cpu_mem_bank_addr(self, i):
        return self.raw_read(self.CPU_MEM_BANKS + (i << 2), int, 4)

    def ppu_mem_bank_addr(self, i):
        return self.raw_read(self.PPU_MEM_BANKS + (i << 2), int, 4)


class NestopiaHandler(MemHandler):
    CLASS_NAME = 'Nestopia'
    WINDOW_NAME = CLASS_NAME

    def attach(self):
        succeed = self.attach_window(self.CLASS_NAME, None)
        self.ram = 0
        self.wram = 0
        self.roms = None

        if succeed:
            with self.raw_env():
                pMsgHandler = self.read_ptr(self.read_ptr(self.proc_base + 0x1b1334)) + 4
                size = self.read_ptr(pMsgHandler + 8) # msgHandler 列表数量
                if size > 0x1000:
                    return False
                start = self.read_ptr(pMsgHandler)
                for i in range(size):
                    if self.read32(start) == 0x0218: # WM_POWERBROADCAST
                        pMain = self.read_ptr(start + 4)
                        pEmulator = self.read_ptr(pMain)
                        pMachine = self.read_ptr(pEmulator)
                        pCpu = pMachine + 48
                        self.ram = pCpu + 104
                        pBoard = self.read_ptr(pCpu + 2664 + (12 * 0x6000))
                        self.wram = self.read_ptr(pBoard + 80)
                        self.roms = struct.unpack('4L', self.read(pBoard + 4, bytes, 16))
                        break

                    start += 12
                else:
                    # succeed = False
                    pass

        return succeed

    def address_map(self, addr):
        if self._raw_addr:
            return addr

        if 0x0000 < addr < 0x1FFF and self.ram:
            return self.ram + addr
        elif 0x6000 < addr < 0x7FFF and self.wram:
            return self.wram + (addr - 0x6000)
        elif 0x8000 <= addr <= 0xFFFF and self.roms:
            return self.roms[(addr >> 13) - 4] + (addr & 0x1FFF)
        return False