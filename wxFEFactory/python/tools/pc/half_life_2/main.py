from functools import partial
from lib.hack.forms import Group, StaticGroup, ModelCheckBox, ModelInput, ModelSelect
from lib.hack.handlers import MemHandler
from lib.win32.keys import VK
from lib import ui
from tools.base.assembly_hacktool import (
    AssemblyHacktool, AssemblyItem, AssemblyItems, AssemblySwitch, VariableType, SimpleButton, Delta
)
from tools.base.assembly_code import AssemblyGroup, Variable
from tools.base import assembly_code
from styles import styles
from . import models


class Main(AssemblyHacktool):
    CLASS_NAME = 'Valve001'
    WINDOW_NAME = 'HALF-LIFE 2'

    def __init__(self):
        super().__init__()
        self.handler = MemHandler()
        # self._global = models.Global(0, self.handler)

    def render_main(self):
        # with Group("global", "全局", self._global):
        #     pass
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_buttons_own)

    def onattach(self):
        super().onattach()
        self._server_base = self.handler.get_module('server.dll')

    def server_base(self):
        return self._server_base

    def render_assembly_buttons_own(self):
        server_base = self.server_base
        nop_6 = b'\x90' * 6
        delta = Delta(0x10000)
        self.render_assembly_buttons((
            AssemblyItem('invincible', '血量不减', b'\x89\xBE\x9C\x00\x00\x00\x5F\x5E\x5D\xB8',
                0x218000, delta, nop_6, find_base=server_base),
            AssemblyItem('suit_keep', '护甲不减', b'\x2B\xE8\x39\xAE\xB4\x0B\x00\x00',
                0x33A000, delta, b'\x90\x90', replace_len=2, find_base=server_base),
            AssemblyItem('ammo_999', '装填弹药999', b'\x89\x9C\xBE\x30\x06\x00\x00\x5F\x5E\x5B',
                0x21A000, delta, b'', b'\xC7\x84\xBE\x30\x06\x00\x00\xE7\x03\x00\x00',
                inserted=True, replace_len=7, find_base=server_base),
            SimpleButton('no_reload_all', '不用换弹', onclick=self.no_reload_all),
            AssemblyItem('no_reload_grenade', '炮弹不用换弹', b'\x89\x9C\xBE\x30\x06\x00\x00\x5F\x5E\x5B',
                0x21A000, delta, b'\x90' * 7, find_base=server_base),
            AssemblyItem('no_reload_pistol', '手枪不用换弹', b'\x89\x9E\xC4\x04\x00\x00\xEB\x39',
                0x218000, delta, nop_6, find_base=server_base),
            AssemblyItem('no_reload_revolver', '左轮不用换弹', b'\x83\x09\x01\x8B\x12\x89\x10',
                0x158000, delta, b'\x83\x09\x01\x8B\x10', find_base=server_base),
            AssemblyItem('no_reload_slot3', '冲锋/步枪不用换弹', b'\x89\xAE\xC4\x04\x00\x00\x33\xED',
                0x37000, delta, nop_6, find_base=server_base),
            AssemblyItem('no_reload_shotgun', '单管霰弹枪不用换弹', b'\x89\x9F\xC4\x04\x00\x00\x8B\x06',
                0x173000, delta, nop_6, find_base=server_base),
            AssemblyItem('no_reload_shotgun2', '双管霰弹枪不用换弹', b'\x89\x9F\xC4\x04\x00\x00\x8B\x06',
                0x173200, delta, nop_6, find_base=server_base),
            AssemblyItem('no_reload_crossbow', '十字弩不用换弹', b'\x89\x9E\xC4\x04\x00\x00\x8D\x54\x24\x24',
                0x15E000, delta, nop_6, find_base=server_base),
        ))

    # def get_hotkeys(self):
    #     this = self.weak
    #     return (
    #         (0, VK.H, this.pull_through),
    #     )

    # def pull_through(self):
    #     self.toggle_assembly_function('health_inf')

    def no_reload_all(self, checked):
        keys = ('no_reload_grenade', 'no_reload_pistol', 'no_reload_revolver', 'no_reload_slot3',
            'no_reload_shotgun', 'no_reload_shotgun2', 'no_reload_crossbow')
        for key in keys:
            self.toggle_assembly_function(key)
