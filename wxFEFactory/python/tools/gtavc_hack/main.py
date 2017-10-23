from functools import partial
from lib.hack.form import Group, InputWidget, CheckBoxWidget, CoordWidget, ModelInputWidget, ModelCoordWidget
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
from lib.win32.sendkey import auto, TextVK
from commonstyle import dialog_style, styles
from . import address, models
from .models import Player, Vehicle
from .data import SLOT_NO_AMMO, WEAPON_LIST, VEHICLE_LIST
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
            ui.Text("")
            ui.Button(label="车坐标->人坐标", onclick=self.from_vehicle_coord)
        with Group("vehicle", "汽车", self._vehicle, handler=self.handler):
            self.vehicle_hp_view = ModelInputWidget("hp", "HP")
            self.vehicle_roll_view = ModelCoordWidget("roll", "滚动")
            self.vehicle_dir_view = ModelCoordWidget("dir", "方向")
            self.vehicle_coord_view = ModelCoordWidget("coord", "坐标", savable=True)
            self.vehicle_speed_view = ModelCoordWidget("speed", "速度")
            self.vehicle_turn_view = ModelCoordWidget("turn", "Turn")
            self.weight_view = ModelInputWidget("weight", "重量")
            ui.Text("")
            ui.Button(label="人坐标->车坐标", onclick=self.from_player_coord)

        with Group("weapon", "武器槽", None, handler=self.handler):
            self.weapon_views = []
            for i in range(11):
                self.weapon_views.append(
                    WeaponWidget("weapon%d" % i, "武器槽%d" % i, i, SLOT_NO_AMMO, WEAPON_LIST, self._player, self.on_weapon_change)
                )

        with Group("global", "全局", 0, handler=self.handler):
            self.money_view = InputWidget("money", "金钱", address.MONEY, (), int)
            self.camera_view = CoordWidget("camera", "摄像机", 0x7E46B8, ())
            self.camera_z_rot_view = InputWidget("camera_z_rot", "摄像机z_rot", 0x7E48CC, (), float)
            self.camera_x_rot_view = InputWidget("camera_x_rot", "摄像机x_rot", 0x7E48BC, (), float)

        with Group(None, "作弊", 0, handler=self.handler, flexgrid=False, hasfootbar=False):
            with ui.Vertical(className="fill container"):
                with ui.GridLayout(cols=4, vgap=10, className="fill container"):
                    CheckBoxWidget("god1", "角色无伤1", 0x5267DC, (), b'\xEB\x10', b'\x75\x15')
                    CheckBoxWidget("god2", "角色无伤2", 0x5267D5, (), b'\x90\x90', b'\x75\x1C')
                    CheckBoxWidget("vehicle_god1", "汽车无伤1", 0x5A9801, (), b'\xc7\x41\x04\x00\x00\x00\x00\xc2\x04', b'\x88\x41\x04\xc2\x04\x00\x00\x00\x00')
                    CheckBoxWidget("vehicle_god2", "汽车无伤2", 0x588A77, (), b'\x90\x90', b'\x75\x09')
                    CheckBoxWidget("infinite_run", "无限奔跑", 0x536F25, (), b'\xEB', b'\x75')
                    CheckBoxWidget("drive_on_water", "水上开车", 0x593908, (), b'\x90\x90', b'\x74\x07')
                    CheckBoxWidget("no_falling_off_the_bike", "摩托老司机", 0x61393D, (), b'\xE9\xBC\x0E\x00\x00\x90', b'\x0F\x84\xBB\x0E\x00\x90')
                    CheckBoxWidget("disable_vehicle_explosions", "不会爆炸", 0x588A77, (), b'\x90\x90', b'\x75\x09')
                    CheckBoxWidget("infinite_ammo1", "无限子弹1", 0x5D4ABE, (), b'\x90\x90\x90', b'\xFF\x4E\x08')
                    CheckBoxWidget("infinite_ammo2", "无限子弹2", 0x5D4AF5, (), b'\x90\x90\x90', b'\xFF\x4E\x0C')

        with Group(None, "快捷键", 0, handler=self.handler, flexgrid=False, hasfootbar=False):
            with ui.Horizontal(className="fill container"):
                self.spawn_vehicle_id_view = ui.ListBox(className="expand", onselect=self.on_spawn_vehicle_id_change, 
                    choices=(item[0] for item in VEHICLE_LIST))
                with ui.ScrollView(className="fill container"):
                    self.render_common_text()
                    ui.Text("附近车辆爆炸(使用秘籍BIGBANG): alt+enter")

        with Group(None, "测试", 0, handler=self.handler, flexgrid=False, hasfootbar=False):
            with ui.GridLayout(cols=4, vgap=10, className="fill container"):
                self.render_common_button()
                ui.Button("瞬移到目的地(粉红)", onclick=partial(self.teleport_to_destination, color=5))
                ui.Button("瞬移到目的地(黄)", onclick=partial(self.teleport_to_destination, color=4))
                ui.Button("敌人爆炸", onclick=self.enemys_explode)

        with Group(None, "工具", 0, flexgrid=False, hasfootbar=False):
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

    def get_rotz(self):
        if self.isInVehicle:
            rotz = self.camera_z_rot_view.mem_value
        else:
            PI = math.pi
            HALF_PI = PI / 2
            rotz = self.rot_view.mem_value
            rotz += HALF_PI
            if rotz > PI:
                rotz += PI * 2
        return rotz

    def promptWrite(self, text):
        text = (text + '\0').encode('utf-16le')
        TEXT1_ADDR = 0x7D3E40
        TEXT2_ADDR = 0x939028
        
        self.handler.ptrsWrite(TEXT1_ADDR, (), text)
        time.sleep(0.01)
        self.handler.ptrsWrite(TEXT2_ADDR, (), text)

    def bigbang(self, _=None):
        self.inputCheat('bigbang')

    def get_camera_rot(self):
        rotz = self.camera_z_rot_view.mem_value
        cam_x = math.cos(rotz)
        cam_y = math.sin(rotz)
        cam_z = self.camera_x_rot_view.mem_value
        if not self.isInVehicle:
            cam_x = -cam_x
            cam_y = -cam_y
        return (cam_x, cam_y, cam_z)