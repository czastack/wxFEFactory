from functools import partial
from lib.hack.forms import Group, StaticGroup, ModelCheckBox, ModelInput, ModelSelect
from lib.hack.handlers import MemHandler
from lib.win32.keys import VK
from tools.assembly_hacktool import AssemblyHacktool, AssemblyItem
from fefactory_api import ui
from . import models


class Main(AssemblyHacktool):
    CLASS_NAME = 'JC3'
    WINDOW_NAME = 'Just Cause 3'

    def __init__(self):
        super().__init__()
        self.handler = MemHandler()
        self._global = models.Global(0, self.handler)

    def render_main(self):
        with Group("global", "全局", self._global, handler=self.handler):
            pass
            # ModelInput("metal", "金属")
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_functions)

    def render_assembly_functions(self):
        functions = (
            AssemblyItem('health_inf', '无限生命', b'\x4C\x8B\xBD\xA8\x11\x00\x00\x48\x8B\x81\xE0\x01\x00\x00',
                0x3A00000, 0x3B00000, b'',
                b'\x53\x48\x8B\x99\xD0\x01\x00\x00\x48\x85\xDB\x74\x09\x66\xC7\x83\x32\x02\x00\x00\x0F\x27\x5B'
                    b'\x4C\x8B\xBD\xA8\x11\x00\x00\x48\x8B\x81\xE0\x01\x00\x00',
                is_inserted=True),
            AssemblyItem('ammo_keep', '子弹不减', b'\x44\x29\xC0\x4C\x8B\x01', 0x3C00000, 0x3D00000,
                b'\x90\x90\x90'),
            AssemblyItem('ammo_inf', '无限弹药/手雷', b'\x41\x39\xE8\x41\x0F\x4C\xE8', 0x3B00000, 0x3C00000,
                b'\x41\x39\xE8\x90\x90\x90\x90'),
            AssemblyItem('freeze_time', '冻结时间', b'\xF3\x0F\x5C\xF7\x48\x89\xD9', 0x3D00000, 0x3E00000,
                b'\x90\x90\x90\x90'),
            # AssemblyItem('player_address', '角色地址', b'\x4C\x89\x41\x04\x44\x89\x41\x0C\x66\x0F\x6E\xC8',
            #     0x3A00000, 0x3B00000, b'', b'\x48\x89\x15\x16\x00\x00\x00\x4C\x89\x41\x04\x44\x89\x41\x0C',
            #     is_inserted=True, args=('player_address',)),
            AssemblyItem('no_recoil', '无后坐力', b'\x48\x8B\x87\x70\x05\x00\x00\x48\x2B\x87\x68\x05\x00\x00',
                0x3C00000, 0x3D00000, b'',
                b'\x48\x8D\x87\x74\x02\x00\x00\x83\x60\xF8\x00\x83\x20\x00\x83\x60\x04\x00'
                    b'\x48\x8B\x87\x70\x05\x00\x00\x48\x2B\x87\x68\x05\x00\x00',
                is_inserted=True),
            AssemblyItem('falcula_inf', '无限钩爪', b'\xFF\xC7\x48\x83\xC0\x10\x4C\x39\xC0',
                0x3C00000, 0x3D00000, b'\x31\xFF'),
        )
        super().render_assembly_functions(functions)

    def get_hotkeys(self):
        this = self.weak
        return (
            (VK.MOD_ALT, VK.H, this.pull_through),
        )

    def pull_through(self, _):
        _global = self._global
