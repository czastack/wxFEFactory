from lib.hack.handlers import ProxyHandler
from lib.hack.handlers.gbahandler import VbaHandler, NogbaHandler
from tools.base.hacktool import ProxyHackTool


class BaseGbaHack(ProxyHackTool):
    handler_class = VbaHandler, NogbaHandler
