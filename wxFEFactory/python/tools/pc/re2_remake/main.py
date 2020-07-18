from lib.hack.forms import (
    Group, StaticGroup, ModelCheckBox, ModelInput, ModelSelect, Choice, ModelCoordWidget
)
from lib.hack.handlers import MemHandler
from lib.hack.models import PropertyField
from lib.win32.keys import VK
from tools.base.native_hacktool import NativeHacktool
from . import assembly, datasets, models


class Main(NativeHacktool):
    CLASS_NAME = 'via'
    WINDOW_NAME = 'RESIDENT EVIL 2'
    key_hook = False
    assembly_address_sources = assembly.ADDRESS_SOURCES

    def __init__(self):
        super().__init__()
        self.version = 'steam'
        self.handler = MemHandler()
        self._global_ins = models.Global(0, self.handler)
        self.char_index = self._global_ins.char_index = 0

    def render_main(self):
        character = (self._character, models.Character)

        with Group("global", "全局", (self._global, models.Global)):
            self.render_global()

        self.lazy_group(Group("character", "角色", character), self.render_character)

        self.lazy_group(
            Group("character_items", "角色物品", (self._global, models.Global), serializable=False, cols=4),
            self.render_character_items)
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_buttons_own)
        self.lazy_group(StaticGroup("功能"), self.render_buttons_own)

    def render_global(self):
        self.version_view = Choice("版本", datasets.VERSIONS, self.on_version_change)
        ModelInput("inventory.capcity", label="物品容量")
        ModelInput("save_count")
        ModelInput("enemy_speed_multi_value", "敌人速度", instance=self.variable_model)
        # ModelCoordWidget("position_struct.coord", labels=('X坐标', 'Z坐标', 'Y坐标'), savable=True, label="角色坐标")
        ModelCoordWidget("char_coord", instance=self, labels=('X坐标', 'Z坐标', 'Y坐标'), savable=True)

    def render_character(self):
        Choice("角色", datasets.CHARACTERS, self.weak.on_character_change)
        ModelInput("health")
        ModelInput("action")
        # ModelInput("weapon_state")
        ModelInput("speed")
        ModelInput("rapid_fire_speed", "快速射击速度", instance=self.variable_model)
        ModelInput("normal_speed", "快速射击时正常速度", instance=self.variable_model)
        ModelCheckBox("invincible")
        # ModelCoordWidget("coord", labels=('X坐标', 'Z坐标', 'Y坐标'), savable=True, label="角色坐标")

    def render_character_items(self):
        """游戏中物品"""
        with ModelSelect.choices_cache:
            for i in range(20):
                ModelSelect("inventory.items.%d.info.choice" % i, "物品%d" % (i + 1), choices=datasets.INVENTORY_LABELS)
                ModelInput("inventory.items.%d.info.count" % i, "数量")

    def render_assembly_buttons_own(self):
        self.render_assembly_buttons(assembly.ASSEMBLY_ITEMS)

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
            return self._global_ins.character_struct.char

    character = property(_character)

    def on_character_change(self, lb):
        self.char_index = self._global_ins.char_index = lb.index

    def pull_through(self):
        self.character.health = 1000.0

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
