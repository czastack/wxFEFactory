from ..base import BaseNdsHack
from lib.hack.form import Group, StaticGroup, ModelCheckBox, ModelMultiCheckBox, ModelInput, ModelSelect, ModelFlagWidget
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
from lib.exui.components import Pagination
from fefactory_api import ui


class MetalMaxHack(BaseNdsHack):
    TRAIN_ITEMS_PAGE_LENGTH = 10
    TRAIN_ITEMS_PAGE_TOTAL = 20

    def __init__(self):
        super().__init__()
        self._global = self.models.Global(0, self.handler)
        self._global.train_items_offset = 0
        self.person = self.models.Person(0, self.handler)
        self.item_index = 1
    
    def render_main(self):
        datasets = self.datasets
        weak = self.weak
        
        with Group("global", "全局", self._global, cols=4):
            ModelInput("money")
            ModelInput("exp")
            ModelInput("stamp")
            ModelInput("game_time")
            ModelInput("after_money")
            ModelInput("after_exp")
            ModelSelect("after_money_rate", choices=datasets.RATE, values=datasets.RATE_VALUES)
            ModelSelect("after_exp_rate", choices=datasets.RATE, values=datasets.RATE_VALUES)
            ModelCheckBox("quick_switch")
            ModelCheckBox("quick_move")
            ModelCheckBox("must_winning")
            ModelCheckBox("tool_count_keep")
            ModelCheckBox("ammo_keep")
            ModelMultiCheckBox("level_up_max")
            ModelMultiCheckBox("weight_zero")
            ModelMultiCheckBox("equip_limit_remove")
            ModelMultiCheckBox("without_material")
            ModelCheckBox("twin_engines")
            ModelCheckBox("drop_item_three_star")
            ModelCheckBox("no_battle")
            ModelCheckBox("must_drop_item")
            ModelCheckBox("must_first")
            ModelMultiCheckBox("through_wall")

        with Group("player", "角色", self.person, cols=4):
            ui.Text("角色", className="input_label expand")
            ui.Choice(className="fill", choices=datasets.PERSONS, onselect=self.on_person_change).setSelection(0)
            ModelInput("hp")
            ModelInput("hpmax")
            ModelInput("battle_level")
            ModelInput("drive_level")
            ModelInput("power")
            ModelInput("strength")
            ModelInput("speed")
            ModelInput("spirit")
            ModelInput("scar")

        # with Group("items", "角色物品", self.person, cols=4):
        #     for i in range(5):
        #         ModelSelect("items.%d.item" % i, "物品%d" % (i + 1), choices=datasets.ITEMS)
        #         ModelInput("items.%d.count" % i, "数量")


        # self.train_items_group = Group("train_items", "运输队", self._global, cols=4)
        # self.lazy_group(self.train_items_group, self.render_train_items)

    def render_train_items(self):
        datasets = self.datasets
        for i in range(10):
            ModelSelect("train_items.%d+train_items_offset.item" % i, "", choices=datasets.ITEMS)
            ModelInput("train_items.%d+train_items_offset.count" % i, "数量")
        with Group.active_group().footer:
            Pagination(self.on_train_items_page, self.TRAIN_ITEMS_PAGE_TOTAL)

    def get_hotkeys(self):
        this = self.weak
        return (
            ('continue_move', MOD_ALT, getVK('m'), this.continue_move),
            ('move_to_cursor', MOD_ALT, getVK('g'), this.move_to_cursor),
            ('move_left', MOD_ALT, getVK('left'), this.move_left),
            ('move_right', MOD_ALT, getVK('right'), this.move_right),
            ('move_up', MOD_ALT, getVK('up'), this.move_up),
            ('move_down', MOD_ALT, getVK('down'), this.move_down),
        )

    def on_person_change(self, lb):
        self.person.set_addr_by_index(lb.index)

    def _config(self):
        return self._global.config

    def on_item_change(self, lb):
        self.item_index = lb.index

    def _iteminfo(self):
        if self.item_index > 0:
            return self._global.iteminfos[self.item_index - 1]

    def copy_iteminfo(self, _=None):
        index = self.copy_iteminfo_view.index
        if index > 0:
            item_from = self._global.iteminfos[index - 1]
            self.handler.write(self._global.iteminfos.addr_at(self.item_index - 1), item_from.to_bytes())

    def continue_move(self, _=None):
        """再移动"""
        self.person.moved = False

    def move_to_cursor(self, _=None):
        person = self.person
        _global = self._global
        person.posx = _global.curx
        person.posy = _global.cury

    def move_left(self, _=None):
        self.person.posx -= 1

    def move_right(self, _=None):
        self.person.posx += 1

    def move_up(self, _=None):
        self.person.posy -= 1

    def move_down(self, _=None):
        self.person.posy += 1

    def on_train_items_page(self, page):
        self._global.train_items_offset = (page - 1) * self.TRAIN_ITEMS_PAGE_LENGTH
        self.train_items_group.read()