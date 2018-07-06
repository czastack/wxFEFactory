from ..base import BaseNesHack
from lib.hack.forms import Group, ModelInput, ModelSelect, ModelCheckBox
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
from lib.hack.models import Model, Field, ByteField, WordField, FieldPrep


class Global(Model):
    invincible_1 = ByteField(0x00D4)
    invincible_2 = ByteField(0x00D5)
    weapon_1 = ByteField(0x00B8)
    weapon_2 = ByteField(0x00B9)
    lives_1 = ByteField(0x0053)
    lives_2 = ByteField(0x0054)


BULLETS = ["普通", "M弹", "S弹", "L弹", "F弹", "F弹(八面)"]
BULLET_VALUES = [i for i in range(len(BULLETS))]
BULLETS = BULLETS + ["快速" + s for s in BULLETS]
BULLET_VALUES = BULLET_VALUES + [0x130 | i for i in BULLET_VALUES]


class Main(BaseNesHack):
    def render_main(self):
        self._global = Global(0, self.handler)

        with Group("global", "全局", self._global):
            ModelCheckBox("invincible_1", "1P无敌", enableData=0xff, disableData=0)
            ModelCheckBox("invincible_2", "2P无敌", enableData=0xff, disableData=0)
            ModelSelect("weapon_1", "1P武器", choices=BULLETS, values=BULLET_VALUES)
            ModelSelect("weapon_2", "2P武器", choices=BULLETS, values=BULLET_VALUES)
            ModelInput("lives_1", "1P生命")
            ModelInput("lives_2", "2P生命")

    def get_hotkeys(self):
        this = self.weak
        return (
            ('invincible', MOD_ALT, getVK('i'), this.invincible),
        )

    def invincible(self, _=None):
        self._global.invincible_1 = 0xFF
        self._global.invincible_2 = 0xFF