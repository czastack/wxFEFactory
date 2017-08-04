from .fields import Field, Group
from lib.lazy import lazyclassmethod
import ctypes

class FormMetaclass(type):
    SLOTS = ()

    def __new__(class_, name, bases, attrs):
        # 排除抽象类:
        if not attrs.get('__abstract__', False):
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
                attrs['__slots__'] = __class__.SLOTS

        return super().__new__(class_, name, bases, attrs)


class BaseForm(metaclass=FormMetaclass):
    """
    表单基类
    """

    __abstract__ = True

    def __init__(self):
        """
        :param data: 数据字典
        """
        pass

    def initPg(self, pg):
        self.elem = pg
        for field in self.fields:
            field.createProperty(pg)

    @classmethod
    def cfield(class_, name):
        return getattr(class_.structure, name, None)

    @classmethod
    def cfield_names(class_):
        for field in class_.structure._fields_:
            yield field[0]

    @classmethod
    def size(class_):
        return ctypes.sizeof(class_.structure)

    @classmethod
    def ptr_from_bytes(class_, data, length=0):
        """
        :param data: bytes 
        """
        length      = length or ctypes.sizeof(class_.structure)
        stream      = (ctypes.c_char * length)()
        stream.raw  = data
        ptr         = ctypes.cast(stream, ctypes.POINTER(class_.structure))
        return ptr

    @classmethod
    def struct_to_bytes(class_, s):
        """
        :param s: struct object
        """
        length  = ctypes.sizeof(s)
        ptr     = ctypes.cast(ctypes.pointer(s), ctypes.POINTER(ctypes.c_char * length))
        return ptr.contents.raw

    @classmethod
    def struct_to_dict(class_, s):
        data = {}
        for name in class_.cfield_names():
            data[name] = getattr(s, name)
        return data

    @classmethod
    def dict_to_struct(class_, data):
        s = class_.structure()
        for name in class_.cfield_names():
            if name in data:
                setattr(s, name, data[name])
        return s

