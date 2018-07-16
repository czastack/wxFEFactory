from lib.hack.handlers.ps2handler import Pcsx2Handler
from ..hacktool import BaseHackTool


class BasePs2Hack(BaseHackTool):
    def __init__(self):
        super().__init__()
        self.handler = Pcsx2Handler()
