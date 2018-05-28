from ..base import BaseNesHack
from lib.hack.form import Group, DialogGroup, ModelInput, ModelCheckBox, ModelSelect, ModelFlagWidget, Input
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
from lib import utils
from . import models, datasets
import fefactory_api
ui = fefactory_api.ui


class Tool(BaseNesHack):

    def __init__(self):
        super().__init__()
        self._global = models.Global(0, self.handler)
        self._personins = models.Person(0, self.handler)
        self._itemholderins = models.ItemHolder(0, self.handler)
        self._skillholderins = models.SkillHolder(0, self.handler)
        self.person_index = 0
    
    def render_main(self):
        with Group("global", "全局", self._global):
            ModelInput("growth_points", "成长点数")

        with Group("player", "我方角色", self.weak._person, cols=4) as group:
            # ModelInput("addr_hex", "地址", readonly=True)
            ui.Text("角色", className="input_label expand")
            with ui.Horizontal(className="fill"):
                ui.Choice(className="fill", choices=("1P", "2P"), onselect=self.on_person_change).setSelection(0)
            
            for addr, name in models.PERSON_ATTRS:
                ModelInput(name)

        with group.footer:
            dialog_style = {'width': 1200, 'height': 640}
            indexs = (0, 8, 1, 9, 2, 10, 3, 11, 4, 12, 5, 13, 6, 14, 7, 15)
            for name, label, choices, values in (("items", "道具", datasets.ITEMS, None),):
                with DialogGroup(name, label, self.weak._itemholder, cols=4, dialog_style=dialog_style) as dialog_group:
                    for i in indexs:
                        ModelSelect("%s.%d" % (name, i), "%s%02d" % (label, i + 1), choices=choices, values=values)
            with DialogGroup("skills", "技能", self.weak._skillholder, dialog_style=dialog_style):
                values = [1 << i for i in range(7, -1, -1)]
                for i, labels in enumerate(datasets.SKILL_ITEMS):
                    ModelFlagWidget("have_%s" % (i+1), "拥有", labels=labels, values=values, checkbtn=True, cols=4)
                    ModelFlagWidget("active_%s" % (i+1), "激活", labels=labels, values=values, checkbtn=True, cols=4)

        with Group("enemy", "敌人", None, cols=4) as group:
            for addr, name in models.ENEMY_ATTRS:
                Input(name, None, addr, size=1)

    def on_person_change(self, lb):
        self.person_index = lb.index

    def _person(self):
        self._personins.addr = self.person_index
        return self._personins

    def _itemholder(self):
        self._itemholderins.addr = self.person_index * models.ItemHolder.SIZE
        return self._itemholderins

    def _skillholder(self):
        return self._skillholderins

    person = property(_person)
    itemholder = property(_itemholder)
    skillholder = property(_skillholder)
