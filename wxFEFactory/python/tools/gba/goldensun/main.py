from ..base import BaseGbaHack
from lib.hack.forms import Group, StaticGroup, ModelInput, ModelSelect, ModelCoordWidget, ModelFlagWidget, Choice
from lib.win32.keys import VK
from lib.exui.components import Pagination
from fefactory_api import ui


class GSHack(BaseGbaHack):
    SKILLS_PAGE_LENGTH = 5
    SKILLS_PAGE_TOTAL = 7

    def __init__(self):
        super().__init__()
        self._global = self.models.Global(0, self.handler)
        self.person = self.models.Person(0, self.handler)
        self.person.skills_offset = 0

    def render_main(self):
        with Group("global", "全局", self._global):
            ModelInput("time", "时间")
            ModelInput("money", "金钱")
            ModelInput("get_money", "战后金钱")
            ModelInput("get_exp", "战后经验")
            ModelInput("battlein", "遇敌率")
            ModelCoordWidget("town_pos", "城镇坐标", length=2, type=int, savable=True, preset=self.coords)
            ModelCoordWidget("map_pos", "地图坐标", length=2, type=int, savable=True, preset=self.coords)

        self.lazy_group(Group("player", "角色", self.person, cols=4), self.render_person)
        self.skills_group = Group("skills", "角色精神力", self.person)
        self.lazy_group(self.skills_group, self.render_skills)
        self.lazy_group(Group("skills", "角色物品", self.person, cols=4), self.render_items)
        self.lazy_group(Group("djinnis", "角色精灵", self.person), self.render_djinnis)
        self.lazy_group(StaticGroup("快捷键"), self.render_hotkeys)

    def render_person(self):
        Choice("角色", self.datasets.PERSONS, self.on_person_change)
        ModelInput("addr_hex", "地址", readonly=True)
        ModelInput("level", "等级")
        ModelInput("exp", "经验")
        ModelInput("hp", "HP")
        ModelInput("hpmax", "HP上限")
        ModelInput("ep", "EP")
        ModelInput("epmax", "EP上限")
        ModelInput("atk", "攻击")
        ModelInput("defense", "防御")
        ModelInput("speed", "速度")
        ModelInput("lucky", "好运")
        for tlabel, tname in self.datasets.ELEMENT_TYPES:
            ModelInput("%s_power" % tname, "%s力量" % tlabel)
            ModelInput("%s_defense" % tname, "%s抗性" % tlabel)

    def render_skills(self):
        for i in range(5):
            ModelSelect("skills.%d+skills_offset.value" % i, "精神力", choices=self.datasets.SKILLS)
        with self.skills_group.footer:
            Pagination(self.on_skills_page, self.SKILLS_PAGE_TOTAL)

    def render_items(self):
        for i in range(15):
            ModelSelect("items.%d.item" % i, "物品%d" % (i + 1), choices=self.datasets.ITEMS)
            ModelInput("items.%d.count" % i, "数量")

    def render_djinnis(self):
        for (tlable, tname), (labels, helps) in zip(self.datasets.ELEMENT_TYPES, self.datasets.DJINNIS):
            ModelFlagWidget("djinni_%s" % tname, "%s精灵" % tlable, labels=labels, helps=helps, checkbtn=True, cols=4)
            ModelFlagWidget("djinni_%s_on" % tname, "附身", labels=labels, helps=helps, checkbtn=True, cols=4)
            ModelInput("djinni_%s_count" % tname, "拥有数量").set_help("至少一个角色精灵数量大于0才会显示精灵菜单")
            ModelInput("djinni_%s_on_count" % tname, "附身数量")

    def render_hotkeys(self):
        ui.Text("左移: alt+left\n"
            "右移: alt+right\n"
            "上移: alt+up\n"
            "下移: alt+right\n"
            "恢复HP: alt+h")

    def get_hotkeys(self):
        this = self.weak
        return (
            (VK.MOD_ALT, VK.LEFT, this.move_left),
            (VK.MOD_ALT, VK.RIGHT, this.move_right),
            (VK.MOD_ALT, VK.UP, this.move_up),
            (VK.MOD_ALT, VK.DOWN, this.move_down),
            (VK.MOD_ALT, VK.H, this.pull_through),
        )

    def on_person_change(self, lb):
        self.person.addr = self.PERSON_ADDR_START + lb.index * self.models.Person.SIZE

    def persons(self):
        person = self.models.Person(0, self.handler)
        for i in range(len(self.datasets.PERSONS)):
            person.addr = self.PERSON_ADDR_START + i * self.models.Person.SIZE
            yield person

    def on_skills_page(self, page):
        self.person.skills_offset = (page - 1) * self.SKILLS_PAGE_LENGTH
        self.skills_group.read()

    def move_left(self):
        if self._global.map_x is 0:
            self._global.town_x -= 10
        else:
            self._global.map_x -= 10

    def move_right(self):
        if self._global.map_x is 0:
            self._global.town_x += 10
        else:
            self._global.map_x += 10

    def move_up(self):
        if self._global.map_x is 0:
            self._global.town_y -= 10
        else:
            self._global.map_y -= 10

    def move_down(self):
        if self._global.map_x is 0:
            self._global.town_y += 10
        else:
            self._global.map_y += 10

    def pull_through(self):
        for person in self.persons():
            person.hp = person.hpmax
