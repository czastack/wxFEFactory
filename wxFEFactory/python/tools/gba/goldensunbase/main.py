from ..base import BaseGbaHack
from lib.hack.form import Group, DialogGroup, ModelCheckBox, ModelInput, ModelSelect, ModelCoordWidget
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
from lib.exui.components import Pagination
import fefactory_api
ui = fefactory_api.ui


class BaseGSTool(BaseGbaHack):

    def __init__(self):
        super().__init__()
        self._global = self.models.Global(0, self.handler)
        self._personins = self.models.Person(0, self.handler)
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
            with ui.Horizontal(className="fill"):
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
            ModelInput("ground_power", "地力量")
            ModelInput("ground_defensive", "地抗性")
            ModelInput("water_power", "水力量")
            ModelInput("water_defensive", "水抗性")
            ModelInput("fire_power", "火力量")
            ModelInput("fire_defensive", "火抗性")
            ModelInput("wind_power", "风力量")
            ModelInput("wind_defensive", "风抗性")

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
        self.person.skills_page = page
        self.skills_group.read()

    def move_left(self, _=None):
        self._global.town_x -= 10

    def move_right(self, _=None):
        self._global.town_x += 10

    def move_up(self, _=None):
        self._global.town_y -= 10

    def move_down(self, _=None):
        self._global.town_y += 10

    def pull_through(self, _=None):
        for person in self.persons():
            person.hp = person.hpmax