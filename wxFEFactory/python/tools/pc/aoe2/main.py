from functools import partial
from lib.hack.forms import Group, StaticGroup, ModelCheckBox, ModelInput, ModelSelect
from lib.hack.handlers import MemHandler
from lib.win32.keys import VK
from tools.native_hacktool import NativeHacktool
from fefactory_api import ui
from . import models


class Main(NativeHacktool):
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

        self.lazy_group(Group("unit", "选中单位兵种", (self._unit_type, models.UnitType), handler=self.handler, cols=4),
            self.render_unit_type)
        self.lazy_group(StaticGroup("功能"), self.render_functions)

    def render_unit_type(self):
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

    def render_functions(self):
        super().render_functions(('all_map', 'no_fog', 'get_car', 'fly_dog', 'angry_boy'))

    def onattach(self):
        super().onattach()
        self._global.addr = self.handler.base_addr

    def get_hotkeys(self):
        this = self.weak
        return (
            (VK.MOD_ALT, VK.H, this.pull_through),
            (VK.MOD_ALT, VK.B, this.selected_finish),
            (VK.MOD_ALT, VK.DELETE, this.selected_die),
        )

    def _resources(self):
        """资源管理器"""
        if self.handler.active:
            return self._global.resources

    def _population_mgr(self):
        """人口管理器"""
        if self.handler.active:
            return self._global.player_mgr.population_mgr

    def _unit(self):
        """当前选中单位"""
        # if self.handler.active:
        #     return self._global.selected_units[0]
        return self._adv_selected_unit

    def _unit_type(self):
        """当前选中单位兵种"""
        if self.handler.active:
            unit = self._unit()
            return unit and unit.type

    resources = property(_resources)

    @property
    def selected_units(self):
        """选中的单位生成器"""
        for unit in self._global.selected_units:
            if not unit.addr:
                break
            if unit.selected:
                yield unit

    @property
    def _adv_selected_unit(self):
        """选中的单位(包括在建建筑)"""
        if self.handler.active:
            return self._global.player_mgr.adv_selected_unit

    def pull_through(self, _):
        """选中单位恢复HP"""
        for unit in self.selected_units:
            unit.hp = unit.type.hp_max

    def selected_finish(self, _):
        """选中单位完成建造"""
        unit = self._adv_selected_unit
        if unit:
            unit_type = unit.type
            unit.construction_progress = unit_type.construction_time
            unit.hp = unit_type.hp_max

    def selected_die(self, _):
        """选中单位死亡"""
        unit = self._adv_selected_unit
        if unit:
            unit.hp = 0

    def excute_cheet_code(self, code):
        """执行作弊代码
        0x75 地图全开
        0x76 去阴影
        0x7a 获得汽车
        0x7e 飞翔的狗狗
        0x7d 暴怒男孩
        """
        this = self._global.player_mgr.addr
        self.native_call_auto(0x42BDC0, '2L', 1, code, this=this)

    def all_map(self, _):
        """地图全开"""
        self.excute_cheet_code(0x75)

    def no_fog(self, _):
        """去阴影"""
        self.excute_cheet_code(0x76)

    def get_car(self, _):
        """获得汽车"""
        self.excute_cheet_code(0x7a)

    def fly_dog(self, _):
        """飞翔的狗狗"""
        self.excute_cheet_code(0x7e)

    def angry_boy(self, _):
        """暴怒男孩"""
        self.excute_cheet_code(0x7d)
