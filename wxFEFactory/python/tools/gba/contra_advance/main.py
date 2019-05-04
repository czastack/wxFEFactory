from lib.hack.forms import Group, StaticGroup, ModelCheckBox, ModelInput, ModelSelect
from lib.exui.components import Pagination
from lib.hack.models import Model, Field, ByteField, WordField, ToggleField
from fefactory_api import ui
from ..base import BaseGbaHack


class Global(Model):
    continues = ByteField(0x03001A84, label="续关")
    lives = ByteField(0x03002C60, label="生命")
    invincible = ToggleField(0x03002CA0, size=1, enable=0xFF, disable=0, label="无敌")
    score = Field(0x03002C64, label="分数")
    weapon = ByteField(0x3002CA8, label="武器种类")
    hit_anywhere = ToggleField(0x080179AC, size=2, enable=0xE014, disable=0x72DC, label="Hit Anywhere")


WEAPONS = ("普通", "S(散弹)", "C(飞弹)", "H(导弹)", "F(火焰)", "L(激光)", "坦克")


class Main(BaseGbaHack):

    def __init__(self):
        super().__init__()
        self._global = Global(0, self.handler)

    def render_main(self):
        with Group("global", "全局", self._global):
            ModelInput("lives")
            ModelInput("continues")
            ModelInput("score")
            ModelSelect("weapon", choices=WEAPONS)
            ModelCheckBox("invincible")
            ModelCheckBox("hit_anywhere")
