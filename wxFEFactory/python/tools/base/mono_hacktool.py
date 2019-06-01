from lib.extypes import WeakBinder
from lib.hack.handlers import MemHandler
from tools.base.native import TempArrayPtr
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
        "mono_class_get_property_from_name": "Ps",  # (MonoClass *klass, const char *name)
        "mono_field_get_value": "3P",  # (MonoObject *obj, MonoClassField *field, void *value)
        "mono_field_set_value": "3P",  # idem
        "mono_field_static_get_value": "3P",  # (MonoVTable *vt, MonoClassField *field, void *value)
        "mono_field_static_set_value": "3P",  # idem
        "mono_property_set_value": "4P",  # (MonoProperty *prop, void *obj, void **params, MonoObject **exc);
        "mono_property_get_value": "4P",  # idem
        "mono_array_addr_with_size": "PiI",  # (MonoArray *array, int size, uintptr_t idx)
        # "mono_array_length": "P",  # (MonoArray *array)
        "mono_compile_method": "P",
        "mono_runtime_invoke": "4P",  # (MonoMethod *method, void *obj, void **params, MonoObject **exc)
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

    def mono_security_call(self, args):
        _, _, *result = self.native_call_n((
            call_arg(*self.mono_thread_attach, self.root_domain),
            call_arg(*self.mono_security_set_mode, 0),
            *args
        ), self.context_array)
        return result

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
        return self.mono_security_call(
            (self.call_arg_int(*self.mono_compile_method, method) for method in methods)
        )

    def op_mono_runtime_invoke(self, method, object, signature, values):
        """返回调用mono函数的call_arg"""
        params = TempArrayPtr(signature, values)
        return self.call_arg_int(*self.mono_runtime_invoke, method, object, params, 0)

    def register_classes(self, classes):
        """注册mono class列表
        :param classes: [MonoClass]
        """
        # 获取class
        items = ((klass.namespace, klass.name) for klass in classes)
        result_iter = iter(self.get_mono_classes(items))

        # 获取vtable, methods和fields
        call_args = []
        # 获取编译的函数
        compile_call_args = []
        for klass in classes:
            klass.mono_class = next(result_iter)

            if klass.need_vtable:
                call_args.append(self.call_arg_int(*self.mono_class_vtable, self.root_domain, klass.mono_class))

            for method in klass.methods:
                call_args.append(self.call_arg_int(*self.mono_class_get_method_from_name,
                    klass.mono_class, method.name, method.param_count))
            for field in klass.fields:
                call_args.append(self.call_arg_int(*self.mono_class_get_field_from_name,
                    klass.mono_class, field.name))
            for prop in klass.properties:
                call_args.append(self.call_arg_int(*self.mono_class_get_property_from_name,
                    klass.mono_class, prop.name))

        # 绑定函数、字段和属性
        result_iter = iter(self.native_call_n_reuse(call_args, self.context_array))
        for klass in classes:
            if klass.need_vtable:
                klass.mono_vtable = next(result_iter)
                klass.owner = self.weak

            for method in klass.methods:
                method.mono_method = next(result_iter)
                # 获取编译的函数
                if method.compile:
                    compile_call_args.append(self.call_arg_int(*self.mono_compile_method, method.mono_method))

            for field in klass.fields:
                field.mono_field = next(result_iter)

            for prop in klass.properties:
                prop.mono_field = next(result_iter)

        # 绑定编译的函数
        if compile_call_args:
            result_iter = iter(self.mono_security_call(compile_call_args))
            for klass in classes:
                for method in klass.methods:
                    if method.compile:
                        method.mono_compile = next(result_iter)
