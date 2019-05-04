from lib.hack.forms import Group, StaticGroup, ModelInput, ModelFlagWidget
from lib.win32.keys import VK
from lib.hack.models import Model, Field, ByteField, WordField, FieldPrep
from ..base import BaseNesHack


class Global(Model):
    LifeField = FieldPrep(lambda ins, x, f: x - 1, lambda ins, x, f: int(x) + 1)
    hp_burns = LifeField(ByteField(0x00B3))
    hp_smish = LifeField(ByteField(0x00B4))
    hp_iron = LifeField(ByteField(0x00B5))
    hp_beans = LifeField(ByteField(0x00B6))
    invincible = ByteField(0x07C8)
    level = ByteField(0x0075)
    weapon_burns = ByteField(0x007F)
    weapon_smish = ByteField(0x0080)
    weapon_iron = ByteField(0x0081)
    weapon_beans = ByteField(0x0082)


class Main(BaseNesHack):
    def render_main(self):
        self._global = Global(0, self.handler)

        with Group("global", "全局", self._global):
            ModelInput("hp_burns", "BURNS生命")
            ModelInput("hp_smish", "SMISH生命")
            ModelInput("hp_iron", "IRON生命")
            ModelInput("hp_beans", "BEANS生命")
            ModelInput("invincible", "无敌(max:95)")
            ModelInput("level", "关卡(0-4)")
            ModelFlagWidget("weapon_burns", "BURNS枪类型", labels=("手雷", "机枪", "发射数+1", "跳跃无敌"))
            ModelFlagWidget("weapon_smish", "SMISH枪类型", labels=("狙击", "导弹", "发射数+1", "跳跃无敌"))
            ModelFlagWidget("weapon_iron", "IRON枪类型", labels=("火焰喷射器", "火箭弹", "发射数+1", "跳跃无敌"))
            ModelFlagWidget("weapon_beans", "BEANS枪类型", labels=("地雷", "C4", "发射数+1", "跳跃无敌"))

    def get_hotkeys(self):
        this = self.weak
        return (
            (VK.MOD_ALT, VK.I, this.invincible),
        )

    def invincible(self):
        self._global.invincible = 90
