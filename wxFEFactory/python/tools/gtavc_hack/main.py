from functools import partial
from lib.hack.form import Group, InputWidget, CheckBoxWidget, CoordWidget, ModelInputWidget, ModelCoordWidget
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
from lib.win32.sendkey import auto, TextVK
from styles import dialog_style, styles
from . import address, models
from .models import Player, Vehicle
from .datasets import SLOT_NO_AMMO, WEAPON_LIST, VEHICLE_LIST
from ..gta_base.widgets import WeaponWidget
from ..gta3_base.main import BaseGTA3Tool
from ..gta3_base.script import RunningScript
import math
import os
import json
import time
import __main__
import fefactory_api
ui = fefactory_api.ui


class Tool(BaseGTA3Tool):
    CLASS_NAME = 'Grand theft auto 3'
    WINDOW_NAME = 'GTA: Vice City'
    address = address
    models = models
    Player = Player
    Vehicle = Vehicle
    RunningScript = RunningScript
    MARKER_RANGE = 32
    SPHERE_RANGE = 16
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
            self.stamina_view = ModelInputWidget("stamina", "体力")
            self.wanted_level_view = ModelInputWidget("wanted_level", "通缉等级")
            self.money_view = InputWidget("money", "金钱", address.MONEY, (), int)
            ui.Hr()
            with ui.GridLayout(cols=5, vgap=10, className="expand"):
                ui.Button(label="车坐标->人坐标", onclick=self.from_vehicle_coord)
                ui.ToggleButton(label="切换无伤状态", onchange=self.set_ped_invincible)
        with Group("vehicle", "汽车", self._vehicle, handler=self.handler):
            self.vehicle_hp_view = ModelInputWidget("hp", "HP")
            self.vehicle_roll_view = ModelCoordWidget("roll", "滚动")
            self.vehicle_dir_view = ModelCoordWidget("dir", "方向")
            self.vehicle_coord_view = ModelCoordWidget("coord", "坐标", savable=True)
            self.vehicle_speed_view = ModelCoordWidget("speed", "速度")
            self.vehicle_turn_view = ModelCoordWidget("turn", "Turn")
            self.weight_view = ModelInputWidget("weight", "重量")
            ui.Hr()
            with ui.GridLayout(cols=5, vgap=10, className="expand"):
                ui.Button(label="人坐标->车坐标", onclick=self.from_player_coord)
                ui.ToggleButton(label="切换无伤状态", onchange=self.set_vehicle_invincible)
                ui.Button(label="锁车", onclick=self.vehicle_lock_door)
                ui.Button(label="开锁", onclick=partial(self.vehicle_lock_door, lock=False))

        with Group("weapon", "武器槽", None, handler=self.handler):
            self.weapon_views = []
            for i in range(11):
                self.weapon_views.append(
                    WeaponWidget(self._player, "weapon%d" % i, "武器槽%d" % i, i, SLOT_NO_AMMO, WEAPON_LIST, self.on_weapon_change)
                )

        with StaticGroup("作弊"):
            with ui.Vertical(className="fill container"):
                with ui.GridLayout(cols=4, vgap=10, className="fill container"):
                    CheckBoxWidget("infinite_run", "无限奔跑", 0x536F25, (), b'\xEB', b'\x75')
                    CheckBoxWidget("drive_on_water", "水上开车", 0x593908, (), b'\x90\x90', b'\x74\x07')
                    CheckBoxWidget("no_falling_off_the_bike", "摩托老司机", 0x61393D, (), b'\xE9\xBC\x0E\x00\x00\x90', b'\x0F\x84\xBB\x0E\x00\x90')
                    CheckBoxWidget("disable_vehicle_explosions", "不会爆炸", 0x588A77, (), b'\x90\x90', b'\x75\x09')
                    CheckBoxWidget("infinite_ammo1", "无限子弹1", 0x5D4ABE, (), b'\x90\x90\x90', b'\xFF\x4E\x08')
                    CheckBoxWidget("infinite_ammo2", "无限子弹2", 0x5D4AF5, (), b'\x90\x90\x90', b'\xFF\x4E\x0C')

        with StaticGroup("快捷键"):
            with ui.Horizontal(className="fill container"):
                self.spawn_vehicle_id_view = ui.ListBox(className="expand", onselect=self.on_spawn_vehicle_id_change, 
                    choices=(item[0] for item in VEHICLE_LIST))
                with ui.ScrollView(className="fill container"):
                    self.render_common_text()
                    ui.Text("附近车辆爆炸(使用秘籍BIGBANG): alt+enter")

        with StaticGroup("测试"):
            with ui.GridLayout(cols=4, vgap=10, className="fill container"):
                self.render_common_button()
                self.set_buttons_contextmenu()

        with StaticGroup("工具"):
            with ui.Vertical(className="fill container"):
                ui.Button("g3l坐标转json", onclick=self.g3l2json)

    def get_hotkeys(self):
        return (
            ('bigbang', MOD_ALT, getVK('enter'), self.bigbang),
        ) + self.get_common_hotkeys()

    def is_model_loaded(self, model_id):
        return self.handler.read8(address.MODEL_INFO + 20 * model_id) == 1

    def load_model(self, model_id):
        if model_id > 0 and not self.is_model_loaded(model_id):
            self.native_call_auto(address.FUNC_CStreaming__RequestModel, '2L', model_id, 0x16)
            self.native_call_auto(address.FUNC_LoadAllRequestedModels, 'L', 0)

    def on_weapon_change(self, weapon_view):
        self.load_model(weapon_view.selected_item[1])

    def get_yaw(self):
        yaw = self.handler.readFloat(address.CAMERA_ROTZ)
        if not self.isInVehicle:
            yaw = yaw - math.pi
        return yaw

    def get_camera_rot(self):
        return self.read_vector(address.CAMERA_FRONT)

    def promptWrite(self, text):
        text = (text + '\0').encode('utf-16le')
        TEXT1_ADDR = 0x7D3E40
        TEXT2_ADDR = 0x939028
        
        self.handler.ptrsWrite(TEXT1_ADDR, (), text)
        time.sleep(0.01)
        self.handler.ptrsWrite(TEXT2_ADDR, (), text)

    def bigbang(self, _=None):
        self.inputCheat('bigbang')

    def vehicle_fix(self, vehicle):
        """修车"""
        model_id = vehicle.model_id

        is_type = lambda addr: self.native_call_auto(addr, 'L', model_id) & 0xFF
        fix_addr = None

        if is_type(address.FUNC_IsCarModel):
            fix_addr = address.FUNC_CAutomobile__Fix
        elif is_type(address.FUNC_IsBikeModel):
            fix_addr = address.FUNC_CBike_Fix

        if fix_addr:
            self.native_call_auto(fix_addr, None, this=vehicle.addr)

    def get_enemys(self):
        """获取敌人标记的peds"""
        return (blip.entity for blip in self.get_target_blips(self.models.Marker.MARKER_COLOR_YELLOW))