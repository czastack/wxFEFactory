from ..base import BaseNesHack
from lib.hack.forms import Group, StaticGroup, ModelInput
from lib.win32.keys import VK
from lib.hack.models import Model, Field, ByteField, WordField, MulFieldPrep


class Global(Model):
    invincible = ByteField(0x0074)
    hp = ByteField(0x007A)
    lives = ByteField(0x007B)
    money = MulFieldPrep(10, WordField(0x007C))
    weapon = ByteField(0x0081)
    arrow = ByteField(0x0527)


class Main(BaseNesHack):
    def render_main(self):
        self._global = Global(0, self.handler)

        with Group("global", "全局", self._global):
            ModelInput("invincible", "无敌时间(max:85)")
            ModelInput("hp", "血量(max:6)")
            ModelInput("lives", "生命(max:9)")
            ModelInput("money", "金钱")

    def get_hotkeys(self):
        this = self.weak
        return (
            ('pull_through',VK.MOD_ALT, VK.H, this.pull_through),
            ('shoot_arrow',VK.MOD_ALT, VK.M, this.shoot_arrow),
        )

    def pull_through(self, _=None):
        self._global.hp = 6

    def shoot_arrow(self, _=None):
        self._global.arrow = 2