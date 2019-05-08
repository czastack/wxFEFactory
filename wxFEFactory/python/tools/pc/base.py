from lib.hack.handlers import MemHandler
from tools.base.hacktool import BaseHackTool


class BasePcHack(BaseHackTool):
    handler_class = MemHandler
