from ..base import BaseNesHack
from lib.hack.forms import Group, ModelInput, ModelSelect, ModelCheckBox
from lib.win32.keys import VK
from lib.hack.models import Model, Field, ByteField, WordField


class Global(Model):
    # invincible_1 = ByteField(0x00AE)
    # invincible_2 = ByteField(0x00AF)
    invincible_1 = ByteField(0x00B0)
    invincible_2 = ByteField(0x00B1)
    weapon_1 = ByteField(0x00AA)
    weapon_2 = ByteField(0x00AB)
    lives_1 = ByteField(0x0032)
    lives_2 = ByteField(0x0033)


BULLETS = ["普通", "M弹", "F弹", "S弹", "L弹"]
BULLET_VALUES = [i for i in range(len(BULLETS))]
BULLETS = BULLETS + ["快速" + s for s in BULLETS]
BULLET_VALUES = BULLET_VALUES + [0x10 | i for i in BULLET_VALUES]


class Main(BaseNesHack):
    def render_main(self):
        self._global = Global(0, self.handler)

        with Group("global", "全局", self._global):
            ModelCheckBox("invincible_1", "1P无敌", enableData=0xFF, disableData=0)
            ModelCheckBox("invincible_2", "2P无敌", enableData=0xFF, disableData=0)
            ModelSelect("weapon_1", "1P武器", choices=BULLETS, values=BULLET_VALUES)
            ModelSelect("weapon_2", "2P武器", choices=BULLETS, values=BULLET_VALUES)
            ModelInput("lives_1", "1P生命")
            ModelInput("lives_2", "2P生命")

    def get_hotkeys(self):
        this = self.weak
        return (
            (VK.MOD_ALT, VK.I, this.invincible),
        )

    def invincible(self, _=None):
        self._global.invincible_1 = 0xFF
        self._global.invincible_2 = 0xFF