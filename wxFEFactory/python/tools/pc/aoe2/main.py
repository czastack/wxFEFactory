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
            ModelInput("construction_progress")

        with Group("unit", "选中单位兵种", (self._unit_type, models.UnitType), handler=self.handler, cols=4):
            ModelInput("hp_max")
            ModelInput("view")
            ModelInput("collision")
            ModelInput("move_speed")
            ModelInput("search")
            ModelInput("work_efficiency")
            ModelInput("base_def")
            ModelInput("base_atk")
            ModelInput("atk")
            ModelInput("atk2")
            ModelInput("atk3")
            ModelInput("short_def")
            ModelInput("far_def")
            ModelInput("range_min")
            ModelInput("range_max")
            ModelInput("range_base")
            ModelInput("damage_radius")
            ModelInput("damage_type")
            ModelInput("atk_spped")
            ModelInput("construction_time")

    def onattach(self):
        super().onattach()
        self._global.addr = self.handler.base_addr

    def get_hotkeys(self):
        this = self.weak
        return (
            (VK.MOD_ALT, VK.H, this.pull_through),
            (VK.MOD_ALT, VK.B, this.select_finish),
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

    @property
    def _adv_selected_unit(self):
        handler = self.handler
        if handler.active:
            ptr = handler.read32(handler.base_addr + 0x003912A0)
            v1 = handler.read32(ptr + 0x424)
            v3 = handler.read16(v1 + 0x94)
            addr = handler.read32(handler.read32(v1 + 0x4C) + 4 * v3)
            addr = handler.read32(addr + 0x01C0)
            return models.Unit(addr, handler)

    def pull_through(self, _):
        for unit in self.selected_units:
            unit.hp = unit.type.hp_max

    def select_finish(self, _):
        """选中单位完成建造"""
        unit = self._adv_selected_unit
        if unit:
            unit_type = unit.type
            unit.construction_progress = unit_type.construction_time
            unit.hp = unit_type.hp_max
