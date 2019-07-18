from lib.hack.forms import Group, StaticGroup, ModelInput, ModelSelect, ModelCheckBox
from lib.win32.keys import VK
from lib.hack.models import Model, Field, ByteField, WordField
from lib import ui
from ..base import BaseNesHack


class Global(Model):
    hp = ByteField(0x0085)
    hpmax = ByteField(0x0086)
    tools = Field(0x009C)
    dragon = ByteField(0x009A)
    dragons = ByteField(0x00D1)
    invincible = ByteField(0x0056)


DRAGONS = ("无", "火龙", "闪电龙", "飞龙", "水龙", "三角龙")


class Main(BaseNesHack):
    def render_main(self):
        self._global = Global(0, self.handler)

        with Group("global", "全局", self._global):
            ModelInput("hp", "HP")
            ModelInput("hpmax", "最大HP")
            ModelCheckBox("invincible", "无敌", enable=0xFF, disable=0)
            ModelSelect("dragon", "当前龙", choices=DRAGONS)

        with StaticGroup("功能"):
            self.render_functions(('hpmax', 'all_dragons', 'all_tools'))

    def get_hotkeys(self):
        this = self.weak
        return (
            (VK.MOD_ALT, VK.H, this.pull_through),
            (VK.MOD_ALT, VK.I, this.invincible),
        )

    def pull_through(self):
        """HP恢复"""
        self._global.set_with('hp', 'hpmax')

    def invincible(self):
        """无敌"""
        self._global.invincible = 0xFF

    def hpmax(self, _=None):
        """HP最大"""
        self._global.hp = 0x20
        self._global.hpmax = 0x20

    def all_dragons(self, _=None):
        """所有恐龙"""
        self._global.dragons = 0x1A

    def all_tools(self, _=None):
        """所有工具"""
        self._global.tools = 0xE0FCFFF0
