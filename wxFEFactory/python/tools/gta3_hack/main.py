from functools import partial
from lib.hack.form import Group, InputWidget, CheckBoxWidget, CoordWidget, ModelInputWidget, ModelCoordWidget
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
from lib.win32.sendkey import auto, TextVK
from commonstyle import dialog_style, styles
from . import address, models
from .data import SLOT_NO_AMMO, WEAPON_LIST, VEHICLE_LIST
from .models import Player, Vehicle
from .script import RunningScript
from ..gta_base.widgets import WeaponWidget
from ..gta3_base.main import BaseGTA3Tool
import math
import os
import json
import time
import __main__
import fefactory_api
ui = fefactory_api.ui


class Tool(BaseGTA3Tool):
    CLASS_NAME = 'Grand theft auto 3'
    WINDOW_NAME = 'GTA3'
    address = address
    models = models
    Player = Player
    Vehicle = Vehicle
    RunningScript = RunningScript
    MARKER_RANGE = 32
    SAFE_SPEED_RATE = 0.3
    GO_FORWARD_COORD_RATE = 2.0
    DEST_DEFAULT_COLOR = 5
    VEHICLE_LIST = VEHICLE_LIST

    def render_main(self):
        with Group("player", "角色", self._player, handler=self.handler):
            self.hp_view = ModelInputWidget("hp", "生命")
            self.ap_view = ModelInputWidget("ap", "防弹衣")
            self.rot_view = ModelInputWidget("rotation", "旋转")
            self.coord_view = ModelCoordWidget("coord", "坐标", savable=True)
            self.speed_view = ModelCoordWidget("speed", "速度")
            self.weight_view = ModelInputWidget("weight", "重量")
            # self.stamina_view = InputWidget("stamina", "体力", None, (0x600,), float)
            self.wanted_level_view = InputWidget("wanted_level", "通缉等级", address.WANTED_BASE, (0x53c, 0x18), int)
            ui.Text("")
            ui.Button(label="车坐标->人坐标", onclick=self.from_vehicle_coord)
        with Group("vehicle", "汽车", self._vehicle, handler=self.handler):
            self.vehicle_hp_view = ModelInputWidget("hp", "HP")
            self.vehicle_roll_view = ModelCoordWidget("roll", "滚动")
            self.vehicle_dir_view = ModelCoordWidget("dir", "方向")
            self.vehicle_coord_view = ModelCoordWidget("coord", "坐标", savable=True)
            self.vehicle_speed_view = ModelCoordWidget("speed", "速度")
            self.weight_view = ModelInputWidget("weight", "重量")
            ui.Text("")
            with ui.Horizontal(className="expand"):
                ui.Button(label="人坐标->车坐标", onclick=self.from_player_coord)
                ui.Button(label="锁车", onclick=self.vehicle_lock_door)
                ui.Button(label="开锁", onclick=partial(self.vehicle_lock_door, lock=False))

        with Group("weapon", "武器槽", None, handler=self.handler):
            self.weapon_views = []
            for i in range(1, 13):
                self.weapon_views.append(WeaponWidget("weapon%d" % i, "武器槽%d" % i, i, SLOT_NO_AMMO, WEAPON_LIST, self._player))

            ui.Button(label="一键最大", onclick=self.weapon_max)

        with Group("global", "全局", 0, handler=self.handler):
            self.money_view = InputWidget("money", "金钱", address.MONEY, (), int)
            
        with Group(None, "快捷键", 0, handler=self.handler, flexgrid=False, hasfootbar=False):
            with ui.Horizontal(className="fill container"):
                self.spawn_vehicle_id_view = ui.ListBox(className="expand", onselect=self.on_spawn_vehicle_id_change, 
                    choices=(item[0] for item in VEHICLE_LIST))
                with ui.ScrollView(className="fill container"):
                    self.render_common_text()
        with Group(None, "测试", 0, handler=self.handler, flexgrid=False, hasfootbar=False):
            with ui.GridLayout(cols=4, vgap=10, className="fill container"):
                self.render_common_button()

        with Group(None, "工具", 0, flexgrid=False, hasfootbar=False):
            with ui.Vertical(className="fill container"):
                ui.Button("g3l坐标转json", onclick=self.g3l2json)

    def weapon_max(self, _=None):
        for v in self.weapon_views:
            v.id_view.index = 1
            if v.has_ammo:
                v.ammo_view.value = 9999

    def is_model_loaded(self, model_id):
        return self.script_call(0x247, 'L', model_id)

    def load_model(self, model_id):
        if model_id > 0 and not self.is_model_loaded(model_id):
            self.script_call(0x248, 'L', model_id)
            self.script_call(0x38b, None)

    def vehicle_fix(self, vehicle):
        """修车"""
        model_id = vehicle.model_id

        is_type = lambda addr: self.native_call_auto(addr, 'L', model_id) & 0xFF
        fix_addr = None

        if not is_type(address.FUNC_IsBoatModel):
            fix_addr = address.FUNC_CAutomobile__Fix

        if fix_addr:
            self.native_call_auto(fix_addr, None, this=vehicle.addr)

    def get_camera_rot(self):
        return self.read_vector(address.CAMERA_FRONT)

    def get_enemys(self):
        """获取敌人标记的peds"""
        return (blip.entity for blip in self.get_target_blips(self.models.Marker.MARKER_COLOR_LIGHT_GREEN))