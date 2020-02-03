import pyapi
from base64 import b64decode
from lib.hack.forms import (
    Group, StaticGroup, DialogGroup, ModelCheckBox, ModelInput, ModelSelect, Choice, ModelCoordWidget,
    ModelChoiceDisplay
)
from lib.hack.handlers import MemHandler
from lib.win32.keys import VK
from tools.base.native_hacktool import NativeHacktool
from tools.base.assembly_hacktool import AssemblyItem, AssemblyItems
from tools.base.assembly_code import AssemblyGroup, ORIGIN
from . import models, datasets


class Main(NativeHacktool):
    CLASS_NAME = 'via'
    WINDOW_NAME = 'RESIDENT EVIL 2'
    key_hook = False

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
            # AssemblyItem('ammo_keep', '子弹不减', b'\x66\x29\x54\x41\x0A\x79\x07', 0x900000, 0xA00000,
            #     b'\x66\x4A\x90\x90\x90'),
            # AssemblyItem('no_recoil', '无后坐力', b'\xF3\x0F\x10\x8E\xFC\x4A\x00\x00', 0x680000, 0x700000, NOP_8),

            AssemblyItem('inf_ammo', '弹药锁定', '48 8B 48 10 48 85 C9 74 05 8B 41 20 EB 02 33 C0 48 85 D2',
                0x00401000, 0x00402000, b'',
                '48 8B 48 10 48 85 C9 74 07 C7 41 20 E7030000',
                inserted=True, replace_len=7),

            AssemblyItems('弹夹子弹锁定',
                AssemblyItem('inf_clip_ammo1', None, '48 8B 48 10 48 85 C9',
                    0x00E88000, 0x00E89000, b'',
                    '48 8B 48 10 48 85 C9 74 13 83 79 1C 00 74 0D 83 79 14 FF 74 07 C7 41 20 63000000 48 85 C9',
                    inserted=True),

                AssemblyItem('inf_clip_ammo2', None, '48 8B 46 10 48 85 C0',
                    0x00E87C00, 0x00E87D00, b'',
                    '48 8B 46 10 48 85 C0 74 14 83 78 1C 00 74 0E 83 78 14 FF 74 08 BB 63000000 89 58 20 48 85 C0',
                    inserted=True)),
            AssemblyItem('inf_modai', '保存时墨带无限', '48 8B 42 10 48 85 C0 74 03 8B 58 20 2B DF', 0xE8AE00, 0xE8B000,
                b'', '48 8B 42 10 48 85 C0 74 07 C7 40 20 0A000000 48 85 C0 74 03 8B 58 20 2B DF',
                inserted=True),

            AssemblyItem('inf_knife', '小刀无限耐久', '48 8B 48 10 48 85 C9 74 05 8B 41 20 EB 02 33 C0 66 0F 6E C6',
                0x00E88000, 0x00E89000, b'',
                '48 8B 48 10 48 85 C9 74 0B 83 79 14 2E 75 05 8B C6 89 41 20 48 85 C9',
                inserted=True, replace_len=7),

            AssemblyItem('min_save_count', '最小保存次数', '8D 42 01 89 41 24', 0xBA0000, 0xBA0200, '31 C0', replace_len=3),
            AssemblyItem('quick_aim', '快速瞄准', 'F3 0F 10 87 20010000 48', 0x01705000, 0x01705F00,
                b'', 'C7 87 20010000 0000C842F3 0F10 87 20010000',
                inserted=True, replace_len=8),
            AssemblyItem('no_recoil', '稳定射击', 'F3 0F10 48 20 F2 0F 58 D6 F3 0F 11 4D 6F', 0x01125000, 0x01126000,
                b'', AssemblyGroup('C7 40 10 00000000 C7 40 14 00000000', ORIGIN),
                inserted=True),
            AssemblyItems('暴君一击倒地&无法起身',
                AssemblyItem('baojun_down_1', None, '39 71 58 0F 9F C0', 0x0178F000, 0x01790000,
                    b'', '83 79 58 01 7E 07 C7 41 58 01000000 39 71 58 0F 9F C0',
                    inserted=True, replace_len=8),
                AssemblyItem('baojun_down_2', None, '66 0F 5A CE F3 0F 11 8F F4 01 00 00 48 8B 43 50 48 39 48 18 75 1F',
                    0x01C62000, 0x01C63000,
                    b'', '68 00 00 C8 41 F3 0F 10 0C 24 48 83 C4 08',
                    inserted=True, replace_len=8),
            )
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
        # person = self.person
        # person.items[person.cur_item].quantity = 1
        self._global.inventory.items[0].info.choice += 1

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
