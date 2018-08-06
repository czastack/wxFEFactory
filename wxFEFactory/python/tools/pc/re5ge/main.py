from functools import partial
from lib.hack.forms import (
    Group, StaticGroup, DialogGroup, ModelCheckBox, ModelInput, ModelSelect, Choice, ModelCoordWidget,
    ModelChoiceDisplay
)
from lib.hack.handlers import MemHandler
from lib.win32.keys import VK
from tools.assembly_hacktool import AssemblyHacktool
from fefactory_api import ui
from . import models, datasets


class Main(AssemblyHacktool):
    CLASS_NAME = 'MTFramework'
    WINDOW_NAME = 'RESIDENT EVIL 5'

    def __init__(self):
        super().__init__()
        self.handler = MemHandler()
        self._global = models.Global(0, self.handler)
        self.character_struct = models.CharacterStruct(0, self.handler)
        self.person = models.Player(0, self.handler)
        self.slot_item = models.SlotItem(0, self.handler)
        self.saved_item = models.SavedItem(0, self.handler)
        self.saved_items = models.SavedItemHolder(0, self.handler)
        self.money = models.Money(0, self.handler)

    def render_top_button(self):
        ui.Button("读取地址", className="vcenter", onclick=self.reload_address)

    def render_main(self):
        with Group("player", "全局", self._global):
            ModelInput("money", "金钱", ins=self.money)

        with Group("player", "角色", self.person):
            self.person_select = Choice("角色", tuple("play%d" % i for i in range(1, 5)), self.weak.on_person_change)
            ModelInput("hp")
            ModelInput("hpmax")
            ModelCoordWidget("moving_coord", savable=True)
            ModelCoordWidget("melee_coord", savable=True)
            ModelInput("target")
            ModelCheckBox("invincible")

        self.lazy_group(Group("person_items", "角色物品", self.person, cols=4), self.render_person_items)
        self.lazy_group(Group("saved_items", "整理界面物品", self.saved_items, cols=6), self.render_saved_items)
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_functions)

    def render_person_items(self):
        for i in range(self.person.slot_items.length):
            prop = "slot_items.%d" % i
            select = ModelChoiceDisplay(prop + ".type", "物品%d" % (i + 1), choices=datasets.INVENTORY_ITEMS.choices,
                values=datasets.INVENTORY_ITEMS.values)
            with select.container:
                ui.Button("详情", className="btn_sm", onclick=partial(__class__.show_slot_item, self.weak,
                    ins=self.person, prop=prop))

    def render_saved_items(self):
        for i in range(self.saved_items.items.length):
            prop = "items.%d" % i
            select = ModelChoiceDisplay(prop + ".type", "", choices=datasets.INVENTORY_ITEMS.choices,
                values=datasets.INVENTORY_ITEMS.values)
            with select.container:
                ui.Button("详情", className="btn_sm", onclick=partial(__class__.show_saved_item, self.weak,
                    ins=self.saved_items, prop=prop))

    def render_assembly_functions(self):
        functions = (
            ('无限弹药', ('infinity_ammo', b'\x8B\x57\x08\x57\x8B\xCB', 0x500000, 0x700000,
                b'', b'\xD9\x47\x0C\xD9\x5F\x08\x8B\x57\x08\x57\x8B\xCB', True, True)),
            ('弹药不减', ('ammo_keep', b'\x2B\x44\x24\x08\x89\x41\x08', 0x84B8FB, 0x900000,
                b'\x90' * 7, None, True)),
            ('快速发射', ('fast_shoot', b'\xF3\x0F\x58\x46\x20\x0F\xB6', 0x800000, 0x900000,
                b'', b'\xC7\x46\x20\x00\x00\xC8\x42\xF3\x0F\x58\x46\x20', True, True, True)),
        )
        super().render_assembly_functions(functions, cols=6)

    def get_slot_item_dialog(self):
        """物品信息对话框"""
        name = 'slot_item_dialog'
        dialog = getattr(self, name, None)
        if dialog is None:
            with DialogGroup(name, "物品详情", self.slot_item, cols=1, dialog_style={'width': 600, 'height': 1200},
                    closable=False, horizontal=False, button=False) as dialog:
                ModelSelect("type", choices=datasets.INVENTORY_ITEMS.choices, values=datasets.INVENTORY_ITEMS.values,
                    ins=self.slot_item)
                ModelInput("quantity")
                ModelInput("max_quantity")
                ModelInput("fire_power")
                ModelInput("reload_speed")
                ModelInput("capacity")
                ModelInput("piercing")
                ModelInput("critical")
                ModelInput("scope")
                ModelInput("attack_range")

            setattr(self, name, dialog)
        return dialog

    def get_saved_item_dialog(self):
        """整理界面物品信息对话框"""
        name = 'saved_item_dialog'
        dialog = getattr(self, name, None)
        if dialog is None:
            with DialogGroup(name, "物品详情", self.saved_item, cols=1, dialog_style={'width': 600, 'height': 1400},
                    closable=False, horizontal=False, button=False) as dialog:
                ModelSelect("type", choices=datasets.INVENTORY_ITEMS.choices, values=datasets.INVENTORY_ITEMS.values,
                    ins=self.saved_item).view.setToolTip('移动后生效')
                ModelInput("quantity")
                ModelInput("max_quantity")
                ModelInput("fire_power")
                ModelInput("reload_speed")
                ModelInput("capacity")
                ModelInput("piercing")
                ModelInput("scope")
                ModelInput("critical")
                ModelInput("attack_range")

            setattr(self, name, dialog)
        return dialog

    def get_hotkeys(self):
        this = self.weak
        return (
            (VK.MOD_ALT, VK.H, this.pull_through),
            (VK.MOD_ALT, VK.R, this.reload_address),
        )

    def onattach(self):
        proc_base = self.handler.proc_base
        self.character_struct.addr = self.handler.read_ptr(proc_base + 0x00DA2A5C)
        self.money.addr = self.handler.read_ptr(proc_base + 0x00DA23D8)
        self.switch_person(self.person_select.index)

    def ondetach(self):
        memory = getattr(self, 'allocated_memory', None)
        if memory is not None:
            self.handler.free_memory(memory)
            self.allocated_memory = None
            self.next_usable_memory = None
            for key, value in self.registed_assembly.items():
                self.unregister_assembly_item(value)
            self.registed_assembly = []

    def on_person_change(self, lb):
        self.switch_person(lb.index)

    def switch_person(self, index):
        self.person.addr = self.character_struct.players[index].addr
        self.saved_items.addr = self.character_struct.saved_items[index].addr

    def show_slot_item(self, view, ins, prop):
        """显示物品详情对话框"""
        item = getattr(ins, prop)
        if item and item.addr:
            self.slot_item.addr = item.addr
            dialog = self.get_slot_item_dialog()
            dialog.read()
            dialog.show()
        else:
            print("没有数据")

    def show_saved_item(self, view, ins, prop):
        """显示整理界面物品详情对话框"""
        item = getattr(ins, prop)
        if item and item.addr:
            self.saved_item.addr = item.addr
            dialog = self.get_saved_item_dialog()
            dialog.read()
            dialog.show()
        else:
            print("没有数据")

    def pull_through(self, _=None):
        for i in range(self.character_struct.players_count):
            self.character_struct.players[i].set_with('hp', 'hpmax')

    def reload_address(self, _):
        self.onattach()
