from lib.hack.handlers.wiihandler import DolphinHandler
from tools.base.hacktool import BaseHackTool


class BaseDolphinHack(BaseHackTool):
    handler_class = DolphinHandler
