import struct
from .handler import MemHandler


GBA_MEMORY_SIZE = (
    0x00003FFF,  # BIOS
    0,           # Const
    0x0003FFFF,  # WRAM
    0x00007FFF,  # IRAM
    0x000003FE,  # IO
    0x000003FF,  # Palette
    0x00017FFF,  # VRAM
    0x000003FF,  # OAM
    0x01FFFFFF,  # ROM
    # 0x01FFFFFF,
    # 0x01FFFFFF,
    # 0x0000FFFF,
)


class GbaEmuHandler(MemHandler):
    def address_map(self, addr):
        if self._raw_addr:
            return addr

        if addr < 0x0A000000:
            index = (addr & 0x0F000000) >> 24
            if (index > 8):
                index = 8
            addr &= 0x00FFFFFF

            if (addr <= GBA_MEMORY_SIZE[index]):
                return self.ptr_table[index] + addr
        return False

    def getRomTitle(self):
        return self.read(0x080000A0, bytes, 16).decode()

    def getRomCode(self):
        return self.read(0x080000AC, bytes, 4).decode()


# struct VBA_PtrEntry
# {
#     DWORD   dwPointer;
#     DWORD   dwSize;
# };

# using PtrEntryRef = const VBA_PtrEntry &;

# struct VBA_PtrStruct
# {
#     VBA_PtrEntry    peBIOS;
#     VBA_PtrEntry    peConst;
#     VBA_PtrEntry    peWRAM;
#     VBA_PtrEntry    peIRAM;
#     VBA_PtrEntry    peIO;
#     VBA_PtrEntry    pePalette;
#     VBA_PtrEntry    peVRAM;
#     VBA_PtrEntry    peOAM;
#     VBA_PtrEntry    peROM;

#     operator const VBA_PtrEntry *() {
#         return  reinterpret_cast<CONST VBA_PtrEntry *>(this);
#     }
# };
class VbaHandler(GbaEmuHandler):
    MAP_ADDR = 0x00604230
    WINDOW_NAME = 'VisualBoyAdvance'

    def attach(self):
        self.hwnd = None
        self.enum_windows(self._enum_window, self.WINDOW_NAME + '-')
        succeed = self.hwnd and self.attach_handle(self.hwnd) or False
        if succeed:
            with self.raw_env():
                ptr_table = self.read(self.MAP_ADDR, bytes, 72)
            self.ptr_table = tuple(int.from_bytes(ptr_table[i * 8: i * 8 + 4], 'little') for i in range(9))

        return succeed

    def _enum_window(self, hwnd, title):
        if len(title) == 21:
            self.hwnd = hwnd
            return False
        return True


class NogbaHandler(GbaEmuHandler):
    PTR_TABLE_BASE = 0x4C3B38
    PTR_TABLE_OFFSET = 0x8E28
    WINDOW_NAME = 'No$gba'

    def attach(self):
        succeed = self.attach_window("No$dlgClass", "No$gba Debugger (Fullversion)")

        if succeed:
            with self.raw_env():
                address = self.read_ptr(self.PTR_TABLE_BASE)
                if address:
                    ptr_table = self.read(address + self.PTR_TABLE_OFFSET, bytes, 36)
                    self.ptr_table = struct.unpack('9L', ptr_table)
                else:
                    succeed = False

        return succeed
