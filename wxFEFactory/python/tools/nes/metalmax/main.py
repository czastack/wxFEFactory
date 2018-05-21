from ..base import BaseNesHack
from lib.hack.form import Group, StaticGroup, ModelCheckBox, ModelInput, ModelSelect, ModelCoordWidget, ModelFlagWidget
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
from lib.exui.components import Pagination
from . import models, datasets
import fefactory_api
ui = fefactory_api.ui


class Tool(BaseNesHack):
    STORAGE_PAGE_LENGTH = 10
    STORAGE_PAGE_TOTAL = 10
    models = models

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
            ModelCheckBox("battlein", "不遇敌", enableData=0xFF, disableData=0)

        with Group("player", "角色", person, cols=4):
            ui.Text("角色", className="input_label expand")
            with ui.Horizontal(className="fill"):
                ui.Choice(className="fill", choices=datasets.PERSONS, onselect=self.on_person_change).setSelection(0)
            ModelInput("level", "等级")
            ModelInput("hpmax", "HP上限")
            ModelInput("hp", "HP")
            ModelInput("atk", "攻击")
            ModelInput("defensive", "守备")
            ModelInput("strength", "强度")
            ModelInput("intelli", "智力")
            ModelInput("stamina", "体力")
            ModelInput("speed", "速度")
            ModelInput("battle", "战斗")
            ModelInput("drive", "驾驶")
            ModelInput("fix", "修理")
            ModelInput("exp", "经验")

        with Group("human_equips", "角色装备", person):
            for i in range(8):
                ModelSelect("equips.%d" % i, "装备%d" % (i + 1), 
                    choices=datasets.HUMAN_EQUIPS, values=datasets.HUMAN_EQUIP_VALUES)

        with Group("human_items", "角色物品", person):
            for i in range(8):
                ModelSelect("items.%d" % i, "物品%d" % (i + 1), 
                    choices=datasets.HUMAN_ITEMS, values=datasets.HUMAN_ITEM_VALUES)

        with Group("chariot", "战车", chariot):
            ui.Text("战车", className="input_label expand")
            with ui.Horizontal(className="fill"):
                ui.Choice(className="fill", choices=datasets.CHARIOTS, onselect=self.on_chariot_change).setSelection(0)
            ModelInput("sp", "装甲片")
            ModelInput("main_bullets_count", "主炮炮弹")
            ModelInput("bullet", "弹仓容量")
            ModelInput("defensive", "守备力")
            ModelInput("weight", "底盘重量")


        with Group("chariot_equips", "战车装备", chariot):
            for i in range(8):
                ModelSelect("equips.%d.type" % i, "装备%d" % (i + 1), 
                    choices=datasets.CHARIOT_EQUIPS, values=datasets.CHARIOT_EQUIP_VALUES)

        with Group("chariot_items", "战车物品", chariot):
            for i in range(8):
                ModelSelect("items.%d" % i, "物品%d" % (i + 1), 
                    choices=datasets.CHARIOT_ITEMS, values=datasets.CHARIOT_ITEM_VALUES)

        # with Group("special_bullets", "特殊炮弹", chariot, cols=4):
        #     for i in range(8):
        #         ModelSelect("special_bullets.%d" % i, "", choices=datasets.SPECIAL_BULLETS)
        #         ModelInput("special_bullets_count.%d" % i, "数量")

        # self.storage_group = Group("storage", "保管物品", self._global)
        # self.lazy_group(self.storage_group, self.render_storage)

        with StaticGroup("快捷键"):
            with ui.ScrollView(className="fill"):
                ui.Text("左移: alt+left")
                ui.Text("右移: alt+right")
                ui.Text("上移: alt+up")
                ui.Text("下移: alt+right")
                ui.Text("恢复HP: alt+h")

    def render_storage(self):
        choices = datasets.HUMAN_EQUIPS + datasets.HUMAN_ITEMS + datasets.CHARIOT_EQUIPS + datasets.CHARIOT_ITEMS
        values = (
            tuple(range(len(datasets.HUMAN_ITEMS))) + 
            tuple((0x0100 | i) for i in range(len(datasets.HUMAN_EQUIPS))) + 
            tuple((0x0200 | i) for i in range(len(datasets.CHARIOT_ITEMS))) + 
            tuple((0x0300 | i) for i in range(len(datasets.CHARIOT_EQUIPS)))
        )
        for i in range(10):
            ModelSelect("storage.%d+storage_offset" % i, "", choices=choices, values=values)
        with Group.active_group().footer:
            Pagination(self.on_storage_page, self.STORAGE_PAGE_TOTAL)

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

    def move_left(self, _=None):
        self._global.posx -= 1
        self._global.offx -= 1

    def move_right(self, _=None):
        self._global.posx += 1
        self._global.offx += 1

    def move_up(self, _=None):
        self._global.posy -= 1
        self._global.offy -= 1

    def move_down(self, _=None):
        self._global.posy += 1
        self._global.offy += 1

    def pull_through(self, _=None):
        for person in self.persons():
            person.hp = person.hpmax