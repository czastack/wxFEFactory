from types import SimpleNamespace
from lib.hack.handlers import MemHandler
from tools.base.native import TempArrayPtr
from tools.base.native_hacktool import (
    NativeHacktool, NativeContextArray, call_arg, FunctionCall
)


class MonoHacktool(NativeHacktool):
    """Unity Mono游戏工具"""
    handler_class = MemHandler
    enable_native_call_n = True
    context_array_reuse = 10  # 复用context_array元素个数，0表示不复用
    MONO_FUNCS = (
        # name, arg_sign, ret_type=None, ret_size=4
        ("mono_get_root_domain", None, "ptr"),
        ("mono_image_loaded", "S", "ptr"),
        ("mono_thread_attach", "P"),
        ("mono_thread_detach", "P"),
        ("mono_security_set_mode", "i"),
        ("mono_class_from_name", "PSS", "ptr"),  # (MonoImage *image, const char* name_space, const char *name)
        ("mono_class_get_method_from_name", "PSi", "ptr"),  # (MonoClass *klass, const char *name, int param_count)
        ("mono_class_vtable", "2P", "ptr"),  # (MonoDomain *domain, MonoClass *klass)
        ("mono_class_get_field_from_name", "PS", "ptr"),  # (MonoClass *klass, const char *name)
        ("mono_class_get_property_from_name", "PS", "ptr"),  # (MonoClass *klass, const char *name)
        ("mono_field_get_value", "3P"),  # (MonoObject *obj, MonoClassField *field, void *value)
        ("mono_field_set_value", "3P"),  # idem
        ("mono_field_static_get_value", "3P"),  # (MonoVTable *vt, MonoClassField *field, void *value)
        ("mono_field_static_set_value", "3P"),  # idem
        ("mono_property_set_value", "4P"),  # (MonoProperty *prop, void *obj, void **params, MonoObject **exc);
        ("mono_property_get_value", "4P", "ptr"),  # idem
        ("mono_array_addr_with_size", "PiI", "ptr"),  # (MonoArray *array, int size, uintptr_t idx)
        # ("mono_array_length", "P", "ptr"),  # (MonoArray *array)
        ("mono_compile_method", "P", "ptr"),
        ("mono_runtime_invoke", "4P", "ptr"),  # (MonoMethod *method, void *obj, void **params, MonoObject **exc)
        ("mono_object_unbox", "P", "ptr"),  # (MonoObject *obj)
        ("mono_string_new", "PS", "ptr"),  # (MonoDomain *domain, const char *text)
    )

    def __init__(self):
        super().__init__()
        self.mono_api = SimpleNamespace()
        self.context_array = None

    def onattach(self):
        super().onattach()
        mono = self.handler.get_module("mono.dll")
        if mono == 0:
            return
        helper = self.handler.get_proc_helper(mono)
        address_map = helper.get_proc_address((item[0] for item in self.MONO_FUNCS))
        # 重新获取mono函数表
        self.mono_api.__dict__.clear()
        for name, *args in self.MONO_FUNCS:
            if address_map[name] == 0:
                raise ValueError('mono_api {} not found'.format(name))
            setattr(self.mono_api, name, FunctionCall(address_map[name], *args))

        self.context_array = (
            NativeContextArray(self.handler, self.context_array_reuse, self.NativeContext)
            if self.context_array_reuse else None)

        self.root_domain, self.image = self.native_call_n((
            self.mono_api.mono_get_root_domain(),
            self.mono_api.mono_image_loaded("Assembly-CSharp"),
        ), self.context_array)

    def ondetach(self):
        super().ondetach()
        if self.context_array:
            self.context_array = None

    def mono_security_call(self, args):
        """安全调用mono api"""
        _, _, *result = self.native_call_n((
            self.mono_api.mono_thread_attach(self.root_domain),
            self.mono_api.mono_security_set_mode(0),
            *args
        ), self.context_array)
        return result

    def mono_security_call_1(self, arg):
        """安全调用1个mono api"""
        return self.mono_security_call((arg,))[0]

    def mono_security_call_reuse(self, args):
        """安全调用多个mono api"""
        return self.native_call_n_reuse(args, self.context_array, preset=(
            self.mono_api.mono_thread_attach(self.root_domain),
            self.mono_api.mono_security_set_mode(0),
        ))

    def get_mono_classes(self, items, image=None):
        """根据mono class和mothod name获取mono class
        :param items: ((namespace, name),)
        """
        return self.native_call_n_reuse((
            self.mono_api.mono_class_from_name(image or self.image, *item) for item in items
        ), self.context_array)

    def get_global_mono_classes(self, names, image=None):
        """获取全局命名空间中的mono class"""
        return self.get_mono_classes((("", name) for name in names), image)

    def get_mono_methods(self, items):
        """根据mono class和mothod name获取mono class
        :param items: ((class, name, param_count),)
        """
        return self.native_call_n((
            self.mono_api.mono_class_get_method_from_name(*item) for item in items
        ), self.context_array)

    def get_mono_compile_methods(self, methods):
        """获取编译后的native method地址"""
        return self.mono_security_call(
            (self.mono_api.mono_compile_method(method) for method in methods)
        )

    # def op_mono_runtime_invoke(self, method, object, signature, values):
    #     """返回调用mono函数的call_arg"""
    #     params = TempArrayPtr(signature, values)
    #     return self.mono_api.mono_runtime_invoke(method, object, params, 0)

    def call_mono_string_new(self, text):
        """创建mono string"""
        return self.mono_security_call_1(self.mono_api.mono_string_new(self.root_domain, text))

    def register_classes(self, classes, image=None):
        """注册mono class列表
        :param classes: [MonoClass]
        """
        # 获取class
        items = ((klass.namespace, klass.name) for klass in classes)
        result_iter = iter(self.get_mono_classes(items, image))

        # 获取vtable, methods和fields
        call_args = []
        # 获取编译的函数
        compile_call_args = []
        for klass in classes:
            klass.mono_class = next(result_iter)

            if klass.mono_class == 0:
                raise ValueError('{} not found'.format(klass))

            if klass.need_vtable:
                call_args.append(self.mono_api.mono_class_vtable(self.root_domain, klass.mono_class))

            for method in klass.methods:
                call_args.append(self.mono_api.mono_class_get_method_from_name(
                    klass.mono_class, method.name, method.param_count))
            for field in klass.fields:
                call_args.append(self.mono_api.mono_class_get_field_from_name(
                    klass.mono_class, field.name))
            for prop in klass.properties:
                call_args.append(self.mono_api.mono_class_get_property_from_name(
                    klass.mono_class, prop.name))

        # 绑定函数、字段和属性
        result_iter = iter(self.native_call_n_reuse(call_args, self.context_array))
        for klass in classes:
            if klass.need_vtable:
                klass.mono_vtable = next(result_iter)
                klass.owner = self.weak

                if not klass.need_vtable:
                    raise ValueError('{}.mono_vtable not found'.format(klass.name))

            for method in klass.methods:
                method.mono_method = next(result_iter)
                if not method.mono_method:
                    raise ValueError('{}.mono_method not found'.format(method.name))
                # 获取编译的函数
                if method.compile:
                    compile_call_args.append(self.mono_api.mono_compile_method(method.mono_method))

            for field in klass.fields:
                field.mono_field = next(result_iter)
                if not field.mono_field:
                    raise ValueError('{}.mono_field not found'.format(field.name))

            for prop in klass.properties:
                prop.mono_property = next(result_iter)
                if not prop.mono_property:
                    raise ValueError('{}.mono_property not found'.format(prop.name))

        # 绑定编译的函数
        if compile_call_args:
            result_iter = iter(self.mono_security_call(compile_call_args))
            for klass in classes:
                for method in klass.methods:
                    if method.compile:
                        method.mono_compile = next(result_iter)
