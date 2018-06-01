from ..base import BaseNesHack
from lib.hack.form import Group, StaticGroup, ModelInput
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
from lib.hack.model import Model, Field, ByteField, WordField, FieldPrep


class Global(Model):
    invincible = ByteField(0x0074)
    hp = ByteField(0x007A)
    life = ByteField(0x007B)
    money = FieldPrep(lambda ins, x, f: x * 10, lambda ins, x, f: int(x) // 10, WordField(0x007C))
    weapon = ByteField(0x0081)
    arrow = ByteField(0x0527)


class Tool(BaseNesHack):
    def render_main(self):
        self._global = Global(0, self.handler)

        with Group("global", "全局", self._global):
            ModelInput("invincible", "无敌时间(max:85)")
            ModelInput("hp", "血量(max:6)")
            ModelInput("life", "生命(max:9)")
            ModelInput("money", "金钱")

    def get_hotkeys(self):
        this = self.weak
        return (
            ('pull_through', MOD_ALT, getVK('h'), this.pull_through),
            ('shoot_arrow', MOD_ALT, getVK('m'), this.shoot_arrow),
        )

    def pull_through(self, _=None):
        self._global.hp = 6

    def shoot_arrow(self, _=None):
        self._global.arrow = 2