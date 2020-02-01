from functools import partial
from lib.hack.forms import Group, StaticGroup, ModelCheckBox, ModelInput, ModelSelect, ModelCoordWidget
from lib.hack.handlers import MemHandler
from lib.win32.keys import VK
from lib import ui
from tools.base.assembly_hacktool import (
    AssemblyHacktool, AssemblyItem, AssemblyItems, AssemblySwitch, VariableType, SimpleButton
)
from tools.base import assembly_code
from . import models


class Main(AssemblyHacktool):
    CLASS_NAME = 'VVideoClass'
    WINDOW_NAME = None

    def __init__(self):
        super().__init__()
        self.handler = MemHandler()
        self._global_ins = models.Global(0, self.handler)
        self._movement_ins = models.Movement(0, self.handler)

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
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_buttons_own)

        # with Group("movement", "移动", (self._movement, models.Movement)):
        #     ModelInput("air_time")
        #     ModelInput("jump_height")
        #     ModelInput("move_speed_mult")
        #     ModelCoordWidget('coord', savable=True)

        with Group("movement", "变量", self.variable_model):
            ModelInput("jump_height", "跳跃高度")

    def render_assembly_buttons_own(self):
        self.render_assembly_buttons((
            AssemblyItem('base', '开启', b'\x04\x00\x00\x00\x48***\x48\x8b\x0c\x01',
                0x137500, 0x137800, b'',
                assembly_code.AssemblyGroup(
                    b'\x41\x81\xFC\xFF\xFF\xFF\xFF'
                    b'\x0F\x85\x02\x01\x00\x00'
                    b'\x3D\xE0\x0A\x00\x00'
                    b'\x0F\x85\xF7\x00\x00\x00'
                    b'\x48\x89\x0D', assembly_code.Offset('base1'),
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

            AssemblyItem('base_move', '开启移动相关', b'\x48\x8B\xFA\x48\x8B\xD9\x66\x0F\x6E\xC0\x0F\x5B\xC0\x0F\x2E\xC6',
                0x1E0D00, 0x1E1000, b'',
                assembly_code.AssemblyGroup(
                    assembly_code.ORIGIN,
                    b'\x48\x89\x3D', assembly_code.Offset('base_move'),
                ),
                args=(('base_move', 8),),
                inserted=True, replace_len=16),
            AssemblyItem('base_move', '超级跳跃', b'\x48\x85\xC0\x74\x0B\xF3\x0F\x11\x48\x34\xB8\x01\x00\x00\x00\xC3',
                0x1B4C00, 0x1B4E00, b'',
                assembly_code.AssemblyGroup(
                    b'\x48\x85\xC0\x74\x1A\x50\xA1', assembly_code.Variable('jump_height'),
                    b'\x66\x0F\x6E\xC8\x58\xF3\x0F\x11\x48\x34\xB8\x01\x00\x00\x00\xC3'
                ),
                args=(VariableType('jump_height', type=float, value=1000.0),), inserted=True),
            AssemblySwitch('s_inf_energy', '无限体力'),
            AssemblySwitch('s_inf_vigour', '无限元气'),
            AssemblySwitch('s_inf_health', '无限元精'),
            AssemblySwitch('s_inf_skill', '无限战意技'),
            AssemblySwitch('s_inf_hit', '无限连击'),
            AssemblySwitch('s_add_atk', '增强攻击'),
            AssemblySwitch('s_add_def', '增加防御'),
            AssemblySwitch('s_add_critical_buff', '增强暴击伤害加成'),
            AssemblySwitch('s_add_critical', '增强暴击率'),
        ))

    def _global(self):
        self._global_ins.addr = self.get_variable_value('base1')
        return self._global_ins

    def _movement(self):
        self._movement_ins.addr = self.get_variable_value('base_move')
        return self._movement_ins

    def get_hotkeys(self):
        this = self.weak
        return (
            (0, VK.U, this.pull_through),
        )

    def pull_through(self):
        self._global_ins.health = 2346
