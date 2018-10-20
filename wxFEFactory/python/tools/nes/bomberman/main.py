from ..base import BaseNesHack
from lib.hack.forms import Group, StaticGroup, ModelInput, ModelCheckBox
from lib.win32.keys import VK
from lib.hack.models import Model, Field, ByteField, WordField, ToggleField


class Global(Model):
    bomb_count = ByteField(0x0074, label="炸弹数量")
    bomb_power = ByteField(0x0073, label="炸弹威力")
    level = ByteField(0x0058, label="选关")
    invincible = ByteField(0x007A, label="无敌时间")
    through_bomb = ToggleField(0x0078, size=1, enable=1, disable=0, label="穿炸弹")
    timebomb = ToggleField(0x0077, size=1, enable=1, disable=0, label="定时炸弹")
    through_wall = ToggleField(0x0076, size=1, enable=1, disable=0, label="穿墙")


class Main(BaseNesHack):
    def render_main(self):
        self._global = Global(0, self.handler)

        with Group("global", "全局", self._global):
            ModelInput("bomb_count")
            ModelInput("bomb_power")
            ModelInput("level")
            ModelInput("invincible")
            ModelCheckBox("through_bomb")
            ModelCheckBox("timebomb")
            ModelCheckBox("through_wall")

    def get_hotkeys(self):
        return (
            (0, VK.N, self.invincible),
        )

    def invincible(self):
        self._global.invincible = 0xFF
