from lib.hack.forms import (
    Group, StaticGroup, DialogGroup, ModelCheckBox, ModelInput, ModelSelect, Choice, ModelCoordWidget,
    ModelChoiceDisplay
)
from lib.hack.handlers import MemHandler
from lib.win32.keys import VK
from tools.base.native_hacktool import NativeHacktool
from tools.base.assembly_hacktool import AssemblyItem, AssemblyItems, VariableType, Delta, AssemblySwitch
from tools.base.assembly_code import AssemblyGroup, ORIGIN, Offset, Cmp, Variable
from . import models, datasets


ADDRESS_SOURCES = {
    'steam': {
        'item_keep': 0x01DA8000,
        'inf_ammo': 0x01DA5000,
        'inf_clip1': 0x01DA5000,
        'max_backpack': 0x010DF000,
        'quick_aim': 0x01CA8000,
        'no_recoil': 0x00D41000,
        'inf_health_base_1': 0x0045A000,
        'inf_health_base_2': 0x00BB5000,
        'tyrant_down': 0x02151000,
        'show_action': 0x02834000,
        'reset_save_count': 0x0165E000,
        'through_wall_xy': 0,
        'through_wall': 0,
        'reset_time': 0x01BA3000,
        'reset_time_all': 0x01BA3000,
    },
}


class Main(NativeHacktool):
    CLASS_NAME = 'via'
    WINDOW_NAME = 'RESIDENT EVIL 3'
    key_hook = False
    assembly_address_sources = ADDRESS_SOURCES

    def __init__(self):
        super().__init__()
        self.version = 'steam'
        self.handler = MemHandler()
        self._global_ins = models.Global(0, self.handler)
        self.char_index = self._global_ins.char_index = 0
        self.char_choice = None

    def render_main(self):
        character = (self._character, models.Character)

        with Group("global", "全局", (self._global, models.Global)):
            self.render_global()

        self.lazy_group(Group("character", "角色", character), self.render_character)
        self.lazy_group(Group("character_items", "角色物品", (self._global, models.Global), serializable=False, cols=4),
            self.render_character_items)
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_buttons_own)
        self.lazy_group(StaticGroup("功能"), self.render_buttons_own)

    def render_global(self):
        self.version_view = Choice("版本", datasets.VERSIONS, self.on_version_change)
        ModelInput("inventory.capcity", label="物品容量")
        ModelInput("save_count")
        ModelInput("speed")
        ModelInput("rapid_fire_speed", "快速射击速度", instance=self.variable_model)
        ModelInput("normal_speed", "快速射击时正常速度", instance=self.variable_model)
        ModelCoordWidget("position_struct.coord", labels=('X坐标', 'Z坐标', 'Y坐标'), savable=True, label="角色坐标")

    def render_character(self):
        self.char_choice = Choice("角色", datasets.CHARACTERS, self.weak.on_character_change)
        ModelInput("health")
        ModelInput("action")
        # ModelInput("weapon_state")
        ModelCheckBox("invincible")

    def render_character_items(self):
        """游戏中物品"""
        with ModelSelect.choices_cache:
            for i in range(20):
                ModelSelect("inventory.items.%d.info.choice" % i, "物品%d" % (i + 1), choices=datasets.INVENTORY_LABELS)
                ModelInput("inventory.items.%d.info.count" % i, "数量")

    def render_assembly_buttons_own(self):
        delta = Delta(0x2000)
        self.render_assembly_buttons((
            AssemblyItem(
                'item_keep', '数量不减', '2B DF 44 8B C3 48 8B D5 48 8B CE', None, delta, b'\x90\x90', replace_len=2),
            AssemblyItem(
                'inf_ammo', '备弹999', '48 8B 48 10 48 85 C9 74 05 8B 41 20 EB 02',
                None, delta, b'',
                '48 8B 48 10 48 85 C9 74 07 C7 41 20 E7030000',
                inserted=True, replace_len=7),
            AssemblyItem(
                'inf_clip1', '弹夹99', '48 8B 48 10 48 85 C9 74 03 8B 59 20 85 DB', None, delta, b'',
                '48 8B 48 10 48 85 C9 74 13 83 79 1C 00 74 0D 83 79 14 FF 74 07 C7 41 20 63 00 00 00 48 85 C9',
                inserted=True, replace_len=7),
            AssemblyItem(
                'max_backpack', '最大背包空间', '39 B2 90 00 00 00 7E * 44 8D 46 FF', None, delta, b'',
                'C7 82 90 00 00 00 14 00 00 00 39 B2 90 00 00 00',
                inserted=True, replace_len=6),
            AssemblyItem(
                'quick_aim', '快速瞄准', 'F3 0F 10 87 28010000 48', None, delta,
                b'', 'F3 0F 10 C1 F3 0F 11 8F 28 01 00 00',
                inserted=True, replace_len=8),
            AssemblyItem(
                'no_recoil', '稳定射击', 'F3 0F 10 48 20 F2 0F 58 D6 48 8D 44 24 20', None, delta,
                b'', AssemblyGroup('C7 40 10 00000000 C7 40 14 00000000', ORIGIN),
                inserted=True, replace_len=5),
            AssemblyItems(
                '玩家地址依赖',
                AssemblyItem(
                    'inf_health_base_1', None, '48 8B 87 C0 02 00 00 48 85 C0 75', None, delta, b'',
                    AssemblyGroup(
                        '48 8B 87 C0 02 00 00 48 85 C0 74 1D 50 8F 05',
                        Offset('character_addr'),
                        Cmp('b_inf_health', 1),
                        '75 0D 53 51 48 8D 58 58 8B 4B FC 89 0B 59 5B',
                        # 快速射击
                        Cmp('b_rapid_fire', 1),
                        '75 52',
                        Cmp('character_addr', 0),
                        '74 49 50 51 52 48 A1', Variable('character_addr'),
                        '48 8B 80 F8 00 00 00 48 8B 88 08 01 00 00 48 8B 49 54 48 8B 90 30 01 00 00'
                        '48 83 F9 10 74 0F 48 83 F9 20 74 09 48 8B 0D',
                        Offset('normal_speed'),
                        'EB 07 48 8B 0D',
                        Offset('rapid_fire_speed'),
                        '48 89 4A 50 5A 59 58',
                    ),
                    inserted=True,
                    replace_len=7,
                    args=(
                        'b_inf_health',
                        'b_one_hit_kill',
                        'b_rapid_fire',
                        VariableType('character_addr', size=8),
                        VariableType('normal_speed', type=float, value=1.0),
                        VariableType('rapid_fire_speed', type=float, value=10.0),
                    )),
                AssemblyItem(
                    'inf_health_base_2', None, '41 8B 49 58 41 8B C0 99 C7 44 24 10 00 00 00 00',
                    None, delta, b'',
                    AssemblyGroup(
                        '49 8D 49 58 48 A1',
                        Variable('character_addr'),
                        '4C 39 C8 75 0A 8B 41 FC 89 01 45 31 C0 EB 17',
                        Cmp('b_one_hit_kill', 1),
                        '75 0E 41 83 F8 00 7E 06 41 C7 41 58 01 00 00 00 8B 09 41 8B C0'
                    ),
                    inserted=True, replace_len=7),
            ),
            AssemblySwitch('b_inf_health', '无限生命', depends=('inf_health_base_1')),
            AssemblySwitch('b_one_hit_kill', '一击必杀', depends=('inf_health_base_1')),
            # AssemblySwitch('b_rapid_fire', '快速射击', depends=('inf_health_base_1')),
            AssemblyItem(
                'tyrant_down', '追踪者无法起身',
                'F2 0F 5C F8 66 0F 5A CF F3 0F 11 8B 94 04 00 00',
                None, delta, '90 90 90 90', replace_len=4),
            AssemblyItem(
                'show_action', '显示可互动及可收集物品', 'F3 0F 59 63 6C F2 0F 10 D6', None, delta, b'',
                AssemblyGroup(
                    '50 51 0F 29 05',
                    Offset('float_1'),
                    'F3 0F 10 43 6C 48 8B 4B 28 48 85 C9 74 35 48 8B 89 80 00 00 00 48 85 C9 74 29'
                    '48 B8 2F 00 4E 00 6F 00 74 00 48 39 41 28 75 19 48 B8 69 00 63 00 65 00 2F 00'
                    '48 39 41 30 75 09 B8 28 00 00 00 F3 0F 2A C0 F3 0F 59 E0 0F 28 05',
                    Offset('float_1'),
                    '59 58',
                ),
                inserted=True,
                replace_len=5,
                args=(VariableType('float_1', size=40, align=16, type=float, value=1.0),)
            ),
            AssemblyItem(
                'reset_save_count', '重置存档次数', '8D 42 01 89 41 24 48 8B 43 50',
                None, delta, '31 C0 90', replace_len=3),
            # AssemblyItem(
            #     'through_wall_xy', '穿墙(忽略地面)', '89 47 30 41 8B 46 04 89 47 34 41 8B 46 08 89 47 38',
            #     None, delta, '90 90 90 41 8B 46 04 89 47 34 41 8B 46 08 90 90 90'),
            # AssemblyItem(
            #     'through_wall', '穿墙(包括地面)', '89 47 30 41 8B 46 04 89 47 34 41 8B 46 08 89 47 38',
            #     None, delta, '90 90 90 41 8B 46 04 90 90 90 41 8B 46 08 90 90 90'),
            AssemblyItem(
                'reset_time', '重置游戏时间',
                '48 8D 04 2A 48 89 41 18 48 8B 43 50 48 39 70 18 0F 85 * * * * 48 8B 47 58', None, delta,
                b'', AssemblyGroup(
                    '48 8D 04 2A 48 89 41 18 48 2B 41 20 81 3D',
                    Offset('reset_time_temp1', size=8),
                    '00879303 7C 0A C7 05',
                    Offset('reset_time_temp1', size=8),
                    '00000000 81 05',
                    Offset('reset_time_temp1', size=8),
                    '40420F00 48 2B 05',
                    Offset('reset_time_temp1'),
                    '48 89 41 30 48 31 C0 48 89 41 28',
                ), inserted=True, replace_len=8, fuzzy=True,
                args=(VariableType('reset_time_temp1', 8),)),
            AssemblyItem(
                'reset_save_count', '重置总游玩时间', '48 8B 02 49 89 40 20',
                None, delta, '48 31 C0 49 89 40 20', replace_len=7),
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
        self._global_ins.position_struct.coord[1] += 2

    def go_down(self):
        self._global_ins.position_struct.coord[1] -= 2
