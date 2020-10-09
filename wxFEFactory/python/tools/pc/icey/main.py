from lib.hack.forms import (
    Group, StaticGroup
)
from lib import ui
from tools.base.assembly_hacktool import AssemblyItem, Delta
from tools.base.mono_hacktool import MonoHacktool
from . import models


class Main(MonoHacktool):
    CLASS_NAME = 'UnityWndClass'
    WINDOW_NAME = 'ICEY'

    def onattach(self):
        super().onattach()

        self.register_classes((
            models.PlayerAttribute,
            models.UIDataBind,
        ))
        self.assembly_address_dict = {
            'unlimited_health': models.PlayerAttribute.set_currentEnergy.mono_compile,
            'unlimited_energy': models.PlayerAttribute.set_currentHP.mono_compile,
            'unlimited_money': models.UIDataBind.UpdateCharInfo.mono_compile + 0x200,
        }

    def render_main(self):
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_buttons_own)

    def render_assembly_buttons_own(self):
        delta = Delta(0x400)

        self.render_assembly_buttons((
            AssemblyItem('unlimited_health', '无限生命', b'\x89\x47\x20\x48\x8B\x7D\xF8', None, delta,
                b'', b'\x8B\x47\x1C\x89\x47\x20\x48\x8B\x7D\xF8', inserted=True, find_base=False),
            AssemblyItem('unlimited_energy', '无限能量', b'\x89\x47\x28\x48\x8B\x7D\xF8', None, delta,
                b'', b'\x8B\x47\x24\x89\x47\x28\x48\x8B\x7D\xF8', inserted=True, find_base=False),
            AssemblyItem('unlimited_money', '无限金钱', b'\x48\x63\x49\x10\x3B\xC1', None, delta,
                b'', b'\xC7\x41\x10\x9F\x86\x01\x00\x48\x63\x49\x10\x39\xC8',
                replace_len=6, inserted=True, find_base=False),
        ))
