from functools import partial
from ..base import BaseDolphinHack
from . import models, datasets
from lib.hack.form import Group, StaticGroup, InputWidget, ModelCheckBoxWidget, ModelInputWidget, ModelSelectWidget
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

        with Group("player", "角色", self._person, handler=self.handler, cols=4):
            ModelInputWidget("addr_hex", "地址", readonly=True)
            ModelInputWidget("no", "角色编号", readonly=True)
            ModelSelectWidget("prof", "职业", None, None, datasets.PROFESSION, 
                tuple(0x1D10 + i * 0x11C for i in range(len(datasets.PROFESSION))))
            ModelInputWidget("hp", "当前HP")
            ModelInputWidget("level", "等级")
            ModelInputWidget("exp", "经验")
            ModelInputWidget("posx", "横坐标")
            ModelInputWidget("posy", "纵坐标")
            ModelInputWidget("physical_add", "体格/重量+")
            ModelInputWidget("move_add", "移动+")
            ModelInputWidget("hp_add", "HP+")
            ModelInputWidget("power_add", "力+")
            ModelInputWidget("magic_add", "魔力+")
            ModelInputWidget("skill_add", "技术+")
            ModelInputWidget("speed_add", "速+")
            ModelInputWidget("lucky_add", "幸运+")
            ModelInputWidget("defensive_add", "守备+")
            ModelInputWidget("magicdef_add", "魔防+")
            ui.Text("  行动状态 ")
            ModelCheckBoxWidget("moved", "已行动", enableData=1, disableData=0)
            # ui.Hr()
            # ui.Hr()
            # ui.Hr()
            # ui.Hr()
            # for i in range(12):
            #     ModelInputWidget("skills", "技能%d" % (i + 1))


    def _person(self):
        pedid = self._ram.pedid
        if pedid:
            return self._ram.persons[pedid]

    person = property(_person)