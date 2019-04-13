from .assembly_hacktool import AssemblyHacktool, AssemblyItem
from .native import NativeContext, NativeContext64
import base64


class NativeHacktool(AssemblyHacktool):
    NativeContext = None

    FUNCTION_NATIVE_CALL = base64.b64decode(b'VYvsg+wMVot1CFeLVgiLAot6BINGBP6LTgRBiUX0iX34g/kBfg+LBIqJRfz/dfxJg/kBf/GD/'
        b'wF2A4tN+P9V9IlFCIX/dQyLRgTB4AKJRfQDZfSLDotFCF9eiQGL5V3DuAAQFADD')

    # x64 native_call
    FUNCTION_NATIVE_CALL_64 = base64.b64decode(
        b'TIvcSYlbGEmJayBWV0FWSIPsMEiLcRBMi/FIiz5Ii24ISIPGEEmJe9hIixaDQQj9i1kISIXSdAz/w0jB5whJiXvY6wRIg8YISDP/g/sFfERIg'
        b'8YgSIPrBEyNFN0gAAAASYvCSIPgD0iFwHQESYPCCEkr4kiL/EiDxyBIM8mLy/NIpUmL+oPDBEkr8kiFwHQESIPGCIP7AQ+MhAAAAEGKQ9g8AH'
        b'QQPAF0BvIPEAbrCfMPEAbrA0iLDoP7AnxkQYpD2TwAdBI8AXQH8g8QTgjrC/MPEE4I6wRIi1YIg/sDfEFBikPaPAB0EjwBdAfyDxBWEOsL8w8'
        b'QVhDrBEyLRhCD+wR8HkGKQ9s8AHQSPAF0B/IPEF4Y6wvzDxBeGOsETItOGP/VSYsOSIkB8w8RQQjyDxFBEEiF/3QDSAPnSIPEMEFeX17D'
    )

    def onattach(self):
        """初始化远程函数"""
        super().onattach()
        is32process = self.handler.is32process
        self.NativeCall = self.handler.write_function(self.FUNCTION_NATIVE_CALL if is32process
            else self.FUNCTION_NATIVE_CALL_64)
        if self.NativeContext is None:
            self.NativeContext = NativeContext if is32process else NativeContext64
        # 初始化Native调用的参数环境
        context_addr = self.handler.alloc_memory(self.NativeContext.SIZE)
        self.native_context = self.NativeContext(context_addr, self.handler)

    def ondetach(self):
        """释放远程函数"""
        super().ondetach()
        self._cached_address = None
        self.handler.free_memory(self.NativeCall)
        self.handler.free_memory(self.native_context.addr)

    def native_call(self, addr, arg_sign, *args, ret_type=int, ret_size=4):
        """ 远程调用参数为NativeContext*的函数
        :param arg_sign: 函数签名
        """
        with self.native_context:
            if arg_sign:
                self.native_context.push(arg_sign, *args)
            self.handler.remote_call(addr, self.native_context.addr)
            if ret_type:
                return self.native_context.get_result(ret_type, ret_size)

    def native_call_auto(self, addr, arg_sign, *args, this=0, ret_type=int, ret_size=4):
        """ 以cdcel, stdcall或thiscall形式调用远程函数(x86)
        :param addr: 目标函数地址
        :param this: this指针，为0时使用cdecl, 1时使用stdcall, 大于1时使用thiscall
        :param arg_sign: 参数签名
        """
        return self.native_call(self.NativeCall, '2P' + (arg_sign if arg_sign is not None else ''),
            addr, this, *args, ret_type=ret_type, ret_size=ret_size)

    def native_call_64(self, addr, arg_sign, *args, this=0, ret_type=int, ret_size=8):
        """ 以x64默认调用约定调用远程函数
        :param addr: 目标函数地址
        :param this: this指针，为0则为普通函数
        :param arg_sign: 参数签名
        """
        self.native_call(self.NativeCall, 'p2Q' + (arg_sign if arg_sign is not None else ''),
            self.native_context.fflag, addr, this, *args, ret_type=None, ret_size=ret_size)
        # 获取结果
        if ret_type is not float:
            return self.native_context.get_result(ret_type, ret_size)
        else:
            if ret_size is 8:
                return self.handler.read_double(self.native_context.m_pReturn + 16)
            return self.handler.read_float(self.native_context.m_pReturn + 8)

    def get_cached_address(self, key, original, find_start, find_end, find_base=True):
        cached_address = getattr(self, '_cached_address', None)
        if cached_address is None:
            cached_address = self._cached_address = {}
        addr = cached_address.get(key, None)
        if addr is None:
            addr = self.find_address(original, find_start, find_end, find_base)
        return addr
