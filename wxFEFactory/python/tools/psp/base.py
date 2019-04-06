from lib.hack.handlers.psphandler import PPSSPPHandler
from ..hacktool import BaseHackTool


class BasePspHack(BaseHackTool):
    handler_class = PPSSPPHandler
