from fefactory_api.emuhacker import ProcessHandler
from lib.hack.form import Group, InputWidget, CheckBoxWidget, CoordsWidget
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
from lib.win32.sendkey import auto, TextVK
from commonstyle import dialog_style, styles
from . import address
from .vehicle import vehicle_list
from .models import Player, Vehicle
from ..gta_base.main import BaseGTATool
import math
import os
import json
import time
import __main__
import fefactory_api
ui = fefactory_api.ui


class Tool(BaseGTATool):

    def __init__(self):
        self.handler = ProcessHandler()
        self.jetPackSpeed = 2.0

    def attach(self):
        self.render()

    def render(self):
        with ui.MenuBar() as menubar:
            with ui.Menu("文件"):
                with ui.Menu("新建"):
                    ui.MenuItem("新建工程\tCtrl+Shift+N", onselect=None)
            with ui.Menu("窗口"):
                ui.MenuItem("关闭\tCtrl+W", onselect=self.closeWindow)

        with ui.HotkeyWindow("罪恶都市Hack", style=win_style, styles=styles, menuBar=menubar) as win:
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
        with Group("player", "角色", address.PLAYER_BASE, handler=self.handler):
            self.hp_view = InputWidget("hp", "生命", None, (0x354,), float)
            self.ap_view = InputWidget("ap", "防弹衣", None, (0x358,), float)
            self.rot_view = InputWidget("rotation", "旋转", None, (0x378,), float)
            self.coord_view = CoordsWidget("coord", "坐标", None, (0x34,), savable=True)
            self.speed_view = CoordsWidget("speed", "速度", None, (0x70,))
            self.weight_view = InputWidget("weight", "重量", None, (0xB8,), float)
            self.stamina_view = InputWidget("stamina", "体力", None, (0x600,), float)
            self.star_view = InputWidget("star", "通缉等级", None, (0x5f4, 0x20), int)
            ui.Text("")
            ui.Button(label="车坐标->人坐标", onclick=self.fromVehicleCoord)
        with Group("vehicle", "汽车", address.VEHICLE_BASE, handler=self.handler):
            self.vehicle_hp_view = InputWidget("vehicle_hp", "HP", None, (0x204,), float)
            self.vehicle_roll_view = CoordsWidget("roll", "滚动", None, (0x04,))
            self.vehicle_dir_view = CoordsWidget("dir", "方向", None, (0x14,))
            self.vehicle_coord_view = CoordsWidget("coord", "坐标", None, (0x34,), savable=True)
            self.vehicle_speed_view = CoordsWidget("speed", "速度", None, (0x70,))
            self.vehicle_turn_view = CoordsWidget("turn", "Turn", None, (0x7C,))
            self.weight_view = InputWidget("weight", "重量", None, (0xB8,), float)
            ui.Text("")
            ui.Button(label="人坐标->车坐标", onclick=self.fromPlayerCoord)
        with Group("global", "全局", 0, handler=self.handler):
            self.money_view = InputWidget("money", "金钱", address.MONEY_BASE, (), int)
            self.camera_view = CoordsWidget("camera", "摄像机", 0x7E46B8, ())
            self.camera_z_rot_view = InputWidget("camera_z_rot", "摄像机z_rot", 0x7E48CC, (), float)
            self.camera_x_rot_view = InputWidget("camera_x_rot", "摄像机x_rot", 0x7E48BC, (), float)
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
                ui.Button("附近的车叠罗汉", onclick=self.nearVehiclePutAtOne)
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

    def checkAttach(self, btn):
        className = 'Grand theft auto 3'
        windowName = 'GTA: Vice City'
        if self.handler.attachByWindowName(className, windowName):
            self.attach_status_view.label = windowName + ' 正在运行'

            self.player = Player(self.handler.read32(address.PLAYER_BASE), self.handler)

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
                    ('bigbang', MOD_ALT, getVK('enter'), self.bigbang),
                    ('jumpOnVehicle', MOD_ALT, getVK('j'), self.jumpOnVehicle),
                    ('vehicleFlip', MOD_ALT, getVK('k'), self.vehicleFlip),
                    ('nearVehicleFlip', MOD_ALT | MOD_SHIFT, getVK('k'), self.nearVehicleFlip),
                ))
        else:
            self.attach_status_view.label = '没有检测到 ' + windowName

    def swithKeeptop(self, cb):
        self.win.keeptop = cb.checked

    def inputCheat(self, text):
        auto.sendKey(TextVK(text), 10)

    @property
    def isInVehicle(self):
        return self.vehicle_hp_view.mem_value >= 1

    @property
    def z_speed_ptr(self):
        speed_view = self.vehicle_speed_view if self.isInVehicle else self.speed_view
        offsets = list(speed_view.offsets)
        offsets[-1] += 8
        return self.handler.readLastAddr(speed_view.addr, offsets)

    def jetPackTick(self, hotkeyId=None, useSpeed=False, detal=0):
        PI = math.pi
        HALF_PI = PI / 2
        jetPackSpeed = detal or self.jetPackSpeed
        isInVehicle = self.isInVehicle

        if isInVehicle:
            coord_view = self.vehicle_coord_view
            speed_view = self.vehicle_speed_view
            rotz = self.camera_z_rot_view.mem_value
        else:
            coord_view = self.coord_view
            speed_view = self.speed_view
            rotz = self.rot_view.mem_value
            rotz += HALF_PI
            if rotz > PI:
                rotz += PI * 2

        xVal = math.cos(rotz)
        yVal = math.sin(rotz)

        if not useSpeed:
            target = coord_view
            values = target.mem_value
            values[0] += xVal * jetPackSpeed
            values[1] += yVal * jetPackSpeed
        else:
            # speed up
            target = speed_view
            values = target.mem_value
            values[0] += xVal * 0.5
            values[1] += yVal * 0.5
            if not isInVehicle:
                values[2] = 0.2
                self.raiseUp(speed=0.2)
                time.sleep(0.1)
        
        target.mem_value = values


        # if False: # UP or FALSE
        #     speed_ptr = self.z_speed_ptr
        #     z_speed = jetPackSpeed * PI * 2
        #     if False: # Donw
        #         z_speed *= -1
        #     self.handler.writeFloat(speed_ptr, z_speed)

    def raiseUp(self, hotkeyId=None, speed=1.0):
        self.handler.writeFloat(self.z_speed_ptr, speed)

    def goDown(self, hotkeyId=None, speed=0.5):
        self.handler.writeFloat(self.z_speed_ptr, -speed)

    def toUp(self, hotkeyId=None):
        view = self.vehicle_coord_view if self.isInVehicle else self.coord_view
        offsets = list(view.offsets)
        offsets[-1] += 8
        ptr = self.handler.readLastAddr(view.addr, offsets)
        self.handler.writeFloat(ptr, self.handler.readFloat(ptr) + 10)

    def stop(self, hotkeyId=None):
        speed_view = self.vehicle_speed_view if self.isInVehicle else self.speed_view
        speed_view.mem_value = (0, 0, 0)

    def restoreHp(self, hotkeyId=None):
        if self.isInVehicle:
            self.vehicle_hp_view.mem_value = 2000
        else:
            self.hp_view.mem_value = 200

    def restoreHpLarge(self, hotkeyId=None):
        if self.isInVehicle:
            self.vehicle_hp_view.mem_value = 2000
        else:
            self.hp_view.mem_value = 999
            self.ap_view.mem_value = 999

    def fromPlayerCoord(self, btn):
        self.vehicle_coord_view.input_value = self.coord_view.input_value

    def fromVehicleCoord(self, btn):
        self.coord_view.input_value = self.vehicle_coord_view.input_value

    def promptWrite(self, text):
        text = (text + '\0').encode('utf-16le')
        TEXT1_ADDR = 0x7D3E40
        TEXT2_ADDR = 0x939028
        
        self.handler.ptrsWrite(TEXT1_ADDR, (), text)
        time.sleep(0.01)
        self.handler.ptrsWrite(TEXT2_ADDR, (), text)

    def bigbang(self, hotkeyId=None):
        self.inputCheat('bigbang')

    def spawnVehicle(self, hotkeyId=None):
        self.inputCheat('betterthanwalking')

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

    def getNearPersons(self, distance=100):
        coord = self.player.coord.values()
        for p in self.getPersons():
            if p.hp != 0 and p.distance(coord) <= distance:
                yield p

    def getVehicles(self):
        pool_ptr = self.handler.read32(address.VEHICLE_POOL_POINTER)
        pool_start = self.handler.read32(pool_ptr)
        pool_size = self.handler.read32(pool_ptr + 8)
        for i in range(pool_size):
            yield Vehicle(pool_start, self.handler)
            pool_start += Vehicle.SIZE

    def getNearVehicles(self, distance=100):
        coord = self.player.coord.values()
        mycarAddr = self.handler.read32(address.VEHICLE_BASE)
        for v in self.getVehicles():
            if v.hp != 0 and v.distance(coord) <= distance:
                if v.addr != mycarAddr:
                    yield v

    def killNearPerson(self, btn=None):
        for p in self.player.nearPersons:
            p.hp = 0

    def nearVehicleBoom(self, btn=None):
        for v in self.getNearVehicles():
            v.hp = 0

    def nearVehicleDown(self, btn=None):
        for v in self.getNearVehicles():
            v.coord[2] -= 0.7

    def nearVehiclePutAtOne(self, btn=None):
        first = None
        for v in self.getNearVehicles():
            if not first:
                first = v
                first.speed = (0, 0, 0)
                coord = first.coord.values()
                lastZ = coord[2] + 8
            else:
                v.coord = coord
                v.coord[2] = lastZ
                lastZ += 8

    def nearVehicleFly(self, btn=None):
        for v in self.getNearVehicles():
            v.coord[2] += 1
            v.speed[2] = 1

    def jumpOnVehicle(self, btn=None):
        for v in self.getNearVehicles():
            if v.numPassengers:
                v.stop()
                coord = v.coord.values()
                coord[2] += 1
                self.player.coord = coord
                break

    def nearVehicleFlip(self, btn=None):
        for v in self.getNearVehicles():
            v.flip()

    def nearPersonFly(self, btn=None):
        for p in self.player.nearPersons:
            p.speed[2] = 1

    def vehicleFlip(self, _=None):
        self.player.lastCar.flip()


win_style = {
    'width': 640,
    'height': 820,
}