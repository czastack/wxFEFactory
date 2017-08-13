from functools import partial
from fefactory_api.emuhacker import ProcessHandler
from lib.hack.form import Group, Widget, InputWidget, CheckBoxWidget, CoordsWidget
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
from lib.win32.sendkey import auto, TextVK
from commonstyle import dialog_style, styles
from .vehicle import vehicle_list
from . import models, cheat
import math
import os
import json
import time
import __main__
import fefactory_api
ui = fefactory_api.ui


ACTOR_POOL_POINTER   = 0x00B74490
ACTOR_POINTER_SELF   = 0x00B7CD98
VEHICLE_POOL_POINTER = 0x00B74494
VEHICLE_POINTER_SELF = 0x00B6F980

PLAYER_BASE  = 0xB6F5F0
PLAYER2_BASE  = 0xB7CD98
VEHICLE_BASE = 0xB6F3B8
MONEY_BASE   = 0xB7CE50

MAX_HEALTH_STAT_ADDR = 0xB793E0
ENERGY_STAT_ADDR = 0xB790B4
WEAPON_PROF_STAT_ADDR = 0xB79494

CHEAT_COUNT_ADDR = 0xB79044
CHEAT_STAT_ADDR = 0x96918C
OPENED_ISLANDS_ADDR = 0xB790F4

FAT_STAT_ADDR = 0xB793D4
STAMINA_STAT_ADDR = 0xB793D8
MUSCLE_STAT_ADDR = 0xB793DC
LUNG_CAPACITY_ADDR = 0xB791A4
GAMBLING_STAT_ADDR = 0xB794C4
CAR_PROF_ADDR = 0xB790A0
BIKE_PROF_ADDR = 0xB791B4
CYCLE_PROF_ADDR = 0xB791B8
FLYING_PROF_ADDR = 0xB7919C

DAYS_IN_GAME_ADDR = 0xB79038
CURR_HOUR_ADDR = 0xB70153
CURR_MINUTE_ADDR = 0xB70152
CURR_WEEKDAY_ADDR = 0xB7014E # 1 to 7
GAME_SPEED_MS_ADDR = 0xB7015C # Defines how many ms = 1 second... default 1000, set to 1 for a headache
GAME_SPEED_PCT_ADDR = 0xB7CB64 # defines the speed of the game, 1 = 100%, float
WEATHER_LOCK_ADDR = 0xC81318
WEATHER_TO_GO_ADDR = 0xC8131C
WEATHER_CURRENT_ADDR = 0xC81320



class WeaponWidget(Widget):
    def __init__(self, name, label, slot):
         self.slot = slot
         self.has_ammo = self.slot in models.SLOT_HAS_AMMO
         super().__init__(name, label, None, None)

    def render(self):
        super().render()
        with ui.Horizontal(className="fill"):
            self.id_view = ui.Choice(className="fill", choices=(item[2] for item in models.WEAPON_LIST[self.slot]))
            if self.has_ammo:
                self.ammo_view = ui.SpinCtrl(className="fill", min=0, max=9999, initial=0)
            self.render_btn()

    @property
    def mem_value(self):
        handler = self._handler
        return models.Player(handler.read32(PLAYER_BASE), handler).weapons[self.slot]

    @mem_value.setter
    def mem_value(self, value):
        self.mem_value.set(value)

    @property
    def input_value(self):
        id_ = models.WEAPON_LIST[self.slot][self.id_view.index][0]
        ammo = self.ammo_view.value if self.has_ammo else 0
        return (id_, ammo)

    @input_value.setter
    def input_value(self, value):
        weapon_id =  value.id
        i = 0
        for item in models.WEAPON_LIST[self.slot]:
            if item[0] == weapon_id:
                break
            i += 1
        else:
            return
        self.id_view.setSelection(i)
        if self.has_ammo:
            self.ammo_view.value = value.ammo

    def read(self):
        self.input_value = self.mem_value

    def write(self):
        self.mem_value = self.input_value


class Tool:

    def __init__(self):
        self.handler = ProcessHandler()
        self.jetPackSpeed = 2.0
        self.spawn_code_injected = False

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

        with ui.HotkeyWindow("圣安地列斯Hack", style=win_style, styles=styles, menuBar=menubar) as win:
            with ui.Vertical():
                with ui.Horizontal(className="expand container"):
                    ui.Button("检测", className="vcenter", onclick=self.checkAttach)
                    self.attach_status_view = ui.Text("", className="label_left grow")
                    ui.CheckBox("保持最前", onchange=self.swithKeeptop)
                with ui.Notebook(className="fill"):
                    self.render_main()

        win.setOnclose(self.onClose)
        self.win = win

    def render_main(self):
        with Group("player", "角色", PLAYER_BASE, handler=self.handler):
            self.hp_view = InputWidget("hp", "生命", None, (0x540,), float)
            self.maxhp_view = InputWidget("maxhp", "最大生命", None, (0x544,), float)
            self.ap_view = InputWidget("ap", "防弹衣", None, (0x548,), float)
            self.rot_view = InputWidget("rotation", "旋转", None, (0x55c,), float)
            self.coord_view = CoordsWidget("coord", "坐标", None, (0x14, 0x30), savable=True)
            self.speed_view = CoordsWidget("speed", "速度", None, (0x44,))
            self.weight_view = InputWidget("weight", "重量", None, (0x8c,), float)
            # self.stamina_view = InputWidget("stamina", "体力", None, (0x600,), float)
            # self.star_view = InputWidget("star", "通缉等级", None, (0x5f4, 0x20), int)
            ui.Text("")
            with ui.Vertical(className="fill"):
                ui.Button(label="车坐标->人坐标", onclick=self.fromVehicleCoord)
                ui.Hr()
                ui.Text("防止主角受到来自以下的伤害")
                with ui.Horizontal(className="fill"):
                    self.player_special_views = [
                        ui.CheckBox("爆炸", className="vcenter", onchange=partial(self.setPlayerSpecial, bitindex=models.Player.SPECIAL_EP)),
                        ui.CheckBox("碰撞", className="vcenter", onchange=partial(self.setPlayerSpecial, bitindex=models.Player.SPECIAL_DP)),
                        ui.CheckBox("子弹", className="vcenter", onchange=partial(self.setPlayerSpecial, bitindex=models.Player.SPECIAL_BP)),
                        ui.CheckBox("火焰", className="vcenter", onchange=partial(self.setPlayerSpecial, bitindex=models.Player.SPECIAL_FP)),
                    ]
                    ui.Button("再次应用", onclick=self.apply_player_special).setToolTip("死亡或者重新读档后需要再次应用")
        with Group("vehicle", "汽车", VEHICLE_BASE, handler=self.handler):
            self.vehicle_hp_view = InputWidget("vehicle_hp", "HP", None, (0x4c0,), float)
            self.vehicle_dir_view = CoordsWidget("dir", "方向", None, (0x14,))
            self.vehicle_grad_view = CoordsWidget("grad", "旋转", None, (0x14, 0))
            self.vehicle_coord_view = CoordsWidget("coord", "坐标", None, (0x14, 0x30), savable=True)
            self.vehicle_speed_view = CoordsWidget("speed", "速度", None, (0x44,))
            self.spin_view = CoordsWidget("spin", "轮子", None, (0x50,))
            self.weight_view = InputWidget("weight", "重量", None, (0x8c,), float)
            ui.Text("")
            with ui.Vertical(className="fill"):
                ui.Button(label="人坐标->车坐标", onclick=self.fromPlayerCoord)
                ui.Hr()
                ui.Text("防止当前载具受到来自以下的伤害")
                with ui.Horizontal(className="fill"):
                    self.vehicle_special_views = [
                        ui.CheckBox("爆炸", className="vcenter", onchange=partial(self.setVehicleSpecial, bitindex=models.Vehicle.SPECIAL_EP)),
                        ui.CheckBox("碰撞", className="vcenter", onchange=partial(self.setVehicleSpecial, bitindex=models.Vehicle.SPECIAL_DP)),
                        ui.CheckBox("子弹", className="vcenter", onchange=partial(self.setVehicleSpecial, bitindex=models.Vehicle.SPECIAL_BP)),
                        ui.CheckBox("火焰", className="vcenter", onchange=partial(self.setVehicleSpecial, bitindex=models.Vehicle.SPECIAL_FP)),
                    ]
                    ui.Button("再次应用", onclick=self.apply_vehicle_special).setToolTip("切换载具后需要再次应用")
        with Group("weapon", "武器", None, handler=self.handler):
            self.weapon_views = []
            for i in range(13):
                self.weapon_views.append(WeaponWidget("weapon%d" % i, "武器槽%d" % (i + 1), i))
            
        with Group("global", "全局", 0, handler=self.handler):
            self.money_view = InputWidget("money", "金钱", MONEY_BASE, (), int)
            InputWidget("cheat_count", "作弊次数", CHEAT_COUNT_ADDR, (), int)
            InputWidget("cheat_stat", "作弊状态", CHEAT_STAT_ADDR, (), int)
            InputWidget("fat_stat", "肥胖度", FAT_STAT_ADDR, (), float)
            InputWidget("stamina_stat", "耐力值", STAMINA_STAT_ADDR, (), float)
            InputWidget("muscle_stat", "肌肉值", MUSCLE_STAT_ADDR, (), float)
            InputWidget("lung_capacity", "肺活量", LUNG_CAPACITY_ADDR, (), int)
            InputWidget("gambling_stat", "赌博技术", GAMBLING_STAT_ADDR, (), int)
            InputWidget("car_prof", "驾驶技术", CAR_PROF_ADDR, (), int)
            InputWidget("bike_prof", "摩托车技术", BIKE_PROF_ADDR, (), int)
            InputWidget("cycle_prof", "自行车技术", CYCLE_PROF_ADDR, (), int)
            InputWidget("flying_prof", "飞行技术", FLYING_PROF_ADDR, (), int)
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
                with ui.Horizontal(className="fill container"):
                    ui.Button("同步", onclick=self.cheat_sync)
                    ui.Button("插入生产载具的代码", onclick=self.inject_spawn_code)
                    self.spawn_code_injected_view = ui.Text("")

        with Group(None, "快捷键", 0, handler=self.handler, flexgrid=False, hasfootbar=False):
            with ui.Horizontal(className="fill container"):
                self.spawn_vehicle_id_view = ui.ListBox(className="expand", onselect=self.onSpawnVehicleIdChange, 
                    choices=(item[0] for item in vehicle_list))
                with ui.ScrollView(className="fill container"):
                    ui.Text("根据左边列表生产载具: alt+V")
                    ui.Text("切换上一辆: ctrl+alt+[")
                    ui.Text("切换下一辆: ctrl+alt+]")
                    ui.Text("向前穿墙: alt+w")
                    ui.Text("向前穿墙大: alt+shift+w")
                    ui.Text("弹射起步: alt+m")
                    ui.Text("上天（有速度）: alt+空格")
                    ui.Text("往上（无速度）: alt+.")
                    ui.Text("下坠: alt+shift+空格")
                    ui.Text("恢复HP: alt+h")
                    ui.Text("恢复大量HP(999生命，999护甲): alt+shift+h")
                    ui.Text("附近的人上天: alt+f")
                    ui.Text("附近的车翻转: alt+shift+k")
                    ui.Text("自己的车翻转: alt+k")
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
        global ins
        ins = None

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
                    ('stop', MOD_ALT, getVK('x'), self.stop),
                    ('restoreHp', MOD_ALT, getVK('h'), self.restoreHp),
                    ('restoreHpLarge', MOD_ALT | MOD_SHIFT, getVK('h'), self.restoreHpLarge),
                    ('spawnVehicle', MOD_ALT, getVK('v'), self.spawnVehicle),
                    ('spawnVehicleIdPrev', MOD_ALT, getVK('['), self.onSpawnVehicleIdPrev),
                    ('spawnVehicleIdNext', MOD_ALT, getVK(']'), self.onSpawnVehicleIdNext),
                    ('jumpOnVehicle', MOD_ALT, getVK('j'), self.jumpOnVehicle),
                    ('nearPersonFly', MOD_ALT, getVK('f'), self.nearPersonFly),
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
    def player(self):
        player_addr = self.handler.read32(PLAYER_BASE)
        if player_addr is 0:
            return None
        player = getattr(self, '_player', None)
        if not player:
            player = self._player = models.Player(player_addr, self.handler)
        elif player.addr != player_addr:
            player.addr = player_addr
        return player

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

    def raiseUp(self, hotkeyId=None, speed=0):
        if not speed:
            speed = 0.6 if self.isInVehicle else 1.0
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

    def onSpawnVehicleIdChange(self, lb):
        self.spwan_vehicle_id = vehicle_list[lb.index][1]

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
        pool_ptr = self.handler.read32(ACTOR_POOL_POINTER)
        pool_start = self.handler.read32(pool_ptr)
        pool_size = self.handler.read32(pool_ptr + 8)
        for i in range(pool_size):
            yield models.Player(pool_start, self.handler)
            pool_start += 0x7c4

    def getNearPersons(self, distance=100):
        coord = self.player.coord.values()
        myaddr = self.handler.read32(PLAYER_BASE)
        for p in self.getPersons():
            if p.hp != 0 and p.distance(coord) <= distance:
                if p.addr != myaddr:
                    yield p

    def getVehicles(self):
        pool_ptr = self.handler.read32(VEHICLE_POOL_POINTER)
        pool_start = self.handler.read32(pool_ptr)
        pool_size = self.handler.read32(pool_ptr + 8)
        for i in range(pool_size):
            yield models.Vehicle(pool_start, self.handler)
            pool_start += 0xa18

    def getNearVehicles(self, distance=100):
        coord = self.player.coord.values()
        mycarAddr = self.handler.read32(VEHICLE_BASE)
        for v in self.getVehicles():
            if v.hp != 0 and v.distance(coord) <= distance:
                if v.addr != mycarAddr:
                    yield v

    def killNearPerson(self, btn=None):
        for p in self.getNearPersons():
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

    def nearVehicleFlip(self, btn=None):
        for v in self.getNearVehicles():
            v.flip()

    def jumpOnVehicle(self, btn=None):
        for v in self.getNearVehicles():
            if v.numPassengers:
                v.stop()
                coord = v.coord.values()
                coord[2] += 1
                self.player.coord = coord
                break

    def nearPersonFly(self, btn=None):
        for p in self.getNearPersons():
            p.speed[2] = 1

    def vehicleFlip(self, _=None):
        grad = self.player.lastCar.flip()

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

    def inject_spawn_code(self, btn=None):
        cheat_config = self.get_cheat_config()

        if not self.spawn_code_injected:
            self.handler.write(cheat_config['CodeInjectJumpAddr'], 0, cheat_config['bInjectedJump'])
            self.handler.write(cheat_config['CodeInjectCodeAddr'], 0, cheat_config['bInjectedCode'])
            self.spawn_code_injected = True
            spawn_code_injected_view.value = "已插入"
        else:
            self.handler.write(cheat_config['CodeInjectJumpAddr'], 0, cheat_config['bNotInjectedJump'])
            self.spawn_code_injected = False
            spawn_code_injected_view.value = ""

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
            self.handler.write(cheat_config['CodeInjectJump_OneHitKillAddr'], 0, cheat_config['bInjectedJump_OneHitKill'])
            self.handler.write(cheat_config['CodeInjectCode_OneHitKillAddr'], 0, cheat_config['bInjectedCode_OneHitKill'])
        else:
            self.handler.write(cheat_config['CodeInjectJump_OneHitKillAddr'], 0, cheat_config['bNotInjectedJump_OneHitKill'])

    def spawnVehicle(self, hotkeyId=None):
        carid = getattr(self, 'spwan_vehicle_id', None)
        if carid:
            self.handler.write32(cheat.SPAWN_VEHICLE_ID_BASE, carid)

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


ins = None
win_style = {
    'width': 640,
    'height': 820,
}

def run():
    global ins
    ins = GTA_VC_Cheat()

if __name__ == 'testgta':
    run()