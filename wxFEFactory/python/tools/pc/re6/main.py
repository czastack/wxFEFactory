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
    CLASS_NAME = WINDOW_NAME = 'RESIDENT EVIL 6'

    def __init__(self):
        super().__init__()
        self.handler = MemHandler()
        self._global = models.Global(0, self.handler)
        self.ingame_item = models.IngameItem(0, self.handler)
        self.char_index = 0

    def render_main(self):
        person = (self._person, models.Character)
        with Group("player", "全局", self._global):
            # ModelInput("money", "金钱", instance=self.money)
            pass

        with Group("player", "角色", person):
            Choice("角色", datasets.PERSONS, self.weak.on_person_change)
            ModelInput("health")
            ModelInput("health_max")
            ModelInput("melee")
            ModelInput("melee_max")
            ModelInput("moving_speed")
            ModelInput("rapid_fire")
            ModelInput("is_wet")
            ModelCoordWidget("coord", labels=('X坐标', 'Z坐标', 'Y坐标'), savable=True)
            ModelCheckBox("invincible")

        self.lazy_group(Group("person_items", "角色物品", person, serializable=False, cols=4),
            self.render_person_items)
        # self.lazy_group(Group("saved_items", "整理界面物品", self.saved_items, serializable=False, cols=6),
        #     self.render_saved_items)
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_functions)
        self.lazy_group(StaticGroup("功能"), self.render_functions)

    def render_person_items(self):
        """游戏中物品"""
        for label, index_range in (('水平武器', (0, 7)), ('药丸', (7, 8)), ('垂直武器', (8, 13)), ('其他物品', (15, 24))):
            r = 1
            for i in range(*index_range):
                prop = "items.%d" % i
                select = ModelChoiceDisplay(prop + ".type", "%s%d" % (label, r),
                    choices=datasets.INVENTORY_ITEMS.choices, values=datasets.INVENTORY_ITEMS.values)
                with select.container:
                    ui.Button("详情", className="btn_sm", onclick=partial(__class__.show_ingame_item, self.weak,
                        instance=self._person, prop=prop))
                r += 1

    def render_saved_items(self):
        """整理界面个人物品"""
        for i in range(self.saved_items.items.length):
            prop = "items.%d" % i
            select = ModelChoiceDisplay(prop + ".type", "", choices=datasets.INVENTORY_ITEMS.choices,
                values=datasets.INVENTORY_ITEMS.values)
            with select.container:
                ui.Button("详情", className="btn_sm", onclick=partial(__class__.show_saved_item, self.weak,
                    instance=self.saved_items, prop=prop))

    def render_assembly_functions(self):
        NOP_7 = b'\x90' * 7
        NOP_8 = b'\x90' * 8
        NOP_9 = b'\x90' * 9
        functions = (
            # ('生命不减', ('hp_keep', b'\x66\x29\x8E\x64\x13\x00\x00', 0x700000, 0x800000, NOP_7, None, True)),
        )
        super().render_assembly_functions(functions)

    def render_functions(self):
        super().render_functions(('unlock_guns',))

    def get_ingame_item_dialog(self):
        """物品信息对话框"""
        name = 'ingame_item_dialog'
        dialog = getattr(self, name, None)
        if dialog is None:
            with DialogGroup(name, "物品详情", self.ingame_item, cols=1, dialog_style={'width': 600, 'height': 1400},
                    closable=False, horizontal=False, button=False) as dialog:
                ModelCheckBox("enabled")
                ModelSelect("type", choices=datasets.INVENTORY_ITEMS.choices, values=datasets.INVENTORY_ITEMS.values,
                    instance=self.ingame_item)
                ModelInput("quantity")
                ModelInput("max_quantity")

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
                    instance=self.saved_item).view.setToolTip('移动后生效')
                ModelInput("quantity")
                ModelInput("max_quantity")
                ModelInput("fire_power")
                ModelInput("reload_speed")
                ModelInput("capacity")
                ModelInput("piercing")
                ModelInput("scope")
                ModelInput("critical")
                ModelInput("attack_range")
                ModelInput("model", hex=True)

            setattr(self, name, dialog)
        return dialog

    def get_hotkeys(self):
        this = self.weak
        return (
            (VK.MOD_ALT, VK.H, this.pull_through),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK.H, this.pull_through_all),
            (VK.MOD_ALT, VK.R, this.set_ammo_full),
            (VK.MOD_ALT, VK.getCode(','), this.save_coord),
            (VK.MOD_ALT, VK.getCode('.'), this.load_coord),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK.getCode(','), this.undo_coord),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK.getCode('.'), this.reload_coord),
            (VK.MOD_ALT, VK.O, this.p1_go_p2),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK.O, this.p2_go_p1),
        )

    def onattach(self):
        self._global.addr = self.handler.base_addr

    def ondetach(self):
        memory = getattr(self, 'allocated_memory', None)
        if memory is not None:
            self.handler.free_memory(memory)
            self.allocated_memory = None
            self.next_usable_memory = None
            for key, value in self.registed_assembly.items():
                self.unregister_assembly_item(value)
            self.registed_assembly = []

    def _person(self):
        if self.handler.active:
            return self._global.character_struct.chars[self.char_index]

    person = property(_person)

    def on_person_change(self, lb):
        self.char_index = lb.index

    def show_ingame_item(self, view, ins, prop):
        """显示物品详情对话框"""
        item = getattr(ins, prop)
        if item and item.addr:
            self.ingame_item.addr = item.addr
            dialog = self.get_ingame_item_dialog()
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
        self.person.set_with('health', 'health_max')

    def pull_through_all(self, _=None):
        character_struct = self._global.character_struct
        for i in range(character_struct.chars_count):
            character_struct.chars[i].set_with('health', 'health_max')

    def set_ammo_full(self, _):
        person = self.person
        person.items[person.cur_item].set_with('quantity', 'max_quantity')

    def save_coord(self, _):
        self.last_coord = self.person.coord.values()

    def load_coord(self, _):
        person = self.person
        self.prev_coord = person.coord.values()
        person.coord = self.last_coord

    def undo_coord(self, _):
        self.person.coord = self.prev_coord

    def reload_coord(self, _):
        self.person.coord = self.last_coord

    def p1_go_p2(self, _):
        chars = self._global.character_struct.chars
        chars[0].coord = chars[1].coord.values()

    def p2_go_p1(self, _):
        chars = self._global.character_struct.chars
        chars[1].coord = chars[0].coord.values()

    def unlock_guns(self, _):
        """解锁横向武器"""
        config = self._global.character_config.chars[self.char_index]
        person = self.person
        for i in range(7):
            if config.weapon_ability[i]:
                person.items[i].enabled = True
