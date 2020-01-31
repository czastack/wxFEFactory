import pyapi
from functools import partial
from lib.hack.forms import (
    Group, StaticGroup, DialogGroup, ModelCheckBox, ModelInput, ModelSelect, Choice, ModelCoordWidget,
    ModelChoiceDisplay
)
from lib.hack.handlers import MemHandler
from lib.win32.keys import VK
from tools.base.native_hacktool import NativeHacktool, AssemblyItem
from . import models, datasets


class Main(NativeHacktool):
    CLASS_NAME = 'via'
    WINDOW_NAME = 'RESIDENT EVIL 2'

    def __init__(self):
        super().__init__()
        self.handler = MemHandler()
        self._global = models.Global(0, self.handler)
        self.char_index = self._global.char_index = 0
        self.char_choice = None

    def render_main(self):
        person = (self._person, models.Character)

        with Group("player", "全局", self._global):
            ModelInput("inventory.capcity", label="物品容量")
            ModelInput("save_count")
            ModelCoordWidget("position_struct.coord", labels=('X坐标', 'Z坐标', 'Y坐标'), savable=True, label="角色坐标")
            # ModelCheckBox("ammo_reducer")

        with Group("player", "角色", person):
            self.char_choice = Choice("角色", datasets.CHARACTERS, self.weak.on_person_change)
            ModelInput("health")
            ModelInput("speed")
            ModelInput("action")
            # ModelInput("weapon_state")
            ModelCheckBox("invincible")

        self.lazy_group(Group("person_items", "角色物品", self._global, serializable=False, cols=4), self.render_person_items)
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_buttons_own)
        self.lazy_group(StaticGroup("功能"), self.render_buttons_own)

    def render_person_items(self):
        """游戏中物品"""
        for i in range(20):
            ModelSelect("inventory.items.%d.info.choice" % i, "物品%d" % (i + 1), choices=datasets.INVENTORY_LABELS)
            ModelInput("inventory.items.%d.info.count" % i, "数量")

    def render_assembly_buttons_own(self):
        NOP_8 = b'\x90' * 8
        self.render_assembly_buttons((
            AssemblyItem('ammo_keep', '子弹不减', b'\x66\x29\x54\x41\x0A\x79\x07', 0x900000, 0xA00000,
                b'\x66\x4A\x90\x90\x90'),
            AssemblyItem('no_recoil', '无后坐力', b'\xF3\x0F\x10\x8E\xFC\x4A\x00\x00', 0x680000, 0x700000, NOP_8),
            AssemblyItem('rapid_fire', '快速射击', b'\xF3\x0F\x5C\xC2\xF3\x0F\x11\x86\x4C\x4F\x00\x00', 0x680000, 0x700000,
                b'', b'\xF3\x0F\x58\xD2\xF3\x0F\x58\xD2\xF3\x0F\x5C\xC2\xF3\x0F\x11\x86\x4C\x4F\x00\x00',
                inserted=True),
        ))

    def render_buttons_own(self):
        self.render_buttons(('unlock_guns', 'give_rocket_launcher'))

    def get_ingame_item_dialog(self):
        """物品信息对话框"""
        pass

    def get_hotkeys(self):
        this = self.weak
        return (
            (VK.MOD_ALT, VK.H, this.pull_through),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK.H, this.pull_through_all),
            (VK.MOD_ALT, VK.E, this.set_ammo_one),
            (VK.MOD_ALT, VK.R, this.set_ammo_full),
            (VK.MOD_ALT, VK(','), this.save_coord),
            (VK.MOD_ALT, VK('.'), this.load_coord),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK(','), this.undo_coord),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK('.'), this.reload_coord),
        )

    def onattach(self):
        super().onattach()
        self._global.addr = self.handler.base_addr

    def _person(self):
        if self.handler.active:
            return self._global.character_struct.chars[0]
            # chars = self._global.character_struct.chars
            # person = chars[self.char_index]
            # if person.addr == 0:
            #     for i in range(len(datasets.CHARACTERS)):
            #         if chars[i].addr:
            #             self.char_choice.index = self.char_index = i
            #             person = chars[i]
            #             break
            # return person

    def _person_config(self):
        if self.handler.active:
            return self._global.character_config.chars[self.char_index]

    person = property(_person)

    def on_person_change(self, lb):
        self.char_index = self._global.char_index = lb.index

    def ingame_item_copy(self, _):
        # pyapi.set_clipboard(self.ingame_item.hex())
        pass

    def ingame_item_paste(self, _):
        # self.ingame_item.fromhex(pyapi.get_clipboard())
        pass

    def pull_through(self):
        self.person.set_with('health', 'health_max').set_with('stamina', 'stamina_max')

    def pull_through_all(self):
        character_struct = self._global.character_struct
        for i in range(character_struct.chars_count):
            character_struct.chars[i].set_with('health', 'health_max')

    def set_ammo_full(self):
        person = self.person
        person.items[person.cur_item].set_with('quantity', 'max_quantity')

    def set_ammo_one(self):
        person = self.person
        person.items[person.cur_item].quantity = 1

    def save_coord(self):
        self.last_coord = self.person.coord.values()

    def load_coord(self):
        if hasattr(self, 'last_coord'):
            person = self.person
            self.prev_coord = person.coord.values()
            person.coord = self.last_coord

    def undo_coord(self):
        if hasattr(self, 'prev_coord'):
            self.person.coord = self.prev_coord

    def reload_coord(self):
        if hasattr(self, 'last_coord'):
            self.person.coord = self.last_coord

    def p1_go_p2(self):
        self._person()  # 确保当前角色正确
        chars = self._global.character_struct.chars
        chars[self.char_index].coord = chars[self.char_index + 1].coord.values()

    def p2_go_p1(self):
        self._person()  # 确保当前角色正确
        chars = self._global.character_struct.chars
        chars[self.char_index + 1].coord = chars[self.char_index].coord.values()
