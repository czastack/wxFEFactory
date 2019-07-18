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
        ModelInput('hpmax')
        ModelInput('attr_red')
        ModelInput('attr_blue')
        ModelInput('attr_green')

    def render_assembly_functions(self):
        super().render_assembly_functions((
            AssemblyItem('health_base', '生命值', b'\x8B\x90\xE8\x00\x00\x00\x89\x55\xF4\xF2',
                0x0D3C6000, 0x0FFF0000, b'',
                AssemblyGroup(
                    b'\xA3',
                    Variable('ptr1'),
                    Cmp('quick_health', 1),
                    b'\x0F\x85\x0C\x00\x00\x00\x8B\x88\xEC\x00\x00\x00\x89\x88\xE8\x00\x00\x00\x8B\x90\xE8\x00\x00\x00'
                ),
                args=('ptr1', 'quick_health'), replace_len=6, inserted=True),
            AssemblySwitch('quick_health', '生命快速恢复'),
            # AssemblyItem('double_gold', '双倍金币', b'\xBA\x01\x00\x00\x00',
            #     models.GoldWallet.Deposit.mono_compile, Delta(0x5d), b'',
            #     AssemblyGroup(b'\x48\x01\xf6', ORIGIN),
            #     inserted=True),
            AssemblyItem('no_cd', '技能无冷却', b'\xF2\x0F\x11\x59\x78\xF2\x0F\x10\x69',
                0x0E1C0000, 0x0E1D0000, b'\x0F\x57\xDB\x90', replace_offset=-9, replace_len=4),
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
