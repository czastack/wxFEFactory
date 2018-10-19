from ..base import BaseNesHack
from lib.hack.forms import Group, StaticGroup, ModelInput, ModelCheckBox, ModelSelect
from lib.win32.keys import VK
from lib.hack.models import Model, Field, ByteField, WordField, ToggleField


class Global(Model):
    lives = ByteField(0x018D, label="战机数量")
    money = ByteField(0x018E, label="金钱")
    bomb_count = ByteField(0x018F, label="炸弹数量")
    bomb_type = ByteField(0x0190, label="炸弹种类")
    armor = ToggleField(0x0032, enable=0xC0, disable=0, label="护甲")
    power = ByteField(0x0033, label="子弹威力")
    bullet_type = ByteField(0x0034, label="子弹种类")
    bomb_power = ByteField(0x003B, label="炸弹威力")
    invincible = ByteField(0x06A0, label="无敌时间")
    bomb_time = ByteField(0x06A1, label="炸弹持续时间")
    level = ByteField(0x0180, label="关卡序号")


class Main(BaseNesHack):
    def render_main(self):
        self._global = Global(0, self.handler)

        with Group("global", "全局", self._global):
            ModelInput("lives")
            ModelInput("money")
            ModelInput("bomb_count")
            ModelSelect("bomb_type", choices=('F', 'B', 'T', 'W'))
            ModelInput("power")
            ModelSelect("bullet_type", choices=('1', '2', '3', '4', '5'))
            ModelInput("bomb_power")
            ModelInput("invincible")
            ModelInput("bomb_time")
            ModelInput("level")
            ModelCheckBox("armor")

    def get_hotkeys(self):
        return (
            (0, VK.B, self.bomb_time),
            (0, VK.N, self.invincible),
        )

    def bomb_time(self):
        self._global.bomb_time = 0xFF

    def invincible(self):
        self._global.invincible = 0xFF
