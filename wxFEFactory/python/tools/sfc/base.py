from lib.hack.handlers.sfchandler import Snes9xHandler
from ..hacktool import BaseHackTool


class BaseSfcHack(BaseHackTool):
    handler_class = Snes9xHandler
