from functools import partial
from lib import extypes
from .assembly_hacktool import AssemblyHacktool, AssemblyItem
from .native import NativeContext, NativeContext64, NativeContextArray, ResultResolver
import base64


class NativeHacktool(AssemblyHacktool):
    NativeContext = None
    enable_native_call_n = False

    # x86 native_call
    FUNCTION_NATIVE_CALL = base64.b64decode(b'VYvsg+wMVot1CFeLVgiLAot6BINGBP6LTgRBiUX0iX34g/kBfg+LBIqJRfz/dfxJg/kBf/GD/'
        b'wF2A4tN+P9V9IlFCIX/dQyLRgTB4AKJRfQDZfSLDotFCF9eiQGL5V3DuAAQFADD')

    # x64 native_call
    FUNCTION_NATIVE_CALL_64 = base64.b64decode(
        b'TIvcSYlbGEmJayBWV0FWSIPsMEiLcRBMi/FIiz5Ii24ISIPGEEmJe9hIixaDQQj9i1kISIXSdAz/w0jB5whJiXvY6wRIg8YISDP/g/sFfERIg'
        b'8YgSIPrBEyNFN0gAAAASYvCSIPgD0iFwHQESYPCCEkr4kiL/EiDxyBIM8mLy/NIpUmL+oPDBEkr8kiFwHQESIPGCIP7AQ+MhAAAAEGKQ9g8AH'
        b'QQPAF0BvIPEAbrCfMPEAbrA0iLDoP7AnxkQYpD2TwAdBI8AXQH8g8QTgjrC/MPEE4I6wRIi1YIg/sDfEFBikPaPAB0EjwBdAfyDxBWEOsL8w8'
        b'QVhDrBEyLRhCD+wR8HkGKQ9s8AHQSPAF0B/IPEF4Y6wvzDxBeGOsETItOGP/VSYsOSIkB8w8RQQjyDxFBEEiF/3QDSAPnSIPEMEFeX17D'
    )

    # x86 native_call_n
    FUNCTION_NATIVE_CALL_N = base64.b64decode(
        b'VYvsUcdF/AAAAADrCYtF/IPAAYlF/ItN/DtNEH0TaVX8jAAAAANVDFL/VQiDxATr3IvlXcM=')

    # x64 native_call_n
    FUNCTION_NATIVE_CALL_N_64 = base64.b64decode(b'RIlEJBhIiVQkEEiJTCQISIPsOMdEJCAAAAAA6wqLRCQg/8CJRCQgi0QkUDlEJCB9IEhj'
        b'RCQgSGnAoAAAAEiLTCRISAPISIvBSIvI/1QkQOvMSIPEOMM=')

    def onattach(self):
        """初始化远程函数"""
        super().onattach()
        self.native_call_addr = self.handler.write_function(self.FUNCTION_NATIVE_CALL if self.is32process
            else self.FUNCTION_NATIVE_CALL_64)
        if self.enable_native_call_n:
            self.native_call_n_addr = self.handler.write_function(self.FUNCTION_NATIVE_CALL_N if self.is32process
                else self.FUNCTION_NATIVE_CALL_N_64)
        if self.NativeContext is None:
            self.NativeContext = NativeContext if self.is32process else NativeContext64
        # 初始化Native调用的参数环境
        context_addr = self.handler.alloc_memory(self.NativeContext.SIZE)
        self.native_context = self.NativeContext(context_addr, self.handler)

    def ondetach(self):
        """释放远程函数"""
        super().ondetach()
        self._cached_address = None
        self.handler.free_memory(self.native_call_addr)
        if self.enable_native_call_n:
            self.handler.free_memory(self.native_call_n_addr)
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
        return self.native_call(self.native_call_addr, '2L' + (arg_sign if arg_sign is not None else ''),
            addr, this, *args, ret_type=ret_type, ret_size=ret_size)

    def native_call_64(self, addr, arg_sign, *args, this=0, ret_type=int, ret_size=8):
        """ 以x64默认调用约定调用远程函数
        :param addr: 目标函数地址
        :param this: this指针，为0则为普通函数
        :param arg_sign: 参数签名
        """
        return self.native_call(self.native_call_addr, 'p2Q' + (arg_sign if arg_sign is not None else ''),
            self.native_context.fflag, addr, this, *args, ret_type=ret_type, ret_size=ret_size)

    def native_call_sys(self, *args, **kwargs):
        """根据程序位数自动选择调用的函数native_call函数"""
        if issubclass(self.NativeContext, NativeContext64):
            return self.native_call_64(*args, **kwargs)
        else:
            return self.native_call_auto(*args, **kwargs)

    def native_call_1(self, item):
        """ 调用一项
        :param item: call_arg
        """
        self.native_call_sys(item['addr'], item['arg_sign'], *item['args'],
            this=item['this'], ret_type=item['ret_type'], ret_size=item['ret_size'])
        # 函数结果
        ret_type = item['ret_type']
        if ret_type:
            if isinstance(ret_type, ResultResolver):
                result = ret_type.get_result(self.native_context)
            else:
                result = self.native_context.get_result(ret_type, item['ret_size'])
        else:
            result = None
        return result

    def native_call_n(self, call_list, context_array=None):
        """一次调用多个函数
        :param call_list: call_arg[]
        """
        if not extypes.is_list_tuple(call_list):
            call_list = tuple(call_list)
        context_reuse = context_array is not None
        if not context_reuse:
            context_array = NativeContextArray(self.handler, len(call_list), self.NativeContext)
        for i, item in enumerate(call_list):
            context = context_array[i]
            if context_reuse:
                context.reset()
            if issubclass(self.NativeContext, NativeContext64):
                context.push('p2Q' + (item['arg_sign'] if item['arg_sign'] is not None else ''),
                    context.fflag, item['addr'], item['this'], *item['args'])
            else:
                context.push('2L' + (item['arg_sign'] if item['arg_sign'] is not None else ''),
                    item['addr'], item['this'], *item['args'])

        self.native_call_sys(self.native_call_n_addr, '2Pi',
            self.native_call_addr, context_array.addr, len(call_list))

        # 函数结果列表
        results = []
        for i, item in enumerate(call_list):
            ret_type = item['ret_type']
            if ret_type:
                if isinstance(ret_type, ResultResolver):
                    result = ret_type.get_result(context_array[i])
                else:
                    result = context_array[i].get_result(ret_type, item['ret_size'])
            else:
                result = None
            results.append(result)
        return results

    def get_cached_address(self, key, original, find_start, find_end, find_base=True):
        """缓存的函数"""
        cached_address = getattr(self, '_cached_address', None)
        if cached_address is None:
            cached_address = self._cached_address = {}
        addr = cached_address.get(key, None)
        if addr is None:
            addr = self.find_address(original, find_start, find_end, find_base)
        return addr


def call_arg(addr, arg_sign, *args, this=0, ret_type=None, ret_size=4):
    return {'addr': addr, 'arg_sign': arg_sign, 'args': args,
        'this': this, 'ret_type': ret_type, 'ret_size': ret_size}


call_arg_int32 = partial(call_arg, ret_type=int, ret_size=4)
call_arg_int64 = partial(call_arg, ret_type=int, ret_size=8)
