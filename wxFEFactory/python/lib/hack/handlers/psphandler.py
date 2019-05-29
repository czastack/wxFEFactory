import re
from .handler import MemHandler


class PPSSPPHandler(MemHandler):
    CLASS_NAME = 'PPSSPPWnd'
    WINDOW_NAME = None

    BASE_32 = {
        '1.8.0': 0x00B54008,
        'default': 0x00B54008,
    }

    BASE_64 = {
        '1.8.0': 0x00DC8FB0,
        'default': 0x00DC8FB0,
    }

    # 0x00010000, "Scratchpad"
    # 0x04000000, "VRAM"
    # 0x08800000, "User memory"
    # 0x08804000, "Default load address"
    # 0x88000000, "Kernel memory"

    def attach(self):
        succeed = self.attach_window(self.CLASS_NAME, self.WINDOW_NAME)
        if succeed:
            BASE = self.BASE_32 if self.is32process else self.BASE_64
            window_text = self.window_text
            match = re.match(r'^PPSSPP v(\d(\.\d)+)', window_text)
            version = match.group(1) if match else 'default'
            self.base = self.raw_read(BASE[version] + self.base_addr, size=self.ptr_size)
            # for cheats
            self.user_memory = self.base + 0x08800000

        return succeed

    def address_map(self, addr):
        if self._raw_addr:
            return addr

        return self.user_memory + addr
