from lib.hack.handlers import MemHandler
from tools.base.native_hacktool import (
    NativeHacktool, NativeContextArray, call_arg, call_arg_int32, call_arg_int64
)


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
        "mono_class_from_name": "Pss",  # (MonoImage *image, const char* name_space, const char *name)
        "mono_class_get_method_from_name": "Psi",  # (MonoClass *klass, const char *name, int param_count)
        "mono_class_vtable": "2P",  # (MonoDomain *domain, MonoClass *klass)
        "mono_class_get_field_from_name": "Ps",  # (MonoClass *klass, const char *name)
        "mono_field_get_value": "3P",  # (MonoObject *obj, MonoClassField *field, void *value)
        "mono_field_static_get_value": "3P",  # (MonoVTable *vt, MonoClassField *field, void *value)
        "mono_field_static_set_value": "3P",  # idem
        "mono_array_addr_with_size": "PiI",  # (MonoArray *array, int size, uintptr_t idx)
        "mono_compile_method": "P",
    }

    def onattach(self):
        super().onattach()
        mono = self.handler.get_module("mono.dll")
        if mono is 0:
            return
        helper = self.handler.get_proc_helper(mono)
        address_map = helper.get_proc_address(self.MONO_FUNC.keys())
        for name, sign in self.MONO_FUNC.items():
            setattr(self, name, (address_map[name], sign))

        self.context_array = (NativeContextArray(self.handler, self.context_array_reuse, self.NativeContext)
            if self.context_array_reuse else None)

        self.call_arg_int = call_arg_int32 if self.is32process else call_arg_int64

        self.root_domain, self.image = self.native_call_n((
            self.call_arg_int(*self.mono_get_root_domain),
            self.call_arg_int(*self.mono_image_loaded, "Assembly-CSharp"),
        ), self.context_array)
        # print(hex(self.image))

    def ondetach(self):
        super().ondetach()
        if self.context_array:
            self.context_array = None

    def get_mono_classes(self, items):
        """根据mono class和mothod name获取mono class
        :param items: ((namespace, name),)
        """
        return self.native_call_n((
            self.call_arg_int(*self.mono_class_from_name, self.image, *item) for item in items
        ), self.context_array)

    def get_global_mono_classes(self, names):
        """获取全局命名空间中的mono class"""
        return self.get_mono_classes((("", name) for name in names))

    def get_mono_methods(self, items):
        """根据mono class和mothod name获取mono class
        :param items: ((class, name, param_count),)
        """
        return self.native_call_n((
            self.call_arg_int(*self.mono_class_get_method_from_name, *item) for item in items
        ), self.context_array)

    def get_mono_compile_methods(self, methods):
        """获取编译后的native method地址"""
        _, _, *result = self.native_call_n((
            call_arg(*self.mono_thread_attach, self.root_domain),
            call_arg(*self.mono_security_set_mode, 0),
            *(self.call_arg_int(*self.mono_compile_method, method) for method in methods)
        ), self.context_array)
        return result

    # def arg_mono_class_vtable(self, klass):
    #     return self.call_arg_int(*self.mono_class_vtable, self.root_domain, klass),

    # def arg_mono_class_get_field_from_name(self, klass, name):
    #     return self.call_arg_int(*self.mono_class_get_field_from_name, klass, name)
