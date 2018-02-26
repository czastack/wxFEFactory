from lib.hack.handler import BigendHandler
from ..hacktool import BaseHackTool


class BaseDolphinHack(BaseHackTool):
    CLASS_NAME = 'wxWindowNR'
    WINDOW_NAME = 'Dolphin 5.0-6372'

    def __init__(self):
        super().__init__()
        self.handler = BigendHandler()

    def check_attach(self, _=None):
        if super().check_attach():
            self.ramaddr = self.handler.readAddr(self.handler.base + 0x14139DC88 - 0x140000000)
            return True
        return False
