from functools import partial
from lib import ui
from lib.hack.forms import (
    Group, StaticGroup, ModelInput
)
from lib.hack.handlers import MemHandler
from lib.win32.keys import VK
from tools.base.assembly_code import AssemblyGroup, MemRead, Variable, Cmp, ORIGIN
from tools.base.assembly_hacktool import (
    AssemblyHacktool, AssemblyItem, AssemblyItems, AssemblySwitch, VariableType, Delta
)
from . import models


class classname(object):
    pass


class Main(AssemblyHacktool):
    CLASS_NAME = 'HL_WIN'
    WINDOW_NAME = None

    def __init__(self):
        super().__init__()
        self.handler = MemHandler()
        self._global = models.Global(self.variable_getter('ptr1'), self.handler)

    def onattach(self):
        super().onattach()

    def render_main(self):
        with Group("player", "全局", self._global):
            self.render_global()
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_functions)
        self.lazy_group(StaticGroup("快捷键"), self.render_hotkeys)

    def render_global(self):
        ui.Hr()
        ui.Text('游戏版本')
        ModelInput('hp')
        ModelInput('hpmax')
        ModelInput('red_tier')
        ModelInput('purple_tier')
        ModelInput('green_tier')

    def render_assembly_functions(self):
        tier_item = AssemblyItem(
            None, None, b'\x89\x45\xF8\x01\x45\xFC\xFF',
            0x0C000000, 0x0FFF0000, b'', AssemblyGroup(b'\x83\xC0\x08', ORIGIN),
            inserted=True, replace_len=7, replace_offset=-7)

        super().render_assembly_functions((
            AssemblyItem('health_base', '生命值', b'\x8B\x90\xE8\x00\x00\x00\x89\x55\xF4\xF2',
                0x0C000000, 0x0FFF0000, b'',
                AssemblyGroup(
                    b'\xA3',
                    Variable('ptr1'),
                    Cmp('quick_health', 1),
                    b'\x0F\x85\x0C\x00\x00\x00\x8B\x88\xEC\x00\x00\x00\x89\x88\xE8\x00\x00\x00\x8B\x90\xE8\x00\x00\x00'
                ),
                args=('ptr1', 'quick_health'), replace_len=6, inserted=True),
            AssemblySwitch('quick_health', '生命快速恢复'),
            AssemblyItem('no_cd', '技能无冷却', b'\xF2\x0F\x11\x59\x78\xF2\x0F\x10\x69',
                0x0C000000, 0x0FFF0000, b'\x0F\x57\xDB\x90', replace_offset=-9, replace_len=4),
            AssemblyItem('no_injured', '敌人无伤害', b'\x2B\x8D\x4C\xFF\xFF\xFF\x89\x8D\x50',
                0x0C000000, 0x0FFF0000, b'', AssemblyGroup(
                    b'\x83\xBD\x4C\xFF\xFF\xFF\x00\x7E\x17\x52\x8B\x55\x08\x3B\x15', Variable('ptr1'),
                    b'\x75\x0A\xC7\x85\x4C\xFF\xFF\xFF\x00\x00\x00\x00\x5A\x2B\x8D\x4C\xFF\xFF\xFF'),
                replace_len=6, inserted=True),
            AssemblyItem('one_kill', '一击必杀', b'\x89\x8A\xE8\x00\x00\x00\x8B\x45\x08',
                0x0C000000, 0x0FFF0000, b'', AssemblyGroup(
                    b'\x3B\x15', Variable('ptr1'), b'\x74\x02\x31\xC9\x89\x8A\xE8\x00\x00\x00'),
                replace_len=6, inserted=True),
            AssemblyItem('inf_arrow', '无限弓箭', b'\x89\x48\x18\x8B\x55\x08\x8B\x42\x04',
                0x0C000000, 0x0FFF0000, b'',
                b'\x83\x78\x18\x06\x0F\x8D\x0D\x00\x00\x00\x83\x78\x18\x00\x0F\x8E\x03\x00\x00\x00'
                b'\x8B\x48\x18\x89\x48\x18\x8B\x55\x08', replace_len=6, inserted=True),
            AssemblyItem('inf_jump', '无限跳跃', b'\x89\x88\xB0\x02\x00\x00\x33\xD2',
                0x0C000000, 0x0FFF0000, b'\x33\xD2\x89\x90\xB0\x02\x00\x00'),
            AssemblyItem('time_reset', '时间重记', b'\x8B\x4D\xE8\xF2\x0F\x11\x49\x28',
                0x0C000000, 0x0FFF0000, b'', b'\x8B\x4D\xE8\x0F\x57\xC9\xF2\x0F\x11\x49\x28', inserted=True),
            AssemblyItem('boss_kill', 'BOSS快速杀死', b'\x8B\x4D\x08\x89\x81\xE8\x00\x00\x00\xE9',
                0x0CE00000, 0x0FFF0000, b'', b'\x8B\x4D\x08\xB8\x00\x00\x00\x00\x89\x81\xE8\x00\x00\x00',
                inserted=True, replace_len=9),
            AssemblyItem('yellow_count', '黄细胞(金币)数量', b'\x03\x45\x0C\x89\x45\xF8\x89\x42\x34',
                0x0C000000, 0x0FFF0000, b'', b'\x89\x45\xF8\xB8\x3F\x42\x0F\x00\x89\x42\x34',
                replace_offset=3, replace_len=6, inserted=True, help='获得1次细胞后开启 '),
            AssemblyItem('blue_count', '蓝细胞数量', b'\x8B\x91\x3C\x03\x00\x00\x89\x55\xF4\xB8????\x89',
                0x0D000000, 0x0FFF0000, b'', b'\xC7\x81\x3C\x03\x00\x00\x36\x42\x0F\x00\x8B\x91\x3C\x03\x00\x00',
                replace_len=6, inserted=True, fuzzy=True, help='投资1次细胞后开启'),
            tier_item.clone().set_data('red_tier', '暴虐等级+8', ordinal=3),
            tier_item.clone().set_data('purple_tier', '战术等级+8', ordinal=1),
            tier_item.clone().set_data('green_tier', '生存等级+8', ordinal=2),
        ))

    def render_hotkeys(self):
        ui.Text("Capslock: 必杀槽满\n"
            "h: 血量满\n")

    def get_hotkeys(self):
        return (
            # (0, VK.H, self.recovery),
        )

    def recovery(self):
        pass
