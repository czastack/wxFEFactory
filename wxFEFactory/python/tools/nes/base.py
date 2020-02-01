from lib.hack.handlers import ProxyHandler
from lib.hack.handlers.neshandler import VirtuaNesHandler, NestopiaHandler
from lib.hack.forms import Group, StaticGroup, ModelInput
from lib.hack.models import Model, Field, ByteField, WordField
from lib.win32.keys import VK
from lib.extypes import new_dataclass
from tools.base.hacktool import ProxyHackTool


class BaseNesHack(ProxyHackTool):
    handler_class = VirtuaNesHandler, NestopiaHandler


FieldItem = new_dataclass('FieldItem', ('addr', 'name', 'size', 'max'))


class SimpleNesHack(BaseNesHack):
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if not hasattr(cls, 'fields'):
            raise ValueError('missing class variable "fields"')

        if not hasattr(cls, 'get_hotkeys') and hasattr(cls, 'pull_through'):
            cls.get_hotkeys = cls._get_hotkeys

        class Global(Model):
            pass

        # 元组或数组统一转成FieldItem类型
        cls.fields = tuple(item if isinstance(item, FieldItem) else FieldItem(*item) for item in cls.fields)
        cls.fields_map = {}

        for item in cls.fields:
            if item.size is None:
                item.size = 1
            cls.fields_map[item.name] = item
            setattr(Global, item.name, Field(item.addr, size=item.size))

        cls.Global = Global

    def set_value(self, name, value):
        setattr(self._global, name, value)

    def set_max(self, name):
        item = self.fields_map[name]
        if item.max is None:
            item.max = ((1 << (item.size << 3)) - 1)
        self.set_value(name, item.max or item.max)

    def render_main(self):
        self._global = self.Global(0, self.handler)

        with Group("global", "全局", self._global):
            for item in self.fields:
                input = ModelInput(item.name)
                if item.max:
                    input.set_help('max:%d' % item.max)

    def _get_hotkeys(self):
        return (
            (VK.MOD_ALT, VK.H, self.weak.pull_through),
        )
