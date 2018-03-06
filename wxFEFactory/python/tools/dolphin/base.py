from lib.hack.handler import BigendHandler
from ..hacktool import BaseHackTool


OFFSET_MAP = {
    '4.0.2': 0x4968938,
    '5.0': 0x1193320,
    '5.0-6372': 0x139DC88,
    '5.0-6414': 0x139DCC8,
}


class BaseDolphinHack(BaseHackTool):
    # CLASS_NAME = 'wxWindowNR'
    # WINDOW_NAME = 'Dolphin 5.0-6372'

    def __init__(self):
        super().__init__()
        self.handler = BigendHandler()

    def _enum_window(self, hwnd, title):
        if len(title) < 20 and title[8].isdigit():
            self.window_name = title
            self.hwnd = hwnd 
            return False
        return True

    def check_attach(self, _=None):
        self.window_name = None
        self.handler.enumWindows(self._enum_window, 'Dolphin ')
        if self.window_name:
            if self.handler.attachByWindowHandle(self.hwnd):
                self.version = self.window_name[8:]
                offset = OFFSET_MAP.get(self.version, None)
                if offset:
                    self.ram_addr = self.handler.readAddr(self.handler.base + offset)
                    try:
                        self._ram.addr = self.ram_addr
                    except:
                        pass
                    self.attach_status_view.label = self.window_name + ' 正在运行'
                    if not self.win.hotkeys:
                        hotkeys = self.get_hotkeys()
                        if hotkeys:
                            self.win.RegisterHotKeys(hotkeys)
                    return True
                else:
                    self.attach_status_view.label = '绑定失败, 不支持的版本: %s' % self.window_name
                    return False

        self.attach_status_view.label = '绑定失败'
        return False
