from lib.hack.handlers import ProxyHandler
from lib.hack.handlers.neshandler import VirtuaNesHandler, NestopiaHandler
from lib.hack.forms import Group, StaticGroup, ModelInput
from lib.hack.models import Model, Field, ByteField, WordField
from lib.win32.keys import getVK, MOD_ALT
from lib.extypes import DataClass
from ..hacktool import BaseHackTool


class BaseNesHack(BaseHackTool):
    def __init__(self):
        super().__init__()
        self.handler = ProxyHandler()

    def check_attach(self, _=None):
        if self.handler.active:
            self.ondetach()
            
        for Handler in (VirtuaNesHandler, NestopiaHandler):
            handler = Handler()
            if handler.attach():
                self.handler.set(handler)
                self.attach_status_view.label = handler.WINDOW_NAME + ' 正在运行'
                if not self.win.hotkeys:
                    hotkeys = self.get_hotkeys()
                    if hotkeys:
                        self.win.RegisterHotKeys(hotkeys)
                self.onattach()
                return True
        else:
            self.attach_status_view.label = '绑定失败, 未找到支持的模拟器进程'
            return False


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
                    input.view.setToolTip('max:%d' % item.max)

    def _get_hotkeys(self):
        return (
            ('pull_through', MOD_ALT, getVK('h'), self.weak.pull_through),
        )