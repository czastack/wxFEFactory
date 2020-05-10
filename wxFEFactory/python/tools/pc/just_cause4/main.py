from functools import partial
from lib.hack.forms import Group, StaticGroup, ModelCheckBox, ModelInput, ModelSelect, Choice
from lib.hack.handlers import MemHandler
from lib.win32.keys import VK
from tools.base.assembly_hacktool import (
    AssemblyHacktool, AssemblyItem, AssemblyItems, AssemblySwitch, VariableType, Delta
)
from tools.base.assembly_code import AssemblyGroup, Variable, Offset, Cmp
from tools.base import assembly_code
from . import models


ADDRESS_SOURCES = {
    'epic': {
        'inf_health': 0x0E500000,
        'one_hit_kill_1': 0x00568000,
        'one_hit_kill_2': 0x0D31F000,
        'ammo_keep': 0x0072C000,
        'inf_ammo': 0x0D44D000,
        'no_reload': 0x00759000,
        # 'no_reload1': 0x00765000,
        # 'no_reload2': 0x00765000,
        'cease_fire': 0x0075A000,
        'rapid_fire': 0x0075A000,
        'no_recoil_base': 0x0CC42000,
        'inf_vehicle_speed': 0x0E9DB000,
        'show_target1': 0x00623000,
        'show_target2': 0x00E68000,
        'lock_time': 0x0DBE6000,
        'pilot_no_cd': 0x0095E000,
        'instant_airdrop': 0x00BF2000,
        'wing_boost_restore': 0x0E503000,
        'wing_inf_boost_auto': 0x0E503000,
        'wing_inf_boost': 0x0E503000,
        'wing_inf_missile': 0x0F2DD000,
    },
    'steam': {
    },
    'codex': {
    }
}


class Main(AssemblyHacktool):
    CLASS_NAME = 'JC4'
    WINDOW_NAME = 'Just Cause 4'
    assembly_address_sources = ADDRESS_SOURCES

    def __init__(self):
        super().__init__()
        self.handler = MemHandler()
        # self._global = models.Global(0, self.handler)

    def render_main(self):
        # with Group("group", "全局", None):
        #     self.render_global()
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_buttons_own)

    def render_global(self):
        self.version_view = Choice("版本", ADDRESS_SOURCES.keys(), self.on_version_change)

    def render_assembly_buttons_own(self):
        delta = Delta(0x2000)
        self.render_assembly_buttons((
            AssemblyItem(
                'inf_health', '无限生命', '0F B7 9E AA 03 00 00', None, delta, b'',
                AssemblyGroup(
                    '48 89 35',
                    Offset('player_addr'),
                    '48 8D 9E AA 03 00 00',
                    Cmp('b_inf_health', 1),
                    '75 0D 66 83 7B 02 00 7E 06 66 C7 43 02 0F 27 0F B7 1B'
                ),
                args=(
                    VariableType('player_addr', size=8),
                    'b_inf_health',
                ),
                inserted=True,
                hidden=True
            ),
            AssemblySwitch('b_inf_health', '无限生命', depends=('inf_health',)),
            AssemblyItems(
                '一击必杀',
                AssemblyItem(
                    'one_hit_kill_1', None, '48 8B 03 48 8B CB FF 90 28 01 00 00 84 C0 75 18', None, delta, b'',
                    AssemblyGroup(
                        '48 89 1D',
                        Offset('vehicle_addr'),
                        '48 8B 03 48 8B CB'
                    ),
                    args=(
                        VariableType('vehicle_addr', size=8),
                        'b_one_hit_kill'
                    ),
                    inserted=True, replace_len=6),
                AssemblyItem(
                    'one_hit_kill_2', None, '66 29 DE 66 85 C0 74 07', None, delta, b'',
                    AssemblyGroup(
                        '50  48 A1',
                        Variable('player_addr'),
                        '48 39 F8  74 32  48 A1',
                        Variable('vehicle_addr'),
                        '48 39 F8  74 15  ',
                        Cmp('b_one_hit_kill', 1),
                        '75 1A  66 83 FB 00  7E 14  66 BB 3075  EB 0E',
                        Cmp('b_inf_health', 1),
                        '75 05  BE 0F270000  58  66 29 DE  66 85 C0',
                    ),
                    inserted=True,
                    replace_len=6,
                    depends=('inf_health',)
                )
            ),
            AssemblyItem(
                'ammo_keep', '子弹不减', '41 2B C4 4C 8B 06 45 33 F6', None, delta,
                b'\x90\x90\x90'),
            AssemblyItem(
                'inf_ammo', '无限备弹', '8B B4 B9 EC 02 00 00 41 39 F0', None, delta, b'',
                'BE E7 03 00 00 44 8B C6', inserted=True, replace_len=7),
            AssemblyItem(
                'no_reload', '无需换弹', '8B 87 6C 05 00 00 48', None, delta, b'',
                'C7 87 6C 05 00 00 63 00 00 00 8B 87 6C 05 00 00', inserted=True, replace_len=6),
            # AssemblyItems(
            #     '无需换弹',
            #     AssemblyItem(
            #         'no_reload1', None, 'C2 D7 18 83 B9 64 02 00 00 00',
            #         None, delta, b'',
            #         'FF C2  83 B9 64 02 00 00 00',
            #         inserted=True, replace_offset=3, replace_len=7),
            #     AssemblyItem(
            #         'no_reload2', None, '8B FA 48 8B D9 85 D2 75 3D 83 B9 70 06 00 00 01', None, delta, b'',
            #         '83 FA 00 75 02 FF C2 8B FA 48 8B D9', inserted=True, replace_len=5)),
            AssemblyItem(
                'cease_fire', '停火', '72 3E 48 8B CF', None, delta,
                'EB 3E', replace_len=2),
            AssemblyItem(
                'rapid_fire', '快速射击', '72 3E 48 8B CF', None, delta,
                '90 90', replace_len=2),
            AssemblyItem(
                'no_recoil_base', '无后坐力/快速射击', 'F3 0F 10 B2 44 05 00 00 48 85 C9', None, delta, b'',
                AssemblyGroup(
                    '53  48 8D 9A 44050000  48 89 15',
                    Offset('no_recoil_addr'),
                    Cmp('b_no_recoil', 1),
                    '75 0D  C7 03 00000000  C7 43 04 00000000',
                    Cmp('b_rapid_fire', 1),
                    '75 07  C7 43 EC 003C1C46  F3 0F10 33  5B'
                ),
                args=(
                    VariableType('no_recoil_addr', size=8),
                    'b_no_recoil',
                    'b_rapid_fire',
                ),
                inserted=True,
                replace_len=8,
                hidden=True),
            AssemblySwitch('b_no_recoil', '无后坐力', depends=('no_recoil_base',)),
            AssemblySwitch('b_rapid_fire', '快速射击', depends=('no_recoil_base',)),
            AssemblyItem(
                'inf_vehicle_speed', '无限氮气加速', 'F3 0F 5C C8 0F 57 C0 F3 0F 5F C8 0F 2F C8', None, delta,
                '90 90 90 90', replace_len=4),
            AssemblyItems(
                '显示隐藏物品/目标',
                AssemblyItem(
                    'show_target1', None, '83 78 38 00 0F 95 C0', None, delta, b'',
                    '83 78 38 00  75 09  C7 40 38 01000000  EB 06  83 78 40 00  7C 07  C7 40 40 00004040'
                    'C7 40 44 0000803F  83 78 38 00  0F95 C0',
                    inserted=True, replace_len=7),
                AssemblyItem(
                    'show_target2', None, '0F B6 58 3C EB 02', None, delta, 'B3 01 90 90', replace_len=4),
            ),
            # AssemblyItem(
            #     'challenge_add_60s', '挑战时间+60s', '', None, delta, b'',
            #     '', inserted=True, replace_len=8),
            AssemblyItem(
                'lock_time', '锁定任务时间', 'F3 0F 5C C7 44 0F B6 F8 41 0F 2F C0', None, delta,
                '90 90 90 90', replace_len=4),
            AssemblyItem(
                'pilot_no_cd', '飞行员无冷却', '0F 57 C0 0F 2E 41 24', None, delta, b'',
                '0F 57 C0 F3 0F 10 F0 0F 2E 41 24', inserted=True, replace_len=7),
            AssemblyItem(
                'instant_airdrop', '瞬间产生空投', 'F3 0F 58 47 24 F3 0F 11 47 24', None, delta, b'',
                'C7 47 24 7F 96 18 4B F3 0F 58 47 24', inserted=True, replace_len=5),
            AssemblyItem(
                'wing_boost_restore', '快速恢复飞翼推进', 'F3 0F 5E C4 F3 0F 58 C2 F3 0F 5F C3', None, delta,
                '90 90 90 90', replace_len=4),
            AssemblyItem(
                'wing_inf_boost_auto', '飞翼无限推进(自动)', 'F3 0F 5C C8 F3 0F 5F CC F3 0F 5D CB', None, delta,
                '90 90 90 90', replace_len=4),
            # xorps xmm0,xmm0
            # comiss xmm1,xmm0
            # je canel
            # push rax
            # mov eax,(float)0.8
            # movd xmm0,eax
            # pop rax
            # comiss xmm1,xmm0
            # movaps xmm0,xmm2
            # mulss xmm0,xmm6
            # jbe do
            # canel:
            # subss xmm1,xmm0
            # do:
            AssemblyItem(
                'wing_inf_boost', '飞翼无限推进', '0F 28 C2 F3 0F 59 C6 F3 0F 5C C8', None, delta, b'',
                '0F 57 C0 0F 2F C8 0F 84 1B 00 00 00 50 B8 CD CC 4C 3F 66 0F 6E C0 58 0F 2F C8 0F 28 C2'
                'F3 0F 59 C6 0F 86 04 00 00 00 F3 0F 5C C8',
                inserted=True),
            # AssemblyItem(
            #     'wing_inf_boost', '飞翼无限推进', '0F 2F 07 77 0D B0 01', None, delta, b'',
            #     'C7 07 00 00 10 41', inserted=True, replace_len=5),
            AssemblyItem(
                'wing_inf_missile', '飞翼无限导弹', '0F 2F 42 F8 0F B6 C1', None, delta, b'',
                'C7 42 F8 00 00 10 41  0F 2F 42 F8  0F B6 C1', inserted=True, replace_len=7),
        ))

    def get_hotkeys(self):
        this = self.weak
        return (
            # (0, VK.H, this.pull_through),
            # (0, VK.P, this.challenge_points_add),
            # (0, VK.T, this.toggle_challenge_time),
            # (0, VK._0, this.clear_hot_level),
            (0, VK.CAPSLOCK, lambda: this.toggle_assembly_function('ammo_keep')),
            (VK.MOD_ALT, VK.CAPSLOCK, lambda: this.toggle_assembly_function('wing_inf_boost')),
            (VK.MOD_ALT, VK.A, lambda: this.toggle_assembly_function('no_reload')),
        )

    def on_version_change(self, lb):
        self.version = lb.text

    def pull_through(self):
        self.toggle_assembly_function('inf_health')

    def challenge_points_add(self):
        self.set_variable_value('challenge_points_add', 1)

    def toggle_challenge_time(self):
        self.toggle_assembly_function('challenge_time')

    def clear_hot_level(self):
        self.toggle_assembly_function('clear_hot_level')
