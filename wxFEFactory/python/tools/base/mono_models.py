from lib.extypes import DataClass, classproperty
from lib.utils import float32


class MonoClass:
    namespace = ''
    name = None
    vtable = None
    need_vtable = False

    def __init__(self, mono_object, owner):
        self.mono_object = mono_object
        self.owner = owner
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
    def __init__(self, name):
        self.name = name

    def __set_name__(self, owner, name):
        if self.name is None:
            self.name = name


class MonoField(MonoMember):
    def __init__(self, name=None, type=int, static=False):
        super().__init__(name)
        self.type = type
        self.static = static

    def __get__(self, instance, owner=None):
        if instance is None:
            return self

        if instance.owner.caching_values:
            return instance.cached_value[self.name]
        else:
            return BoundMember(instance, self)

    def get_op(self, instance):
        """用于获取的call_arg"""
        return

    def __set__(self, instance, value):
        if not isinstance(value, self.type):
            value = self.type(value)
        pass


class BoundField:
    __slots__ = ('instance', 'field')

    def __init__(self, instance, field):
        self.instance = instance
        self.field = field

    def get_op(self):
        return self.field.get_op(self.instance)


class MonoObjectField(MonoField):
    pass


class MonoStaticField(MonoField):
    pass


class MonoMethod(MonoMember):
    def __init__(self, name, param_count=0, compile=True):
        super().__init__(name)
        self.param_count = param_count
