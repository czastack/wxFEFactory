from lib.hack.handlers.ps2handler import Pcsx2Handler
from ..hacktool import BaseHackTool


class BasePs2Hack(BaseHackTool):
    handler_class = Pcsx2Handler
