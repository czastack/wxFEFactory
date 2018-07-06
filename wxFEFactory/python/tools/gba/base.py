from lib.hack.handlers import ProxyHandler
from lib.hack.handlers.gbahandler import VbaHandler, NogbaHandler
from ..hacktool import ProxyHackTool


class BaseGbaHack(ProxyHackTool):
    handlers = VbaHandler, NogbaHandler
