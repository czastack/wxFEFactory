from functools import partial
from lib.hack.forms import Group, StaticGroup, ModelCheckBox, ModelInput, ModelSelect
from lib.hack.handlers import MemHandler
from lib.win32.keys import VK
from tools.assembly_hacktool import AssemblyHacktool, AssemblyItem, AssemblyItems, AssemblySwitch
from tools.assembly_code import AssemblyGroup, Variable
from tools import assembly_code
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
            AssemblyItems('无限生命',
                AssemblyItem('health_inf1', '无限生命1', b'\x0F\xBF\x82\x32\x02\x00\x00\x4C\x89\x41\x04\x44\x89\x41\x0C',
                    0x3A00000, 0x3B00000, b'',
                    b'\x66\x8B\x82\xB0\x01\x00\x00\x66\x89\x82\x32\x02\x00\x00'
                        b'\x0F\xBF\x82\x32\x02\x00\x00\x4C\x89\x41\x04\x44\x89\x41\x0C',
                    is_inserted=True),
                AssemblyItem('health_inf2', '无限生命2', b'\x4C\x8D\x44\x24\x70\x0F\x28\xCE\x48\x8B\x8B\xD0\x01\x00\x00',
                    0x3A00000, 0x3B00000, b'',
                    b'\x4C\x8D\x44\x24\x70\x0F\x28\xCE\x48\x8B\x8B\xD0\x01\x00\x00\x66\xC7\x81\x32\x02\x00\x00\x0F\x27',
                    is_inserted=True)),
            AssemblyItem('ammo_keep', '子弹不减', b'\x44\x29\xC0\x4C\x8B\x01', 0x3C00000, 0x3D00000,
                b'\x90\x90\x90'),
            AssemblyItem('ammo_inf', '无限弹药/手雷', b'\x41\x39\xE8\x41\x0F\x4C\xE8', 0x3B00000, 0x3C00000,
                b'\x41\x39\xE8\x90\x90\x90\x90'),
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
            AssemblyItems('挑战时间不减',
                AssemblyItem('challenge_time1', None, b'\x29\xC1\x89\x8B\xC8\x00\x00\x00',
                    0x3D00000, 0x3E00000, b'\x90\x90'),
                AssemblyItem('challenge_time2', None, b'\xF3\x0F\x5C\xC7\x0F\x2F\xC6\x77\x03',
                    0x3E00000, 0x3F00000, b'\x90\x90\x90\x90'),
                AssemblyItem('challenge_time3', None, b'\xF3\x41\x0F\x2C\xC1\x01\x87\xC8\x00\x00\x00',
                    0x3E00000, 0x3F00000, b'\xF3\x41\x0F\x2C\xC1\x90\x90\x90\x90\x90\x90')),
            AssemblyItems('快速射击',
                AssemblyItem('rapid_fire1', None, b'\x41\x83\xBC\x24\x24\x02\x00\x00\x04\x0F\x87',
                    0x4680000, 0x4780000, b'',
                    AssemblyGroup(
                        b'\x51\x52\x53',
                        assembly_code.IfInt64('rapid_fire_temp',
                            AssemblyGroup(b'\x4C\x89\x25', assembly_code.Offset('rapid_fire_temp', 7)),
                            AssemblyGroup(b'\x4C\x89\x24\x25', assembly_code.Variable('rapid_fire_temp'))
                        ),
                        b'\x41\x8B\x94\x24\x24\x02\x00\x00\x48\x8B\x4E\x60\x48\x81\xC1\x80\x09\x00\x00'
                        b'\x8B\x9C\x91\xF0\x01\x00\x00\x89\x9C\x91\xB0\x01\x00\x00\x5B\x5A\x59'
                        b'\x41\x83\xBC\x24\x24\x02\x00\x00\x04'),
                    args=(('rapid_fire_temp', 8),),
                    is_inserted=True,
                    replace_len=9),
                AssemblyItem('rapid_fire2', None, b'\xF3\x0F\x10\x87\x98\x01\x00\x00\x0F\x2F\xC6',
                    0x3C00000, 0x3D00000, b'',
                    AssemblyGroup(
                        b'\x50\x48\xA1', assembly_code.Variable('rapid_fire_temp', 8),
                        b'\x48\x39\xF8\x75\x0A\xC7\x87\x98\x01\x00\x00\x00\xC0\x79\x44'
                        b'\x58\xF3\x0F\x10\x87\x98\x01\x00\x00'),
                    is_inserted=True,
                    replace_len=8)),
            # TODO 没法保证Alloc的地址是32位的
            AssemblyItem('challenge_points', '挑战分数',
                b'\x48\x03\x7B\x18\x48\x8B\x1B\x49\x3B\x9C\x24\x88\x01\x00\x00',
                0x3D00000, 0x3E00000, b'',
                AssemblyGroup(assembly_code.Cmp('challenge_points_add', 0),
                    b'\x7E\x0D\x81\x43\x18\x10\x27\x00\x00',
                    assembly_code.Dec('challenge_points_add'),
                    b'\x48\x03\x7B\x18\x48\x8B\x1B\x49\x3B\x9C\x24\x88\x01\x00\x00'),
                args=('challenge_points_add',),
                is_inserted=True),
            AssemblySwitch('challenge_points_add', '挑战分数+10000'),
            AssemblyItem('unlock_all_rebel_drops', '解锁全部叛军空投', b'\x80\xB9\x78\x01\x00\x00\x00',
                0x3F00000, 0x4000000, b'\x80\xB9\x78\x01\x00\x00\xFF'),
            AssemblyItem('rebel_drop_cool_down', '呼叫叛军空投', b'\x66\x0F\x6E\x8B\x38\x01\x00\x00',
                0x4500000, 0x4600000, b'',
                b'\xC7\x83\x38\x01\x00\x00\x00\x00\x00\x00\x66\x0F\x6E\x8B\x38\x01\x00\x00',
                is_inserted=True),
        )
        super().render_assembly_functions(functions)

    def get_hotkeys(self):
        this = self.weak
        return (
            (VK.MOD_ALT, VK.H, this.pull_through),
            (VK.MOD_ALT, VK.P, this.challenge_points_add),
        )

    def pull_through(self, _):
        _global = self._global

    def challenge_points_add(self, _):
        self.set_variable_value('challenge_points_add', 1)
