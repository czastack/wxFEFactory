from lib.utils import float32
from tools.base.native_hacktool import call_arg
from tools.base.native import NativeContext, TempPtr, TempArrayPtr


class MonoType:
    pass


class MonoClass(MonoType):
    namespace = ''
    name = None
    vtable = None
    need_vtable = False

    def __init__(self, mono_object, owner):
        self.mono_object = mono_object
        self.owner = owner

    def __init_subclass__(cls):
        super().__init_subclass__()
        if not getattr(cls, '__abstract__', False):
            if cls.name is None:
                cls.name = cls.__name__

            cls.methods = []
            cls.fields = []
            cls.properties = []

            for value in cls.__dict__.values():
                if isinstance(value, MonoField):
                    cls.fields.append(value)
                elif isinstance(value, MonoProperty):
                    cls.properties.append(value)
                elif isinstance(value, MonoMethod):
                    cls.methods.append(value)

    def field(self, name):
        # 兼容lib.hack.models
        return getattr(self.__class__, name)


class MonoMember:
    def __init__(self, name=None):
        self.name = name

    def __set_name__(self, owner, name):
        if self.name is None:
            self.name = name


class MonoTyping:
    """带有类型的数据"""
    def __init__(self, type, size):
        if type is None or issubclass(type, MonoType):
            size = 0
        self.type = type
        self.size = size

    @property
    def real_type(self):
        type = self.type
        if type and issubclass(type, MonoType):
            type = int
        return type

    def case_value(self, result, instance):
        # 转为类实例
        if self.type is not int and callable(self.type):
            if issubclass(self.type, MonoType):
                result = self.type(result, instance.owner)
            else:
                result = self.type(result)
        return result

    def prepare_value(self, value):
        type = self.real_type
        if type and not isinstance(value, type):
            value = type(value)
        return value


class MonoField(MonoMember, MonoTyping):
    """字段"""
    def __init__(self, name=None, type=int, size=4, label=None):
        MonoMember.__init__(self, name)
        MonoTyping.__init__(self, type, size)
        self.label = label
        self.mono_field = None

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        # return BoundField(instance, self)
        return self.get_value(instance)

    def __set__(self, instance, value):
        self.set_value(instance, value)

    def temp_ptr(self, value=None):
        """临时地址"""
        return TempPtr(type=self.real_type, size=self.size, value=value)

    def op_getter(self, instance):
        """用于获取值的call_arg"""
        if not instance.mono_object or not self.mono_field:
            raise ValueError('mono_object或mono_field未初始化')
        temp_ptr = self.temp_ptr()
        return call_arg(*instance.owner.mono_field_get_value, instance.mono_object, self.mono_field,
            temp_ptr, ret_type=temp_ptr)

    def op_setter(self, instance, value):
        """用于设置值的call_arg"""
        if not instance.mono_object or not self.mono_field:
            raise ValueError('mono_object或mono_field未初始化')
        temp_ptr = self.temp_ptr(value)
        return call_arg(*instance.owner.mono_field_set_value, instance.mono_object, self.mono_field, temp_ptr)

    def get_value(self, instance):
        """获取值"""
        result = instance.owner.native_call_1(self.op_getter(instance))
        return self.case_value(result, instance)

    def set_value(self, instance, value):
        """设置值"""
        instance.owner.native_call_1(self.op_setter(instance, self.prepare_value(value)))


class MonoStaticField(MonoField):
    """静态字段"""
    def op_getter(self, instance):
        """用于获取值的call_arg"""
        if not self.mono_field:
            raise ValueError('mono_field未初始化')
        temp_ptr = self.temp_ptr()
        return call_arg(*instance.owner.mono_field_static_get_value,
            instance.mono_vtable, self.mono_field, temp_ptr, ret_type=temp_ptr)

    def op_setter(self, instance, value):
        """用于设置值的call_arg"""
        if not self.mono_field:
            raise ValueError('mono_field未初始化')
        temp_ptr = self.temp_ptr(value)
        return call_arg(*instance.owner.mono_field_static_set_value, instance.mono_vtable, self.mono_field, temp_ptr)


class MonoProperty(MonoMember, MonoTyping):
    """属性"""
    def __init__(self, name=None, type=int, size=4, label=None):
        MonoMember.__init__(self, name)
        MonoTyping.__init__(self, type, size)
        self.label = label
        self.mono_property = None

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        # return BoundField(instance, self)
        return self.get_value(instance)

    def __set__(self, instance, value):
        self.set_value(instance, value)

    def op_getter(self, instance):
        """用于获取值的call_arg"""
        if not self.mono_property:
            raise ValueError('mono_property未初始化')
        return instance.owner.call_arg_ptr(*instance.owner.mono_property_get_value,
            self.mono_property, instance.mono_object, 0, 0)

    def op_setter(self, instance, value):
        """用于设置值的call_arg"""
        if not self.mono_property:
            raise ValueError('mono_property未初始化')
        params = TempArrayPtr(NativeContext.type_signature(self.real_type, self.size), (value,))
        return call_arg(*instance.owner.mono_property_set_value,
            self.mono_property, instance.mono_object, params, 0)

    def get_value(self, instance):
        """获取值"""
        owner = instance.owner
        result = owner.mono_security_call_1(self.op_getter(instance))
        if result and not issubclass(self.type, MonoType):
            # 获取值要先解包，得到地址
            result = owner.native_call_1(owner.call_arg_ptr(*owner.mono_object_unbox, result))
            # TODO 判断类型
            result = owner.handler.read(result, self.real_type, self.size)
        return self.case_value(result, instance)

    def set_value(self, instance, value):
        """设置值"""
        instance.owner.mono_security_call_1(self.op_setter(instance, self.prepare_value(value)))


# class BoundField:
#     """绑定(实例)的字段"""
#     __slots__ = ('instance', 'field')

#     def __init__(self, instance, field):
#         self.instance = instance
#         self.field = field

#     def op_getter(self):
#         return self.field.op_getter(self.instance)

#     @property
#     def value(self):
#         return self.field.get_value(self.instance)

#     @value.setter
#     def value(self, value):
#         return self.field.set_value(self.instance, value)


class MonoMethod(MonoMember, MonoTyping):
    """mono方法"""
    def __init__(self, name=None, param_count=0, signature=None, compile=False, type=None, size=4):
        MonoMember.__init__(self, name)
        MonoTyping.__init__(self, type, size)
        self.param_count = param_count
        self.signature = signature
        self.compile = compile
        self.mono_method = None
        self.mono_compile = None

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return BoundMethod(instance, self)

    def op_runtime_invoke(self, instance, signature=None, values=()):
        """方法调用的call_arg"""
        if signature is None:
            signature = self.signature
        params = TempArrayPtr(signature, values) if self.param_count else 0
        return instance.owner.call_arg_ptr(*instance.owner.mono_runtime_invoke,
            self.mono_method, instance.mono_object, params, 0)

    def call(self, instance, values):
        """直接调用"""
        owner = instance.owner
        result = owner.mono_security_call_1(self.op_runtime_invoke(instance, values=values))
        if self.type:
            if result and not issubclass(self.type, MonoType):
                print(hex(result))
                # 获取值要先解包，得到地址
                result = owner.native_call_1(owner.call_arg_ptr(*owner.mono_object_unbox, result))
                # TODO 判断类型
                result = owner.handler.read(result, self.real_type, self.size)
            return self.case_value(result, instance)


class BoundMethod:
    """绑定的方法"""
    __slots__ = ('instance', 'method')

    def __init__(self, instance, method):
        self.instance = instance
        self.method = method

    def __call__(self, *values):
        """方法调用"""
        return self.method.call(self.instance, values)


class MonoArray(MonoType):
    """数组类型属性"""
    type = int
    itemsize = 0

    def __init__(self, mono_object, owner, type=None, itemsize=None):
        self.mono_object = mono_object
        self.owner = owner
        if type is not None:
            self.type = type
        if itemsize is not None:
            self.itemsize = itemsize

    def op_size(self):
        return self.owner.call_arg_ptr(*self.owner.mono_array_length, self.mono_object)

    def op_addr_at(self, index):
        if index < 0:
            index += self.size
        itemsize = self.itemsize or self.owner.handler.ptr_size
        return self.owner.call_arg_ptr(*self.owner.mono_array_addr_with_size,
            self.mono_object, itemsize, index)

    @property
    def size(self):
        return self.owner.native_call_1(self.op_size())

    def addr_at(self, index):
        return self.owner.native_call_1(self.op_addr_at(index))

    def __getitem__(self, index):
        addr = self.addr_at(index)
        result = self.owner.handler.read(addr, int, self.itemsize)
        if self.type is not int and callable(self.type):
            result = self.type(result, self.owner)
        return result

    def __setitem__(self, index, value):
        pass


class MonoArrayT(type):
    """主要用于field的type参数，表示这是一个数组"""
    def __new__(class_, type_=int, itemsize=0, a=None):
        return type('MonoArrayNew', (MonoArray,), {'type': type_, 'itemsize': itemsize})
