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
import math
import os
import json
import time
import __main__
import fefactory_api
ui = fefactory_api.ui


class Tool:

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
            # self.star_view = InputWidget("star", "通缉等级", None, (0x5f4, 0x20), int)
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
            for i in range(13):
                self.weapon_views.append(WeaponWidget("weapon%d" % i, "武器槽%d" % (i + 1), i))

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
                ))
        else:
            self.attach_status_view.label = '没有检测到 ' + windowName

    def _player(self):
        player_addr = self.handler.read32(address.PLAYER_BASE)
        if player_addr is 0:
            return None
        player = getattr(self, '_playerins', None)
        if not player:
            player = self._playerins = Player(player_addr, self.handler)
        elif player.addr != player_addr:
            player.addr = player_addr
        return player

    def _vehicle(self):
        addr = self.handler.read32(address.VEHICLE_BASE)
        if addr:
            return Vehicle(addr, self.handler)

    player = property(_player)
    vehicle = property(_vehicle)

    def swithKeeptop(self, cb):
        self.win.keeptop = cb.checked

    def inputCheat(self, text):
        auto.sendKey(TextVK(text), 10)

    @property
    def player_entity(self):
        return self.vehicle if self.player.isInVehicle else self.player

    def jetPackTick(self, hotkeyId=None, useSpeed=False, detal=0):
        PI = math.pi
        HALF_PI = PI / 2
        jetPackSpeed = detal or self.jetPackSpeed
        isInVehicle = self.player.isInVehicle

        if isInVehicle:
            coord_view = self.vehicle_coord_view
            speed_view = self.vehicle_speed_view
            # rotz = self.camera_z_rot_view.mem_value
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
            values = target.mem_value.values()
            values[0] += xVal * jetPackSpeed
            values[1] += yVal * jetPackSpeed
        else:
            # speed up
            target = speed_view
            values = target.mem_value.values()
            values[0] += xVal * 0.3
            values[1] += yVal * 0.3
            if not isInVehicle:
                values[2] = 0.2
                self.raiseUp(speed=0.2)
                time.sleep(0.1)
        
        target.mem_value = values

    def raiseUp(self, hotkeyId=None, speed=1.0):
        self.player_entity.speed[2] = speed

    def goDown(self, hotkeyId=None, speed=0.5):
        self.player_entity.speed[2] = -speed

    def toUp(self, hotkeyId=None):
        self.player_entity.coord[2] += 10

    def stop(self, hotkeyId=None):
        speed_view = self.vehicle_speed_view if self.player.isInVehicle else self.speed_view
        speed_view.mem_value = (0, 0, 0)

    def restoreHp(self, hotkeyId=None):
        if self.player.isInVehicle:
            self.vehicle_hp_view.mem_value = 2000
        else:
            self.hp_view.mem_value = 200

    def restoreHpLarge(self, hotkeyId=None):
        if self.player.isInVehicle:
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

    """获取前面一点的坐标"""
    def get_front_coord(self):
        PI = math.pi
        HALF_PI = PI / 2
        rotz = self.rot_view.mem_value
        rotz += HALF_PI
        if rotz > PI:
            rotz += PI * 2

        xVal = math.cos(rotz)
        yVal = math.sin(rotz)
        coord = self.player.coord.values()
        coord[0] += xVal * 5
        coord[1] += yVal * 5
        return coord

    def nearVehicleToFront(self, btn=None):
        coord = self.get_front_coord()
        for p in self.getNearVehicles():
            p.coord = coord

    def nearPersonToFront(self, btn=None):
        coord = self.get_front_coord()
        for p in self.getNearPersons():
            p.coord = coord

    def jumpOnVehicle(self, btn=None):
        for v in self.getNearVehicles():
            if v.numPassengers:
                v.stop()
                coord = v.coord.values()
                coord[2] += 1
                self.player.coord = coord
                break

    def nearVehicleFlip(self, _=None):
        for v in self.getNearVehicles():
            v.flip()

    def nearPersonFly(self, _=None):
        for p in self.player.nearPersons:
            p.speed[2] = 1

    def nearVehicleFly(self, btn=None):
        for v in self.getNearVehicles():
            v.coord[2] += 1
            v.speed[2] = 1

    def nearFly(self, btn=None):
        self.nearPersonFly()
        self.nearVehicleFly()

    def vehicleFlip(self, _=None):
        self.player.lastCar.flip()

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

    def g3l2json(self, btn=None):
        """g3l坐标转json"""
        path = fefactory_api.choose_file("选择要读取的文件", wildcard='*.g3l')
        if path:
            with open(path) as file:
                if not file.readline().strip() == '[Locks]':
                    fefactory_api.alert('不支持的格式')
                    return

                coord = [0, 0, 0]
                datas = []
                while True:
                    line = file.readline()
                    if not line:
                        break
                    line = line.strip()
                    if line.startswith('x='):
                        coord[0] = float(line[2:])
                    elif line.startswith('y='):
                        coord[1] = float(line[2:])
                    elif line.startswith('z='):
                        coord[2] = float(line[2:])
                    elif line.startswith('desc='):
                        datas.append({'name': line[5:], 'value': tuple(coord)})

            jsonpath = path[:path.rfind('.') + 1] + 'json'
            with open(jsonpath, 'w', encoding="utf-8") as file:
                json.dump(datas, file, ensure_ascii=False)

            fefactory_api.alert('转换成功: ' + jsonpath)


win_style = {
    'width': 640,
    'height': 820,
}