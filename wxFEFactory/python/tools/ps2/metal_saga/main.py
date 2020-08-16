import os
from lib import ui
from lib.hack.forms import (
    Group, StaticGroup, DialogGroup, ModelCheckBox, ModelInput, ModelSelect, ModelChoiceDisplay, Choice
)
from lib.ui.components import Pagination
from lib.win32.keys import VK
from lib.lazy import classlazy
from tools.base.utils import PresetDialog
from functools import partial
from lib.gba.dictionary import Dictionary
from ..base import BasePs2Hack
from . import models, datasets


class Main(BasePs2Hack):
    HUMEN_ITEMS_PAGE_LENGTH = 16
    HUMEN_ITEMS_PAGE_TOTAL = 4

    def __init__(self):
        super().__init__()
        self._global = models.Global(0, self.handler)
        self._global.human_items_offset = 0
        self.character = models.Character(0, self.handler)
        self.character_grow = models.CharacterGrow(0, self.handler)
        self.chariot = models.Chariot(0, self.handler)
        self.static_item = models.StaticItem(0, self.handler)
        self.item_info = models.ItemInfo(0, self.handler)
        self.enemy = models.Enemy(0, self.handler)
        self.item_preset_dialog = PresetDialog('物品', datasets.ITEM_HEADS, datasets.ITEMS_DATA, self.item_info)

    def render_main(self):
        character = self.character
        chariot = self.chariot
        with Group("global", "全局", self._global):
            ModelInput("money")
            ModelInput("battlein")
            ModelCheckBox("no_battle")
            ModelInput("battle_count")
            ModelInput("win_count")
            ModelInput("die_count")
            ModelInput("escape_count")

        self.lazy_group(Group("character", "角色", self.character, cols=4), self.render_character)
        self.lazy_group(Group("character_grow", "角色成长", self.character_grow, cols=4), self.render_character_grow)
        self.lazy_group(Group("character_equips", "角色装备", character), self.render_character_equips)
        self.human_items_group = Group("human_items", "人类道具", self._global, cols=4)
        self.lazy_group(self.human_items_group, self.render_human_items)
        self.lazy_group(Group("chariot", "战车", chariot, cols=4), self.render_chariot)
        self.lazy_group(Group("special_bullets", "特殊炮弹", chariot, cols=4), self.render_special_bullets)
        # self.lazy_group(Group("wanted", "赏金首", self._global, cols=4), self.render_wanted)
        self.lazy_group(StaticGroup("功能"), self.render_buttons_own)

        with StaticGroup("快捷键"):
            ui.Text("左移(目标战车坐标): alt+left\n"
                "右移: alt+right\n"
                "上移: alt+up\n"
                "下移: alt+right\n"
                "恢复HP: alt+h")

    def render_character(self):
        Choice("角色", datasets.PERSONS, self.on_character_change)
        ModelInput("level")
        ModelInput("exp")
        ModelInput("hpmax")
        ModelInput("hp")
        ModelInput("atk")
        ModelInput("defense")
        ModelInput("drive")
        ModelInput("title")
        ModelSelect("prof", choices=datasets.PROFS)
        # ModelInput("status")
        with ModelSelect.choices_cache:
            for i in range(self.character.skills.length):
                ModelSelect("skills.%d" % i, "技能%d" % (i + 1),
                    choices=datasets.SPECIAL_SKILLS.choices, values=datasets.SPECIAL_SKILLS.values)

    def render_character_grow(self):
        ModelInput("hp_init")
        ModelInput("hp_grow")
        ModelInput("atk_init")
        ModelInput("atk_grow")
        ModelInput("def_init")
        ModelInput("def_grow")
        ModelInput("drive_init")
        ModelInput("drive_grow")

    def render_character_equips(self):
        for i, label in enumerate(('武器', '头部', '躯干', '手臂', '脚部', '胸甲')):
            prop = "equips.%d" % i
            select = ModelChoiceDisplay(prop + ".item", label, choices=datasets.ALL_EQUIP.choices,
                values=datasets.ALL_EQUIP.values)
            with select.container:
                ui.Button("详情", class_="btn_sm", onclick=partial(self.__class__.show_item_info, self.weak,
                    instance=self.character, prop=prop))
                ui.Button("选择", class_="btn_sm", onclick=partial(self.__class__.show_item_preset, self.weak,
                    instance=self.character, prop=prop))

    def render_human_items(self):
        for i in range(self.HUMEN_ITEMS_PAGE_LENGTH):
            prop = "items.%d+human_items_offset" % i
            select = ModelChoiceDisplay(prop + ".item", "物品%d" % (i + 1),
                choices=datasets.ALL_HUMEN_ITEM.choices, values=datasets.ALL_HUMEN_ITEM.values)
            with select.container:
                ui.Button("详情", class_="btn_sm", onclick=partial(self.__class__.show_item_info, self.weak,
                    instance=self._global, prop=prop))
                ui.Button("选择", class_="btn_sm", onclick=partial(self.__class__.show_item_preset, self.weak,
                    instance=self._global, prop=prop))
        with Group.active_group().footer:
            Pagination(self.on_human_items_page, self.HUMEN_ITEMS_PAGE_TOTAL)

    def on_human_items_page(self, page):
        self._global.human_items_offset = (page - 1) * self.HUMEN_ITEMS_PAGE_LENGTH
        self.human_items_group.read()

    def render_chariot(self):
        Choice("战车", datasets.CHARIOTS, self.on_chariot_change)
        ModelInput("sp")

        # with ModelSelect.choices_cache:
        #     for i in range(self.chariot.hole_type.length):
        #         ModelSelect("hole_type.%d" % i, "炮穴%d类型" % (i + 1),
        #             choices=datasets.HOLE_TYPES, values=datasets.HOLE_TYPE_VALUES)

        # ModelInput("position", hex=True)

        for i in range(self.chariot.equips.length):
            prop = "equips.%d" % i
            select = ModelChoiceDisplay(prop + ".item", "物品%d" % (i + 1),
                choices=datasets.CHARIOT_ALL_ITEM.choices, values=datasets.CHARIOT_ALL_ITEM.values)
            with select.container:
                ui.Button("详情", class_="btn_sm", onclick=partial(self.__class__.show_item_info, self.weak,
                    instance=self.chariot, prop=prop))
                ui.Button("选择", class_="btn_sm", onclick=partial(self.__class__.show_item_preset, self.weak,
                    instance=self.chariot, prop=prop))

    def render_special_bullets(self):
        for i in range(self.chariot.special_bullets.length):
            prop = "special_bullets.%d" % i
            select = ModelChoiceDisplay(prop + ".item", "特殊炮弹%d" % (i + 1),
                choices=datasets.SPECIAL_BULLETS.choices, values=datasets.SPECIAL_BULLETS.values)
            with select.container:
                ui.Button("详情", class_="btn_sm", onclick=partial(self.__class__.show_item_info, self.weak,
                    instance=self.chariot, prop=prop))
                ui.Button("选择", class_="btn_sm", onclick=partial(self.__class__.show_item_preset, self.weak,
                    instance=self.chariot, prop=prop))

    def render_wanted(self):
        with ModelSelect.choices_cache:
            for i, name in enumerate(datasets.WANTED_LIST):
                ModelSelect("wanted_status.%d" % i, name, choices=datasets.WANTED_STATUS,
                    values=datasets.WANTED_STATUS_VALUES)

    def render_buttons_own(self):
        self.render_buttons(('fake_down',))

    def get_hotkeys(self):
        this = self.weak
        return (
            # (VK.MOD_ALT, VK.LEFT, this.move_left),
            # (VK.MOD_ALT, VK.RIGHT, this.move_right),
            # (VK.MOD_ALT, VK.UP, this.move_up),
            # (VK.MOD_ALT, VK.DOWN, this.move_down),
            (VK.MOD_ALT, VK.H, this.pull_through),
        )

    @classlazy
    def dictionary(self):
        return Dictionary(os.path.join(os.path.dirname(__file__), 'dict.txt'), low_range=(0x81, 0x98), use_ascii=True)

    def get_item_info_dialog(self):
        """物品信息对话框"""
        name = 'item_info_dialog'
        dialog = getattr(self, name, None)
        if dialog is None:
            with DialogGroup(name, "物品详情", self.item_info, cols=1, dialog_style={'width': 600, 'height': 1200},
                    closable=False, horizontal=False, button=False) as dialog:
                ModelChoiceDisplay("item", choices=datasets.ITEMS, instance=self.item_info)
                ModelInput("attr1")
                ModelInput("status")
                ModelInput("atk_addition")
                ModelInput("str_addition")
                ui.Button("种类详情", onclick=self.show_static_item)

            setattr(self, name, dialog)
        return dialog

    def get_static_item_dialog(self):
        """静态物品对话框"""
        name = 'static_item_dialog'
        dialog = getattr(self, name, None)
        if dialog is None:
            with DialogGroup(None, "静态物品", self.static_item, cols=1, dialog_style={'width': 600, 'height': 1200},
                    closable=False, horizontal=False, button=False) as dialog:
                ModelChoiceDisplay("item", choices=datasets.ITEMS, instance=self.item_info)
                ModelInput("weight")
                ModelInput("load")
                ModelInput("atk")
                ModelInput("defense")
                ModelInput("strength")

            setattr(self, name, dialog)
        return dialog

    def show_item_info(self, view, instance, prop):
        """显示物品详情对话框"""
        item = getattr(instance, prop)
        if item and item.addr:
            self.item_info.addr = item.addr
            dialog = self.get_item_info_dialog()
            if self.handler.active:
                dialog.read()
            dialog.show()
        else:
            print("没有数据")

    def show_static_item(self, view):
        """显示静态物品对话框"""
        if self.item_info.addr:
            index = self.item_info.item
            item = self._global.static_items[index - 1]
            self.static_item.addr = item.addr
            dialog = self.get_static_item_dialog()
            if self.handler.active:
                dialog.read()
            dialog.show()

    def show_item_preset(self, view, instance, prop):
        """显示预设对话框"""
        item = getattr(instance, prop)
        if item and item.addr:
            self.item_info.addr = item.addr
            self.item_preset_dialog.show(self.item_info.item)
        else:
            print("没有数据")

    def on_character_change(self, lb):
        index = lb.index
        self.character.set_addr_by_index(index)
        self.character_grow.set_addr_by_index(index)

    def on_chariot_change(self, lb):
        self.chariot.set_addr_by_index(lb.index)

    def characters(self):
        character = models.Character(0, self.handler)
        for i in range(len(datasets.PERSONS)):
            character.set_addr_by_index(i)
            yield character

    def chariots(self):
        chariot = models.Chariot(0, self.handler)
        for i in range(len(datasets.CHARIOTS)):
            chariot.set_addr_by_index(i)
            yield chariot

    # def move_left(self):
    #     self.chariot.posx -= 24

    # def move_right(self):
    #     self.chariot.posx += 24

    # def move_up(self):
    #     self.chariot.posy -= 24

    # def move_down(self):
    #     self.chariot.posy += 24

    def pull_through(self):
        for character in self.characters():
            character.hp = character.hpmax

    def equip_all(self):
        self.character.equip_all()

    def fake_down(self):
        """假装下车"""
        flag = getattr(self, '_fake_downed', False)
        if not flag:
            i = 0
            indexs = []
            for character in self._global.characters:
                if i > 5:
                    break
                if character.driving == 1:
                    indexs.append(i)
                    character.driving = 0
                    if len(indexs) == 3:
                        break
                i += 1
            self._fake_downed = True
            self._fake_downed_indexs = indexs
        else:
            for i in self._fake_downed_indexs:
                self._global.characters[i].driving = 1
            self._fake_downed = False
