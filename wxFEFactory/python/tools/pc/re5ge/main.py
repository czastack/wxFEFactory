from functools import partial
from lib.hack.forms import (
    Group, DialogGroup, ModelCheckBox, ModelInput, ModelSelect, Choice, ModelCoordWidget, ModelChoiceDisplay
)
from lib.hack.handlers import MemHandler
from lib.win32.keys import VK
from tools.hacktool import BaseHackTool
from fefactory_api import ui
from . import models, datasets


class Main(BaseHackTool):
    CLASS_NAME = 'MTFramework'
    WINDOW_NAME = 'RESIDENT EVIL 5'

    def __init__(self):
        super().__init__()
        self.handler = MemHandler()
        self._global = models.Global(0, self.handler)
        self.character_struct = models.CharacterStruct(0, self.handler)
        self.person = models.Player(0, self.handler)
        self.slot_item = models.SlotItem(0, self.handler)
        self.money = models.Money(0, self.handler)

    def render_main(self):
        with Group("player", "全局", self._global):
            ModelInput("money", "金钱", ins=self.money)

        with Group("player", "角色", self.person):
            Choice("角色", tuple("play%d" % i for i in range(1, 5)), self.on_person_change)
            ModelInput("hp")
            ModelInput("hpmax")
            ModelCoordWidget("moving_coord", savable=True)
            ModelCoordWidget("melee_coord", savable=True)
            ModelInput("target")
            ModelCheckBox("invincible")

        self.lazy_group(Group("person_items", "角色物品", self.person, cols=4), self.render_person_items)

    def render_person_items(self):
        for i in range(self.person.slot_items.length):
            prop = "slot_items.%d" % i
            select = ModelChoiceDisplay(prop + ".type", "物品%d" % (i + 1), choices=datasets.INVENTORY_ITEMS.choices,
                values=datasets.INVENTORY_ITEMS.values)
            with select.container:
                ui.Button("详情", className="btn_sm", onclick=partial(__class__.show_slot_item, self.weak,
                    ins=self.person, prop=prop))

    def get_slot_item_dialog(self):
        """物品信息对话框"""
        name = 'slot_item_dialog'
        dialog = getattr(self, name, None)
        if dialog is None:
            with DialogGroup(name, "物品详情", self.slot_item, cols=1, dialog_style={'width': 600, 'height': 1200},
                    closable=False, horizontal=False, button=False) as dialog:
                ModelSelect("type", choices=datasets.INVENTORY_ITEMS.choices, values=datasets.INVENTORY_ITEMS.values,
                    ins=self.slot_item)
                ModelInput("ammo")
                ModelInput("ammo_max")
                ModelInput("slot")

            setattr(self, name, dialog)
        return dialog

    def get_hotkeys(self):
        this = self.weak
        return (
            (VK.MOD_ALT, VK.H, this.pull_through),
        )

    def onattach(self):
        proc_base = self.handler.proc_base
        # self.health_check = self.handler.find_bytes(b'\x66\x83\xB9\x64\x13\x00\x00\x00\x0F\x9E\xC0\xC3',
        #     proc_base + 0x00700000, proc_base + 0x00800000)
        # print(hex(self.health_check))
        self.character_struct.addr = self.handler.read_ptr(proc_base + 0x00DA2A5C)
        self.money.addr = self.handler.read_ptr(proc_base + 0x00DA23D8)
        self.person.addr = self.character_struct.players[0].addr

    def on_person_change(self, lb):
        self.person.addr = self.character_struct.players[lb.index].addr

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

    def pull_through(self, _=None):
        for i in range(self.character_struct.players_count):
            self.character_struct.players[i].set_with('hp', 'hpmax')
