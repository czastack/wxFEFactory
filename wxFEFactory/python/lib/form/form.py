from .fields import Field, Group
from fefactory_api import PropertyGridListPage as PG
import ctypes

class FormMetaclass(PG.__class__):
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
                '_fields_': [(field.name, field.CTYPE) for field in base_fields if field.size],
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


class BaseForm(PG, metaclass=FormMetaclass):
    """
    表单基类
    """

    __abstract__ = True

    def __init__(self, data=None):
        """
        :param data: 数据字典
        """
        super().__init__(self.title, data)

    def show(self):
        if super().show():
            for field in self.fields:
                field.show(self)

            if self.data:
                self.setValues(self.data)

    @classmethod
    def cfield(class_, name):
        return getattr(class_.structure, name)

    @classmethod
    def size(class_):
        return ctypes.sizeof(class_.structure)

    def bytes(self):
        return self.data