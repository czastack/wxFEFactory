from lib.hack.forms import (
    Group, StaticGroup
)
from lib.hack.handlers import MemHandler
from lib import ui
from tools.base.assembly_hacktool import AssemblyItem
from tools.base.mono_hacktool import MonoHacktool
# from . import models, datasets


class Main(MonoHacktool):
    CLASS_NAME = 'UnityWndClass'
    WINDOW_NAME = 'ICEY'

    def onattach(self):
        super().onattach()

        PlayerAttribute, UIDataBind = self.get_global_mono_classes((
            "PlayerAttribute",
            "UIDataBind",
        ))

        (
            self.set_currentEnergy_native,
            self.set_currentHP_native,
            self.UpdateCharInfo_native,
        ) = self.get_mono_compile_methods(self.get_mono_methods((
            (PlayerAttribute, "set_currentEnergy", 1),
            (PlayerAttribute, "set_currentHP", 1),
            (UIDataBind, "UpdateCharInfo", 0),
        )))

    def render_main(self):
        Group("player", "全局", None)
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_buttons_own)

    def render_assembly_buttons_own(self):
        self.render_assembly_buttons((
            AssemblyItem('unlimited_health', '无限生命', b'\x89\x47\x20\x48\x8B\x7D\xF8',
                self.set_currentHP_native, self.set_currentHP_native + 0x100,
                b'', b'\x8B\x47\x1C\x89\x47\x20\x48\x8B\x7D\xF8',
                inserted=True, find_base=False),
            AssemblyItem('unlimited_energy', '无限能量', b'\x89\x47\x28\x48\x8B\x7D\xF8',
                self.set_currentEnergy_native, self.set_currentEnergy_native + 0x100,
                b'', b'\x8B\x47\x24\x89\x47\x28\x48\x8B\x7D\xF8',
                inserted=True, find_base=False),
            AssemblyItem('unlimited_money', '无限金钱', b'\x48\x63\x49\x10\x3B\xC1',
                self.UpdateCharInfo_native + 0x200, self.UpdateCharInfo_native + 0x400,
                b'', b'\xC7\x41\x10\x9F\x86\x01\x00\x48\x63\x49\x10\x39\xC8',
                replace_len=6, inserted=True, find_base=False),
        ))
