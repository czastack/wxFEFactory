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
            ModelInput("max")

        with Group("unit", "选中单位", (self._unit, models.Unit), handler=self.handler):
            ModelInput("hp")
            ModelInput("resource")
            ModelInput("selected")

        with Group("unit", "选中单位兵种", (self._unit_type, models.UnitType), handler=self.handler):
            ModelInput("hp_max")
            ModelInput("view")
            ModelInput("collision")
            ModelInput("move_speed")
            ModelInput("search")
            ModelInput("work_efficiency")
            ModelInput("short_defense")
            ModelInput("far_defense")
            ModelInput("atk")
            ModelInput("range_max")
            ModelInput("damage_radius")
            ModelInput("damage_type")
            ModelInput("atk_spped")
            ModelInput("range_min")

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

    def _unit(self):
        if self.handler.active:
            return self._global.selected_units[0]

    def _unit_type(self):
        if self.handler.active:
            unit = self._unit()
            return unit and unit.type

    resources = property(_resources)

    @property
    def selected_units(self):
        for unit in self._global.selected_units:
            if not unit.addr:
                break
            if unit.selected:
                yield unit

    def pull_through(self, _=None):
        _global = self._global
