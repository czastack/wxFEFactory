import abc
import ctypes
from .fields import Field, Group


class FormMeta(abc.ABCMeta):
    SLOTS = ()

    def __new__(cls, name, bases, attrs):
        # 排除抽象类
        attrs.setdefault('__abstract__', False)
        if not attrs['__abstract__']:
            # 获取所有的Field

            base_fields = []

            def handle(children, parent=None):
                for field in children:
                    if isinstance(field, Group):
                        handle(field.children, field)

                    elif isinstance(field, Field):
                        base_fields.append(field)
                        if parent:
                            field.name = parent.name + '_' + field.name

            handle(attrs['fields'])

            structure_name = (name[:-4] if name.endswith('Form') else name) + 'Structure'
            structure = type(structure_name, (ctypes.Structure,), {
                '_fields_': [(field.name, field.CTYPE) for field in base_fields if field.size > 0],
                '__module__': attrs['__module__'],
            })

            attrs['base_fields'] = base_fields
            attrs['structure'] = structure

            slots = attrs.get('__slots__', False)
            if slots is None:
                attrs.pop('__slots__')
            elif slots is False:
                attrs['__slots__'] = cls.SLOTS

        return super().__new__(cls, name, bases, attrs)


class BaseForm(metaclass=FormMeta):
    """
    表单基类
    """

    __abstract__ = True

    @abc.abstractproperty
    def fields(self):
        pass

    @abc.abstractproperty
    def structure(self):
        pass

    def __init__(self):
        """
        :param data: 数据字典
        """
        pass

    def init_pg(self, pg):
        self.elem = pg
        for field in self.fields:
            field.create_property(pg)

    @classmethod
    def cfield(cls, name):
        return getattr(cls.structure, name, None)

    @classmethod
    def cfield_names(cls):
        for field in cls.structure._fields_:
            yield field[0]

    @classmethod
    def size(cls):
        return ctypes.sizeof(cls.structure)

    @classmethod
    def ptr_from_bytes(cls, data, length=0):
        """
        :param data: bytes
        """
        length = length or ctypes.sizeof(cls.structure)
        stream = (ctypes.c_char * length)()
        stream.raw = data
        ptr = ctypes.cast(stream, ctypes.POINTER(cls.structure))
        return ptr

    @classmethod
    def struct_to_bytes(cls, s):
        """
        :param s: struct object
        """
        length = ctypes.sizeof(s)
        ptr = ctypes.cast(ctypes.pointer(s), ctypes.POINTER(ctypes.c_char * length))
        return ptr.contents.raw

    @classmethod
    def struct_to_dict(cls, s):
        data = {}
        for name in cls.cfield_names():
            data[name] = getattr(s, name)
        return data

    @classmethod
    def dict_to_struct(cls, data):
        s = cls.structure()
        for name in cls.cfield_names():
            if name in data:
                setattr(s, name, data[name])
        return s
