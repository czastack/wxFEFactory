from ..base import BaseGbaHack
from lib.hack.form import Group, StaticGroup, ModelCheckBox, ModelInput, ModelSelect, ModelCoordWidget, ModelFlagWidget
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
from lib.exui.components import Pagination
from . import models, datasets
import fefactory_api
ui = fefactory_api.ui


class Tool(BaseGbaHack):
    def __init__(self):
        super().__init__()
        self._global = models.Global(0, self.handler)
        self._personins = models.Person(0, self.handler)
        self.person_index = 0
    
    def render_main(self):
        person = self.weak._person
        with Group("global", "全局", self._global):
            ModelInput("tp", "TP")
            ModelInput("kill_slot", "必杀槽")
            ModelInput("rage", "RAGE")
            ModelInput("member_num", "队伍人数")
            for i in range(5):
                ModelSelect("members.%d" % i, "第%d位队员" % (i + 1), choices=datasets.PERSONS)
            ModelInput("item_num", "道具数量")

        with Group("favors", "好感度", self._global):
            i = 0
            for item in datasets.GIRLS:
                ModelInput("favors.%d" % i, "%s累计好感度" % item)
                i += 1
            for item in datasets.GIRLS:
                ModelInput("favors.%d" % i, "%s本章好感度" % item)
                i += 1

        with Group("items", "道具", self._global, cols=4):
            for i in range(16):
                ModelSelect("items.%d.item" % i, "道具%d" % (i + 1), choices=datasets.ITEMS)
                ModelInput("items.%d.count" % i, "数量")

        with Group("person_battles", "战斗中", self._global, cols=4):
            for i in range(6):
                ModelInput("person_battles.%d.hp" % i, "人物%dHP" % (i + 1))

        with Group("player", "角色", person, cols=4):
            ui.Text("角色", className="input_label expand")
            with ui.Horizontal(className="fill"):
                ui.Choice(className="fill", choices=datasets.PERSONS, onselect=self.on_person_change).setSelection(0)
            ModelInput("hpmax", "HP上限")
            ModelInput("resist", "RESIST")
            ModelInput("str", "STR")
            ModelInput("mgc", "MGC")
            ModelInput("agl", "AGL")
            ModelInput("vit", "VIT")
            ModelInput("_resist", "抗性")

        with StaticGroup("快捷键"):
            with ui.ScrollView(className="fill"):
                ui.Text("恢复HP: alt+h")

    def get_hotkeys(self):
        return (
            ('pull_through', MOD_ALT, getVK('h'), self.weak.pull_through),
        )

    def on_person_change(self, lb):
        self.person_index = lb.index

    def _person(self):
        person_addr = self.person_index * models.Person.SIZE
        self._personins.addr = person_addr
        return self._personins

    def persons(self):
        person = models.Person(0, self.handler)
        for i in range(len(datasets.PERSONS)):
            person.addr = i * models.Person.SIZE
            yield person

    person = property(_person)

    def pull_through(self, _=None):
        for person in self.persons():
            person.hp = person.hpmax