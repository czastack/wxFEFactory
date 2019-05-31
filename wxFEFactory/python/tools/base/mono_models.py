from lib.extypes import WeakBinder
from lib.utils import float32


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
        self.bound_member = {}

    def __init_subclass__(cls):
        super().__init_subclass__()
        if not getattr(cls, '__abstract__', False):
            if cls.name is None:
                cls.name = cls.__name__

            cls.fields = []
            cls.methods = []

            for value in cls.__dict__.values():
                if isinstance(value, MonoField):
                    cls.fields.append(value)
                elif isinstance(value, MonoMethod):
                    cls.methods.append(value)


class MonoMember:
    def __init__(self, name=None):
        self.name = name

    def __set_name__(self, owner, name):
        if self.name is None:
            self.name = name


class MonoField(MonoMember):
    def __init__(self, name=None, type=int):
        super().__init__(name)
        self.type = type
        self.mono_field = None

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        field = instance.bound_member.get(self.name, None)
        if field is None:
            field = instance.bound_member[self.name] = BoundField(instance, self)
        return field

    def __set__(self, instance, value):
        self.set_value(instance, value)

    def op_getter(self, instance):
        """用于获取值的call_arg"""
        if not instance.mono_object or not self.mono_field:
            raise ValueError('mono_object或mono_field未初始化')
        return instance.owner.op_mono_field_get_value(instance.mono_object, self.mono_field)

    def op_setter(self, instance, value):
        """用于设置值的call_arg"""
        if not instance.mono_object or not self.mono_field:
            raise ValueError('mono_object或mono_field未初始化')
        return instance.owner.op_mono_field_set_value(instance.mono_object, self.mono_field, value)

    def get_value(self, instance):
        """获取值"""
        result = instance.owner.native_call_1(self.op_getter(instance))
        # 转为类实例
        if self.type is not int and callable(self.type):
            result = self.type(result, instance.owner)
        return result

    def set_value(self, instance, value):
        # if self.type and not isinstance(value, self.type):
        #     value = self.type(value)
        instance.owner.native_call_1(self.op_setter(instance, value))


class MonoStaticField(MonoField):
    """静态属性"""
    def op_getter(self, instance):
        """用于获取值的call_arg"""
        if not self.mono_field:
            raise ValueError('mono_field未初始化')
        return instance.owner.op_mono_field_static_get_value(instance.mono_vtable, self.mono_field)

    def op_setter(self, instance, value):
        """用于设置值的call_arg"""
        if not self.mono_field:
            raise ValueError('mono_field未初始化')
        return instance.owner.op_mono_field_static_set_value(instance.mono_vtable, self.mono_field, value)


class BoundField:
    """绑定(实例)的字段"""
    __slots__ = ('instance', 'field')

    def __init__(self, instance, field):
        self.instance = WeakBinder(instance)
        self.field = field

    def op_getter(self):
        return self.field.op_getter(self.instance)

    @property
    def value(self):
        return self.field.get_value(self.instance)

    @value.setter
    def value(self, value):
        return self.field.set_value(self.instance, value)


class MonoMethod(MonoMember):
    """mono方法"""
    def __init__(self, name=None, param_count=0, compile=False):
        super().__init__(name)
        self.param_count = param_count
        self.compile = compile
        self.mono_method = None
        self.mono_compile = None

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        field = instance.bound_member.get(self.name, None)
        if field is None:
            field = instance.bound_member[self.name] = BoundMethod(instance, self)
        return field

    def op_runtime_invoke(self, instance, signature, values):
        """方法调用的call_arg"""
        return instance.owner.op_mono_runtime_invoke(self.mono_method, instance.mono_object, signature, values)


class BoundMethod:
    """绑定的方法"""
    __slots__ = ('instance', 'method')

    def __init__(self, instance, method):
        self.instance = WeakBinder(instance)
        self.method = method

    def __call__(self, signature, values):
        """方法调用"""
        return self.instance.owner.native_call_1(
            self.field.op_runtime_invoke(self.instance, signature, values))


class MonoArray(MonoClass):
    """数组类型属性"""
    def __init__(self, mono_object, owner, type=int, itemsize=0):
        super().__init__(mono_object, owner)
        self.type = type
        self.itemsize = itemsize

    def op_size(self):
        return self.owner.call_arg_int(*self.owner.mono_array_length, self.mono_object)

    def op_addr_at(self, index):
        if index < 0:
            index += self.size
        itemsize = self.itemsize or self.owner.handler.ptr_size
        return self.owner.call_arg_int(*self.owner.mono_array_addr_with_size,
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


class MonoArrayT:
    """主要用于field的type参数，表示这是一个数组"""
    def __init__(self, type=int, itemsize=0):
        self.type = type
        self.itemsize = itemsize

    def __call__(self, mono_object, owner):
        return MonoArray(mono_object, owner, self.type, self.itemsize)
