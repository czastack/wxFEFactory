from .handler import MemHandler
import struct


NDS_MEMORY_SIZE = (
    0x00003FFF,  # 0X Instruction TCM (32KB)
    0x00000003,  # 1X UNUSED_RAM
    0x003FFFFF,  # 2X Main Memory     (4MB)
    0x00007FFF,  # 3X Shared WRAM     (0KB, 16KB, or 32KB can be allocated to ARM9)
    0x00FFFFFF,  # 4X ARM9-I/O Ports
    0x000007FF,  # 5X Standard Palettes (2KB)
    0x00FFFFFF,  # 6X VRAM
    0x000007FF,  # 7X OAM (2KB)
    0x01FFFFFF,  # 8X GBA Slot ROM (max 32MB)
    0x0000FFFF,  # 9X GBA Slot RAM (max 64KB)
    # 0x00000003,  # AX
    # 0x00000003,  # BX
    # 0x00000003,  # CX
    # 0x00000003,  # DX
    # 0x00000003,  # EX
    # 0x00007FFF,  # FX
)


class NdsEmuHandler(MemHandler):
    def address_map(self, addr, size):
        if self._raw_addr:
            return addr

        addr &= 0xFFFFFFFF
        if addr < 0x0A000000:
            index = (addr & 0x0F000000) >> 24
            if (index > 8):
                index = 8
            addr &= 0x00FFFFFF

            if (addr + size <= NDS_MEMORY_SIZE[index]):
                return self.ptr_table[index] + addr
        return False


class DeSmuMEHandler(NdsEmuHandler):
    # DeSmuME_0.9.10?: 0x51E8B90
    CLASS_NAME = "DeSmuME"

    def attach(self):
        succeed = self.attach_window(self.CLASS_NAME, None)
        if succeed:
            self.base_addr = self.proc_base + 0x5411250
        return succeed

    def address_map(self, addr, size):
        if self._raw_addr:
            return addr

        addr &= 0xFFFFFFFF
        if addr < 0x0A000000:
            addr &= 0x00FFFFFF

            if addr + size <= NDS_MEMORY_SIZE[2]:
                return self.base_addr + addr
        return False


class NogbaHandler(NdsEmuHandler):
    PTR_TABLE_BASE = 0x4C3B38
    PTR_TABLE_OFFSET = 0x8E28
    WINDOW_NAME = "No$gba"

    def attach(self):
        succeed = self.attach_window("No$dlgClass", "No$gba Debugger (Fullversion)");
    
        if succeed:
            with self.raw_env():
                address = self.read_ptr(self.PTR_TABLE_BASE)
                if address:
                    ptr_table = self.read(address + self.PTR_TABLE_OFFSET, bytes, 36)
                    self.ptr_table = struct.unpack('9L', ptr_table)
                else:
                    succeed = False
        
        return succeed