from lib.hack.handler import BigendHandler
from ..hacktool import BaseHackTool


OFFSET_MAP = {
    '5.0': 0x1193320,
    '5.0-6372': 0x139DC88,
}


class BaseDolphinHack(BaseHackTool):
    CLASS_NAME = 'wxWindowNR'
    WINDOW_NAME = 'Dolphin 5.0-6372'

    def __init__(self):
        super().__init__()
        self.handler = BigendHandler()

    def check_attach(self, _=None):
        if super().check_attach():
            self.ramaddr = self.handler.readAddr(self.handler.base + 0x139DC88)
            return True
        return False
