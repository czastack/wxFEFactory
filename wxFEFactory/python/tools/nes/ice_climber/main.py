from ..base import BaseNesHack
from lib.hack.form import Group, StaticGroup, ModelInput, ModelCheckBox, ModelFlagWidget
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
from lib.hack.model import Model, Field, ByteField, WordField, Fields


class Global(Model):
    life_1 = ByteField(0x0076)
    life_2 = ByteField(0x0076)
    medicine_1 = Fields(ByteField(0x0369), ByteField(0x0078))
    medicine_2 = Fields(ByteField(0x0369), ByteField(0x0079))
    invincible_1 = ByteField(0x03D2)
    invincible_2 = ByteField(0x03D2)


MEDICINE = ("红", "蓝", "褐")


class Tool(BaseNesHack):
    def render_main(self):
        self._global = Global(0, self.handler)

        with Group("global", "全局", self._global):
            ModelInput("life_1", "1P生命")
            ModelInput("life_2", "2P生命")
            ModelCheckBox("invincible_1", "1P无敌", enableData=0xFF, disableData=0)
            ModelCheckBox("invincible_2", "2P无敌", enableData=0xFF, disableData=0)
            # ModelInput("level", "关卡(0-4)")
            ModelFlagWidget("medicine_1", "1P药水效果", labels=MEDICINE)
            ModelFlagWidget("medicine_2", "2P药水效果", labels=MEDICINE)

    def get_hotkeys(self):
        this = self.weak
        return (
            ('invincible', MOD_ALT, getVK('i'), this.invincible),
        )

    def invincible(self, _=None):
        self._global.invincible_1 = 90
        self._global.invincible_2 = 90