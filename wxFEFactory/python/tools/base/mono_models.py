from lib.extypes import WeakBinder
from lib.utils import float32


class MonoType:
    pass


class MonoClass(MonoType):
    namespace = ''
    name = None
    vtable = None
    need_vtable = False
    owner = None

    def __init__(self, mono_object, owner):
        self.mono_object = mono_object
        self.owner = owner
        self.bound_member = {}
        self.cached_value = {}

    def __init_subclass__(cls):
        super().__init_subclass__()
        if not getattr(cls, '__abstract__', False):
            if cls.name is None:
                cls.name == cls.__name__

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
        if not instance.mono_object or not self.field.mono_field:
            raise ValueError('mono_object或mono_field未初始化')
        return instance.owner.op_mono_field_get_value(instance.mono_object, self.field.mono_field)

    def op_setter(self, instance, value):
        """用于设置值的call_arg"""
        if not instance.mono_object or not self.field.mono_field:
            raise ValueError('mono_object或mono_field未初始化')
        return instance.owner.op_mono_field_set_value(instance.mono_object, self.field.mono_field, value)

    def get_value(self, instance):
        """获取值"""
        result, = instance.owner.native_call_1(self.op_getter(instance))
        return result

    def set_value(self, instance, value):
        if self.type and not isinstance(value, self.type):
            value = self.type(value)
        instance.owner.native_call_1(self.op_setter(instance, value))


class BoundField:
    __slots__ = ('instance', 'field')

    def __init__(self, instance, field):
        self.instance = WeakBinder(instance)
        self.field = field

    @property
    def op_getter(self):
        return self.field.op_getter(self.instance)

    @property
    def value(self):
        return self.field.get_value(self.instance)

    @value.setter
    def value(self, value):
        return self.field.set_value(self.instance, value)


class MonoStaticField(MonoMember):
    """静态属性"""
    def __init__(self, name=None, type=int):
        super().__init__(name)
        self.type = type
        self.mono_field = None

    def __set_name__(self, owner, name):
        super().__set_name__(owner, name)
        self.owner = WeakBinder(owner)

    def op_getter(self):
        """用于获取值的call_arg"""
        if not self.field.mono_field:
            raise ValueError('mono_field未初始化')
        return self.owner.owner.op_mono_field_static_get_value(self.owner.vtable, self.field.mono_field)

    def op_setter(self, value):
        """用于设置值的call_arg"""
        if not self.field.mono_field:
            raise ValueError('mono_field未初始化')
        return self.owner.owner.op_mono_field_static_set_value(self.owner.vtable, self.field.mono_field, value)

    def get_value(self):
        """获取值"""
        result, = self.owner.owner.native_call_1(self.op_getter(self.owner))
        return result

    def set_value(self, value):
        if self.type and not isinstance(value, self.type):
            value = self.type(value)
        self.owner.owner.native_call_1(self.op_setter(self.owner, value))

    value = property(get_value, set_value)


class MonoMethod(MonoMember):
    def __init__(self, name, param_count=0, compile=True):
        super().__init__(name)
        self.param_count = param_count
        self.mono_method = None

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        field = instance.bound_member.get(self.name, None)
        if field is None:
            field = instance.bound_member[self.name] = BoundMethod(instance, self)
        return field

    def op_runtime_invoke(self, instance, signature, values):
        return instance.owner.op_mono_runtime_invoke(self.mono_method, instance.mono_object, signature, values)


class BoundMethod:
    __slots__ = ('instance', 'method')

    def __init__(self, instance, method):
        self.instance = WeakBinder(instance)
        self.method = method

    def __call__(self):
        pass


class MonoObject(MonoType):
    """MonoObject类型属性"""


class MonoArray(MonoType):
    """数组类型属性"""
    pass
