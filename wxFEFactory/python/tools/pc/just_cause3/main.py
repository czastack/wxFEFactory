from lib.hack.forms import Group, StaticGroup, ModelInput, ModelSelect
from lib.hack.handlers import MemHandler
from lib.win32.keys import VK
from tools.base.assembly_hacktool import AssemblyHacktool
from . import assembly


class Main(AssemblyHacktool):
    CLASS_NAME = 'JC3'
    WINDOW_NAME = 'Just Cause 3'

    def __init__(self):
        super().__init__()
        self.handler = MemHandler()
        # self._global = models.Global(0, self.handler)

    def render_main(self):
        # with Group("global", "全局", self._global):
        #     pass
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_buttons_own)

    def render_assembly_buttons_own(self):
        self.render_assembly_buttons(assembly.ASSEMBLY_ITEMS)

    def get_hotkeys(self):
        this = self.weak
        return (
            (0, VK.H, this.pull_through),
            (0, VK.P, this.challenge_points_add),
            (0, VK.T, this.toggle_challenge_time),
            (0, VK._0, this.clear_hot_level),
        )

    def pull_through(self):
        self.toggle_assembly_function('inf_health')

    def challenge_points_add(self):
        self.set_variable_value('challenge_points_add', 1)

    def toggle_challenge_time(self):
        self.toggle_assembly_function('challenge_time')

    def clear_hot_level(self):
        self.toggle_assembly_function('clear_hot_level')
