from ..base import BaseNesHack
from lib.hack.forms import Group, StaticGroup, ModelCheckBox, ModelInput, ModelSelect, ModelFlagWidget, Choice
from lib.win32.keys import VK
from lib.exui.components import Pagination
from fefactory_api import ui
from . import models, datasets


class Main(BaseNesHack):
    def __init__(self):
        super().__init__()
        self._global = models.Global(0, self.handler)
        self._global.storage_offset = 0
        self.person = models.Person(0, self.handler)
        self.chariot = models.Chariot(0, self.handler)

    def render_main(self):
        person = self.person
        chariot = self.chariot
        with Group("global", "全局", self._global):
            ModelInput("money", "金钱")
            ModelInput("battlein", "遇敌率")
            ModelCheckBox("battlein", "不遇敌", enable=0xFF, disable=0)

        with Group("player", "角色", person, cols=4):
            Choice("角色", datasets.PERSONS, self.on_person_change)
            ModelInput("level", "等级")
            ModelInput("hpmax", "HP上限")
            ModelInput("hp", "HP")
            ModelInput("atk", "攻击")
            ModelInput("defense", "守备")
            ModelInput("strength", "强度")
            ModelInput("intelli", "智力")
            ModelInput("stamina", "体力")
            ModelInput("speed", "速度")
            ModelInput("battle", "战斗")
            ModelInput("drive", "驾驶")
            ModelInput("fix", "修理")
            ModelInput("exp", "经验")

        self.lazy_group(Group("human_items", "角色装备/物品", person, cols=4), self.render_human_items)
        self.lazy_group(Group("chariot", "战车", chariot, cols=4), self.render_chariot)
        self.lazy_group(Group("chariot_items", "战车装备/物品", chariot, cols=4), self.render_chariot_items)

        with StaticGroup("快捷键"):
            ui.Text("左移: alt+left\n"
                "右移: alt+right\n"
                "上移: alt+up\n"
                "下移: alt+right\n"
                "恢复HP: alt+h")

    def render_human_items(self):
        for i in range(self.person.equips.length):
            ModelSelect("equips.%d" % i, "装备%d" % (i + 1),
                choices=datasets.HUMAN_EQUIPS, values=datasets.HUMAN_EQUIP_VALUES)
        for i in range(self.person.items.length):
            ModelSelect("items.%d" % i, "物品%d" % (i + 1),
                choices=datasets.HUMAN_ITEMS, values=datasets.HUMAN_ITEM_VALUES)

    def render_chariot(self):
        Choice("战车", datasets.CHARIOTS, self.on_chariot_change)
        ModelInput("sp", "装甲片")
        ModelInput("main_bullets_count", "主炮炮弹")
        ModelInput("bullet", "弹仓容量")
        ModelInput("defense", "守备力")
        ModelInput("weight", "底盘重量")

    def render_chariot_items(self):
        for i in range(self.chariot.equips.length):
            ModelSelect("equips.%d.type" % i, "装备%d" % (i + 1),
                choices=datasets.CHARIOT_EQUIPS, values=datasets.CHARIOT_EQUIP_VALUES)
        for i in range(self.chariot.items.length):
            ModelSelect("items.%d" % i, "物品%d" % (i + 1),
                choices=datasets.CHARIOT_ITEMS, values=datasets.CHARIOT_ITEM_VALUES)

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
        self.person.set_index(lb.index)

    def on_chariot_change(self, lb):
        self.chariot.set_index(lb.index)

    def on_storage_page(self, page):
        self._global.storage_offset = (page - 1) * self.STORAGE_PAGE_LENGTH
        self.storage_group.read()

    def persons(self):
        person = models.Person(0, self.handler)
        for i in range(len(datasets.PERSONS)):
            person.set_index(i)
            yield person

    def chariots(self):
        chariot = models.chariot(0, self.handler)
        for i in range(len(datasets.CHARIOTS)):
            chariot.set_index(i)
            yield chariot

    def move_left(self):
        self._global.posx -= 1
        self._global.offx -= 1

    def move_right(self):
        self._global.posx += 1
        self._global.offx += 1

    def move_up(self):
        self._global.posy -= 1
        self._global.offy -= 1

    def move_down(self):
        self._global.posy += 1
        self._global.offy += 1

    def pull_through(self):
        for person in self.persons():
            person.hp = person.hpmax
