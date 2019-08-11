from functools import partial
from lib import ui
from lib.hack.forms import (
    Group, StaticGroup, ModelInput, ModelAddrInput, ProxyInput, Title
)
from lib.hack.handlers import MemHandler
from lib.win32.keys import VK
from tools.base.assembly_code import AssemblyGroup, MemRead, Variable, Offset, Cmp, ORIGIN
from tools.base.assembly_hacktool import (
    AssemblyHacktool, AssemblyItem, AssemblyItems, AssemblySwitch, VariableType, Delta
)
from . import models


class Main(AssemblyHacktool):
    CLASS_NAME = 'NieR:Automata_MainWindow'
    WINDOW_NAME = 'NieR:Automata'
    key_hook = False

    def __init__(self):
        super().__init__()
        self.handler = MemHandler()
        self.game = models.Game(0, self.handler)

    def onattach(self):
        super().onattach()
        self.game.addr = self.handler.base_addr

    def render_main(self):
        with Group(None, "全局", self.game):
            self.render_global()
        self.lazy_group(Group("player", "玩家", None), self.render_player)
        self.lazy_group(Group("weapon", "武器", None), self.render_weapon)
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_functions)
        self.lazy_group(StaticGroup("快捷键"), self.render_hotkeys)

    def render_global(self):
        Title('游戏版本: 1.1')
        ModelInput('money')
        ModelInput('exp')
        ModelInput('exp_mult', '多倍经验', instance=self.variable_model)

    def render_game(self):
        for name in models.Game.field_names:
            ModelInput(name)

    def render_player(self):
        ModelAddrInput()
        for name in models.Player.form_fields:
            ModelInput(name)

    def render_weapon(self):
        pass

    def render_assembly_functions(self):
        delta = Delta(0x1000)
        super().render_assembly_functions((
            AssemblyItem('inf_health', '无限生命', b'\x89\x87\x58\x08\x00\x00\x8B\x9F\x68\x06\x01\x00', 0x001A6800, delta,
                b'', b'\xC7\x87\x58\x08\x00\x00\x7F\x96\x98\x00\x8B\x9F\x68\x06\x01\x00', inserted=True),
            AssemblyItem('locked_item', '锁定物品', b'\x44\x01\x40\x08\x83\x78\x08', 0x005DCC00, delta, b'',
                b'\x41\x83\xF8\x00\x7D\x09\x83\x78\x08\x01\x7E\x03\x45\x31\xC0\x44\x01\x40\x08\x83\x78\x08\x00',
                inserted=True),
            AssemblyItem('inf_item', '无限物品', b'\x8B\x40\x08\x48\x83\xC4\x28\xC3\x41', 0x005DCC00, delta, b'',
                b'\x83\x78\x08\x01\x7E\x07\xC7\x40\x08\x63\x00\x00\x00\x8B\x40\x08\x48\x83\xC4\x28',
                replace_len=7, inserted=True),
            # AssemblyItem('double_jump', '无限二段跳', b'\x44\x39\x82\xA8\x14\x00\x00', 0x004E1900, delta, b'',
            #     b'\xC7\x82\xA8\x14\x00\x00\x00\x00\x00\x00\x44\x39\x82\xA8\x14\x00\x00', inserted=True),
            AssemblyItem('double_jump', '无限二段跳', b'\x83\xBB\xA8\x14\x00\x00\x02\x0F\x8D', 0x001E2C00, delta,
                b'\xFF\x0F\x8C', replace_offset=6, replace_len=3),
            AssemblyItem('pod_no_cd', 'pod技能无冷却', b'\xF3\x0F\x10\x8C\xC1\x24\x6A\x01\x00', 0x00148200, delta, b'',
                b'\x0F\x57\xC9\xF3\x0F\x11\x8C\xC1\x24\x6A\x01\x00', inserted=True),
            AssemblyItem('chip_cost_1', '芯片占用1', b'\x8B\xAC\xCA\x60\x1F\x00\x00', 0x006DB200, delta, b'',
                b'\xBD\x01\x00\x00\x00\x89\xAC\xCA\x60\x1F\x00\x00', inserted=True),
            AssemblyItem('chip_position', '芯片位置', b'\x45\x03\xB4\xCA\x60\x1F\x00\x00', 0x005EB800, delta,
                b'\x4D\x31\xF6', replace_len=8, help='芯片自适应后叠加'),
            AssemblyItem('weapon_upgrade_freely', '武器自由升级', b'\x45\x8B\x94\xD4\x94\x00\x00\x00',
                0x005EE400, delta, b'', b'\x45\x31\xD2\x45\x89\x94\xD4\x94\x00\x00\x00', inserted=True),
            AssemblyItem('pod_upgrade_freely', 'Pod自由升级', b'\x45\x8B\x94\xD7\x94\x00\x00\x00',
                0x005EE400, delta, b'', b'\x45\x31\xD2\x45\x89\x94\xD7\x94\x00\x00\x00', inserted=True),
            AssemblyItem('hacking_inf_health', '入侵时无限生命', b'\x75\x08\x89\xB1\xDC\x28\x01\x00',
                0x0020D800, delta, b'\xEB\x0E', replace_len=2),
            AssemblyItem('hacking_inf_time', '入侵时无限时间', b'\xF3\x0F\x10\x49\x08\xF3\x0F\x58\x41\x04',
                0x0078A000, delta, b'', b'\xF3\x0F\x10\x49\x08\x0F\x57\xC0\xF3\x0F\x11\x41\x04\xF3\x0F\x58\x41\x04',
                inserted=True),
            AssemblyItem('hacking_one_hit', '一击回满入侵槽', b'\xF3\x0F\x58\xB3\x78\x6D\x01\x00',
                0x0025B200, delta, b'', b'\xC7\x83\x78\x6D\x01\x00\x00\x3C\x1C\x46\xF3\x0F\x58\xB3\x78\x6D\x01\x00',
                inserted=True),
            AssemblyItems(
                '穿墙',
                AssemblyItem('throu_wall', None, b'\x0F\x29\x42\x50\x44\x39\x82\x68\x05\x00\x00',
                    0x00135200, delta, b'\x90\x90\x90\x90', replace_len=4),
                AssemblyItem('throu_wall_2', None, b'\x0F\x29\x43\x50\x39\x93\x68\x05\x00\x00\x7E\x39',
                    0x00135500, delta, b'\x90\x90\x90\x90', replace_len=4),
            ),
            AssemblyItem('air_dashes', '空气爆发', b'\xC7\x83\x88\x0A\x01\x00\x01\x00\x00\x00', 0x001E2C00, delta,
                b'\x00', replace_offset=6, replace_len=1),
            AssemblyItem('easy_kill', '容易击杀', b'\x4D\x8B\xC7\x8B\xD3\xFF\xC9',
                0x002F5200, delta, b'', b'\x4D\x8B\xC7\xBA\x40\x54\x89\x00\xFF\xC9', inserted=True),
            AssemblyItem('exp_mult', '多倍经验', b'\x03\xCF\xB8\x7F\x96\x98\x00',
                0x00596000, delta, b'', AssemblyGroup(b'\x0F\xAF\x3D', Offset('exp_mult'), ORIGIN), inserted=True,
                args=(VariableType('exp_mult', value=2),)),
        ))

    def render_hotkeys(self):
        ui.Text("h: 血量满\n")

    def get_hotkeys(self):
        return (
            # (VK.MOD_ALT, VK.B, self.quick_health),
        )

    def quick_health(self):
        self.toggle_assembly_button('quick_health')
