from base64 import b64decode
from lib.hack.forms import (
    Group, StaticGroup, DialogGroup, ModelCheckBox, ModelInput, ModelSelect, Choice, ModelCoordWidget,
    ModelChoiceDisplay
)
from lib.hack.handlers import MemHandler
from lib.hack.models import PropertyField
from lib.win32.keys import VK
from tools.base.native_hacktool import NativeHacktool
from tools.base.assembly_hacktool import AssemblyItem, AssemblyItems, VariableType, Delta, AssemblySwitch
from tools.base.assembly_code import AssemblyGroup, ORIGIN, Offset, Cmp, Variable
from . import models, datasets


ADDRESS_SOURCES = {
    'steam': {
        'lock_health': 0x00584000,
        'ammo_keep': 0x004B1000,
        'item_keep': 0x002A0000,
        'inf_ammo': 0x0029E000,
        'inf_clip': 0x004B1000,
        'inf_item1': 0x002A0000,
        'inf_item2': 0x01BB5000,
        'show_action': 0x019A1000,
        'clear_time': 0x01241000,
    },
    'codex': {
    }
}


class Main(NativeHacktool):
    CLASS_NAME = 'via'
    WINDOW_NAME = 'RESIDENT EVIL 7 biohazard'
    key_hook = False
    assembly_address_sources = ADDRESS_SOURCES

    def __init__(self):
        super().__init__()
        self.version = 'steam'
        self.handler = MemHandler()
        self._global_ins = models.Global(0, self.handler)

    def render_main(self):
        character = (self._character, models.Character)
        _global = (self._global, models.Global)

        with Group("group", "全局", _global):
            self.render_global()

        self.lazy_group(Group("character", "角色", character), self.render_character)

        self.lazy_group(Group("bag_items", "背包", _global, serializable=False, cols=4), self.render_bag_items)
        self.lazy_group(Group("box_items", "物品箱", _global, serializable=False, cols=4), self.render_box_items)
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_buttons_own)
        self.lazy_group(StaticGroup("功能"), self.render_buttons_own)

    def render_global(self):
        self.version_view = Choice("版本", datasets.VERSIONS, self.on_version_change)
        # ModelInput("inventory.capcity", label="物品容量")
        # ModelInput("save_count")
        ModelCoordWidget("char_coord", instance=self, labels=('X坐标', 'Z坐标', 'Y坐标'), savable=True)

    def render_character(self):
        ModelInput("health")
        ModelInput("health_max")

    def render_bag_items(self):
        """背包"""
        with ModelSelect.choices_cache:
            for i in range(20):
                ModelSelect(
                    "manager.bag_items.%d.name" % i, "物品%d" % (i + 1),
                    choices=datasets.INVENTORY_LABELS, values=datasets.INVENTORY_VALUES)
                ModelInput("manager.bag_items.%d.quantity" % i, "数量")

    def render_box_items(self):
        """物品箱"""
        with ModelSelect.choices_cache:
            for i in range(20):
                ModelSelect(
                    "manager.box_items.%d.name" % i, "物品%d" % (i + 1),
                    choices=datasets.INVENTORY_LABELS, values=datasets.INVENTORY_VALUES)
                ModelInput("manager.box_items.%d.quantity" % i, "数量")

    def render_assembly_buttons_own(self):
        delta = Delta(0x2000)
        self.render_assembly_buttons((
            AssemblyItem(
                'lock_health', '锁血', '0F 57 F6 F3 0F 10 40 24', None, delta, b'',
                'F3 0F 10 40 20 F3 0F 11 40 24', inserted=True, replace_len=5, replace_offset=3),

            AssemblyItem(
                'ammo_keep', '子弹不减', '41 FF C8 48 8B D3 48 8B CF', None, delta, b'\x90\x90\x90', replace_len=3),

            AssemblyItem(
                'item_keep', '物品不减', '2B F0 89 B7 88 00 00 00', None, delta, b'\x90\x90\x90\x90\x90\x90\x90\x90'),

            AssemblyItem(
                'inf_ammo', '备弹99', '41 03 B6 88 00 00 00', None, delta, b'',
                '41 C7 86 88000000 63000000  41 03 B6 88000000', inserted=True),

            AssemblyItem(
                'inf_clip', '弹夹99', '74 04 44 8B 40 24 41 FF C8', None, delta, b'',
                '74 06  41 B8 7F969800', replace_len=6, inserted=True),

            AssemblyItems(
                '无限物品',
                AssemblyItem(
                    'inf_item1', None, '2B F0 89 B7 88 00 00 00', None, delta, b'',
                    '39 C6 7F 05 83 FE 01 74 07 31 C0 BE 63 00 00 00 2B F0 89 B7 88 00 00 00',
                    inserted=True, replace_len=8),
                AssemblyItem(
                    'inf_item2', None, '48 8B D7 44 8B B7 88 00 00 00', None, delta, b'',
                    '41 BE 63 00 00 00 44 89 B7 88 00 00 00',
                    inserted=True, replace_len=7, replace_offset=3),
            ),

            AssemblyItem(
                'show_action', '显示可互动及可收集物品', 'F3 0F 10 40 28 0F 5A C0 0F 5A CA', None, delta, b'',
                '68 00 00 FA 43 F3 0F 10 04 24 48 83 C4 08', inserted=True, replace_len=5),

            AssemblyItem(
                'clear_time', '清空游戏时间', '66 0F 5A C2 F3 0F 11 85 20 01 00 00', None, delta, '0F 57 C0', replace_len=4),

            # AssemblyItem(
            #     'max_backpack', '最大背包空间', '39 B2 90 00 00 00 7E * 44 8D 46 FF', None, delta, b'',
            #     'C7 82 90 00 00 00 14 00 00 00 39 B2 90 00 00 00',
            #     inserted=True, replace_len=6),
        ))

    def render_buttons_own(self):
        pass

    def get_hotkeys(self):
        this = self.weak
        return (
            (VK.MOD_ALT, VK.H, this.pull_through),
            (VK.MOD_ALT, VK(','), this.save_coord),
            (VK.MOD_ALT, VK('.'), this.load_coord),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK(','), this.undo_coord),
            (VK.MOD_ALT, VK.W, this.go_up),
            (VK.MOD_ALT, VK.S, this.go_down),
        )

    def onattach(self):
        super().onattach()
        self._global_ins.addr = self.handler.base_addr

    def on_version_change(self, lb):
        self.version = lb.text
        self._global_ins = models.SPECIFIC_GLOBALS[self.version](self._global_ins.addr, self.handler)
        self._global_ins.char_index = self.char_index

    def _global(self):
        return self._global_ins

    def _character(self):
        if self.handler.active:
            return self._global_ins.manager.character

    character = property(_character)

    def on_character_change(self, lb):
        self.char_index = self._global_ins.char_index = lb.index

    def pull_through(self):
        self.character.set_with('health', 'health_max')

    def save_coord(self):
        self.last_coord = self.character.coord.values()

    def load_coord(self):
        if hasattr(self, 'last_coord'):
            character = self.character
            self.prev_coord = character.coord.values()
            character.coord = self.last_coord

    def undo_coord(self):
        if hasattr(self, 'prev_coord'):
            self.character.coord = self.prev_coord

    def reload_coord(self):
        if hasattr(self, 'last_coord'):
            self.character.coord = self.last_coord

    def go_up(self):
        coord_z = self.character.coord[1]
        coord_z += 2
        self.character.coord[1] = coord_z
        self._global_ins.position_struct.coord[1] = coord_z

    def go_down(self):
        coord_z = self.character.coord[1]
        coord_z -= 2
        self.character.coord[1] = coord_z
        self._global_ins.position_struct.coord[1] = coord_z

    @PropertyField(label="角色坐标")
    def char_coord(self):
        return self.character.coord

    @char_coord.setter
    def char_coord(self, value):
        value = list(value)
        self.character.coord = value
        self._global_ins.position_struct.coord = value
