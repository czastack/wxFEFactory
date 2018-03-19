from ..base import BaseGbaHack
from lib.hack.form import Group, DialogGroup, ModelCheckBox, ModelInput, ModelSelect
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
from lib.exui.components import Pagination
import fefactory_api
ui = fefactory_api.ui


class Tool(BaseGbaHack):
    from . import models, datasets
    PERSON_ADDR_START = 0x02000500

    def __init__(self):
        super().__init__()
        self._global = self.models.Global(0, self.handler)
        self.person_index = 0
    
    def render_main(self):
        datasets = self.datasets
        person = self.weak._person
        with Group("global", "全局", self._global):
            ModelInput("time", "时间")
            ModelInput("money", "金钱")
            ModelInput("get_money", "战后金钱")
            ModelInput("get_exp", "战后经验")
            ModelInput("battlein", "遇敌率")

        with Group("player", "角色", person, cols=4):
            # ModelInput("addr_hex", "地址", readonly=True)
            ui.Text("角色", className="input_label expand")
            with ui.Horizontal(className="fill"):
                ui.Choice(className="fill", choices=datasets.PERSONS, onselect=self.on_person_change).setSelection(0)
            ModelInput("level", "等级")
            ModelInput("exp", "经验")
            ModelInput("hp", "HP")
            ModelInput("ep", "HP上限")
            ModelInput("hpmax", "EP上限")
            ModelInput("epmax", "EP")
            ModelInput("atk", "攻击")
            ModelInput("defensive", "防御")
            ModelInput("speed", "速度")
            ModelInput("lucky", "好运")

        with Group("skills", "角色精神力", person) as skills_group:
            for i in range(5):
                ModelSelect("skills.%d" % i, "精神力", choices=datasets.SKILLS)
            with Group.active_group().footer:
                Pagination(self.on_skills_page, 7)
        self.skills_group = skills_group

        with Group("skills", "角色物品", person, cols=4):
            for i in range(15):
                ModelSelect("items.%d" % i, "物品%d" % (i + 1), choices=datasets.ITEMS)
                ModelInput("items_count.%d" % i, "数量")

    def on_person_change(self, lb):
        self.person_index = lb.index

    def _person(self):
        person_addr = self.PERSON_ADDR_START + self.person_index * self.models.Person.SIZE
        if person_addr:
            person = getattr(self, '_personins', None)
            if not person:
                person = self._personins = self.models.Person(person_addr, self.handler)
            elif person.addr != person_addr:
                person.addr = person_addr
            return person

    person = property(_person)

    def on_skills_page(self, page):
        self.person.skills_page = page
        self.skills_group.read()