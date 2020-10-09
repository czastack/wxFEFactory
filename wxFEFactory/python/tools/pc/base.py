from lib.hack.handlers import MemHandler
from tools.base.hacktool import BaseHackTool


class PcHacktool(BaseHackTool):
    handler_class = MemHandler
