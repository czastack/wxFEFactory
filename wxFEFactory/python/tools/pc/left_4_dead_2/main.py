from functools import partial
from lib.hack.forms import Group, StaticGroup, ModelCheckBox, ModelInput, ModelSelect
from lib.win32.keys import VK
from lib import ui
from tools.base.assembly_hacktool import (
    AssemblyHacktool, AssemblyItem, AssemblyItems, VariableSwitch, VariableType, SimpleButton, Delta
)
from tools.base.assembly_code import AssemblyGroup, Variable
from tools.base import assembly_code
from styles import styles
from . import models


class Main(AssemblyHacktool):
    CLASS_NAME = 'Valve001'
    WINDOW_NAME = 'Left 4 Dead 2'

    def render_main(self):
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_buttons_own)

    def onattach(self):
        super().onattach()
        self._server_base = self.handler.get_module('server.dll')
        self._client_base = self.handler.get_module('client.dll')

    def server_base(self):
        return self._server_base

    def client_base(self):
        return self._client_base

    def render_assembly_buttons_own(self):
        server_base = self.server_base
        delta = Delta(0x2000)
        self.render_assembly_buttons((
            AssemblyItem(
                'inf_team_health', '团队生命无限', '8B 8E * * * * 8B 15 * * * * 38 9E',
                0x2BA000, delta, b'', 'C7 86 EC 00 00 00 E7 03 00 00 8B 8E EC 00 00 00',
                find_base=server_base, replace_len=6, inserted=True, fuzzy=True),
            AssemblyItem(
                'inf_health', '生命无限', '8B 8F * * * * 8B 17 8B 82 * * * * 89 4D * 8B CF FF D0 DA 45 * D9 46',
                0x38F000, delta, b'', 'C7 87 EC 00 00 00 E7 03 00 00 8B 8F EC 00 00 00',
                find_base=server_base, replace_len=6, inserted=True, fuzzy=True),
            AssemblyItem(
                'no_reload', '不用换弹', '8B 86 * * * * 89 45 * 85 C0 0F 8F',
                0x3D2000, delta, b'', 'FF 86 14 14 00 00 8B 86 14 14 00 00',
                find_base=server_base, replace_len=6, inserted=True, fuzzy=True),
            AssemblyItem(
                'unlimited_specammo', '无限特殊弹药', '8A 86 * * * * 84 C0 74 * 0F B6 * 49',
                0x3D3000, delta, b'', 'C7 86 88 17 00 00 63 00 00 00 8A 86 88 17 00 00',
                find_base=server_base, replace_len=6, inserted=True, fuzzy=True),
            AssemblyItem(
                'unlimited_granades', '无限榴弹', '8B 84 * * * * * 53',
                0x2EF000, delta, b'', 'C7 84 BE 74 18 00 00 63 00 00 00 8B 84 BE 74 18 00 00',
                find_base=server_base, replace_len=7, inserted=True, fuzzy=True),
            AssemblyItem(
                'perfect_accuraty', '超级精准度', 'F3 0F 10 86 0C 0D 00 00 8B',
                0x2DA000, delta, b'', 'C7 86 0C 0D 00 00 00 00 00 00 F3 0F 10 86 0C 0D 00 00',
                find_base=self.client_base, replace_len=8, inserted=True),
        ))
