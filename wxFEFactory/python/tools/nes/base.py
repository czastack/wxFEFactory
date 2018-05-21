from lib.hack.handler import ProxyHandler
from lib.hack.neshandler import VirtuaNesHandler
from ..hacktool import BaseHackTool


class BaseNesHack(BaseHackTool):
    def __init__(self):
        super().__init__()
        self.handler = ProxyHandler()

    def check_attach(self, _=None):
        if self.handler.active:
            self.ondetach()
            
        for Handler in (VirtuaNesHandler, ):
            handler = Handler()
            if handler.attach():
                self.handler.set(handler)
                self.attach_status_view.label = handler.WINDOW_NAME + ' 正在运行'
                if not self.win.hotkeys:
                    hotkeys = self.get_hotkeys()
                    if hotkeys:
                        self.win.RegisterHotKeys(hotkeys)
                self.onattach()
                return True
        else:
            self.attach_status_view.label = '绑定失败, 未找到支持的模拟器进程'
            return False
