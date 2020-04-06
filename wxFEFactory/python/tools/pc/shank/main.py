from functools import partial
from lib.hack.forms import Group, StaticGroup, ModelCheckBox, ModelInput, ModelSelect
from lib.hack.handlers import MemHandler
from tools.base.assembly_hacktool import (
    AssemblyHacktool, AssemblyItem, Delta
)
# from . import models


class Main(AssemblyHacktool):
    CLASS_NAME = 'Shank'
    WINDOW_NAME = 'Shank'

    def __init__(self):
        super().__init__()
        self.handler = MemHandler()
        # self._global = models.Global(0, self.handler)

    def render_main(self):
        # with Group("global", "全局", self._global):
        #     pass
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_buttons_own)

    def render_assembly_buttons_own(self):
        delta = Delta(0x10000)
        self.render_assembly_buttons((
            AssemblyItem(
                'inf_health', '无限生命', 'D9 40 70 8B 78 08 DD 5C 24 4C',
                0x000A3000, delta, b'', 'C7 40 70 00 00 7A 44 D9 40 70 8B 78 08',
                inserted=True, replace_len=6),
            AssemblyItem(
                'inf_grenade', '无限手雷', '8B 40 10 5E 5B',
                0x00085000, delta, b'', 'C7 40 10 09 00 00 00 8B 40 10 5E 5B',
                inserted=True, replace_len=5),
        ))
