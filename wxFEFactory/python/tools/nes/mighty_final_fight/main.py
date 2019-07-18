from lib.hack.forms import Group, StaticGroup, ModelInput, ModelSelect, ModelCheckBox
from lib.win32.keys import VK
from lib import ui
from ..base import BaseNesHack
from . import models, datasets


class Main(BaseNesHack):
    def __init__(self):
        super().__init__()
        self._global = models.Global(0, self.handler)

    def render_main(self):
        with Group("global", "全局", self._global):
            ModelSelect("enemy", "角色", choices=datasets.PLAYERS)
            ModelSelect("enemy", "敌人模型", choices=datasets.ENEMY_LABELS, values=datasets.ENEMY_VALUES)
            ModelInput("level", "等级")
            ModelInput("lives", "命数")
            ModelInput("hp", "HP")
            ModelInput("exp", "总经验")
            ModelInput("tool_count", "手持物数量")
            ModelInput("play_level", "关卡")
            ModelCheckBox("invincible", "无伤", enable=0xffff, disable=0)

        with StaticGroup("快捷键"):
            ui.Text("恢复HP: alt+h\n"
                "敌人一击必杀: alt+空格")

    def get_hotkeys(self):
        this = self.weak
        return (
            (VK.MOD_ALT, VK.H, this.pull_through),
            (VK.MOD_ALT, VK.SPACE, this.one_hit_kill),
        )

    def pull_through(self):
        self._global.hp = self._global.hpmax

    def one_hit_kill(self):
        self._global.enemy_hp = 0
