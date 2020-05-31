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
    '3dm': {
        'inf_health': 0x00153000,
        'vehicle_inf_health': 0x006D4000,
        'inf_money': 0x003F3000,
        'inf_ammo': 0x0076D000,
        'no_reload': 0x003F6000,
        'inf_explosive': 0x0076D000,
        'no_overheat': 0x005BB000,
    },
    'steam': {
    }
}


class Main(AssemblyHacktool):
    CLASS_NAME = 'SR3'
    WINDOW_NAME = 'Saints Row: The Third'
    assembly_address_sources = ADDRESS_SOURCES

    def __init__(self):
        super().__init__()
        self.handler = MemHandler()
        self.version = ''
        # self._global = models.Global(0, self.handler)

    def render_main(self):
        # with Group("group", "全局", None):
        #     self.render_global()
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_buttons_own)

    def render_global(self):
        Choice("版本", ADDRESS_SOURCES.keys(), self.on_version_change)

    def render_assembly_buttons_own(self):
        delta = Delta(0x2000)
        self.render_assembly_buttons((
            AssemblyItem(
                'inf_health', '无限生命', 'F3 0F 10 80 B8 1C 00 00 F3 0F 2A C9', None, delta, b'',
                'C7 80 B8 1C 00 00 00 3C 1C 46 F3 0F 10 80 B8 1C 00 00', inserted=True, replace_len=8),
            AssemblyItem(
                'vehicle_inf_health', '载具无限生命', '83 BF 64 15 00 00 00', None, delta, b'',
                '50 9C 60 81 BE B8 1C 00 00 00 A0 0C 46 0F 8E 0C 00 00 00 8B 87 5C 15 00 00 89 87 64 15 00 00'
                '61 9D 58 83 BF 64 15 00 00 00',
                inserted=True, replace_len=7, depends=('inf_health',)),
            AssemblyItem(
                'inf_money', '无限金钱(99999)', 'F3 0F 2A 83 A0 1C 00 00', None, delta, b'',
                'C7 83 A0 1C 00 00 1C 96 98 00 F3 0F 2A 83 A0 1C 00 00', inserted=True, replace_len=8),
            AssemblyItem(
                'inf_ammo', '无限子弹', '8B 40 04 C2 08 00 CC 8B', None, delta, b'',
                'C7 40 04 0F 27 00 00 8B 40 04 C2 08 00', inserted=True, replace_len=6),
            AssemblyItem(
                'no_reload', '无需换弹', '8B 81 A4 01 00 00 0F 96 44 24 38', None, delta, b'',
                'C7 81 A4 01 00 00 0F 27 00 00 8B 81 A4 01 00 00', inserted=True, replace_len=6),
            AssemblyItem(
                'inf_explosive', '无限爆炸物', '8B 48 04 56 8B 74 24 0C', None, delta, b'',
                'C7 40 04 0F 27 00 00 8B 48 04 56 8B 74 24 0C', inserted=True, replace_len=8),
            AssemblyItem(
                'no_overheat', '机枪不会过热', 'D9 80 D4 02 00 00', None, delta, b'',
                'C7 80 D4 02 00 00 00 00 00 00 D9 80 D4 02 00 00', inserted=True, replace_len=6),
        ))

    def get_hotkeys(self):
        return (
            # (0, VK.H, self.pull_through),
            # (0, VK.P, self.challenge_points_add),
            # (0, VK.T, self.toggle_challenge_time),
            # (0, VK._0, self.clear_hot_level),
        )

    def on_version_change(self, lb):
        self.version = lb.text

    def pull_through(self):
        self.toggle_assembly_function('inf_health')
