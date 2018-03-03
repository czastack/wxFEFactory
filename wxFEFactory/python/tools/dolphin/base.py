from lib.hack.handler import BigendHandler
from ..hacktool import BaseHackTool


OFFSET_MAP = {
    '5.0': 0x1193320,
    '5.0-6372': 0x139DC88,
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
        if self.handler.active:
            self.free_remote_function()

        self.window_name = None
        self.handler.enumWindows(self._enum_window, 'Dolphin ')
        if self.window_name:
            if self.handler.attachByWindowHandle(self.hwnd):
                offset = OFFSET_MAP.get(self.window_name[8:], None)
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
                    self.init_remote_function()
                    return True
                else:
                    self.attach_status_view.label = '绑定失败, 不支持的版本: %s' % self.window_name
                    return False

        self.attach_status_view.label = '绑定失败'
        return False
