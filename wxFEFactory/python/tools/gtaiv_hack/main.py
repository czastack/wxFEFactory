from functools import partial
from lib.hack.form import Group, InputWidget, CheckBoxWidget, CoordWidget, ModelInputWidget, ModelCoordWidget
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
from lib.win32.sendkey import auto, TextVK
from lib import utils
from commonstyle import dialog_style, styles
from ..gta_base.main import BaseGTATool
from ..gta_base.widgets import WeaponWidget
from . import address, models
from .data import SLOT_NO_AMMO, WEAPON_LIST, VEHICLE_LIST
from .models import Player, Vehicle
from .native import NativeContext
import math
import os
import json
import time
import __main__
import fefactory_api
ui = fefactory_api.ui


VERSION_101 = 0x831F7518
VERSION_102 = 0xC483FFE4
VERSION_103 = 0x280F0000
VERSION_104 = 0x110FF300
VERSION_105 = 0xf3385058
VERSION_106 = 0x00a42494
VERSION_106J = 0xda280f30
VERSION_107 = 0x1006e857
VERSION_EFLC1 = 0x0f14247c
VERSION_EFLC2 = 0x0d5c0ff3
VERSION_EFLC1R = 0x41110ff3
VERSION_RFG = 0x108b1874
VERSION_DR2 = 0x1B10044


class Tool(BaseGTATool):
    address = address
    models = models
    Player = Player
    Vehicle = Vehicle

    SAFE_SPEED_RATE = 0.3

    def render(self):
        with self.render_win() as win:
            with ui.Vertical():
                with ui.Horizontal(className="expand container"):
                    ui.Button("检测", className="vcenter", onclick=self.checkAttach)
                    self.attach_status_view = ui.Text("", className="label_left grow")
                    ui.CheckBox("保持最前", onchange=self.swithKeeptop)
                with ui.Notebook(className="fill"):
                    self.render_main()

        win.setOnClose(self.onClose)

    def render_main(self):
        with Group("player", "角色", self._player, handler=self.handler):
            self.hp_view = ModelInputWidget("hp", "生命")
            self.ap_view = ModelInputWidget("ap", "防弹衣")
            self.coord_view = ModelCoordWidget("coord", "坐标", savable=True)
            self.weight_view = ModelInputWidget("gravity", "重量")
            self.wanted_level = ModelInputWidget("wanted_level", "通缉等级")
            ui.Text("")
            with ui.Horizontal(className="expand"):
                ui.Button(label="车坐标->人坐标", onclick=self.from_vehicle_coord)
                ui.Button(label="开启无伤", onclick=self.set_ped_invincible)
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

        # with Group("global", "全局", 0, handler=self.handler):
        #     self.money_view = InputWidget("money", "金钱", address.MONEY, (), int)
            
        with Group(None, "快捷键", 0, handler=self.handler, flexgrid=False, hasfootbar=False):
            with ui.Horizontal(className="fill container"):
                self.spawn_vehicle_id_view = ui.ListBox(className="expand", onselect=self.onSpawnVehicleIdChange, 
                    choices=(item[0] for item in VEHICLE_LIST))
                with ui.ScrollView(className="fill container"):
                    ui.Text("根据左边列表生产载具: alt+V")
                    ui.Text("切换上一辆: alt+[")
                    ui.Text("切换下一辆: alt+]")
                    ui.Text("向前穿墙: alt+w")
                    ui.Text("向前穿墙大: alt+shift+w")
                    ui.Text("弹射起步: alt+m")
                    ui.Text("上天（有速度）: alt+空格")
                    ui.Text("往上（无速度）: alt+.")
                    ui.Text("下坠: alt+shift+空格")
                    ui.Text("恢复HP: alt+h")
                    ui.Text("恢复大量HP(999生命，999护甲): alt+shift+h")
                    ui.Text("附近车辆爆炸(使用秘籍BIGBANG): alt+enter")
        with Group(None, "测试", 0, handler=self.handler, flexgrid=False, hasfootbar=False):
            with ui.GridLayout(cols=3, vgap=10, className="fill container"):
                ui.Button("杀掉附近的人", onclick=self.kill_near_persons)
                ui.Button("附近的车起火", onclick=self.near_vehicles_boom)
                ui.Button("附近的车下陷", onclick=self.near_vehicles_down)
                ui.Button("附近的车移到眼前", onclick=self.near_vehicles_to_front)
                ui.Button("附近的人移到眼前", onclick=self.near_persons_to_front)
                ui.Button("附近的车上天", onclick=self.near_vehicles_fly)
                ui.Button("附近的人上天", onclick=self.near_persons_fly)
                ui.Button("附近的车翻转", onclick=self.near_vehicles_flip)
                ui.Button("跳上一辆车", onclick=self.jump_on_vehicle)
        with Group(None, "工具", 0, flexgrid=False, hasfootbar=False):
            with ui.Vertical(className="fill container"):
                ui.Button("g3l坐标转json", onclick=self.g3l2json)

    def closeWindow(self, m=None):
        self.onClose()
        self.win.close()

    def onClose(self, _=None):
        self.free_remote_function()

    def checkAttach(self, _=None):
        className = 'grcWindow'
        windowName = 'GTAIV'

        if self.handler.active:
            self.free_remote_function()
            
        if self.handler.attachByWindowName(className, windowName):
            self.attach_status_view.label = windowName + ' 正在运行'
            self.MODULE_BASE = self.handler.base - 0x400000

            if not self.win.hotkeys:
                self.win.RegisterHotKeys((
                    # ('jetPackTick', MOD_ALT, getVK('w'), self.jetPackTick),
                    # ('jetPackTickLarge', MOD_ALT | MOD_SHIFT, getVK('w'), lambda hotkeyId:self.jetPackTick(hotkeyId, detal=10)),
                    # ('jetPackTickSpeed', MOD_ALT, getVK('m'), lambda hotkeyId:self.jetPackTick(hotkeyId, useSpeed=True)),
                    # ('raise_up', MOD_ALT, getVK(' '), self.raise_up),
                    ('go_down', MOD_ALT | MOD_SHIFT, getVK(' '), self.go_down),
                    ('to_up', MOD_ALT, getVK('.'), self.to_up),
                    ('stop', MOD_ALT, getVK('x'), self.stop),
                    ('restore_hp', MOD_ALT, getVK('h'), self.restore_hp),
                    ('restore_hp_large', MOD_ALT | MOD_SHIFT, getVK('h'), self.restore_hp_large),
                    # ('spawnVehicle', MOD_ALT, getVK('v'), self.spawnVehicle),
                    # ('spawnVehicleIdPrev', MOD_ALT, getVK('['), self.onSpawnVehicleIdPrev),
                    # ('spawnVehicleIdNext', MOD_ALT, getVK(']'), self.onSpawnVehicleIdNext),
                    ('jump_on_vehicle', MOD_ALT, getVK('j'), self.jump_on_vehicle),
                    ('near_persons_fly', MOD_ALT, getVK('f'), self.near_persons_fly),
                    ('near_fly', MOD_ALT | MOD_SHIFT, getVK('f'), self.near_fly),
                    ('vehicle_flip', MOD_ALT, getVK('k'), self.vehicle_flip),
                    ('near_vehicles_flip', MOD_ALT | MOD_SHIFT, getVK('k'), self.near_vehicles_flip),
                    ('move_near_vehicle_to_front', MOD_ALT, getVK('p'), self.near_vehicles_to_front),
                    ('move_near_person_to_front', MOD_ALT | MOD_SHIFT, getVK('p'), self.near_persons_to_front),
                    ('go_prev_pos', MOD_ALT | MOD_SHIFT, getVK(','), self.go_prev_pos),
                    ('go_next_pos', MOD_ALT | MOD_SHIFT, getVK('.'), self.go_next_pos),
                ))
            self.init_addr()
            self.init_remote_function()
        else:
            self.attach_status_view.label = '没有检测到 ' + windowName

    def get_addr(self, addr):
        return self.MODULE_BASE + addr

    def rel_addr(self, addr):
        return addr - self.MODULE_BASE

    def get_version(self):
        return self.handler.read32(self.get_addr(address.VERSION))

    def init_addr(self):
        version = self.get_version()
        if version == VERSION_104:
            address.PED_POOL     = self.get_addr(0x0175B77C)
            address.VEHICLE_POOL = self.get_addr(0x011F4F30)
            address.OBJECT_POOL  = self.get_addr(0x011FADD8)
            address.LOCAL_PLAYER_ID  = self.get_addr(0xEA68A8)
            address.PLAYER_INFO_ARRAY  = self.get_addr(0x1033058)
            address.FindNativeAddress = 0x617280
        elif version == VERSION_107:
            address.PED_POOL     = self.get_addr(0x18A82AC)
            address.VEHICLE_POOL = self.get_addr(0x1619240)
            address.OBJECT_POOL  = self.get_addr(0x1350CE0)
            address.LOCAL_PLAYER_ID  = self.get_addr(0xF1CC68)
            address.PLAYER_INFO_ARRAY  = self.get_addr(0x11A7008)
            address.FindNativeAddress = 0x5A76D0

        self.FUNCTION_FIND_NATIVE_ADDRESS = (
            b'\x55\x8B\xEC\x83\xEC\x08\x56\xC7\x45\xF8' + utils.u32bytes(address.FindNativeAddress) + 
            b'\xC7\x45\xFC\x00\x00\x00\x00\x56\x8B\x75\x08\xFF\x55\xF8\x5E\x89\x45\xFC\x8B\x45\xFC\x5E\x8B\xE5\x5D\xC3'
        )

    def init_remote_function(self):
        self.FindNativeAddress = self.handler.write_function(self.FUNCTION_FIND_NATIVE_ADDRESS)
        # 初始化Native调用的参数环境
        context_addr = self.handler.alloc_memory(NativeContext.SIZE)
        self.native_context = NativeContext(context_addr, self.handler)

    def free_remote_function(self):
        self.handler.free_memory(self.FindNativeAddress)
        self.handler.free_memory(self.native_context.addr)
        self._playerins = None

    def native_call(self, name, arg_sign, *args, ret_type=int, ret_size=4):
        """ 远程调用GTAIV中的方法
        :param name: 方法名称，见address.NATIVE_ADDRS
        :param arg_sign: 函数签名
        """
        with self.native_context:
            fn_addr = self.get_addr(address.NATIVE_ADDRS[name])
            if arg_sign:
                self.native_context.push(arg_sign, *args)
            self.handler.remote_call(fn_addr, self.native_context.addr)
            if ret_type:
                return self.native_context.get_result(ret_type, ret_size)

    def _player(self):
        # player_addr = self.handler.read32(self.handler.read32(self.address.PLAYER_INFO_ARRAY) + 0x58C)
        # if player_addr is 0:
        #     return None
        player = getattr(self, '_playerins', None)

        index_of_pool = 0

        if not player:
            player = self._playerins = self.Player(self.get_player_index(), self.native_call, self.native_context)
        else:
            player.index = self.get_player_index()
        return player

    def _vehicle(self):
        pass
        # return self.Vehicle(self.handler.read32(self.address.VEHICLE_PTR), self.handler)

    player = property(_player)
    vehicle = property(_vehicle)

    def get_player_index(self, index=0):
        player_id = (index or self.get_player_index_of_pool()) << 8
        return player_id | self.handler.read8(
            self.handler.read32(self.handler.read32(address.PED_POOL) + 4) + (player_id >> 8)
        )

    def get_ped_addr(self):
        return self.handler.read32(self.handler.read32(self.address.PLAYER_INFO_ARRAY) + 0x58C)

    def get_player_index_of_pool(self):
        """获取当前ped在ped_pool中的index"""
        ped_addr = self.get_ped_addr()
        pool = self.ped_pool
        for i in range(pool.size):
            if pool.addr_at(i) == ped_addr:
                return i

    def onSpawnVehicleIdChange(self, lb):
        self.handler.write32(address.SPAWN_VEHICLE_ID_BASE, VEHICLE_LIST[lb.index][1])

    def onSpawnVehicleIdPrev(self, _=None):
        pos = self.spawn_vehicle_id_view.index
        if pos == 0:
            pos = len(VEHICLE_LIST)
        self.spawn_vehicle_id_view.setSelection(pos - 1, True)

    def onSpawnVehicleIdNext(self, _=None):
        pos = self.spawn_vehicle_id_view.index
        if pos == len(VEHICLE_LIST) - 1:
            pos = -1
        self.spawn_vehicle_id_view.setSelection(pos + 1, True)

    def vehicle_lock_door(self, _=None, lock=True):
        car = self.player.vehicle
        if car:
            if lock:
                car.lock_door()
            else:
                car.unlock_door()

    def weapon_max(self, _=None):
        for v in self.weapon_views:
            v.id_view.index = 1
            if v.has_ammo:
                v.ammo_view.value = 9999

    def set_ped_invincible(self):
        self.player.set_invincible(True)

    def flash_weapon_icon(self):
        self.native_call('FLASH_WEAPON_ICON', 'L', 1, ret_type=None)

    def get_player_id(self):
        return self.native_call('GET_PLAYER_ID', None)