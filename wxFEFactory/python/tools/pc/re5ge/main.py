from functools import partial
from lib.hack.forms import (
    Group, StaticGroup, DialogGroup, ModelCheckBox, ModelInput, ModelSelect, Choice, ModelCoordWidget,
    ModelChoiceDisplay
)
from lib.hack.handlers import MemHandler
from lib.win32.keys import VK
from lib import ui
from tools.base.native_hacktool import NativeHacktool, AssemblyItem, Delta
from . import models, datasets


class Main(NativeHacktool):
    CLASS_NAME = 'MTFramework'
    WINDOW_NAME = 'RESIDENT EVIL 5'

    def __init__(self):
        super().__init__()
        self.handler = MemHandler()
        self._global = models.Global(0, self.handler)
        self.ingame_item = models.IngameItem(0, self.handler)
        self.saved_item = models.SavedItem(0, self.handler)
        self.inventory_treasure_item = models.InventoryTreasureItem(0, self.handler)
        self.char_index = self._global.char_index = 0

    def render_main(self):
        person = (self._person, models.Character)

        with Group("player", "全局", self._global):
            ModelInput("money.money", "金钱")

        with Group("player", "角色", person):
            self.render_player()

        self.lazy_group(Group("person_items", "角色物品", person, serializable=False, cols=4),
            self.render_person_items)
        self.lazy_group(Group("saved_items", "整理界面物品", self._saved_items, serializable=False, cols=4),
            self.render_saved_items)
        self.lazy_group(StaticGroup("物品箱/宝物箱"), self.render_inventory_treasure_items)
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_buttons_own)

    def render_player(self):
        Choice("角色", tuple("play%d" % i for i in range(1, 5)), self.weak.on_person_change)
        ModelInput("health")
        ModelInput("health_max")
        ModelCoordWidget("coord", labels=('X坐标', 'Z坐标', 'Y坐标'), savable=True)
        ModelCheckBox("invincible")

    def render_person_items(self):
        """游戏中物品"""
        for i in range(models.Character.items.length):
            prop = "items.%d" % i
            select = ModelChoiceDisplay(prop + ".type", "物品%d" % (i + 1), choices=datasets.INVENTORY_ITEMS.choices,
                values=datasets.INVENTORY_ITEMS.values)
            with select.container:
                ui.Button("详情", class_="btn_sm", onclick=partial(__class__.show_ingame_item, self.weak,
                    instance=self._person, prop=prop))

    def render_saved_items(self):
        """整理界面个人物品"""
        for i in range(models.SavedItemHolder.items.length):
            prop = "items.%d" % i
            select = ModelChoiceDisplay(
                prop + ".type", "", choices=datasets.INVENTORY_ITEMS.choices, values=datasets.INVENTORY_ITEMS.values)
            with select.container:
                ui.Button("详情", class_="btn_sm", onclick=partial(
                    __class__.show_saved_item, self.weak, instance=self._saved_items, prop=prop))

    def render_inventory_treasure_items(self):
        """仓库中的物品"""
        with ui.Notebook(class_="fill") as book:
            for label, key in (('物品箱', 'inventory_items'), ('宝物箱', 'treasure_items')):
                with Group(None, label, self._global, cols=4):
                    for i in range(54):
                        prop = "inventory_treasure_holder.%s.%d" % (key, i)
                        select = ModelChoiceDisplay(prop + ".type", "",
                            choices=datasets.INVENTORY_TREASURE_ITEMS.choices,
                            values=datasets.INVENTORY_TREASURE_ITEMS.values)
                        with select.container:
                            ui.Button("详情", class_="btn_sm",
                                onclick=partial(__class__.show_inventory_treasure_item, self.weak,
                                    instance=self._global.character_struct, prop=prop))

    def render_assembly_buttons_own(self):
        nop_7 = b'\x90' * 7
        nop_8 = b'\x90' * 8
        nop_9 = b'\x90' * 9
        delta = Delta(0x200000)
        self.render_assembly_buttons((
            AssemblyItem('hp_keep', '生命不减', b'\x66\x29\x8E\x64\x13\x00\x00', 0x700000, delta, nop_7),
            AssemblyItem('ammo_keep', '弹药不减', b'\x2B\x44\x24\x08\x89\x41\x08', 0x800000, delta, nop_7),
            AssemblyItem('grenade_keep', '手雷不减', b'\x8B\x46\x08\x83\xE8\x01\x89\x44\x24\x14',
                         0x300000, delta, b'\x90\x90\x90', replace_len=3, replace_offset=3),
            AssemblyItem('infinity_ammo', '无限弹药', b'\x8B\x57\x08\x57\x8B\xCB', 0x500000, delta,
                         b'', b'\xD9\x47\x0C\xD9\x5F\x08\x8B\x57\x08\x57\x8B\xCB', inserted=True),
            AssemblyItem('fast_shoot', '快速射击', b'\xF3\x0F\x58\x46\x20\x0F\xB6', 0x800000, delta,
                         b'', b'\xC7\x46\x20\x00\x00\xC8\x42\xF3\x0F\x58\x46\x20', inserted=True, replace_len=5),
            AssemblyItem('no_hot', '武器不会过热', b'\xF3\x0F\x58\x86\x68\x1C\x00\x00', 0x700000, delta,
                         b'', b'\x0F\x57\xC0\xF3\x0F\x11\x86\x68\x1C\x00\x00', inserted=True),
            AssemblyItem('merce_timer_keep', '佣兵模式时间不减', b'\xF3\x0F\x11\x87\xDC\x04\x00\x00',
                         0x300000, delta, nop_8),
            AssemblyItem('combo_timer_keep', '连击时间不减', b'\xF3\x0F\x11\x84\x31\xA0\x06\x00\x00\x5F',
                         0x300000, delta, nop_9),
        ))

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
                    instance=self.saved_item).set_help('移动后生效')
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

    def get_inventory_treasure_item_dialog(self):
        """仓库物品信息对话框"""
        name = 'inventory_treasure_item_dialog'
        dialog = getattr(self, name, None)
        if dialog is None:
            with DialogGroup(name, "物品详情", self.inventory_treasure_item, cols=1,
                    dialog_style={'width': 600, 'height': 1400},
                    closable=False, horizontal=False, button=False) as dialog:
                ModelSelect("type", choices=datasets.INVENTORY_TREASURE_ITEMS.choices,
                    values=datasets.INVENTORY_TREASURE_ITEMS.values,
                    instance=self.inventory_treasure_item).set_help('移动后生效')
                ModelInput("quantity")

            setattr(self, name, dialog)
        return dialog

    def get_hotkeys(self):
        this = self.weak
        return (
            (VK.MOD_ALT, VK.H, this.pull_through),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK.H, this.pull_through_all),
            (VK.MOD_ALT, VK(','), this.save_coord),
            (VK.MOD_ALT, VK('.'), this.load_coord),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK(','), this.undo_coord),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK('.'), this.reload_coord),
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
        if callable(instance):
            instance = instance()
        item = getattr(instance, prop)
        if item and item.addr:
            self.ingame_item.addr = item.addr
            dialog = self.get_ingame_item_dialog()
            if self.handler.active:
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
            if self.handler.active:
                dialog.read()
            dialog.show()
        else:
            print("没有数据")

    def show_inventory_treasure_item(self, view, instance, prop):
        """显示整理界面物品详情对话框"""
        if callable(instance):
            instance = instance()
        item = getattr(instance, prop)
        if item and item.addr:
            self.inventory_treasure_item.addr = item.addr
            dialog = self.get_inventory_treasure_item_dialog()
            dialog.read()
            dialog.show()
        else:
            print("没有数据")

    def pull_through(self):
        self.person.set_with('health', 'health_max')

    def pull_through_all(self):
        character_struct = self._global.character_struct
        for i in range(character_struct.chars_count):
            character_struct.chars[i].set_with('health', 'health_max')

    def save_coord(self):
        self.last_coord = self.person.coord.values()

    def load_coord(self):
        self.prev_coord = self.person.coord.values()
        self.person.coord = self.last_coord

    def undo_coord(self):
        self.person.coord = self.prev_coord

    def reload_coord(self):
        self.person.coord = self.last_coord

    def p1_go_p2(self):
        chars = self._global.character_struct.chars
        chars[0].coord = chars[1].coord.values()

    def p2_go_p1(self):
        chars = self._global.character_struct.chars
        chars[1].coord = chars[0].coord.values()

    def set_ingame_item(self, type, quantity, max_quantity, slot, fire_power=0, reload_speed=0, capacity=0,
            critical=0, piercing=0, scope=0, char_addr=0):
        char_addr = char_addr or self.person.addr
        func_addr = self.get_cached_address('_set_ingame_item', b'\x8B\x44\x24\x48\x8B\x54\x24\x44\x50',
            0x800000, 0x900000)
        if func_addr > 0:
            self.native_call_auto(func_addr, '18L', type, quantity, max_quantity, 0, 0, slot, fire_power, 0,
                reload_speed, capacity, 0, critical, piercing, 0, scope, char_addr, 8, 0, this=char_addr + 0x21A0)
