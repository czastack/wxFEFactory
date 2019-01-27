from functools import partial
from lib.hack.forms import Group, StaticGroup, ModelCheckBox, ModelInput, ModelSelect
from lib.hack.handlers import MemHandler
from lib.win32.keys import VK
from tools.assembly_hacktool import (
    AssemblyHacktool, AssemblyItem, AssemblyItems, AssemblySwitch, VariableType, SimpleButton
)
from tools.assembly_code import AssemblyGroup, Variable
from tools import assembly_code
from fefactory_api import ui
from . import models
import fefactory_api


class Main(AssemblyHacktool):
    CLASS_NAME = 'VVideoClass'
    WINDOW_NAME = None

    def __init__(self):
        super().__init__()
        self.handler = MemHandler()
        self._globalins = models.Global(0, self.handler)

    def render_main(self):
        with Group("global", "全局", (self._global, models.Global)):
            ModelInput("energy")
            ModelInput("vigour")
            ModelInput("health")
            ModelInput("skill")
            ModelInput("atk").set_help("更换装备、升级、保存载入还原，下同")
            ModelInput("defense")
            ModelInput("critical_buff")
            ModelInput("critical")
            ModelInput("attr_wood")
            ModelInput("attr_fire")
            ModelInput("attr_earth")
            ModelInput("attr_metal")
            ModelInput("attr_water")
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_functions)

    def render_assembly_functions(self):
        functions = (
            AssemblyItem('invincible', '开启', b'\x04\x00\x00\x00\x48???\x48\x8b\x0c\x01',
                0x137500, 0x137800, b'',
                AssemblyGroup(
                    b'\x41\x81\xFC\xFF\xFF\xFF\xFF'
                    b'\x0F\x85\x02\x01\x00\x00'
                    b'\x3D\xE0\x0A\x00\x00'
                    b'\x0F\x85\xF7\x00\x00\x00'
                    b'\x48\x89\x0D', assembly_code.Offset('base1', 4),
                    assembly_code.Cmp('s_inf_energy', 1),
                    b'\x75\x0A'
                    b'\xC7\x81\xE4\x0A\x00\x00\x00\x00\xC6\x42',
                    assembly_code.Cmp('s_inf_vigour', 1),
                    b'\x75\x16'
                    b'\x81\xB9\xB4\x0A\x00\x00\x00\x00\x00\x00'
                    b'\x72\x0A'
                    b'\xC7\x81\xB4\x0A\x00\x00\x00\x00\xC6\x42',
                    assembly_code.Cmp('s_inf_health', 1),
                    b'\x75\x0A'
                    b'\xC7\x81\x98\x0A\x00\x00\x0F\x27\x00\x00',
                    assembly_code.Cmp('s_inf_skill', 1),
                    b'\x75\x0A'
                    b'\xC7\x81\x18\x0B\x00\x00\x0F\x27\x00\x00',
                    assembly_code.Cmp('s_inf_hit', 1),
                    b'\x75\x13'
                    b'\x83\xB9\x48\x0A\x00\x00\x01'
                    b'\x7E\x0A'
                    b'\xC7\x81\x48\x0A\x00\x00\x62\x00\x00\x00',
                    assembly_code.Cmp('s_add_atk', 1),
                    b'\x75\x16'
                    b'\x81\xB9\x88\x0B\x00\x00\x0F\x27\x00\x00'
                    b'\x7D\x0A'
                    b'\xC7\x81\x88\x0B\x00\x00\x0F\x27\x00\x00',
                    assembly_code.Cmp('s_add_def', 1),
                    b'\x75\x16'
                    b'\x81\xB9\xB8\x0B\x00\x00\x0F\x27\x00\x00'
                    b'\x7D\x0A'
                    b'\xC7\x81\xB8\x0B\x00\x00\x0F\x27\x00\x00',
                    assembly_code.Cmp('s_add_critical_buff', 1),
                    b'\x75\x16'
                    b'\x81\xB9\xE8\x0B\x00\x00\xE7\x03\x00\x00'
                    b'\x7D\x0A'
                    b'\xC7\x81\xE8\x0B\x00\x00\xE7\x03\x00\x00',
                    assembly_code.Cmp('s_add_critical', 1),
                    b'\x75\x16'
                    b'\x81\xB9\xF0\x0B\x00\x00\xE7\x03\x00\x00'
                    b'\x7D\x0A'
                    b'\xC7\x81\xF0\x0B\x00\x00\xE7\x03\x00\x00'
                    b'\x48\x8B\x0C\x08'
                    b'\xB8\x01\x00\x00\x00'
                    b'\x48\x89\x4A\x18\xC3'),
                args=(('base1', 8), 's_inf_energy', 's_inf_vigour', 's_inf_health', 's_inf_skill', 's_inf_hit',
                    's_add_atk', 's_add_def', 's_add_critical_buff', 's_add_critical'),
                inserted=True, replace_offset=8, replace_len=14, fuzzy=True),
            # AssemblyItem('suit_keep', '护甲不减', b'\x2B\xE8\x39\xAE\xB4\x0B\x00\x00',
            #     0x33A000, 0x33B000, b'\x90\x90', replace_len=2),
            # AssemblyItem('ammo_999', '装填弹药999', b'\x89\x9C\xBE\x30\x06\x00\x00\x5F\x5E\x5B',
            #     0x21A000, 0x220000, b'', b'\xC7\x84\xBE\x30\x06\x00\x00\xE7\x03\x00\x00',
            #     inserted=True, replace_len=7),
            # AssemblyItem('no_reload_crossbow', '十字弩不用换弹', b'\x89\x9E\xC4\x04\x00\x00\x8D\x54\x24\x24',
            #     0x15E000, 0x160000, NOP_6),
            AssemblySwitch('s_inf_energy', '无限体力'),
            AssemblySwitch('s_inf_vigour', '无限元气'),
            AssemblySwitch('s_inf_health', '无限元精'),
            AssemblySwitch('s_inf_skill', '无限战意技'),
            AssemblySwitch('s_inf_hit', '无限连击'),
            AssemblySwitch('s_add_atk', '增强攻击'),
            AssemblySwitch('s_add_def', '增加防御'),
            AssemblySwitch('s_add_critical_buff', '增强暴击伤害加成'),
            AssemblySwitch('s_add_critical', '增强暴击率'),
        )
        super().render_assembly_functions(functions)

    def _global(self):
        self._globalins.addr = self.get_variable_value('base1')
        return self._globalins

    # def get_hotkeys(self):
    #     this = self.weak
    #     return (
    #         (0, VK.H, this.pull_through),
    #     )

    # def pull_through(self):
    #     self.toggle_assembly_button('health_inf')
