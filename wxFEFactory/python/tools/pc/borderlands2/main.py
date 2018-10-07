from functools import partial
from lib.hack.forms import Group, StaticGroup, ModelCheckBox, ModelInput, ModelSelect
from lib.hack.handlers import MemHandler
from lib.win32.keys import VK
from tools.assembly_hacktool import AssemblyHacktool, AssemblyItem, AssemblyItems, AssemblySwitch
from tools.assembly_code import AssemblyGroup, Variable
from tools import assembly_code
from fefactory_api import ui
from styles import styles
from . import models
import fefactory_api


class Main(AssemblyHacktool):
    CLASS_NAME = 'LaunchUnrealUWindowsClient'
    WINDOW_NAME = 'Borderlands 2 (32-bit, DX9)'

    def __init__(self):
        super().__init__()
        self.handler = MemHandler()
        self._global = models.Global(0, self.handler)

    def render_main(self):
        # with Group("global", "全局", self._global, handler=self.handler):
        #     pass
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_functions)

    def render_assembly_functions(self):
        functions = (
            AssemblyItems('子弹不减+精准+无后坐',
                AssemblyItem('ammo_keep', None, b'\x88\x5D\xFC\x8B\x86',
                    0x00DE0000, 0x00EF0000, b'',
                    b'\x9C\x60\xA1\x04\x09\xB7\x03\x8B\x80\x70\x04\x00\x00\x39\xF0\x0F\x85\x5E\x00\x00\x00'
                    b'\xC7\x86\xDC\x09\x00\x00\x00\x00\x00\x00\x8B\x80\xD0\x09\x00\x00\xC7\x80\x04\x01\x00\x00'
                    b'\x02\x00\x00\x00\xC7\x86\xEC\x08\x00\x00\x00\x7C\x12\x48\xC7\x86\xD8\x08\x00\x00\xCD\xCC\x4C\x3D'
                    b'\xC7\x86\xC4\x08\x00\x00\xCD\xCC\x4C\x3D\x31\xC9\x8B\x3D\x08\x09\xB7\x03\x89\x8F\x0C\x0E\x00\x00'
                    b'\x89\x8F\x10\x0E\x00\x00\x89\x8F\x14\x0E\x00\x00\x89\x8F\x18\x0E\x00\x00\x89\x8F\x1C\x0E\x00\x00'
                    b'\x61\x9D\x8B\x86\x28\x0A\x00\x00',
                    inserted=True, replace_len=6, replace_offset=3),
                AssemblyItem('ammo_keep2', None, b'\x89\x7D?\x89\x7D?\x89\x7D?\x8B\x06\x8B\x55',
                    0x008A0000, 0x008B0000, b'',
                    b'\x9C\x60\x8B\x0D\x04\x09\xB7\x03\x8B\x89\x70\x04\x00\x00\x39\xC8\x0F\x85\x08\x00\x00\x00'
                    b'\xC7\x44\x24\x2C\x00\x00\x00\x00\x61\x9D\x55\x8B\xEC\x6A\xFF',
                    inserted=True, replace_len=5, replace_offset=-0x2F, fuzzy=True)),
        )
        super().render_assembly_functions(functions)

    def get_hotkeys(self):
        this = self.weak
        return (
            (0, VK.H, this.pull_through),
        )

    def pull_through(self):
        self.toggle_assembly_button('health_inf')
