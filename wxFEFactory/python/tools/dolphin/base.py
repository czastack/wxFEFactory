from lib.hack.handlers.wiihandler import DolphinHandler
from ..hacktool import BaseHackTool


class BaseDolphinHack(BaseHackTool):
    handler_class = DolphinHandler
