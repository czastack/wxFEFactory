from ..base import BaseGbaHack
from lib.hack.form import Group, StaticGroup, ModelCheckBox, ModelInput, ModelSelect, CheckBox
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
from lib.exui.components import Pagination
from lib.hack.model import Model, Field, ByteField, WordField
from lib import utils
import fefactory_api
ui = fefactory_api.ui


class Global(Model):
    continues = ByteField(0x03001A84)
    lives = ByteField(0x03002C60)
    invincible = ByteField(0x03002CA0)
    score = Field(0x03002C64)
    weapon = ByteField(0x3002CA8)


WEAPONS = ("普通", "S(散弹)", "C(飞弹)", "H(导弹)", "F(火焰)", "L(激光)", "坦克")


class Tool(BaseGbaHack):

    def __init__(self):
        super().__init__()
        self._global = Global(0, self.handler)
    
    def render_main(self):
        with Group("global", "全局", self._global):
            ModelInput("lives", "生命")
            # ModelInput("tankhp", "载具生命(50)")
            ModelInput("continues", "续关")
            ModelInput("score", "分数")
            ModelSelect("weapon", "武器种类", choices=WEAPONS)
            ModelCheckBox("invincible", "无敌", enableData=0xFF, disableData=0)
            CheckBox("hit_anywhere", "Hit Anywhere", 0x080179AC, enableData=0xE014, disableData=0x72DC)
