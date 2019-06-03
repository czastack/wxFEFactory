from .handler import BigendHandler


class DolphinHandler(BigendHandler):
    CLASS_NAME = 'Dolphin'  # 只用于显示

    OFFSET_MAP = {
        '4.0.2': 0x4968938,
        '5.0': 0x1193320,
        '5.0-6372': 0x139DC88,
        '5.0-6414': 0x139DCC8,
    }

    def address_map(self, addr):
        if self._raw_addr:
            return addr

        return self.ram_addr + addr

    def attach(self):
        self.WINDOW_NAME = None
        self.enum_windows(self._enum_window, 'Dolphin ')
        if self.WINDOW_NAME:
            if self.attach_handle(self.hwnd):
                self.version = self.WINDOW_NAME[8:]
                offset = self.OFFSET_MAP.get(self.version, None)
                if offset:
                    with self.raw_env():
                        self.ram_addr = self.read_addr(self.base_addr + offset)
                    return True
        return False

    def _enum_window(self, hwnd, title):
        if len(title) < 20 and title[8].isdigit():
            self.WINDOW_NAME = title
            self.hwnd = hwnd
            return False
        return True
