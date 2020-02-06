import pyapi
from base64 import b64decode
from lib.hack.forms import (
    Group, StaticGroup, DialogGroup, ModelCheckBox, ModelInput, ModelSelect, Choice, ModelCoordWidget,
    ModelChoiceDisplay
)
from lib.hack.handlers import MemHandler
from lib.win32.keys import VK
from tools.base.native_hacktool import NativeHacktool
from tools.base.assembly_hacktool import AssemblyItem, AssemblyItems, VariableType, Delta
from tools.base.assembly_code import AssemblyGroup, ORIGIN, Offset, Variable
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

        self.lazy_group(Group("person_items", "角色物品", self._global, serializable=False, cols=4),
            self.render_person_items)
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_buttons_own)
        self.lazy_group(StaticGroup("功能"), self.render_buttons_own)

    def render_person_items(self):
        """游戏中物品"""
        for i in range(20):
            ModelSelect("inventory.items.%d.info.choice" % i, "物品%d" % (i + 1), choices=datasets.INVENTORY_LABELS)
            ModelInput("inventory.items.%d.info.count" % i, "数量")

    def render_assembly_buttons_own(self):
        delta = Delta(0x1000)
        self.render_assembly_buttons((
            # AssemblyItem('ammo_keep', '子弹不减', b'\x66\x29\x54\x41\x0A\x79\x07', 0x900000, 0xA00000,
            #     b'\x66\x4A\x90\x90\x90'),
            # AssemblyItem('no_recoil', '无后坐力', b'\xF3\x0F\x10\x8E\xFC\x4A\x00\x00', 0x680000, 0x700000, NOP_8),

            AssemblyItem('inf_ammo', '弹药锁定', '48 8B 48 10 48 85 C9 74 05 8B 41 20 EB 02 33 C0 48 85 D2',
                0x00401000, delta, b'',
                '48 8B 48 10 48 85 C9 74 07 C7 41 20 E7030000',
                inserted=True, replace_len=7),

            AssemblyItems('弹夹子弹锁定',
                AssemblyItem('inf_clip_ammo1', None, '48 8B 48 10 48 85 C9',
                    0x00E88000, delta, b'',
                    '48 8B 48 10 48 85 C9 74 13 83 79 1C 00 74 0D 83 79 14 FF 74 07 C7 41 20 63000000 48 85 C9',
                    inserted=True),

                AssemblyItem('inf_clip_ammo2', None, '48 8B 46 10 48 85 C0',
                    0x00E87C00, delta, b'',
                    '48 8B 46 10 48 85 C0 74 14 83 78 1C 00 74 0E 83 78 14 FF 74 08 BB 63000000 89 58 20 48 85 C0',
                    inserted=True)),
            AssemblyItem('inf_modai', '保存时墨带无限', '48 8B 42 10 48 85 C0 74 03 8B 58 20 2B DF', 0xE8AE00, delta,
                b'', '48 8B 42 10 48 85 C0 74 07 C7 40 20 0A000000 48 85 C0 74 03 8B 58 20 2B DF',
                inserted=True),

            AssemblyItem('inf_knife', '小刀无限耐久', '48 8B 48 10 48 85 C9 74 05 8B 41 20 EB 02 33 C0 66 0F 6E C6',
                0x00E88000, delta, b'',
                '48 8B 48 10 48 85 C9 74 0B 83 79 14 2E 75 05 8B C6 89 41 20 48 85 C9',
                inserted=True, replace_len=7),

            AssemblyItem('min_save_count', '最小保存次数', '8D 42 01 89 41 24', 0xBA0000, delta, '31 C0', replace_len=3),
            AssemblyItem('quick_aim', '快速瞄准', 'F3 0F 10 87 20010000 48', 0x01705000, delta,
                b'', 'C7 87 20010000 0000C842F3 0F10 87 20010000',
                inserted=True, replace_len=8),
            AssemblyItem('no_recoil', '稳定射击', 'F3 0F10 48 20 F2 0F 58 D6 F3 0F 11 4D 6F', 0x01125000, delta,
                b'', AssemblyGroup('C7 40 10 00000000 C7 40 14 00000000', ORIGIN),
                inserted=True),
            AssemblyItems('一击必杀',
                AssemblyItem('one_hit_kill_1', None, '48 8B 87 30 02 00 00 48 85 C0 75', 0x004CD400, 0x004CD800, b'',
                    AssemblyGroup('48 8B 87 30 02 00 00 48 85 C0 74 14 50 8F 05',
                        Offset('player_addr'),
                        '53 51 48 8D 58 58 8B 4B FC 89 0B 59 5B'),
                    inserted=True, replace_len=7, args=(VariableType('player_addr', size=8),)),
                AssemblyItem('one_hit_kill_2', None,
                    '8B 4A 58 41 8B C0 99 33 C2 2B C2 2B C8 33 C0',
                    0x00C58600, 0x00C58800, b'',
                    AssemblyGroup(
                        '48 8D 4A 58 48 A1',
                        Variable('player_addr'),
                        '48 39 D0 0F 85 0D 00 00 00 8B 41 FC 89 01 45 31 C0 E9 10 00 00 00 41 83 F8 00'
                        '0F 8E 06 00 00 00 41 B8 9F 86 01 00 8B 09 41 8B C0'
                    ),
                    inserted=True, replace_len=6),
            ),
            AssemblyItems('暴君一击倒地&无法起身',
                AssemblyItem('baojun_down_1', None, '39 71 58 0F 9F *', 0x0178F000, delta,
                    b'', '83 79 58 01 7E 07 C7 41 58 01000000 39 71 58 0F 9F C0',
                    inserted=True, fuzzy=True),
                AssemblyItem('baojun_down_2', None,
                    'F2 0F 5C F0 66 0F 5A CE F3 0F 11 8F F4 01 00 00 48 8B 43 50 48 39 48 18 75 1F',
                    0x01C62000, delta,
                    b'', '68 00 00 C8 41 F3 0F 10 0C 24 48 83 C4 08',
                    inserted=True, replace_len=8),
            ),
            AssemblyItem('show_action', '显示可互动&可收集物品', 'F3 0F 59 63 6C F2 0F 10 D6', 0x022BE000, delta,
                b'', AssemblyGroup(
                    '50 51 0F 29 05',
                    Offset('float_1'),
                    'F3 0F 10 43 6C 48 8B 4B 28 48 85 C9 74 35 48 8B 89 80 00 00 00 48 85 C9 74 29'
                    '48 B8 2F 00 4E 00 6F 00 74 0048 39 41 30 75 19 48 B8 69 00 63 00 65 00 2F 00'
                    '48 39 41 38 75 09 B8 28 00 00 00 F3 0F 2A C0 F3 0F 59 E0 0F 28 05',
                    Offset('float_1'),
                    '59 58',
                ),
                inserted=True, replace_len=5,
                args=(VariableType('float_1', size=40, type=float, value=1.0),)),
            AssemblyItem('through_wall_xy', '穿墙(忽略地面)', '89 47 30 41 8B 46 04 89 47 34 41 8B 46 08 89 47 38',
                0x01DC8000, delta, '90 90 90 41 8B 46 04 89 47 34 41 8B 46 08 90 90 90'),
            AssemblyItem('through_wall', '穿墙(包括地面)', '89 47 30 41 8B 46 04 89 47 34 41 8B 46 08 89 47 38',
                0x01DC8000, delta, '90 90 90 41 8B 46 04 90 90 90 41 8B 46 08 90 90 90'),
            AssemblyItem('reset_time', '重置游戏时间',
                '48 8D 04 2A 48 89 41 18 48 8B 43 50 4C 39 70 18 0F85 * * * *'
                '44 38 77 53 0F85 * * * * 44 38 77 52 75 52', 0x00B7F000, delta,
                b'', AssemblyGroup(
                    '48 8D 04 2A 48 89 41 18 48 2B 41 20 81 3D',
                    Offset('reset_time_temp1'),
                    '00879303 7C 0A C7 05',
                    Offset('reset_time_temp1'),
                    '00000000 81 05',
                    Offset('reset_time_temp1'),
                    '40420F00 48 2B 05',
                    Offset('reset_time_temp1'),
                    '48 89 41 30 48 31 C0 48 89 41 28',
                ), inserted=True, replace_len=8, fuzzy=True,
                args=(VariableType('reset_time_temp1', 8),)),
            AssemblyItem('lock_time', '锁定倒计时', 'F3 0F 10 47 78 0F 57 F6', 0x0187A000, delta,
                b'', 'C7 47 78 00 A0 0C 47 F3 0F 10 47 78', replace_len=5, inserted=True),
        ))

    def render_buttons_own(self):
        pass

    def get_ingame_item_dialog(self):
        """物品信息对话框"""
        pass

    def get_hotkeys(self):
        this = self.weak
        return (
            (VK.MOD_ALT, VK.H, this.pull_through),
            (VK.MOD_ALT, VK.E, this.set_ammo_up),
            (VK.MOD_ALT, VK.R, this.set_ammo_full),
            (VK.MOD_ALT, VK(','), this.save_coord),
            (VK.MOD_ALT, VK('.'), this.load_coord),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK(','), this.undo_coord),
            (VK.MOD_ALT, VK.W, this.go_up),
            (VK.MOD_ALT, VK.S, this.go_down),
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
        # person = self.person
        # person.items[person.cur_item].set_with('quantity', 'max_quantity')
        self._global.inventory.items[0].info.count = 99

    def set_ammo_up(self):
        # person = self.person
        # person.items[person.cur_item].quantity = 1
        self._global.inventory.items[0].info.count += 10

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

    def go_up(self):
        self._global.position_struct.coord[1] += 2

    def go_down(self):
        self._global.position_struct.coord[1] -= 2
