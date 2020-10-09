from lib.hack.forms import Group, StaticGroup, ModelCheckBox, ModelInput, ModelSelect, Choice
from lib.win32.keys import VK
from tools.base.assembly_hacktool import AssemblyHacktool
from . import assembly, models


class Main(AssemblyHacktool):
    CLASS_NAME = 'JC4'
    WINDOW_NAME = 'Just Cause 4'
    assembly_address_sources = assembly.ADDRESS_SOURCES

    def render_main(self):
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_buttons_own)

    def render_global(self):
        self.version_view = Choice("版本", assembly.ADDRESS_SOURCES.keys(), self.on_version_change)

    def render_assembly_buttons_own(self):
        self.render_assembly_buttons(assembly.ASSEMBLY_ITEMS)

    def get_hotkeys(self):
        this = self.weak
        return (
            # (0, VK.H, this.pull_through),
            # (0, VK.P, this.challenge_points_add),
            # (0, VK.T, this.toggle_challenge_time),
            # (0, VK._0, this.clear_hot_level),
            (0, VK.CAPSLOCK, lambda: this.toggle_assembly_function('ammo_keep')),
            (VK.MOD_ALT, VK.CAPSLOCK, lambda: this.toggle_assembly_function('wing_inf_boost')),
            (VK.MOD_ALT, VK.A, lambda: this.toggle_assembly_function('no_reload')),
        )

    def on_version_change(self, lb):
        self.version = lb.text

    def pull_through(self):
        self.toggle_assembly_function('inf_health')

    def challenge_points_add(self):
        self.set_variable_value('challenge_points_add', 1)

    def toggle_challenge_time(self):
        self.toggle_assembly_function('challenge_time')

    def clear_hot_level(self):
        self.toggle_assembly_function('clear_hot_level')
