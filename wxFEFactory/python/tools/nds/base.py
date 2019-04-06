from lib.hack.handlers import ProxyHandler
from lib.hack.handlers.ndshandler import DeSmuMEHandler, NogbaHandler
from ..hacktool import ProxyHackTool


class BaseNdsHack(ProxyHackTool):
    handler_class = DeSmuMEHandler, NogbaHandler
