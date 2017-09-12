from functools import partial
from fefactory_api.emuhacker import ProcessHandler
from lib.hack.form import (
    Group, InputWidget, ProxyInputWidget, SelectWidget, ModelInputWidget, ModelCoordsWidget
)
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
from lib.win32.sendkey import auto, TextVK
from lib.utils import normalFloat
from commonstyle import dialog_style, styles
from .data import SLOT_NO_AMMO, WEAPON_LIST, VEHICLE_LIST, WEATHER_LIST, COLOR_LIST
from .models import Player, Vehicle, Marker
from . import cheat, address
from ..gta_base.main import BaseGTATool
from ..gta_base.widgets import WeaponWidget, ColorWidget
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

    def __init__(self):
        self.handler = ProcessHandler()
        self.jetPackSpeed = 2.0
        self.spawn_code_injected = False

    def attach(self):
        self.render()
        self.checkAttach()

    def render(self):
        with ui.MenuBar() as menubar:
            with ui.Menu("窗口"):
                ui.MenuItem("关闭\tCtrl+W", onselect=self.closeWindow)

        with ui.HotkeyWindow("圣安地列斯Hack", style=win_style, styles=styles, menuBar=menubar) as win:
            with ui.Vertical():
                with ui.Horizontal(className="expand container"):
                    ui.Button("检测", className="vcenter", onclick=self.checkAttach)
                    self.attach_status_view = ui.Text("", className="label_left grow")
                    ui.CheckBox("保持最前", onchange=self.swithKeeptop)
                with ui.Notebook(className="fill"):
                    self.render_main()
        self.win = win

    def render_main(self):
        with Group("player", "角色", self._player, handler=self.handler):
            self.hp_view = ModelInputWidget("hp", "生命")
            self.maxhp_view = ModelInputWidget("maxhp", "最大生命")
            self.ap_view = ModelInputWidget("ap", "防弹衣")
            self.rot_view = ModelInputWidget("rotation", "旋转")
            self.coord_view = ModelCoordsWidget("coord", "坐标", savable=True)
            self.speed_view = ModelCoordsWidget("speed", "速度")
            self.weight_view = ModelInputWidget("weight", "重量")
            self.wanted_level_view = ProxyInputWidget("wanted_level", "通缉等级", self.getWantedLevel, self.setWantedLevel)
            ui.Text("")
            with ui.Vertical(className="fill"):
                with ui.Horizontal(className="expand"):
                    ui.Button(label="车坐标->人坐标", onclick=self.fromVehicleCoord)
                    ui.Button(label="从地图读取坐标", onclick=self.playerCoordFromMap)
                ui.Hr()
                ui.Text("防止主角受到来自以下的伤害")
                with ui.Horizontal(className="fill"):
                    self.player_special_views = [
                        ui.CheckBox("爆炸", className="vcenter", onchange=partial(self.setPlayerSpecial, bitindex=Player.SPECIAL_EP)),
                        ui.CheckBox("碰撞", className="vcenter", onchange=partial(self.setPlayerSpecial, bitindex=Player.SPECIAL_DP)),
                        ui.CheckBox("子弹", className="vcenter", onchange=partial(self.setPlayerSpecial, bitindex=Player.SPECIAL_BP)),
                        ui.CheckBox("火焰", className="vcenter", onchange=partial(self.setPlayerSpecial, bitindex=Player.SPECIAL_FP)),
                    ]
                    ui.Button("再次应用", onclick=self.apply_player_special).setToolTip("死亡或者重新读档后需要再次应用")
        with Group("vehicle", "汽车", self._vehicle, handler=self.handler):
            self.vehicle_hp_view = ModelInputWidget("hp", "HP")
            self.vehicle_dir_view = ModelCoordsWidget("dir", "方向")
            self.vehicle_grad_view = ModelCoordsWidget("grad", "旋转")
            self.vehicle_coord_view = ModelCoordsWidget("coord", "坐标", savable=True)
            self.vehicle_speed_view = ModelCoordsWidget("speed", "速度")
            self.weight_view = ModelInputWidget("weight", "重量")
            ui.Text("")
            with ui.Vertical(className="fill"):
                with ui.Horizontal(className="expand"):
                    ui.Button(label="人坐标->车坐标", onclick=self.fromPlayerCoord)
                    ui.Button(label="从地图读取坐标", onclick=self.vehicleCoordFromMap)
                    ui.Button(label="锁车", onclick=self.vehicleLockDoor)
                    ui.Button(label="开锁", onclick=partial(self.vehicleLockDoor, lock=False))
                ui.Hr()
                ui.Text("防止当前载具受到来自以下的伤害")
                with ui.Horizontal(className="fill"):
                    self.vehicle_special_views = [
                        ui.CheckBox("爆炸", className="vcenter", onchange=partial(self.setVehicleSpecial, bitindex=Vehicle.SPECIAL_EP)),
                        ui.CheckBox("碰撞", className="vcenter", onchange=partial(self.setVehicleSpecial, bitindex=Vehicle.SPECIAL_DP)),
                        ui.CheckBox("子弹", className="vcenter", onchange=partial(self.setVehicleSpecial, bitindex=Vehicle.SPECIAL_BP)),
                        ui.CheckBox("火焰", className="vcenter", onchange=partial(self.setVehicleSpecial, bitindex=Vehicle.SPECIAL_FP)),
                    ]
                    ui.Button("再次应用", onclick=self.apply_vehicle_special).setToolTip("切换载具后需要再次应用")
            ui.Text("颜色")
            with ui.Horizontal(className="fill"):
                self.vehicle_body_color_view = ColorWidget("body_color", "车身1", self._vehicle, "body_color", COLOR_LIST)
                self.vehicle_body2_color_view = ColorWidget("body2_color", "车身2", self._vehicle, "body2_color", COLOR_LIST)
                self.vehicle_stripe_color_view = ColorWidget("stripe_color", "条纹1", self._vehicle, "stripe_color", COLOR_LIST)
                self.vehicle_stripe2_color_view = ColorWidget("stripe2_color", "条纹2", self._vehicle, "stripe2_color", COLOR_LIST)

        with Group("weapon", "武器槽", None, handler=self.handler):
            self.weapon_views = []
            for i in range(13):
                self.weapon_views.append(WeaponWidget("weapon%d" % i, "武器槽%d" % (i + 1), i, SLOT_NO_AMMO, WEAPON_LIST, self._player))

        with Group("weapon_prop", "武器熟练度", None, handler=self.handler):
            self.weapon_prop_views = [
                ProxyInputWidget("weapon_prop_%d" % i, label, 
                    partial(self.get_weapon_prop, index=i), partial(self.set_weapon_prop, index=i)) for i, label in enumerate((
                        '手枪', '消音手枪', '沙漠之鹰', '霰弹枪', '短管霰弹枪', '战斗霰弹枪', 'MP5', 'Tech9', 'AK47', 'M4',
                    ))
            ]
            
        with Group("global", "全局", 0, handler=self.handler):
            self.money_view = InputWidget("money", "金钱", address.MONEY_BASE)
            InputWidget("cheat_count", "作弊次数", address.CHEAT_COUNT_ADDR)
            InputWidget("cheat_stat", "作弊状态", address.CHEAT_STAT_ADDR)
            InputWidget("fat_stat", "肥胖度", address.FAT_STAT_ADDR, (), float)
            InputWidget("stamina_stat", "耐力值", address.STAMINA_STAT_ADDR, (), float)
            InputWidget("muscle_stat", "肌肉值", address.MUSCLE_STAT_ADDR, (), float)
            InputWidget("lung_capacity", "肺活量", address.LUNG_CAPACITY_ADDR)
            InputWidget("gambling_stat", "赌博技术", address.GAMBLING_STAT_ADDR)
            InputWidget("car_prof", "驾驶技术", address.CAR_PROF_ADDR)
            InputWidget("bike_prof", "摩托车技术", address.BIKE_PROF_ADDR)
            InputWidget("cycle_prof", "自行车技术", address.CYCLE_PROF_ADDR)
            InputWidget("cycle_prof", "飞机技术", address.FLYING_PROF_ADDR)
            InputWidget("days_in_game", "天数", address.DAYS_IN_GAME_ADDR)
            InputWidget("curr_hour", "当前小时", address.CURR_HOUR_ADDR, size=1)
            InputWidget("curr_minute", "当前分钟", address.CURR_MINUTE_ADDR, size=1)
            InputWidget("curr_weekday", "当前星期", address.CURR_WEEKDAY_ADDR, size=1)
            SelectWidget("curr_weather", "当前天气", address.WEATHER_CURRENT_ADDR, (), WEATHER_LIST)
        with Group(None, "作弊", 0, handler=self.handler, flexgrid=False, hasfootbar=False):
            with ui.Vertical(className="fill container"):
                with ui.GridLayout(cols=4, vgap=10, className="fill container"):
                    self.cheat_views = [
                        ui.CheckBox(label, onchange=partial(self.toggle_cheat, index=i)) for i, label in enumerate((
                            '不被通缉', '决不会饿', '无限健康', '无限氧气', '无限弹药', '坦克模式', '超级攻击', '超级跳跃', '最大威望', '最大引力',
                            '满街跑车', '满街破车', '无限奔跑', '主角防火', '完美操控', '交通通畅', '超级兔跳', '液压装置', '船可以飞', '车可以飞'
                        ))
                    ]
                    ui.CheckBox("冻结任务计时", onchange=self.freeze_timer)
                    ui.CheckBox("一击必杀", onchange=self.one_hit_kill)
                with ui.Horizontal(className="container"):
                    ui.Button("同步", onclick=self.cheat_sync)
                    ui.Button("插入生产载具的代码", onclick=self.inject_spawn_code)
                    self.spawn_code_injected_view = ui.Text("", className="vcenter")
        with Group(None, "女友进度", 0, handler=self.handler):
            # TODO
            address.GIRL_FRIEND_PROGRESS_ADDR = self.get_cheat_config()['GIRL_FRIEND_PROGRESS_ADDR']
            for i, label in enumerate(['Denise', 'Michelle', 'Helena', 'Katie', 'Barbara', 'Millie']):
                InputWidget(label, label, address.GIRL_FRIEND_PROGRESS_ADDR[i])
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
                    ui.Text("附近的人上天: alt+f")
                    ui.Text("附近的人和车上天: alt+shift+f")
                    ui.Text("附近的车翻转: alt+shift+k")
                    ui.Text("自己的车翻转: alt+k")
                    ui.Text("瞬移到地图指针处: ctrl+alt+g")
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
                ui.Button("召唤上一辆车回来", onclick=self.callVehicle)
                ui.Button("回到上一辆车旁边", onclick=self.goVehicle)
        with Group(None, "工具", 0, flexgrid=False, hasfootbar=False):
            with ui.Vertical(className="fill container"):
                ui.Button("g3l坐标转json", onclick=self.g3l2json)

    def closeWindow(self, m=None):
        self.win.close()

    def checkAttach(self, btn=None):
        className = 'Grand theft auto San Andreas'
        windowName = 'GTA: San Andreas'
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
                    ('toDown', MOD_ALT | MOD_SHIFT, getVK('.'), self.toDown),
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
                    ('moveToMapPtr', MOD_CONTROL | MOD_ALT, getVK('g'), self.moveToMapPtr),
                    ('dir_correct', MOD_ALT, getVK('e'), self.dir_correct),
                    ('re_cal_markers', MOD_ALT, getVK("'"), self.re_cal_markers),
                    ('go_next_marker', MOD_ALT, getVK('/'), self.go_next_marker),
                    ('move_marker_to_front', MOD_ALT | MOD_SHIFT, getVK('/'), self.move_marker_to_front),
                    ('move_near_vehicle_to_front', MOD_ALT, getVK('p'), self.nearVehicleToFront),
                    ('move_near_person_to_front', MOD_ALT | MOD_SHIFT, getVK('p'), self.nearPersonToFront),
                ))
        else:
            self.attach_status_view.label = '没有检测到 ' + windowName

    def dir_correct(self, _=None):
        # 按当前视角方向旋转
        if self.isInVehicle:
            mycar = self.vehicle
            mycar.coord[2] += 0.05
            self.handler.write(mycar.pos.addr, self.handler.read(address.CAM_Z_ADDR, bytes, 28), 0)
            mycar.flip()
        else:
            PI = math.pi
            HALF_PI = PI / 2
            cam_x = self.handler.readFloat(address.CAM_Z_ADDR)
            cam_y = self.handler.readFloat(address.CAM_Z_ADDR + 4)
            rot = -math.atan2(cam_x, cam_y) - HALF_PI
            self.rot_view.mem_value = rot

    def playerCoordFromMap(self, btn=None):
        # 从大地图读取坐标
        self.coord_view.views[0].value = str(self.handler.readFloat(address.MAP_X_ADDR))
        self.coord_view.views[1].value = str(self.handler.readFloat(address.MAP_Y_ADDR))

    def vehicleCoordFromMap(self, btn=None):
        # 从大地图读取坐标
        self.vehicle_coord_view.views[0].value = str(self.handler.readFloat(address.MAP_X_ADDR))
        self.vehicle_coord_view.views[1].value = str(self.handler.readFloat(address.MAP_Y_ADDR))

    def onSpawnVehicleIdChange(self, lb):
        self.spwan_vehicle_id = VEHICLE_LIST[lb.index][1]

    def onSpawnVehicleIdPrev(self, hotkeyId=None):
        pos = self.spawn_vehicle_id_view.index
        if pos == 0:
            pos = len(VEHICLE_LIST)
        self.spawn_vehicle_id_view.setSelection(pos - 1, True)

    def onSpawnVehicleIdNext(self, hotkeyId=None):
        pos = self.spawn_vehicle_id_view.index
        if pos == len(VEHICLE_LIST) - 1:
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

    def moveToMapPtr(self, _=None):
        coord = self.vehicle.coord
        coord[0] = self.handler.readFloat(address.MAP_X_ADDR)
        coord[1] = self.handler.readFloat(address.MAP_Y_ADDR)

    def setPlayerSpecial(self, checkbox, bitindex):
        """设置玩家特殊属性"""
        self.player.setSpecial(checkbox.checked, bitindex)

    def setVehicleSpecial(self, checkbox, bitindex):
        """设置当前汽车特殊属性"""
        self.player.lastCar.setSpecial(checkbox.checked, bitindex)

    def apply_player_special(self, btn=None):
        for cb in self.player_special_views:
            if cb.checked:
                cb.onchange(cb)

    def apply_vehicle_special(self, btn=None):
        for cb in self.vehicle_special_views:
            if cb.checked:
                cb.onchange(cb)

    def get_cheat_config(self):
        return cheat.version_config['V1.0']

    def toggle_cheat(self, checkbox, index):
        cheat_config = self.get_cheat_config()
        self.handler.write8(cheat_config['CHEATS_ADDR'][index], 1 if checkbox.checked else 0)

    def cheat_sync(self, btn=None):
        cheat_config = self.get_cheat_config()
        for index, view in enumerate(self.cheat_views):
            view.checked = self.handler.read8(cheat_config['CHEATS_ADDR'][index]) == 1

    """武器熟练度"""
    def get_weapon_prop(self, index):
        addr = self.get_cheat_config()['WEAPON_PROF_ADDR'][index]
        return normalFloat(self.handler.readFloat(addr))

    def set_weapon_prop(self, value, index):
        addr = self.get_cheat_config()['WEAPON_PROF_ADDR'][index]
        return self.handler.writeFloat(addr, value)

    def inject_spawn_code(self, btn=None):
        cheat_config = self.get_cheat_config()

        if not self.spawn_code_injected:
            if (
                self.handler.write(cheat_config['CodeInjectJumpAddr'], cheat_config['bInjectedJump'], 0)
                and self.handler.write(cheat_config['CodeInjectCodeAddr'], cheat_config['bInjectedCode'], 0)
            ):
                self.spawn_code_injected = True
                self.spawn_code_injected_view.label = "已插入"
        else:
            self.handler.write(cheat_config['CodeInjectJumpAddr'], cheat_config['bNotInjectedJump'], 0)
            self.spawn_code_injected = False
            self.spawn_code_injected_view.label = ""

    def freeze_timer(self, cb):
        """冻结任务中的计时"""
        cheat_config = self.get_cheat_config()
        if cb.checked:
            self.handler.write16(cheat_config['CodeInjectNOP_FreezeTimerDownAddr'], cheat.NOP)
            self.handler.write16(cheat_config['CodeInjectNOP_FreezeTimerUpAddr'], cheat.NOP)
        else:
            self.handler.write16(cheat_config['CodeInjectNOP_FreezeTimerDownAddr'], cheat.ORIGIN_TIMER_DOWN)
            self.handler.write16(cheat_config['CodeInjectNOP_FreezeTimerUpAddr'], cheat.ORIGIN_TIMER_UP)

    def one_hit_kill(self, cb):
        """一击必杀"""
        cheat_config = self.get_cheat_config()

        if cb.checked:
            self.handler.write(cheat_config['CodeInjectJump_OneHitKillAddr'], cheat_config['bInjectedJump_OneHitKill'], 0)
            self.handler.write(cheat_config['CodeInjectCode_OneHitKillAddr'], cheat_config['bInjectedCode_OneHitKill'], 0)
        else:
            self.handler.write(cheat_config['CodeInjectJump_OneHitKillAddr'], cheat_config['bNotInjectedJump_OneHitKill'], 0)

    def spawnVehicle(self, hotkeyId=None):
        carid = getattr(self, 'spwan_vehicle_id', None)
        if carid:
            self.handler.write32(cheat.SPAWN_VEHICLE_ID_BASE, carid)

    def vehicleLockDoor(self, btn=None, lock=True):
        car = self.player.lastCar
        if car:
            if lock:
                car.lockDoor()
            else:
                car.unlockDoor()

    def getWantedLevel(self):
        ptr = self.handler.read32(address.WANTED_LEVEL_ADDR)
        return self.handler.read8(ptr + 0x2C)

    def setWantedLevel(self, level):
        level = int(level)
        ptr = self.handler.read32(address.WANTED_LEVEL_ADDR)
        cops = (0, 1, 3, 5, 9, 1, 2)[level]
        wantedLevel = (0, 60, 200, 700, 1500, 3000, 5000)[level]
        self.handler.write32(ptr, wantedLevel)
        self.handler.write8(ptr + 0x19, cops)
        self.handler.write8(ptr + 0x2C, level)

    """重新获取人/车标记点"""
    def re_cal_markers(self, _=None):
        addr = address.MARKER_ADDR
        it = Marker(addr, self.handler)
        self._markers = []

        for i in range(175):
            blipType = it.blipType
            if blipType is Marker.MARKER_TYPE_CAR or blipType is Marker.MARKER_TYPE_CHAR:
                self._markers.append(Marker(it.addr, self.handler))

            it.next()

        self._marker_index = 0

    """到下一处 人/车标记点"""
    def go_next_marker(self, _=None):
        if not hasattr(self, '_markers'):
            self.re_cal_markers()

        while True:
            try:
                entity = self._markers[self._marker_index].entity
            except IndexError:
                self.re_cal_markers()
                return
            if entity:
                self.vehicle.coord = self._markers[self._marker_index].entity.coord
                break
            self._marker_index += 1

    """人/车标记点目标移到眼前"""
    def move_marker_to_front(self, _=None):
        if not hasattr(self, '_markers'):
            self.re_cal_markers()

        moved_car_addr = []
        front_coord = self.get_front_coord()

        for marker in self._markers:
            entity = marker.entity
            if isinstance(entity, Player):
                car = entity.lastCar
                if car and car.hp > 1: 
                    if car.addr not in moved_car_addr:
                        moved_car_addr.append(car.addr)
                        car.coord = front_coord
                else:
                    entity.coord = front_coord
            elif isinstance(entity, Vehicle):
                entity.coord = front_coord


ins = None
win_style = {
    'width': 680,
    'height': 920,
}