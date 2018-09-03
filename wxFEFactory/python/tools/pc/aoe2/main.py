from functools import partial
from lib.hack.forms import Group, ModelCheckBox, ModelInput, ModelSelect
from lib.hack.handlers import MemHandler
from lib.win32.keys import VK
from tools.hacktool import BaseHackTool
from fefactory_api import ui
from . import models


class Main(BaseHackTool):
    CLASS_NAME = WINDOW_NAME = 'Age of Empires II Expansion'

    def __init__(self):
        super().__init__()
        self.handler = MemHandler()
        self._global = models.Global(0, self.handler)

    def render_main(self):
        with Group("global", "全局", (self._resources, models.ResourceManager), handler=self.handler):
            ModelInput("food")
            ModelInput("wood")
            ModelInput("rock")
            ModelInput("gold")

        with Group("population", "人口", (self._population_mgr, models.PopulationManager), handler=self.handler):
            ModelInput("current")
            ModelInput("total")

        with Group("unit", "选中单位", self._global, handler=self.handler):
            pass

    def onattach(self):
        super().onattach()
        self._global.addr = self.handler.base_addr

    def get_hotkeys(self):
        this = self.weak
        return (
            (VK.MOD_ALT, VK.H, this.pull_through),
        )

    def _resources(self):
        if self.handler.active:
            return self._global.resources

    def _population_mgr(self):
        if self.handler.active:
            return self._global.population_mgr

    resources = property(_resources)

    def pull_through(self, _=None):
        _global = self._global
