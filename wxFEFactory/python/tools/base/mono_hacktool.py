from lib.hack.handlers import MemHandler
from tools.base.native_hacktool import NativeHacktool, NativeContextArray, call_arg, call_arg_int64


class MonoHacktool(NativeHacktool):
    handler_class = MemHandler
    enable_native_call_n = True
    context_array_reuse = 10  # 复用context_array元素个数，0表示不复用
    MONO_FUNC = {
        "mono_get_root_domain": None,
        "mono_image_loaded": "s",
        "mono_thread_attach": "P",
        "mono_thread_detach": "P",
        "mono_security_set_mode": "i",
        "mono_class_from_name": "Pss",
        "mono_class_get_method_from_name": "Psi",
        # "mono_class_get_field_from_name": "Ps",
        # "mono_field_get_value ": "3P",
        "mono_compile_method": "P",
    }

    def onattach(self):
        super().onattach()
        mono = self.handler.get_module("mono.dll")
        if mono is 0:
            return
        helper = self.handler.get_proc_helper(mono)
        for name, sign in self.MONO_FUNC.items():
            setattr(self, name, (helper.get_proc_address(name), sign))

        self.context_array = (NativeContextArray(self.handler, self.context_array_reuse, self.NativeContext)
            if self.context_array_reuse else None)

        self.root_domain, self.image = self.native_call_n((
            call_arg_int64(*self.mono_get_root_domain),
            call_arg_int64(*self.mono_image_loaded, "Assembly-CSharp"),
        ), self.context_array)
        # print(hex(self.image))

    def ondetach(self):
        super().ondetach()
        if self.context_array:
            self.context_array = None
