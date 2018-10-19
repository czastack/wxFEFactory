from lib.hack.handlers import ProxyHandler
from lib.hack.handlers.neshandler import VirtuaNesHandler, NestopiaHandler
from lib.hack.forms import Group, StaticGroup, ModelInput
from lib.hack.models import Model, Field, ByteField, WordField
from lib.win32.keys import VK
from lib.extypes import DataClass
from ..hacktool import ProxyHackTool


class BaseNesHack(ProxyHackTool):
    handlers = VirtuaNesHandler, NestopiaHandler


FieldItem = DataClass('FieldItem', ('addr', 'name', 'size', 'max'))


class SimpleNesHack(BaseNesHack):
    def __init_subclass__(cls):
        super().__init_subclass__()

        if not hasattr(cls, 'fields'):
            raise ValueError('missing class variable "fields"')

        if hasattr(cls, 'pull_through'):
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

    def set_max(self, name):
        item = self.fields_map[name]
        if item.max:
            setattr(self._global, name, item.max)

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
