from ..base import BaseNesHack
from lib.hack.form import Group, StaticGroup, ModelInput, ModelSelect, ModelCheckBox
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
from . import models, datasets
import fefactory_api
ui = fefactory_api.ui


class Tool(BaseNesHack):
    def __init__(self):
        super().__init__()
        self._global = models.Global(0, self.handler)
    
    def render_main(self):
        with Group("global", "全局", self._global):
            ModelSelect("enemy", "角色", choices=datasets.PLAYERS)
            ModelSelect("enemy", "敌人模型", choices=datasets.ENEMY_LABELS, values=datasets.ENEMY_VALUES)
            ModelInput("level", "等级")
            ModelInput("life", "命数")
            ModelInput("hp", "HP")
            ModelInput("exp", "总经验")
            ModelInput("tool_count", "手持物数量")
            ModelInput("play_level", "关卡")
            ModelCheckBox("invincible", "无伤", enableData=0xffff, disableData=0)

        with StaticGroup("快捷键"):
            with ui.ScrollView(className="fill"):
                ui.Text("恢复HP: alt+h")
                ui.Text("敌人一击必杀: alt+空格")

    def get_hotkeys(self):
        this = self.weak
        return (
            ('pull_through', MOD_ALT, getVK('h'), this.pull_through),
            ('one_hit_kill', MOD_ALT, getVK('space'), this.one_hit_kill),
        )

    def pull_through(self, _=None):
        self._global.hp = self._global.maxhp

    def one_hit_kill(self, _=None):
        self._global.enemy_hp = 0