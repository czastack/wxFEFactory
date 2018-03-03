from functools import partial
from ..base import BaseDolphinHack
from . import models, datasets
from lib.hack.form import Group, StaticGroup, InputWidget, CheckBoxWidget, ModelInputWidget
import fefactory_api
ui = fefactory_api.ui


class Tool(BaseDolphinHack):

    def __init__(self):
        super().__init__()
        self._ram = models.Ram(0, self.handler)
        self.count_data = {}
    
    def render_main(self):
        with Group("global", "全局", self._ram, handler=self.handler):
            ModelInputWidget("money1", "小队1金钱")
            ModelInputWidget("money2", "小队2金钱")
            ModelInputWidget("money3", "小队3金钱")
            ModelInputWidget("exp1", "据点1分配经验值")
            ModelInputWidget("exp2", "据点2分配经验值")
            ModelInputWidget("exp3", "据点3分配经验值")

        with Group("player", "角色", self._ram, handler=self.handler):
            ModelInputWidget("hp", "hp")
            ModelInputWidget("physical", "体格/重量+")
            ModelInputWidget("move_add", "移动+")
            ModelInputWidget("hp_add", "HP+")
            ModelInputWidget("power", "力")
            ModelInputWidget("magic", "魔力")
            ModelInputWidget("skill", "技术")
            ModelInputWidget("speed", "速")
            ModelInputWidget("lucky", "幸运")
            ModelInputWidget("defensive", "守备")
            ModelInputWidget("magicdef", "魔防")