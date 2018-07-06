from lib.hack.handlers.handler import BigendHandler
from ..hacktool import BaseHackTool


OFFSET_MAP = {
    '4.0.2': 0x4968938,
    '5.0': 0x1193320,
    '5.0-6372': 0x139DC88,
    '5.0-6414': 0x139DCC8,
}


class DolphinHandler(BigendHandler):
    def address_map(self, addr, size=0):
        if self._raw_addr:
            return addr

        return self.ram_addr + addr

    def attach(self):
        self.window_name = None
        self.enum_windows(self._enum_window, 'Dolphin ')
        if self.window_name:
            if self.attach_handle(self.hwnd):
                self.version = self.window_name[8:]
                offset = OFFSET_MAP.get(self.version, None)
                if offset:
                    with self.raw_env():
                        self.ram_addr = self.read_addr(self.base + offset)
                    return True
        return False


    def _enum_window(self, hwnd, title):
        if len(title) < 20 and title[8].isdigit():
            self.window_name = title
            self.hwnd = hwnd 
            return False
        return True



class BaseDolphinHack(BaseHackTool):
    def __init__(self):
        super().__init__()
        self.handler = DolphinHandler()

    def check_attach(self, _=None):
        if self.handler.active:
            self.ondetach()

        if self.handler.attach():
            self.attach_status_view.label = self.handler.window_name + ' 正在运行'
            if not self.win.hotkeys:
                hotkeys = self.get_hotkeys()
                if hotkeys:
                    self.win.RegisterHotKeys(hotkeys)
                self.onattach()
            return True
        else:
            self.attach_status_view.label = (('绑定失败, 不支持的版本: %s' % self.handler.window_name) 
                if self.handler.window_name else '绑定失败')
            return False
