from lib.hack.handlers.sfchandler import Snes9xHandler
from ..hacktool import BaseHackTool


class BaseSfcHack(BaseHackTool):
    def __init__(self):
        super().__init__()
        self.handler = Snes9xHandler()
