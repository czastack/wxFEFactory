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

    InvalidateCacheRangeAsm = [
        b'\x48\xA1',
        bytes.fromhex('4C 8B C2 48 8B D1 48 8B 48 48 48 8B 01 FF 50 28 C3')
    ]

    def __init__(self):
        super().__init__()
        self.hwnd = None
        self.g_memory = 0
        self.s_instance = 0
        self.InvalidateCacheRangeAddr = 0

    def __del__(self):
        if self.InvalidateCacheRangeAddr:
            self.free_memory(self.InvalidateCacheRangeAddr)

    def attach(self):
        self.enum_windows(self._enum_window, 'Citra ')
        succeed = False
        if self.hwnd:
            succeed = self.attach_handle(self.hwnd)
        if succeed:
            with self.raw_env():
                # 查找g_memory
                find_start = self.base_addr + 0x130000
                asm_start = self.find_bytes(b'\x41\xB8\x00\x40\x00\x00\x31\xD2\x48\x8D\x35',
                    find_start, find_start + 0x20000)
                if asm_start != -1:
                    g_memory_start = asm_start + 18
                    offset = self.read_int(g_memory_start, 4)
                    g_memory_start = g_memory_start + offset + 4
                    self.g_memory = self.read_ptr(g_memory_start)

                    # 查找Core::System::GetInstance()
                    mov_rax_720 = self.read(asm_start, bytes, 0x80).find(
                        b'\x48\xB8\xD0\x02\x00\x00\x00\x30\x27\x18\x48\x8B\x0D')
                    if mov_rax_720 != -1:
                        s_instance_start = asm_start + mov_rax_720 + 13
                        offset = self.read_int(s_instance_start, 4)
                        s_instance_start = s_instance_start + offset + 4

                        self.InvalidateCacheRangeAddr = self.write_function(
                            s_instance_start.to_bytes(8, 'little').join(self.InvalidateCacheRangeAsm),
                            self.InvalidateCacheRangeAddr
                        )
                    else:
                        print('无法使用InvalidateCacheRangeAddr')
                else:
                    print('不支持的Citra版本！')

        return succeed

    def _enum_window(self, hwnd, title):
        if title.startswith('Citra '):
            self.WINDOW_NAME = title
            self.hwnd = hwnd
            return False
        return True

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
