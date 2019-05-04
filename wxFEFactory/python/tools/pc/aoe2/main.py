from functools import partial
from lib.exui.controls import SearchListBox
from lib.hack.forms import Group, StaticGroup, ModelCheckBox, ModelInput, ModelSelect, ModelCoordWidget
from lib.hack.handlers import MemHandler
from lib.win32.keys import VK
from tools.base.native_hacktool import NativeHacktool
from fefactory_api import ui
from . import models, datasets
import base64


class Main(NativeHacktool):
    CLASS_NAME = WINDOW_NAME = 'Age of Empires II Expansion'

    FUNC_CREATE_UNIT = base64.b64decode(b'VYvsoaASeQBWV2oAi4AkBAAAagJqAYPsCItATMdEJAQAAIC/i3AEuGB+VgDHBCQAAIC/am2LTnj/'
        b'0Iv4hf90PotXQIvOiwZqAVL/dzyLgKwAAABS/3UI/9CL8GoAV4vOixaLkuAAAAD/0mgAAIC/aAAAgL9WuOCwTACLz//QX15dww==')

    def __init__(self):
        super().__init__()
        self.handler = MemHandler()
        self._global = models.Global(0, self.handler)

    def render_main(self):
        with Group("global", "全局", (self._resources, models.ResourceManager)):
            ModelInput("food")
            ModelInput("wood")
            ModelInput("rock")
            ModelInput("gold")

        with Group("population", "人口", (self._population_mgr, models.PopulationManager)):
            ModelInput("current")
            ModelInput("total")
            ModelInput("max")

        with Group("unit", "选中单位", (self._unit, models.Unit)):
            ModelInput("hp")
            ModelInput("resource")
            ModelInput("selected")
            ModelInput("construction_progress")

        self.lazy_group(Group("unit", "选中单位兵种", (self._unit_type, models.UnitType), cols=4),
            self.render_unit_type)
        self.lazy_group(StaticGroup("选中单位兵种攻防"), self.render_unit_type_atk_def)
        self.lazy_group(StaticGroup("快捷键"), self.render_hotkeys)
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
        ModelInput("range_min")
        ModelInput("range_max")
        ModelInput("range_base")
        ModelInput("damage_radius")
        ModelSelect("damage_type", choices=datasets.DAMAGE_TYPE)
        ModelInput("atk_interval")
        ModelInput("atk_interval2")
        ModelInput("construction_time")
        ModelInput("thrown_object")
        ModelInput("addition_thrown_object")
        ModelInput("min_thrown_object_count")
        ModelCoordWidget("thrown_object_area", savable=False, wrap=True)

    def render_unit_type_atk_def(self):
        AtkDefItemsMgr(self.weak, '攻击', 'atk_items').render()
        AtkDefItemsMgr(self.weak, '防御', 'def_items').render()

    def render_hotkeys(self):
        with ui.Horizontal(className="fill"):
            SearchListBox(className="expand",
                choices=(item[1] for item in datasets.UNITS),
                onselect=self.on_spawn_unit_type_change)
            ui.Text("选中单位恢复HP: alt+h\n"
                "选中建筑完成修建: alt+b\n"
                "选中单位死亡: alt+delete\n"
                "选中单位投诚: alt+f\n"
                "生成指定兵种单位: alt+v", className="padding")

    def render_functions(self):
        super().render_functions(('all_map', 'no_fog', 'get_car', 'fly_dog', 'angry_boy',
            'create_all_unit'))

    def onattach(self):
        super().onattach()
        self._global.addr = self.handler.base_addr
        self._create_unit = self.handler.write_function(self.FUNC_CREATE_UNIT)

    def ondetach(self):
        super().ondetach()
        self.handler.free_memory(self._create_unit)

    def get_hotkeys(self):
        this = self.weak
        return (
            (VK.MOD_ALT, VK.H, this.pull_through),
            (VK.MOD_ALT, VK.B, this.selected_finish),
            (VK.MOD_ALT, VK.DELETE, this.selected_die),
            (VK.MOD_ALT, VK.F, this.selected_join),
            (VK.MOD_ALT, VK.V, this.create_selected_unit_type),
        )

    def _resources(self):
        """资源管理器"""
        if self.handler.active:
            return self._global.player.resources

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

    def create_unit(self, type):
        """创作指定类别单位"""
        if self.handler.active:
            self.handler.remote_call(self._create_unit, type)

    def pull_through(self):
        """选中单位恢复HP"""
        for unit in self.selected_units:
            unit.hp = unit.type.hp_max

    def selected_finish(self):
        """选中单位完成建造"""
        unit = self._adv_selected_unit
        if unit:
            unit_type = unit.type
            unit.construction_progress = unit_type.construction_time
            unit.hp = unit_type.hp_max

    def selected_die(self):
        """选中单位死亡"""
        unit = self._adv_selected_unit
        if unit:
            unit.hp = 0

    def selected_join(self):
        """选中单位投诚"""
        unit = self._adv_selected_unit
        if unit:
            unit.player = self._global.player

    def on_spawn_unit_type_change(self, view):
        self._spawn_unit_type = datasets.UNITS[view.index][0]

    def create_selected_unit_type(self):
        """生成单位"""
        type = getattr(self, '_spawn_unit_type', None)
        if type:
            self.create_unit(type)

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

    def create_all_unit(self, _):
        """生成全部单位"""
        for item in datasets.UNITS:
            self.create_unit(item[0])


class AtkDefItemsMgr:
    """攻击防御项管理器"""
    def __init__(self, owner, label, items_key):
        self.owner = owner
        self.label = label
        self.items_key = items_key

    def render(self):
        with ui.Horizontal(className="fill padding"):
            self.listbox = ui.ListBox(className="expand", style={'width': 400},
                onselect=self.on_listbox_change)
            with Group(None, None, (self.get_item, models.AtkDefItem),
                    handler=self.owner.handler, hasfooter=False) as group:
                self.group = group
                ModelSelect("type", "%s类型" % self.label, choices=datasets.ATK_TYPES)
                ModelInput("value", "%s力" % self.label)
                ui.Hr()
                ui.Button("读取列表", onclick=self.read_list)

    def on_listbox_change(self, _):
        self.group.read()

    def read_list(self, _):
        """读取选中单位兵种攻击项列表"""
        result = []
        unit_type = self.owner._unit_type()
        if unit_type:
            for item in getattr(unit_type, self.items_key).items:
                item_type = item.type
                if not item_type:
                    break
                if 0 < item_type < len(datasets.ATK_TYPES):
                    result.append("类别: %s, 值: %d" % (datasets.ATK_TYPES[item_type], item.value))
                else:
                    result.append("类别: %d, 值: %d" % (item_type, item.value))
            self.listbox.setItems(result)

    def get_item(self):
        unit_type = self.owner._unit_type()
        if unit_type:
            return getattr(unit_type, self.items_key).items[self.listbox.index]
