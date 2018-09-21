from ..base import BaseGbaHack
from lib.hack.forms import Group, StaticGroup, ModelInput, ModelSelect, ModelFlagWidget, Choice
from lib.win32.keys import VK
from lib.exui.components import Pagination
from fefactory_api import ui
from . import models, datasets


class Main(BaseGbaHack):
    STORAGE_PAGE_LENGTH = 10
    STORAGE_PAGE_TOTAL = 10

    def __init__(self):
        super().__init__()
        self._global = models.Global(0, self.handler)
        self._global.storage_offset = 0
        self.person = models.Person(0, self.handler)
        self.chariot = models.Chariot(0, self.handler)

    def render_main(self):
        with Group("global", "全局", self._global):
            ModelInput("money")
            ModelInput("battlein")

        with Group("player", "角色", self.person, cols=4):
            Choice("角色", datasets.PERSONS, self.on_person_change)
            ModelInput("level")
            ModelInput("hp")
            ModelInput("hpmax")
            ModelInput("atk")
            ModelInput("defense")
            ModelInput("power")
            ModelInput("intelli")
            ModelInput("stamina")
            ModelInput("speed")
            ModelInput("battle")
            ModelInput("drive")
            ModelInput("fix")
            ModelInput("exp")

        self.lazy_group(Group("human_items", "角色装备/物品", self.person), self.render_human_items)
        self.lazy_group(Group("chariot", "战车", self.chariot, cols=4), self.render_chariot)
        self.lazy_group(Group("chariot_items", "战车装备/物品", self.chariot), self.render_chariot_items)
        self.lazy_group(Group("special_bullets", "特殊炮弹", self.chariot, cols=4), self.render_special_bullets)
        self.storage_group = Group("storage", "保管物品", self._global)
        self.lazy_group(self.storage_group, self.render_storage)

        with StaticGroup("快捷键"):
            with ui.ScrollView(className="fill"):
                ui.Text("左移: alt+left")
                ui.Text("右移: alt+right")
                ui.Text("上移: alt+up")
                ui.Text("下移: alt+right")
                ui.Text("恢复HP: alt+h")

    def render_human_items(self):
        for i in range(self.person.equips.length):
            ModelSelect("equips.%d" % i, "装备%d" % (i + 1), choices=datasets.HUMAN_EQUIPS, dragable=True)
        for i in range(self.person.items.length):
            ModelSelect("items.%d" % i, "物品%d" % (i + 1), choices=datasets.HUMAN_ITEMS, dragable=True)

    def render_chariot(self):
        Choice("战车", datasets.CHARIOTS, self.on_chariot_change)
        ModelInput("sp")
        ModelInput("bullet")
        ModelInput("defense")
        ModelInput("weight")

    def render_chariot_items(self):
        for i in range(self.chariot.equips.length):
            ModelSelect("equips.%d" % i, "装备%d" % (i + 1), choices=datasets.CHARIOT_EQUIPS, dragable=True)
        for i in range(self.chariot.items.length):
            ModelSelect("items.%d" % i, "物品%d" % (i + 1), choices=datasets.CHARIOT_ITEMS, dragable=True)

    def render_special_bullets(self):
        for i in range(self.chariot.special_bullets.length):
            ModelSelect("special_bullets.%d" % i, "炮弹%d" % (i + 1), choices=datasets.SPECIAL_BULLETS, dragable=True)
            ModelInput("special_bullets_count.%d" % i, "数量")

    def render_storage(self):
        choices = datasets.HUMAN_EQUIPS + datasets.HUMAN_ITEMS + datasets.CHARIOT_EQUIPS + datasets.CHARIOT_ITEMS
        values = (tuple(range(len(datasets.HUMAN_ITEMS)))
            + tuple((0x0100 | i) for i in range(len(datasets.HUMAN_EQUIPS)))
            + tuple((0x0200 | i) for i in range(len(datasets.CHARIOT_ITEMS)))
            + tuple((0x0300 | i) for i in range(len(datasets.CHARIOT_EQUIPS))))

        for i in range(10):
            ModelSelect("storage.%d+storage_offset" % i, "", choices=choices, values=values, dragable=True)
        with Group.active_group().footer:
            Pagination(self.on_storage_page, self.STORAGE_PAGE_TOTAL)

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
        self.person.addr = lb.index * models.Person.SIZE

    def on_chariot_change(self, lb):
        self.chariot.addr = lb.index * models.Chariot.SIZE

    def on_storage_page(self, page):
        self._global.storage_offset = (page - 1) * self.STORAGE_PAGE_LENGTH
        self.storage_group.read()

    def persons(self):
        person = models.Person(0, self.handler)
        for i in range(len(datasets.PERSONS)):
            person.addr = i * models.Person.SIZE
            yield person

    def chariots(self):
        chariot = models.chariot(0, self.handler)
        for i in range(len(datasets.CHARIOTS)):
            chariot.addr = i * models.chariot.SIZE
            yield chariot

    def move_left(self):
        self._global.posx -= 1

    def move_right(self):
        self._global.posx += 1

    def move_up(self):
        self._global.posy -= 1

    def move_down(self):
        self._global.posy += 1

    def pull_through(self):
        for person in self.persons():
            person.hp = person.hpmax
