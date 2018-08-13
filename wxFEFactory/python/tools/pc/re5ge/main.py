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
        self.ingame_item = models.IngameItem(0, self.handler)
        self.saved_item = models.SavedItem(0, self.handler)
        # self.inventory_treasure_item = models.InventoryTreasureItem(0, self.handler)
        self.char_index = self._global.char_index = 0

    def render_main(self):
        person = (self._person, models.Character)

        with Group("player", "全局", self._global):
            ModelInput("money.money", "金钱")

        with Group("player", "角色", person):
            Choice("角色", tuple("play%d" % i for i in range(1, 5)), self.weak.on_person_change)
            ModelInput("health")
            ModelInput("health_max")
            ModelCoordWidget("coord", labels=('X坐标', 'Z坐标', 'Y坐标'), savable=True)
            ModelCheckBox("invincible")

        self.lazy_group(Group("person_items", "角色物品", person, serializable=False, cols=4),
            self.render_person_items)
        self.lazy_group(Group("saved_items", "整理界面物品", self._saved_items, serializable=False, cols=6),
            self.render_saved_items)
        # self.lazy_group(StaticGroup("物品箱/宝物箱"), self.render_inventory_treasure_items)
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_functions)

    def render_person_items(self):
        """游戏中物品"""
        for i in range(models.Character.items.length):
            prop = "items.%d" % i
            select = ModelChoiceDisplay(prop + ".type", "物品%d" % (i + 1), choices=datasets.INVENTORY_ITEMS.choices,
                values=datasets.INVENTORY_ITEMS.values)
            with select.container:
                ui.Button("详情", className="btn_sm", onclick=partial(__class__.show_ingame_item, self.weak,
                    instance=self._person, prop=prop))

    def render_saved_items(self):
        """整理界面个人物品"""
        for i in range(models.SavedItemHolder.items.length):
            prop = "items.%d" % i
            select = ModelChoiceDisplay(prop + ".type", "", choices=datasets.INVENTORY_ITEMS.choices,
                values=datasets.INVENTORY_ITEMS.values)
            with select.container:
                ui.Button("详情", className="btn_sm", onclick=partial(__class__.show_saved_item, self.weak,
                    instance=self._saved_items, prop=prop))

    # def render_inventory_treasure_items(self):
    #     """仓库中的物品"""
    #     with ui.Notebook(className="fill") as book:
    #         for label, key in (('物品箱', 'inventory_items'), ('宝物箱', 'treasure_items')):
    #             with Group(None, label, self._gloabl.character_struct, cols=6):
    #                 for i in range(54):
    #                     prop = "inventory_treasure_holder.%s.%d" % (key, i)
    #                     select = ModelChoiceDisplay(prop + ".type", "",
    #                         choices=datasets.INVENTORY_TREASURE_ITEMS.choices,
    #                         values=datasets.INVENTORY_TREASURE_ITEMS.values)
    #                     with select.container:
    #                         ui.Button("详情", className="btn_sm",
    #                             onclick=partial(__class__.show_inventory_treasure_item, self.weak,
    #                                 instance=self._gloabl.character_struct, prop=prop))

    def render_assembly_functions(self):
        NOP_7 = b'\x90' * 7
        NOP_8 = b'\x90' * 8
        NOP_9 = b'\x90' * 9
        functions = (
            ('生命不减', ('hp_keep', b'\x66\x29\x8E\x64\x13\x00\x00', 0x700000, 0x800000, NOP_7, None, True)),
            ('弹药不减', ('ammo_keep', b'\x2B\x44\x24\x08\x89\x41\x08', 0x800000, 0x900000, NOP_7, None, True)),
            ('无限弹药', ('infinity_ammo', b'\x8B\x57\x08\x57\x8B\xCB', 0x500000, 0x700000,
                b'', b'\xD9\x47\x0C\xD9\x5F\x08\x8B\x57\x08\x57\x8B\xCB', True, True)),
            ('快速发射', ('fast_shoot', b'\xF3\x0F\x58\x46\x20\x0F\xB6', 0x800000, 0x900000,
                b'', b'\xC7\x46\x20\x00\x00\xC8\x42\xF3\x0F\x58\x46\x20', True, True, True)),
            ('佣兵模式时间不减', ('merce_timer_keep', b'\xF3\x0F\x11\x87\xDC\x04\x00\x00', 0x300000, 0x400000,
                NOP_8, None, True)),
            ('连击时间不减', ('combo_timer_keep', b'\xF3\x0F\x11\x84\x31\xA0\x06\x00\x00\x5F', 0x300000, 0x400000,
                NOP_9, None, True)),
        )
        super().render_assembly_functions(functions)

    def get_ingame_item_dialog(self):
        """物品信息对话框"""
        name = 'ingame_item_dialog'
        dialog = getattr(self, name, None)
        if dialog is None:
            with DialogGroup(name, "物品详情", self.ingame_item, cols=1, dialog_style={'width': 600, 'height': 1400},
                    closable=False, horizontal=False, button=False) as dialog:
                ModelSelect("type", choices=datasets.INVENTORY_ITEMS.choices, values=datasets.INVENTORY_ITEMS.values,
                    instance=self.ingame_item)
                ModelInput("quantity")
                ModelInput("max_quantity")
                ModelInput("fire_power")
                ModelInput("reload_speed")
                ModelInput("capacity")
                ModelInput("piercing")
                ModelInput("critical")
                ModelInput("scope")
                ModelInput("attack_range")
                ModelInput("model", hex=True)

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

    # def get_inventory_treasure_item_dialog(self):
    #     """仓库物品信息对话框"""
    #     name = 'inventory_treasure_item_dialog'
    #     dialog = getattr(self, name, None)
    #     if dialog is None:
    #         with DialogGroup(name, "物品详情", self.inventory_treasure_item, cols=1,
    #                 dialog_style={'width': 600, 'height': 1400},
    #                 closable=False, horizontal=False, button=False) as dialog:
    #             ModelSelect("type", choices=datasets.INVENTORY_TREASURE_ITEMS.choices,
    #                 values=datasets.INVENTORY_TREASURE_ITEMS.values,
    #                 instance=self.inventory_treasure_item).view.setToolTip('移动后生效')
    #             ModelInput("quantity")

    #         setattr(self, name, dialog)
    #     return dialog

    def get_hotkeys(self):
        this = self.weak
        return (
            (VK.MOD_ALT, VK.H, this.pull_through),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK.H, this.pull_through_all),
            (VK.MOD_ALT, VK.getCode(','), this.save_coord),
            (VK.MOD_ALT, VK.getCode('.'), this.load_coord),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK.getCode(','), this.undo_coord),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK.getCode('.'), this.reload_coord),
            (VK.MOD_ALT, VK.O, this.p1_go_p2),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK.O, this.p2_go_p1),
        )

    def onattach(self):
        super().onattach()
        self._global.addr = self.handler.base_addr

    def _person(self):
        if self.handler.active:
            return self._global.character_struct.chars[self.char_index]

    def _saved_items(self):
        if self.handler.active:
            return self._global.character_struct.saved_items[self.char_index]

    person = property(_person)
    saved_items = property(_saved_items)

    def on_person_change(self, lb):
        self.char_index = self._global.char_index = lb.index

    def show_ingame_item(self, view, instance, prop):
        """显示物品详情对话框"""
        item = getattr(instance, prop)
        if item and item.addr:
            self.ingame_item.addr = item.addr
            dialog = self.get_ingame_item_dialog()
            dialog.read()
            dialog.show()
        else:
            print("没有数据")

    def show_saved_item(self, view, instance, prop):
        """显示整理界面物品详情对话框"""
        if callable(instance):
            instance = instance()
        item = getattr(instance, prop)
        if item and item.addr:
            self.saved_item.addr = item.addr
            dialog = self.get_saved_item_dialog()
            dialog.read()
            dialog.show()
        else:
            print("没有数据")

    # def show_inventory_treasure_item(self, view, instance, prop):
    #     """显示整理界面物品详情对话框"""
    #     item = getattr(instance, prop)
    #     if item and item.addr:
    #         self.inventory_treasure_item.addr = item.addr
    #         dialog = self.get_inventory_treasure_item_dialog()
    #         dialog.read()
    #         dialog.show()
    #     else:
    #         print("没有数据")

    def pull_through(self, _=None):
        self.person.set_with('health', 'health_max')

    def pull_through_all(self, _=None):
        character_struct = self._global.character_struct
        for i in range(character_struct.chars_count):
            character_struct.chars[i].set_with('health', 'health_max')

    def save_coord(self, _):
        self.last_coord = self.person.coord.values()

    def load_coord(self, _):
        self.prev_coord = self.person.coord.values()
        self.person.coord = self.last_coord

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
