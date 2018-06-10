from ..base import BaseNesHack
from lib.hack.form import Group, StaticGroup, ModelInput, ModelSelect, ModelCheckBox
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
from lib.hack.model import Model, Field, ByteField, WordField, FieldPrep
import fefactory_api
ui = fefactory_api.ui


class Global(Model):
    hp = ByteField(0x0085)
    hpmax = ByteField(0x0086)
    tools = Field(0x009C)
    dragon = ByteField(0x009A)
    dragons = ByteField(0x00D1)
    invincible = ByteField(0x0056)


DRAGONS = ("无", "火龙", "闪电龙", "飞龙", "水龙", "三角龙")


class Tool(BaseNesHack):
    def render_main(self):
        self._global = Global(0, self.handler)

        with Group("global", "全局", self._global):
            ModelInput("hp", "HP")
            ModelInput("hpmax", "最大HP")
            ModelCheckBox("invincible", "无敌", enableData=0xFF, disableData=0)
            ModelSelect("dragon", "当前龙", choices=DRAGONS)

        with StaticGroup("功能"):
            with ui.GridLayout(cols=4, vgap=10, className="expand"):
                for name in ('pull_through', 'hp_max', 'all_dragons', 'all_tools'):
                    func = getattr(self.weak, name)
                    ui.Button(func.__doc__, onclick=func)

    def get_hotkeys(self):
        this = self.weak
        return (
            ('invincible', MOD_ALT, getVK('i'), this.invincible),
        )

    def pull_through(self, _=None):
        """HP恢复"""
        self._global.set_with('hp', 'hpmax')

    def hp_max(self, _=None):
        """HP最大"""
        self._global.hp = 0x20
        self._global.hpmax = 0x20

    def invincible(self, _=None):
        """无敌"""
        self._global.invincible = 0xFF

    def all_dragons(self, _=None):
        """所有恐龙"""
        self._global.dragons = 0x1A

    def all_tools(self, _=None):
        """所有工具"""
        self._global.tools = 0xE0FCFFF0