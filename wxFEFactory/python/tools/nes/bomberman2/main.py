from ..base import BaseNesHack
from lib.hack.forms import Group, StaticGroup, ModelInput, ModelCheckBox
from lib.win32.keys import VK
from lib.hack.models import Model, Field, ByteField, WordField, ToggleField, FieldPrep


class Global(Model):
    bomb_count = ByteField(0x0082, label="炸弹数量")
    bomb_power = ByteField(0x0085, label="炸弹威力")
    lives = ByteField(0x04E5, label="生命")
    speed = ByteField(0x00A5, label="速度")
    invincible = ToggleField(0x04E6, size=1, enable=1, disable=0, label="无敌开启")
    invincible_time = ByteField(0x04E8, label="无敌时间")
    through_wall = ToggleField(0x009F, size=1, enable=1, disable=0, label="穿墙")
    through_bomb = ToggleField(0x00A0, size=1, enable=1, disable=0, label="穿炸弹")
    timebomb = ToggleField(0x00A1, size=1, enable=1, disable=0, label="定时炸弹")

    def time_getter(self, value, field):
        return ((value >> 16) & 0xFF) * 100 + ((value >> 8) & 0xFF) * 10 + (value & 0xFF)

    def time_setter(self, value, field):
        value = int(value)
        return ((value // 100 % 10) << 16) | ((value // 10 % 10) << 8) | (value % 10)

    time = FieldPrep(time_getter, time_setter, Field(0x0559, label="时间"))


class Main(BaseNesHack):
    def render_main(self):
        self._global = Global(0, self.handler)

        with Group("global", "全局", self._global):
            ModelInput("bomb_count")
            ModelInput("bomb_power")
            ModelInput("lives")
            ModelInput("speed")
            ModelInput("time")
            ModelInput("invincible_time")
            ModelCheckBox("invincible")
            ModelCheckBox("through_wall")
            ModelCheckBox("through_bomb")
            ModelCheckBox("timebomb")

    def get_hotkeys(self):
        return (
            (0, VK.N, self.invincible),
        )

    def invincible(self):
        self._global.invincible = Global.invincible.enable
        self._global.invincible_time = 0xFF
