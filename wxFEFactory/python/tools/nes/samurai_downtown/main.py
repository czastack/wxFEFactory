from ..base import BaseNesHack
from lib.hack.forms import Group, DialogGroup, StaticGroup, ModelInput, ModelSelect, ModelFlagWidget, Input, Choice
from lib.win32.keys import VK
from lib import utils
from fefactory_api import ui
from . import models, datasets


class Main(BaseNesHack):

    def __init__(self):
        super().__init__()
        self._global = models.Global(0, self.handler)
        self.person = models.Person(0, self.handler)
        self.itemholder = models.ItemHolder(0, self.handler)
        self.skillholder = models.SkillHolder(0, self.handler)

    def render_main(self):
        with Group("global", "全局", self._global):
            ModelInput("growth_points", "成长点数")
            ModelInput("money_1p", "1p金钱")
            ModelInput("money_2p", "2p金钱")

        with Group("player", "我方角色", self.person, cols=4) as group:
            Choice("角色", ("1P", "2P"), self.on_person_change)

            for addr, name in models.PERSON_ATTRS:
                ModelInput(name)

        with group.footer:
            dialog_style = {'width': 1200, 'height': 900}
            with DialogGroup("items", "道具", self.itemholder, cols=4, dialog_style=dialog_style) as dialog_group:
                indexs = (0, 8, 1, 9, 2, 10, 3, 11, 4, 12, 5, 13, 6, 14, 7, 15)
                for i in indexs:
                    ModelSelect("items.%d" % i, "道具%02d" % (i + 1), choices=datasets.ITEMS)
            with DialogGroup("skills", "技能", self.skillholder, dialog_style=dialog_style):
                values = [1 << i for i in range(7, -1, -1)]
                for i, labels in enumerate(datasets.SKILL_ITEMS):
                    ModelFlagWidget("have_%s" % (i + 1), "拥有", labels=labels, values=values, checkbtn=True, cols=4)
                    ModelFlagWidget("active_%s" % (i + 1), "激活", labels=labels, values=values, checkbtn=True, cols=4)

        with Group("enemy", "敌人", None, cols=4) as group:
            for addr, name in models.ENEMY_ATTRS:
                Input(name, None, addr, size=1)

        with StaticGroup("快捷键"):
            with ui.ScrollView(className="fill"):
                ui.Text("恢复HP: alt+h")

    def get_hotkeys(self):
        this = self.weak
        return (
            (VK.MOD_ALT, VK.H, this.pull_through),
        )

    def on_person_change(self, lb):
        index = lb.index
        self.person.addr = index
        self.itemholder.addr = index * models.ItemHolder.SIZE
        # self.skillholder.addr = index * models.SkillHolder.SIZE

    def persons(self):
        person = models.Person(0, self.handler)
        for i in range(2):
            person.addr = i
            yield person

    def pull_through(self):
        for person in self.persons():
            person.set_with("体力最大值", "体力当前值").set_with("气力最大值", "气力当前值")
