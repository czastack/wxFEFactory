from tools.base.native import NativeContext, TempPtr, TempArrayPtr
from lib.hack.utils import resolve_type


class MonoHeld:
    """被托管的，有owner"""


class MonoClass(MonoHeld):
    """mono类"""
    # name: str 类名称
    namespace = ''
    namepath = None  # 内部类前缀 /分隔
    vtable = None
    need_vtable = False

    def __init__(self, mono_object, owner):
        self.mono_object = mono_object
        self.owner = owner

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, '__abstract__'):
            cls.__abstract__ = False
        if not cls.__abstract__:
            if 'name' not in cls.__dict__:
                cls.name = cls.__name__
                if cls.namepath is not None:
                    cls.name = cls.namepath + cls.name

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

    def cast(self, cast_type):
        return cast_type(self.mono_object, self.owner)


class MonoMember:
    """mono成员"""
    def __init__(self, name=None):
        self.name = name

    def __set_name__(self, owner, name):
        if self.name is None:
            self.name = name


class MonoTyping:
    """带有类型的数据"""
    def __init__(self, type, size):
        self.is_mono_type = False
        if type is not int:
            if type is None:
                size = 0
            elif type is str:
                self.is_mono_type = True
            elif isinstance(type, str) or issubclass(type, MonoHeld):
                size = 0
                self.is_mono_type = True
        self.type = type
        self.size = size

    @property
    def real_type(self):
        if self.is_mono_type:
            return int
        return self.type

    def case_value(self, result, instance):
        """传出时转换值，例如转为类实例"""
        vtype = self.type
        if vtype is not int:
            if vtype is str:
                # 转换string类型
                result = instance.owner.mono_string_to_utf8(result, self.size)
                return result

            if isinstance(vtype, str):
                vtype = resolve_type(instance, vtype)
                if vtype:
                    self.type = vtype
                else:
                    raise ValueError('无法识别的类型%s' % self.type)

            if callable(vtype):
                if issubclass(vtype, MonoHeld):
                    result = vtype(result, instance.owner)
                else:
                    result = vtype(result)
        return result

    def case_boxed_value(self, result, instance):
        """转换被装箱的值，通常是mono函数调用或者property"""
        if result and not self.is_mono_type:
            owner = instance.owner
            # 获取值要先解包，得到地址
            result = owner.native_call_1(owner.mono_api.mono_object_unbox(result))
            # TODO 判断类型
            result = owner.handler.read(result, self.real_type, self.size)
        return self.case_value(result, instance)

    def prepare_value(self, value):
        """传入前预处理值"""
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
        return self.get_value(instance)

    def __set__(self, instance, value):
        self.set_value(instance, value)

    def temp_ptr(self, value=None):
        """临时地址"""
        return TempPtr(type=self.real_type, size=self.size, value=value)

    def op_getter(self, instance):
        """用于获取值的call_arg"""
        if not instance.mono_object:
            raise ValueError('mono_object未初始化')
        if not self.mono_field:
            raise ValueError('mono_field未初始化')
        temp_ptr = self.temp_ptr()
        return instance.owner.mono_api.mono_field_get_value(
            instance.mono_object, self.mono_field, temp_ptr, ret_type=temp_ptr)

    def op_setter(self, instance, value):
        """用于设置值的call_arg"""
        if not instance.mono_object:
            raise ValueError('mono_object未初始化')
        if not self.mono_field:
            raise ValueError('mono_field未初始化')
        temp_ptr = self.temp_ptr(value)
        return instance.owner.mono_api.mono_field_set_value(instance.mono_object, self.mono_field, temp_ptr)

    def get_value(self, instance):
        """获取值"""
        result = instance.owner.native_call_1(self.op_getter(instance))
        return self.case_value(result, instance)

    def set_value(self, instance, value):
        """设置值"""
        instance.owner.native_call_1(self.op_setter(instance, self.prepare_value(value)))

    def __repr__(self):
        return '{}({}, {}, {}, {})'.format(
            self.__class__.__name__, self.name, self.type, self.size, self.label)


class MonoStaticField(MonoField):
    """静态字段"""
    def op_getter(self, instance):
        """用于获取值的call_arg"""
        if not self.mono_field:
            raise ValueError('mono_field未初始化')
        temp_ptr = self.temp_ptr()
        return instance.owner.mono_api.mono_field_static_get_value(
            instance.mono_vtable, self.mono_field, temp_ptr, ret_type=temp_ptr)

    def op_setter(self, instance, value):
        """用于设置值的call_arg"""
        if not self.mono_field:
            raise ValueError('mono_field未初始化')
        temp_ptr = self.temp_ptr(value)
        return instance.owner.mono_api.mono_field_static_set_value(instance.mono_vtable, self.mono_field, temp_ptr)


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
        return self.get_value(instance)

    def __set__(self, instance, value):
        self.set_value(instance, value)

    def op_getter(self, instance):
        """用于获取值的call_arg"""
        if not self.mono_property:
            raise ValueError('mono_property未初始化')
        return instance.owner.mono_api.mono_property_get_value(
            self.mono_property, instance.mono_object, 0, 0)

    def op_setter(self, instance, value):
        """用于设置值的call_arg"""
        if not self.mono_property:
            raise ValueError('mono_property未初始化')
        params = TempArrayPtr(NativeContext.type_signature(self.real_type, self.size), (value,))
        return instance.owner.mono_api.mono_property_set_value(
            self.mono_property, instance.mono_object, params, 0)

    def get_value(self, instance):
        """获取值"""
        owner = instance.owner
        result = owner.mono_security_call_1(self.op_getter(instance))
        return self.case_boxed_value(result, instance)

    def set_value(self, instance, value):
        """设置值"""
        instance.owner.mono_security_call_1(self.op_setter(instance, self.prepare_value(value)))

    def __repr__(self):
        return '{}({}, {}, {}, {})'.format(
            self.__class__.__name__, self.name, self.type, self.size, self.label)


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

    def op_runtime_invoke(self, instance, args=()):
        """方法调用的call_arg"""
        # 类型处理
        signature = self.signature
        arg_convert = False
        for arg in args:
            if isinstance(arg, (MonoClass, str)):
                arg_convert = True
                break
        if arg_convert:
            # 需要转换
            signature_new = []
            args_new = []
            for fmt, arg in zip(signature, args):
                if '0' <= fmt <= '9':
                    raise ValueError('转换参数不支持repeat')
                if isinstance(arg, MonoClass):
                    arg = arg.mono_object
                    if fmt != 'P':
                        raise ValueError('MonoClass对象参数必须对应P')
                elif isinstance(arg, str):
                    # 转换成mono的string类型
                    arg = instance.owner.mono_string_new(arg)
                    fmt = 'P'
                args_new.append(arg)
                signature_new.append(fmt)
            signature = ''.join(signature_new)
            args = args_new

        params = TempArrayPtr(signature, args) if self.param_count else 0
        return instance.owner.mono_api.mono_runtime_invoke(
            self.mono_method, instance.mono_object, params, 0)

    def call(self, instance, args):
        """直接调用"""
        owner = instance.owner
        result = owner.mono_security_call_1(self.op_runtime_invoke(instance, args=args))
        if self.type:
            return self.case_boxed_value(result, instance)


class BoundMethod:
    """绑定的方法"""
    __slots__ = ('instance', 'method')

    def __init__(self, instance, method):
        self.instance = instance
        self.method = method

    def __call__(self, *values):
        """方法调用"""
        return self.method.call(self.instance, values)


class MonoArray(MonoHeld):
    """数组类型属性"""
    type = int
    itemsize = 0

    def __init__(self, mono_object, owner, type=None, itemsize=None):
        if mono_object == 0:
            raise ValueError('mono_object == 0')
        self.mono_object = mono_object
        self.owner = owner
        if type is not None:
            self.type = type
        if itemsize is not None:
            self.itemsize = itemsize

    def op_size(self):
        return self.owner.mono_api.mono_array_length(self.mono_object)

    def op_addr_at(self, index):
        if index < 0:
            index += self.size
        itemsize = self.itemsize or self.owner.handler.ptr_size
        return self.owner.mono_api.mono_array_addr_with_size(
            self.mono_object, itemsize, index)

    @property
    def size(self):
        return self.owner.native_call_1(self.op_size())

    def addr_at(self, index):
        return self.owner.native_call_1(self.op_addr_at(index))

    def __len__(self):
        return self.size

    def __getitem__(self, index):
        addr = self.addr_at(index)
        result = self.owner.handler.read(addr, int, self.itemsize)
        if self.type is not int and callable(self.type):
            result = self.type(result, self.owner)
        return result

    def __setitem__(self, index, value):
        # raise NotImplementedError()
        # TODO 判断类型
        addr = self.addr_at(index)
        self.owner.handler.write(addr, value, self.itemsize)


class MonoArrayT(type):
    """主要用于field的type参数，表示这是一个数组"""
    def __new__(cls, type_=int, itemsize=0):
        return type('MonoArrayNew', (MonoArray,), {'type': type_, 'itemsize': itemsize})
