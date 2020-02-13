from lib.hack.handlers.n3dshandler import CitraHandler
from tools.base.native_hacktool import NativeHacktool


class BaseN3dsHack(NativeHacktool):
    handler_class = CitraHandler

    def __init__(self):
        super().__init__()
        self.handler.after_write = self.InvalidateCacheRange

    def InvalidateCacheRange(self, addr, size):
        if self.native_context and self.handler.InvalidateCacheRangeAddr:
            with self.handler.raw_env():
                self.native_call_sys(self.handler.InvalidateCacheRangeAddr, '2Q', addr, size, ret_type=None)
