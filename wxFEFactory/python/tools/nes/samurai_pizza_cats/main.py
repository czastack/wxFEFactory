from ..base import BaseNesHack
from lib.hack.form import Group, StaticGroup, ModelInput
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
from lib.hack.model import Model, Field, ByteField, WordField


class Global(Model):
    ninjutsu = ByteField(0x003d)
    hp = ByteField(0x003F)
    energe = ByteField(0x0040)
    help = ByteField(0x0041)
    life = ByteField(0x0044)
    level = WordField(0x005d)


class Tool(BaseNesHack):
    def render_main(self):
        self._global = Global(0, self.handler)

        with Group("global", "全局", self._global):
            ModelInput("hp", "血量(max:10)")
            ModelInput("life", "能量(max:255)")
            ModelInput("energe", "生命(max:9)")
            ModelInput("help", "援助(max:192)")
            ModelInput("ninjutsu", "忍术(1-3)")
            ModelInput("level", "关卡")

    def get_hotkeys(self):
        this = self.weak
        return (
            ('pull_through', MOD_ALT, getVK('h'), this.pull_through),
        )

    def pull_through(self, _=None):
        self._global.hp = 10
        self._global.energe = 0xFF
        self._global.help = 0xC0