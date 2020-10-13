from lib.hack.forms import Group, StaticGroup, ModelCheckBox, ModelInput, ModelSelect, Choice
from lib.win32.keys import VK
from tools.base.assembly_hacktool import (
    AssemblyHacktool, AssemblyItem, AssemblyItems, VariableSwitch, VariableType, Delta
)
from . import assembly, models


class Main(AssemblyHacktool):
    CLASS_NAME = 'H2'
    WINDOW_NAME = 'Call of Duty®: Modern Warfare® 2 Campaign Remastered'
    assembly_address_sources = assembly.ADDRESS_SOURCES

    def __init__(self):
        super().__init__()
        self.version = ''
        # self._global = models.Global(0, self.handler)

    def render_main(self):
        # with Group("group", "全局", None):
        #     self.render_global()
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_buttons_own)

    def render_global(self):
        Choice("版本", ADDRESS_SOURCES.keys(), self.on_version_change)

    def render_assembly_buttons_own(self):
        self.render_assembly_buttons(assembly.ASSEMBLY_ITEMS)

    def get_hotkeys(self):
        return (
            (0, VK.H, self.toggle_health),
            (VK.MOD_ALT, VK.R, self.toggle_no_reload),
            (VK.MOD_ALT, VK.V, self.toggle_bullet_time),
            (VK.MOD_ALT, VK.B, self.toggle_super_speed),
        )

    def on_version_change(self, lb):
        self.version = lb.text

    def toggle_health(self):
        self.toggle_assembly_function('inf_health')

    def toggle_no_reload(self):
        self.toggle_assembly_function('no_reload')

    def toggle_super_speed(self):
        self.toggle_assembly_function('super_speed')

    def toggle_bullet_time(self):
        self.toggle_assembly_function('bullet_time')
