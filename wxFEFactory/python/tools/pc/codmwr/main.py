from lib.hack.forms import Group, StaticGroup, ModelCheckBox, ModelInput, ModelSelect, Choice
from lib.win32.keys import VK
from tools.base.assembly_hacktool import (
    AssemblyHacktool, AssemblyItem, AssemblyItems, AssemblySwitch, VariableType, Delta
)
from . import assembly, models


class Main(AssemblyHacktool):
    CLASS_NAME = 'H1'
    WINDOW_NAME = 'Call of Duty? Modern Warfare?Remastered'
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
            # (0, VK.H, self.pull_through),
            # (0, VK.P, self.challenge_points_add),
            # (0, VK.T, self.toggle_challenge_time),
            # (0, VK._0, self.clear_hot_level),
        )

    def on_version_change(self, lb):
        self.version = lb.text

    def pull_through(self):
        self.toggle_assembly_function('inf_health')
