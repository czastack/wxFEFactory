from functools import partial
from lib.hack.forms import Group, StaticGroup, Input, ModelInput, ModelCoordWidget
from lib.win32.sendkey import auto, TextVK
from styles import dialog_style, styles
from . import address, models, coords
from .datasets import SLOT_NO_AMMO, WEAPON_LIST, VEHICLE_LIST
from .models import Player, Vehicle
from .script import RunningScript
from ..gta_base.widgets import WeaponWidget
from ..gta3_base.main import BaseGTA3Tool
from fefactory_api import ui
import math
import os
import json
import time
import __main__


class Main(BaseGTA3Tool):
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
        player = self.weak._player
        vehicle = self.weak._vehicle
        with Group("player", "角色", player, handler=self.handler):
            ModelInput("hp", "生命")
            ModelInput("ap", "防弹衣")
            ModelInput("rotation", "旋转")
            self.coord_view = ModelCoordWidget("coord", "坐标", savable=True, preset=coords)
            ModelCoordWidget("speed", "速度")
            ModelInput("weight", "重量")
            ModelInput("wanted_level", "通缉等级")
            ui.Hr()
            with ui.GridLayout(cols=5, vgap=10, className="expand"):
                ui.Button(label="车坐标->人坐标", onclick=self.from_vehicle_coord)
                ui.ToggleButton(label="切换无伤状态", onchange=self.set_ped_invincible)
        with Group("vehicle", "汽车", vehicle, handler=self.handler):
            ModelInput("hp", "HP")
            ModelCoordWidget("roll", "滚动")
            ModelCoordWidget("dir", "方向")
            self.vehicle_coord_view = ModelCoordWidget("coord", "坐标", savable=True, preset=coords)
            ModelCoordWidget("speed", "速度")
            ModelInput("weight", "重量")
            ui.Hr()
            with ui.GridLayout(cols=5, vgap=10, className="expand"):
                ui.Button(label="人坐标->车坐标", onclick=self.from_player_coord)
                ui.ToggleButton(label="切换无伤状态", onchange=self.set_vehicle_invincible)
                ui.Button(label="锁车", onclick=self.vehicle_lock_door)
                ui.Button(label="开锁", onclick=partial(self.vehicle_lock_door, lock=False))

        with Group("weapon", "武器槽", None, handler=self.handler):
            self.weapon_views = []
            for i in range(1, 13):
                self.weapon_views.append(WeaponWidget(player, "weapon%d" % i, "武器槽%d" % i, i,
                    SLOT_NO_AMMO, WEAPON_LIST))

            ui.Button(label="一键最大", onclick=self.weapon_max)

        with Group("global", "全局", 0, handler=self.handler):
            Input("money", "金钱", address.MONEY)

        with StaticGroup("快捷键"):
            with ui.Horizontal(className="fill container"):
                self.spawn_vehicle_id_view = ui.ListBox(className="expand", onselect=self.on_spawn_vehicle_id_change,
                    choices=(item[0] for item in VEHICLE_LIST))
                with ui.ScrollView(className="fill container"):
                    self.render_common_text()

        with StaticGroup("测试"):
            with ui.GridLayout(cols=4, vgap=10, className="expand"):
                self.render_common_button()
                self.set_buttons_contextmenu()

        with Group(None, "工具", 0, flexgrid=False, hasfooter=False):
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
        fix_addr = None

        if not self.native_call_auto(address.FUNC_IsBoatModel, 'L', model_id) & 0xFF:
            fix_addr = address.FUNC_CAutomobile__Fix

        if fix_addr:
            self.native_call_auto(fix_addr, None, this=vehicle.addr)

    def get_camera_rot(self):
        return self.read_vector(address.CAMERA_FRONT)

    def get_enemys(self):
        """获取敌人标记的peds"""
        return (blip.entity for blip in self.get_target_blips(self.models.Marker.MARKER_COLOR_LIGHT_GREEN))

    def teleport_to_blip(self, blip):
        if blip.bright:
            return super().teleport_to_blip(blip)
