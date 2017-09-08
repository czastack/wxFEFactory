from functools import partial
from fefactory_api.emuhacker import ProcessHandler
from lib.hack.form import Group, InputWidget, CheckBoxWidget, CoordsWidget, ModelInputWidget, ModelCoordsWidget
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
from lib.win32.sendkey import auto, TextVK
from commonstyle import dialog_style, styles
from . import address
from .vehicle import vehicle_list
from .models import Player, Vehicle
from .widgets import WeaponWidget
from ..gta_base.main import BaseGTATool
import math
import os
import json
import time
import __main__
import fefactory_api
ui = fefactory_api.ui


class Tool(BaseGTATool):
    address = address
    Player = Player
    Vehicle = Vehicle

    safe_speed_rate = 0.3

    def __init__(self):
        self.handler = ProcessHandler()
        self.jetPackSpeed = 2.0

    def attach(self):
        self.render()
        self.checkAttach()

    def render(self):
        with ui.MenuBar() as menubar:
            with ui.Menu("文件"):
                with ui.Menu("新建"):
                    ui.MenuItem("新建工程\tCtrl+Shift+N", onselect=None)
            with ui.Menu("窗口"):
                ui.MenuItem("关闭\tCtrl+W", onselect=self.closeWindow)

        with ui.HotkeyWindow("GTA3 Hack", style=win_style, styles=styles, menuBar=menubar) as win:
            with ui.Vertical():
                with ui.Horizontal(className="expand container"):
                    ui.Button("检测", className="vcenter", onclick=self.checkAttach)
                    self.attach_status_view = ui.Text("", className="label_left grow")
                    ui.CheckBox("保持最前", onchange=self.swithKeeptop)
                with ui.Notebook(className="fill"):
                    self.render_main()

        win.setOnClose(self.onClose)
        self.win = win

    def render_main(self):
        with Group("player", "角色", self._player, handler=self.handler):
            self.hp_view = ModelInputWidget("hp", "生命")
            self.ap_view = ModelInputWidget("ap", "防弹衣")
            self.rot_view = ModelInputWidget("rotation", "旋转")
            self.coord_view = ModelCoordsWidget("coord", "坐标", savable=True)
            self.speed_view = ModelCoordsWidget("speed", "速度")
            self.weight_view = ModelInputWidget("weight", "重量")
            # self.stamina_view = InputWidget("stamina", "体力", None, (0x600,), float)
            self.star_view = InputWidget("star", "通缉等级", address.WANTED_BASE, (0x53c, 0x18), int)
            ui.Text("")
            ui.Button(label="车坐标->人坐标", onclick=self.fromVehicleCoord)
        with Group("vehicle", "汽车", self._vehicle, handler=self.handler):
            self.vehicle_hp_view = ModelInputWidget("hp", "HP")
            self.vehicle_roll_view = ModelCoordsWidget("roll", "滚动")
            self.vehicle_dir_view = ModelCoordsWidget("dir", "方向")
            self.vehicle_coord_view = ModelCoordsWidget("coord", "坐标", savable=True)
            self.vehicle_speed_view = ModelCoordsWidget("speed", "速度")
            self.weight_view = ModelInputWidget("weight", "重量")
            ui.Text("")
            with ui.Horizontal(className="expand"):
                ui.Button(label="人坐标->车坐标", onclick=self.fromPlayerCoord)
                ui.Button(label="锁车", onclick=self.vehicleLockDoor)
                ui.Button(label="开锁", onclick=partial(self.vehicleLockDoor, lock=False))

        with Group("weapon", "武器槽", None, handler=self.handler):
            self.weapon_views = []
            for i in range(1, 13):
                self.weapon_views.append(WeaponWidget("weapon%d" % i, "武器槽%d" % i, i))

            ui.Button(label="一键最大", onclick=self.weaponMax)

        with Group("global", "全局", 0, handler=self.handler):
            self.money_view = InputWidget("money", "金钱", address.MONEY_BASE, (), int)
            
        with Group(None, "快捷键", 0, handler=self.handler, flexgrid=False, hasfootbar=False):
            with ui.Horizontal(className="fill container"):
                self.spawn_vehicle_id_view = ui.ListBox(className="expand", onselect=self.onSpawnVehicleIdChange, 
                    choices=(item[0] for item in vehicle_list))
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
                ui.Button("杀掉附近的人", onclick=self.killNearPerson)
                ui.Button("附近的车起火", onclick=self.nearVehicleBoom)
                ui.Button("附近的车下陷", onclick=self.nearVehicleDown)
                ui.Button("附近的车移到眼前", onclick=self.nearVehicleToFront)
                ui.Button("附近的人移到眼前", onclick=self.nearPersonToFront)
                ui.Button("附近的车上天", onclick=self.nearVehicleFly)
                ui.Button("附近的人上天", onclick=self.nearPersonFly)
                ui.Button("附近的车翻转", onclick=self.nearVehicleFlip)
                ui.Button("跳上一辆车", onclick=self.jumpOnVehicle)
        with Group(None, "工具", 0, flexgrid=False, hasfootbar=False):
            with ui.Vertical(className="fill container"):
                ui.Button("g3l坐标转json", onclick=self.g3l2json)

    def closeWindow(self, m=None):
        self.onClose()
        self.win.close()

    def onClose(self, _=None):
        pass

    def checkAttach(self, _=None):
        className = 'Grand theft auto 3'
        windowName = 'GTA3'
        if self.handler.attachByWindowName(className, windowName):
            self.attach_status_view.label = windowName + ' 正在运行'

            if not self.win.hotkeys:
                self.win.RegisterHotKeys((
                    ('jetPackTick', MOD_ALT, getVK('w'), self.jetPackTick),
                    ('jetPackTickLarge', MOD_ALT | MOD_SHIFT, getVK('w'), lambda hotkeyId:self.jetPackTick(hotkeyId, detal=10)),
                    ('jetPackTickSpeed', MOD_ALT, getVK('m'), lambda hotkeyId:self.jetPackTick(hotkeyId, useSpeed=True)),
                    ('raiseUp', MOD_ALT, getVK(' '), self.raiseUp),
                    ('goDown', MOD_ALT | MOD_SHIFT, getVK(' '), self.goDown),
                    ('toUp', MOD_ALT, getVK('.'), self.toUp),
                    ('stop', MOD_ALT, getVK('x'), self.stop),
                    ('restoreHp', MOD_ALT, getVK('h'), self.restoreHp),
                    ('restoreHpLarge', MOD_ALT | MOD_SHIFT, getVK('h'), self.restoreHpLarge),
                    ('spawnVehicle', MOD_ALT, getVK('v'), self.spawnVehicle),
                    ('spawnVehicleIdPrev', MOD_ALT, getVK('['), self.onSpawnVehicleIdPrev),
                    ('spawnVehicleIdNext', MOD_ALT, getVK(']'), self.onSpawnVehicleIdNext),
                    ('jumpOnVehicle', MOD_ALT, getVK('j'), self.jumpOnVehicle),
                    ('nearPersonFly', MOD_ALT, getVK('f'), self.nearPersonFly),
                    ('nearFly', MOD_ALT | MOD_SHIFT, getVK('f'), self.nearFly),
                    ('vehicleFlip', MOD_ALT, getVK('k'), self.vehicleFlip),
                    ('nearVehicleFlip', MOD_ALT | MOD_SHIFT, getVK('k'), self.nearVehicleFlip),
                    ('move_near_vehicle_to_front', MOD_ALT, getVK('p'), self.nearVehicleToFront),
                    ('move_near_person_to_front', MOD_ALT | MOD_SHIFT, getVK('p'), self.nearPersonToFront),
                    ('go_prev_pos', MOD_ALT | MOD_SHIFT, getVK(','), self.go_prev_pos),
                    ('go_next_pos', MOD_ALT | MOD_SHIFT, getVK('.'), self.go_next_pos),
                ))
        else:
            self.attach_status_view.label = '没有检测到 ' + windowName

    def onSpawnVehicleIdChange(self, lb):
        self.handler.write32(address.SPAWN_VEHICLE_ID_BASE, vehicle_list[lb.index][1])

    def onSpawnVehicleIdPrev(self, hotkeyId=None):
        pos = self.spawn_vehicle_id_view.index
        if pos == 0:
            pos = len(vehicle_list)
        self.spawn_vehicle_id_view.setSelection(pos - 1, True)

    def onSpawnVehicleIdNext(self, hotkeyId=None):
        pos = self.spawn_vehicle_id_view.index
        if pos == len(vehicle_list) - 1:
            pos = -1
        self.spawn_vehicle_id_view.setSelection(pos + 1, True)

    def getPersons(self):
        pool_ptr = self.handler.read32(address.ACTOR_POOL_POINTER)
        pool_start = self.handler.read32(pool_ptr)
        pool_size = self.handler.read32(pool_ptr + 8)
        for i in range(pool_size):
            yield Player(pool_start, self.handler)
            pool_start += Player.SIZE

    def getVehicles(self):
        pool_ptr = self.handler.read32(address.VEHICLE_POOL_POINTER)
        pool_start = self.handler.read32(pool_ptr)
        pool_size = self.handler.read32(pool_ptr + 8)
        for i in range(pool_size):
            yield Vehicle(pool_start, self.handler)
            pool_start += Vehicle.SIZE

    def vehicleLockDoor(self, btn=None, lock=True):
        car = self.player.lastCar
        if car:
            if lock:
                car.lockDoor()
            else:
                car.unlockDoor()

    def weaponMax(self, _=None):
        for v in self.weapon_views:
            v.id_view.index = 1
            if v.has_ammo:
                v.ammo_view.value = 9999


win_style = {
    'width': 640,
    'height': 820,
}