from ..base import BaseNesHack
from lib.hack.form import Group, StaticGroup, ModelInput, ModelSelect, ModelCheckBox
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
from lib.hack.model import Model, Field, ByteField, WordField, FieldPrep
import fefactory_api
ui = fefactory_api.ui


class Global(Model):
    hp = ByteField(0x0597)
    star = ByteField(0x0598) # 音波等形态次数
    lives = ByteField(0x0599)
    credits = ByteField(0x07BB) # 无限Credits, 02
    invincible = ByteField(0x05F9)
    invincible2 = ByteField(0x05FB) # 44
    form = ByteField(0x05E0)
    ability = ByteField(0x05E3)


ABILITY = ("吐火", "火花", "回力刀", "剑士", "烈焰", "镭射", "音波", "车轮", "锤子", 
    "阳伞", "睡觉", "针刺", "冰冻", "冻结", "高跳", "光束", "石头", "球球", "旋风", 
    "必杀", "光明", "摔跤", "投掷", "UFO", "星之杖")


class Tool(BaseNesHack):
    def render_main(self):
        self._global = Global(0, self.handler)

        with Group("global", "全局", self._global):
            ModelInput("hp", "HP(max:47)")
            ModelInput("star", "星星")
            ModelInput("lives", "生命")
            # ModelInput("credits", "分数")
            ModelCheckBox("invincible", "闪光无敌", enableData=0xFF, disableData=0)
            ModelCheckBox("invincible2", "状态无敌", enableData=0x44, disableData=0)
            ModelInput("form", "形态")
            ModelSelect("ability", "能力", choices=ABILITY)


    def get_hotkeys(self):
        this = self.weak
        return (
            ('pull_through', MOD_ALT, getVK('h'), this.pull_through),
        )

    def pull_through(self, _=None):
        """HP恢复"""
        # self._global.hp = 0x2F
        self._global.ability += 1