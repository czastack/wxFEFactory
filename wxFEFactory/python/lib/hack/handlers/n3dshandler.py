import struct
from .handler import LookAfterHandler


N3DS_MEMORY_SIZE = (

)


class N3dsEmuHandler(LookAfterHandler):
    pass
    # def address_map(self, addr):
    #     if self._raw_addr:
    #         return addr

    #     return False



PAGE_MASK = 0x0FFF


class CitraHandler(N3dsEmuHandler):
    CLASS_NAME = "Qt5QWindowOwnDCIcon"
    WINDOW_NAME = "Citra"

    InvalidateCacheRangeAsm = [
        b'\x48\xA1',
        bytes.fromhex('4C 8B C2 48 8B D1 48 8B 48 48 48 8B 01 FF 50 28 C3')
    ]

    # CLASS_NAME = "Qt5QWindowIcon"
    # WINDOW_NAME = "Citra Nightly 1419 | Fire Emblem Echoes"

    def __init__(self):
        super().__init__()
        self.g_memory = 0
        self.s_instance = 0
        self.InvalidateCacheRangeAddr = 0

    def attach(self):
        succeed = self.attach_window(self.CLASS_NAME, None)
        if succeed:
            with self.raw_env():
                # 查找g_memory
                find_start = self.base_addr + 0x13E000
                asm_start = self.find_bytes(b'\x41\xB8\x00\x40\x00\x00\x31\xD2\x48\x8D\x35',
                    find_start, find_start + 0x10000)
                if asm_start:
                    g_memory_start = asm_start + 18
                    offset = self.read_int(g_memory_start, 4)
                    g_memory_start = g_memory_start + offset + 4
                    self.g_memory = self.read_ptr(g_memory_start)

                # 查找RPCServer::HandleWriteMemory
                find_start = self.base_addr + 0x14D000
                asm_start = self.find_bytes(b'\x49\x89\xE8\x89\xF2\x48\x8B\x48\x48\x48\x8B\x01',
                    find_start, find_start + 0x10000)
                if asm_start:
                    s_instance_start = asm_start - 4
                    offset = self.read_int(s_instance_start, 4)
                    s_instance_start = s_instance_start + offset + 4

                    self.InvalidateCacheRangeAddr = self.write_function(
                        s_instance_start.to_bytes(8, 'little').join(self.InvalidateCacheRangeAsm)
                    )
                else:
                    print('无法使用InvalidateCacheRangeAddr')

        return succeed

    def address_map(self, addr):
        if self._raw_addr:
            return addr

        addr &= 0xFFFFFFFF
        if self.g_memory:
            page_pointer = (addr >> 12) * 8
            offset = addr & PAGE_MASK
            with self.raw_env():
                return self.ptrs_read(self.g_memory, (0x18, page_pointer)) + offset
        return False
