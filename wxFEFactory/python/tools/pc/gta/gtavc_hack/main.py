import math
import os
import json
import time
import __main__
from functools import partial
from lib.hack.forms import Group, StaticGroup, Input, SimpleCheckBox, ModelInput, ModelCoordWidget
from lib.win32.keys import VK
from lib.win32.sendkey import auto, TextVK
from styles import dialog_style, styles
from fefactory_api import ui
from ..gta_base.widgets import WeaponWidget
from ..gta3_base.main import BaseGTA3Tool
from ..gta3_base.script import RunningScript
from . import address, models, coords
from .models import Player, Vehicle
from .datasets import SLOT_NO_AMMO, WEAPON_LIST, VEHICLE_LIST


class Main(BaseGTA3Tool):
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
        with Group("player", "角色", self.weak._player):
            self.render_player()

        self.lazy_group(Group("vehicle", "载具", self.weak._vehicle), self.render_vehicle)
        self.lazy_group(Group("weapon", "武器槽", None), self.render_weapon)
        self.lazy_group(StaticGroup("作弊"), self.render_cheat)
        self.lazy_group(StaticGroup("快捷键"), self.render_hotkey)
        self.lazy_group(StaticGroup("功能"), self.render_func)
        self.lazy_group(StaticGroup("工具"), self.render_tool)

    def render_player(self):
        ModelInput("hp", "生命")
        ModelInput("ap", "防弹衣")
        ModelInput("rotation", "旋转")
        self.coord_view = ModelCoordWidget("coord", "坐标", savable=True, preset=coords)
        ModelCoordWidget("speed", "速度")
        ModelInput("weight", "重量")
        ModelInput("stamina", "体力")
        ModelInput("wanted_level", "通缉等级")
        Input("money", "金钱", address.MONEY)
        ui.Hr()
        with ui.GridLayout(cols=5, vgap=10, className="expand"):
            ui.Button(label="车坐标->人坐标", onclick=self.from_vehicle_coord)
            ui.ToggleButton(label="切换无伤状态", onchange=self.set_ped_invincible)

    def render_vehicle(self):
        ModelInput("hp", "HP")
        ModelCoordWidget("roll", "滚动")
        ModelCoordWidget("dir", "方向")
        self.vehicle_coord_view = ModelCoordWidget("coord", "坐标", savable=True, preset=coords)
        ModelCoordWidget("speed", "速度")
        ModelCoordWidget("turn", "Turn")
        ModelInput("weight", "重量")
        ui.Hr()
        with ui.GridLayout(cols=5, vgap=10, className="expand"):
            ui.Button(label="人坐标->车坐标", onclick=self.from_player_coord)
            ui.ToggleButton(label="切换无伤状态", onchange=self.set_vehicle_invincible)
            ui.Button(label="锁车", onclick=self.vehicle_lock_door)
            ui.Button(label="开锁", onclick=partial(self.vehicle_lock_door, lock=False))

    def render_weapon(self):
        player = self.weak._player
        self.weapon_views = []
        for i in range(11):
            self.weapon_views.append(
                WeaponWidget(player, "weapon%d" % i, "武器槽%d" % i, i, SLOT_NO_AMMO, WEAPON_LIST,
                    self.on_weapon_change)
            )

    def render_cheat(self):
        with ui.Vertical(className="fill padding"):
            with ui.GridLayout(cols=4, vgap=10, className="expand"):
                SimpleCheckBox("infinite_run", "无限奔跑", 0x536F25, (), b'\xEB', b'\x75')
                SimpleCheckBox("drive_on_water", "水上开车", 0x593908, (), b'\x90\x90', b'\x74\x07')
                SimpleCheckBox("no_falling_off_the_bike", "摩托老司机", 0x61393D, (),
                    b'\xE9\xBC\x0E\x00\x00\x90', b'\x0F\x84\xBB\x0E\x00\x90')
                SimpleCheckBox("disable_vehicle_explosions", "不会爆炸", 0x588A77, (), b'\x90\x90', b'\x75\x09')
                SimpleCheckBox("infinite_ammo1", "无限子弹1", 0x5D4ABE, (), b'\x90\x90\x90', b'\xFF\x4E\x08')
                SimpleCheckBox("infinite_ammo2", "无限子弹2", 0x5D4AF5, (), b'\x90\x90\x90', b'\xFF\x4E\x0C')

    def render_hotkey(self):
        with ui.Horizontal(className="fill padding"):
            self.spawn_vehicle_id_view = ui.ListBox(className="expand",
                onselect=self.on_spawn_vehicle_id_change,
                choices=(item[0] for item in VEHICLE_LIST))
            with ui.ScrollView(className="fill padding"):
                self.render_common_text()
                ui.Text("附近车辆爆炸(使用秘籍BIGBANG): alt+enter")

    def render_func(self):
        with ui.GridLayout(cols=4, vgap=10, className="expand"):
            self.render_common_button()
            self.set_buttons_contextmenu()

    def render_tool(self):
        with ui.Vertical(className="fill padding"):
            ui.Button("g3l坐标转json", onclick=self.g3l2json)

    def get_hotkeys(self):
        return (
            (VK.MOD_ALT, VK.ENTER, self.bigbang),
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
        yaw = self.handler.read_float(address.CAMERA_ROTZ)
        if not self.isInVehicle:
            yaw = yaw - math.pi
        return yaw

    def get_camera_rot(self):
        return self.read_vector(address.CAMERA_FRONT)

    def promptWrite(self, text):
        text = (text + '\0').encode('utf-16le')
        TEXT1_ADDR = 0x7D3E40
        TEXT2_ADDR = 0x939028

        self.handler.ptrs_write(TEXT1_ADDR, (), text)
        time.sleep(0.01)
        self.handler.ptrs_write(TEXT2_ADDR, (), text)

    def bigbang(self):
        self.inputCheat('bigbang')

    def vehicle_fix(self, vehicle):
        """修车"""
        model_id = vehicle.model_id

        def is_type(addr):
            return self.native_call_auto(addr, 'L', model_id) & 0xFF

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
