from ..base import BaseGbaHack
from lib.hack.form import Group, StaticGroup, ModelInput, ModelSelect, ModelCoordWidget, ModelFlagWidget
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
from lib.exui.components import Pagination
import fefactory_api
ui = fefactory_api.ui


class BaseGSTool(BaseGbaHack):
    SKILLS_PAGE_LENGTH = 5
    SKILLS_PAGE_TOTAL = 7

    def __init__(self):
        super().__init__()
        self._global = self.models.Global(0, self.handler)
        self._personins = self.models.Person(0, self.handler)
        self._personins.skills_offset = 0
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
            ModelCoordWidget("town_pos", "城镇坐标", length=2, type_=int, savable=True, preset=self.coords)
            ModelCoordWidget("map_pos", "地图坐标", length=2, type_=int, savable=True, preset=self.coords)

        with Group("player", "角色", person, cols=4):
            ui.Text("角色", className="input_label expand")
            ui.Choice(className="fill", choices=datasets.PERSONS, onselect=self.on_person_change).setSelection(0)
            ModelInput("addr_hex", "地址", readonly=True)
            ModelInput("level", "等级")
            ModelInput("exp", "经验")
            ModelInput("hp", "HP")
            ModelInput("hpmax", "HP上限")
            ModelInput("ep", "EP")
            ModelInput("epmax", "EP上限")
            ModelInput("atk", "攻击")
            ModelInput("defensive", "防御")
            ModelInput("speed", "速度")
            ModelInput("lucky", "好运")
            for tlabel, tname in datasets.ELEMENT_TYPES:
                ModelInput("%s_power" % tname, "%s力量" % tlabel)
                ModelInput("%s_defensive" % tname, "%s抗性" % tlabel)

        with Group("skills", "角色精神力", person) as skills_group:
            for i in range(5):
                ModelSelect("skills.%d+skills_offset.value" % i, "精神力", choices=datasets.SKILLS)
            with skills_group.footer:
                Pagination(self.on_skills_page, self.SKILLS_PAGE_TOTAL)
        self.skills_group = skills_group

        with Group("skills", "角色物品", person, cols=4):
            for i in range(15):
                ModelSelect("items.%d.item" % i, "物品%d" % (i + 1), choices=datasets.ITEMS)
                ModelInput("items.%d.count" % i, "数量")

        self.lazy_group(Group("djinnis", "角色精灵", person), self.render_djinnis)

        with StaticGroup("快捷键"):
            with ui.ScrollView(className="fill"):
                ui.Text("左移: alt+left")
                ui.Text("右移: alt+right")
                ui.Text("上移: alt+up")
                ui.Text("下移: alt+right")
                ui.Text("恢复HP: alt+h")

    def render_djinnis(self):
        for (tlable, tname), (labels, helps) in zip(self.datasets.ELEMENT_TYPES, self.datasets.DJINNIS):
            ModelFlagWidget("djinni_%s" % tname, "%s精灵" % tlable, labels=labels, helps=helps, checkbtn=True, cols=8)
            ModelFlagWidget("djinni_%s_on" % tname, "附身", labels=labels, helps=helps, checkbtn=True, cols=8)
            ModelInput("djinni_%s_count" % tname, "拥有数量").view.setToolTip("至少一个角色精灵数量大于0才会显示精灵菜单")
            ModelInput("djinni_%s_on_count" % tname, "附身数量")

    def get_hotkeys(self):
        this = self.weak
        return (
            ('move_left', MOD_ALT, getVK('left'), this.move_left),
            ('move_right', MOD_ALT, getVK('right'), this.move_right),
            ('move_up', MOD_ALT, getVK('up'), this.move_up),
            ('move_down', MOD_ALT, getVK('down'), this.move_down),
            ('pull_through', MOD_ALT, getVK('h'), this.pull_through),
        )

    def on_person_change(self, lb):
        self.person_index = lb.index

    def _person(self):
        person_addr = self.PERSON_ADDR_START + self.person_index * self.models.Person.SIZE
        self._personins.addr = person_addr
        return self._personins

    def persons(self):
        person = self.models.Person(0, self.handler)
        for i in range(len(self.datasets.PERSONS)):
            person.addr = self.PERSON_ADDR_START + i * self.models.Person.SIZE
            yield person

    person = property(_person)

    def on_skills_page(self, page):
        self.person.skills_offset = (page - 1) * self.SKILLS_PAGE_LENGTH
        self.skills_group.read()

    def move_left(self, _=None):
        if self._global.map_x is 0:
            self._global.town_x -= 10
        else:
            self._global.map_x -= 10

    def move_right(self, _=None):
        if self._global.map_x is 0:
            self._global.town_x += 10
        else:
            self._global.map_x += 10

    def move_up(self, _=None):
        if self._global.map_x is 0:
            self._global.town_y -= 10
        else:
            self._global.map_y -= 10

    def move_down(self, _=None):
        if self._global.map_x is 0:
            self._global.town_y += 10
        else:
            self._global.map_y += 10

    def pull_through(self, _=None):
        for person in self.persons():
            person.hp = person.hpmax