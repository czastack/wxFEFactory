from ..base import BaseNesHack
from lib.hack.forms import Group, StaticGroup, ModelInput, ModelCheckBox, ModelFlagWidget
from lib.win32.keys import VK
from lib.hack.models import Model, Field, ByteField, WordField, Fields


class Global(Model):
    lives_1 = ByteField(0x0076)
    lives_2 = ByteField(0x0076)
    medicine_1 = Fields(ByteField(0x0369), ByteField(0x0078))
    medicine_2 = Fields(ByteField(0x0369), ByteField(0x0079))
    invincible_1 = ByteField(0x03D2)
    invincible_2 = ByteField(0x03D2)


MEDICINE = ("红", "蓝", "褐")


class Main(BaseNesHack):
    def render_main(self):
        self._global = Global(0, self.handler)

        with Group("global", "全局", self._global):
            ModelInput("lives_1", "1P生命")
            ModelInput("lives_2", "2P生命")
            ModelCheckBox("invincible_1", "1P无敌", enable=0xFF, disable=0)
            ModelCheckBox("invincible_2", "2P无敌", enable=0xFF, disable=0)
            # ModelInput("level", "关卡(0-4)")
            ModelFlagWidget("medicine_1", "1P药水效果", labels=MEDICINE)
            ModelFlagWidget("medicine_2", "2P药水效果", labels=MEDICINE)

    def get_hotkeys(self):
        this = self.weak
        return (
            (VK.MOD_ALT, VK.I, this.invincible),
        )

    def invincible(self):
        self._global.invincible_1 = 90
        self._global.invincible_2 = 90
