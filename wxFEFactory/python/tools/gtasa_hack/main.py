from functools import partial
from lib.hack.form import (
    Group, InputWidget, ProxyInputWidget, SelectWidget, ModelInputWidget, ModelCoordWidget
)
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
from lib.win32.sendkey import auto, TextVK
from lib.utils import normalFloat
from commonstyle import dialog_style, styles
from . import cheat, address, models
from .data import SLOT_NO_AMMO, WEAPON_LIST, VEHICLE_LIST, WEATHER_LIST, COLOR_LIST
from .models import Player, Vehicle
from .script import RunningScript
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
    CLASS_NAME = 'Grand theft auto San Andreas'
    WINDOW_NAME = 'GTA: San Andreas'
    address = address
    models = models
    Player = Player
    Vehicle = Vehicle
    MARKER_RANGE = 175
    GO_FORWARD_COORD_RATE = 2.0
    SLING_SPEED_RATE = 4
    DEST_DEFAULT_COLOR = 0
    VEHICLE_LIST = VEHICLE_LIST
    RunningScript = RunningScript

    def render_main(self):
        with Group("player", "角色", self._player, handler=self.handler):
            self.hp_view = ModelInputWidget("hp", "生命")
            self.maxhp_view = ModelInputWidget("maxhp", "最大生命")
            self.ap_view = ModelInputWidget("ap", "防弹衣")
            self.rot_view = ModelInputWidget("rotation", "旋转")
            self.coord_view = ModelCoordWidget("coord", "坐标", savable=True)
            self.speed_view = ModelCoordWidget("speed", "速度")
            self.weight_view = ModelInputWidget("weight", "重量")
            self.wanted_level_view = ProxyInputWidget("wanted_level", "通缉等级", self.get_wanted_level, self.set_wanted_level)
            ui.Text("")
            with ui.Vertical(className="fill"):
                with ui.Horizontal(className="expand"):
                    ui.Button(label="车坐标->人坐标", onclick=self.from_vehicle_coord)
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
                    ui.Button("全部", onclick=self.player_special_all)
                    ui.Button("再次应用", onclick=self.player_special_apply).setToolTip("死亡或者重新读档后需要再次应用")
        with Group("vehicle", "汽车", self._vehicle, handler=self.handler):
            self.vehicle_hp_view = ModelInputWidget("hp", "HP")
            self.vehicle_dir_view = ModelCoordWidget("dir", "方向")
            self.vehicle_grad_view = ModelCoordWidget("grad", "旋转")
            self.vehicle_coord_view = ModelCoordWidget("coord", "坐标", savable=True)
            self.vehicle_speed_view = ModelCoordWidget("speed", "速度")
            self.weight_view = ModelInputWidget("weight", "重量")
            ui.Text("")
            with ui.Vertical(className="fill"):
                with ui.Horizontal(className="expand"):
                    ui.Button(label="人坐标->车坐标", onclick=self.from_player_coord)
                    ui.Button(label="从地图读取坐标", onclick=self.vehicleCoordFromMap)
                    ui.Button(label="锁车", onclick=self.vehicle_lock_door)
                    ui.Button(label="开锁", onclick=partial(self.vehicle_lock_door, lock=False))
                ui.Hr()
                ui.Text("防止当前载具受到来自以下的伤害")
                with ui.Horizontal(className="fill"):
                    self.vehicle_special_views = [
                        ui.CheckBox("爆炸", className="vcenter", onchange=partial(self.setVehicleSpecial, bitindex=Vehicle.SPECIAL_EP)),
                        ui.CheckBox("碰撞", className="vcenter", onchange=partial(self.setVehicleSpecial, bitindex=Vehicle.SPECIAL_DP)),
                        ui.CheckBox("子弹", className="vcenter", onchange=partial(self.setVehicleSpecial, bitindex=Vehicle.SPECIAL_BP)),
                        ui.CheckBox("火焰", className="vcenter", onchange=partial(self.setVehicleSpecial, bitindex=Vehicle.SPECIAL_FP)),
                    ]
                    ui.Button("全部", onclick=self.vehicle_special_all)
                    ui.Button("再次应用", onclick=self.vehicle_special_apply).setToolTip("切换载具后需要再次应用")
            ui.Text("颜色")
            with ui.Horizontal(className="fill"):
                self.vehicle_body_color_view = ColorWidget("body_color", "车身1", self._vehicle, "body_color", COLOR_LIST)
                self.vehicle_body2_color_view = ColorWidget("body2_color", "车身2", self._vehicle, "body2_color", COLOR_LIST)
                self.vehicle_stripe_color_view = ColorWidget("stripe_color", "条纹1", self._vehicle, "stripe_color", COLOR_LIST)
                self.vehicle_stripe2_color_view = ColorWidget("stripe2_color", "条纹2", self._vehicle, "stripe2_color", COLOR_LIST)

        with Group("weapon", "武器槽", None, handler=self.handler):
            self.weapon_views = []
            for i in range(13):
                self.weapon_views.append(
                    WeaponWidget("weapon%d" % i, "武器槽%d" % (i + 1), i, SLOT_NO_AMMO, WEAPON_LIST, self._player, self.on_weapon_change)
                )

        with Group("weapon_prop", "武器熟练度", None, handler=self.handler):
            self.weapon_prop_views = [
                ProxyInputWidget("weapon_prop_%d" % i, label, 
                    partial(self.get_weapon_prop, index=i), partial(self.set_weapon_prop, index=i)) for i, label in enumerate((
                        '手枪', '消音手枪', '沙漠之鹰', '霰弹枪', '短管霰弹枪', '战斗霰弹枪', 'MP5', 'Tech9', 'AK47', 'M4',
                    ))
            ]
            
        with Group("global", "全局", 0, handler=self.handler):
            self.money_view = InputWidget("money", "金钱", address.MONEY)
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
            InputWidget("police_time", "义警回车时间(ms)", address.POLICE_TIME_ADDR)

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

        with Group(None, "女友进度", 0, handler=self.handler):
            # TODO
            address.GIRL_FRIEND_PROGRESS_ADDR = self.get_cheat_config()['GIRL_FRIEND_PROGRESS_ADDR']
            for i, label in enumerate(['Denise', 'Michelle', 'Helena', 'Katie', 'Barbara', 'Millie']):
                InputWidget(label, label, address.GIRL_FRIEND_PROGRESS_ADDR[i])

        with Group(None, "快捷键", 0, handler=self.handler, flexgrid=False, hasfootbar=False):
            with ui.Horizontal(className="fill container"):
                self.spawn_vehicle_id_view = ui.ListBox(className="expand", onselect=self.on_spawn_vehicle_id_change, 
                    choices=(item[0] for item in VEHICLE_LIST))
                with ui.ScrollView(className="fill container"):
                    self.render_common_text()
                    ui.Text("根据左边列表生产载具: alt+V")
                    ui.Text("瞬移到地图指针处: ctrl+alt+g")
                    ui.Text("切换转向并加速: alt+shift+m")

        with Group(None, "测试", 0, handler=self.handler, flexgrid=False, hasfootbar=False):
            with ui.GridLayout(cols=4, vgap=10, className="fill container"):
                self.render_common_button()
                ui.Button(label="洗衣服", onclick=self.clothes_rebuild)
                ui.Button("敌人爆炸", onclick=self.enemys_explode)
                ui.Button("瞬移到目的地(红)", onclick=self.teleport_to_destination)
                ui.Button("瞬移到目的地(绿)", onclick=partial(self.teleport_to_destination, color=1))
                ui.Button("瞬移到目的地(黄)", onclick=partial(self.teleport_to_destination, color=8))
                
        with Group(None, "工具", 0, flexgrid=False, hasfootbar=False):
            with ui.Vertical(className="fill container"):
                ui.Button("g3l坐标转json", onclick=self.g3l2json)

    def get_hotkeys(self):
        return (
            ('turn_and_speed_up', MOD_ALT | MOD_SHIFT, getVK('m'), self.turn_and_speed_up),
            ('near_objects_to_front', MOD_ALT | MOD_SHIFT, getVK('o'), self.near_objects_to_front),
            ('dir_correct', MOD_ALT, getVK('e'), self.dir_correct),
            ('moveToMapPtr', MOD_CONTROL | MOD_ALT, getVK('g'), self.moveToMapPtr),
        ) + self.get_common_hotkeys()

    def init_remote_function(self):
        super().init_remote_function()
        
        script_ctx_addr = self.handler.alloc_memory(self.RunningScript.SIZE)
        self.script_context = self.RunningScript(script_ctx_addr, self, 
            address.SCRIPT_SPACE_BASE, address.FUNC_CRunningScript__ProcessOneCommand, address.FUNC_CRunningScript__Init)

    def free_remote_function(self):
        super().free_remote_function()
        del self.script_context

    def script_call(self, command_id, signature, *args):
        """执行一条脚本"""
        if self.handler.active:
            return self.script_context.run(command_id, signature, *args)

    def is_model_loaded(self, model_id):
        return self.native_call_auto(address.FUNC_CStreaming__HasModelLoaded, 'L', model_id) & 0xFF

    def load_model(self, model_id):
        if model_id > 0 and not self.is_model_loaded(model_id):
            self.native_call_auto(address.FUNC_CStreaming__RequestModel, '2L', model_id, 6)
            self.native_call_auto(address.FUNC_LoadAllRequestedModels, 'L', 0)

    def on_weapon_change(self, weapon_view):
        self.load_model(weapon_view.selected_item[1])

    def restore_hp(self, _=None):
        """恢复hp，所乘载具会复原"""
        super().restore_hp()
        if self.isInVehicle:
            vehicle = self.vehicle
            self.fix_vehicle(vehicle)

    def dir_correct(self, _=None):
        # 按当前视角方向旋转
        if self.isInVehicle:
            mycar = self.vehicle
            mycar.coord[2] += 0.05
            self.handler.write(mycar.pos.addr, self.handler.read(address.CAMERA, bytes, 28), 0)
            mycar.flip()
        else:
            PI = math.pi
            HALF_PI = PI / 2
            cam_x = self.handler.readFloat(address.CAMERA)
            cam_y = self.handler.readFloat(address.CAMERA + 4)
            rot = -math.atan2(cam_x, cam_y) - HALF_PI
            self.rot_view.mem_value = rot

    def playerCoordFromMap(self, _=None):
        # 从大地图读取坐标
        self.coord_view.views[0].value = str(self.handler.readFloat(address.MAP_X_ADDR))
        self.coord_view.views[1].value = str(self.handler.readFloat(address.MAP_Y_ADDR))

    def vehicleCoordFromMap(self, _=None):
        # 从大地图读取坐标
        self.vehicle_coord_view.views[0].value = str(self.handler.readFloat(address.MAP_X_ADDR))
        self.vehicle_coord_view.views[1].value = str(self.handler.readFloat(address.MAP_Y_ADDR))

    def moveToMapPtr(self, _=None):
        coord = self.vehicle.coord
        coord[0] = self.handler.readFloat(address.MAP_X_ADDR)
        coord[1] = self.handler.readFloat(address.MAP_Y_ADDR)

    def setPlayerSpecial(self, checkbox, bitindex):
        """设置玩家特殊属性"""
        self.player.setSpecial(checkbox.checked, bitindex)

    def setVehicleSpecial(self, checkbox, bitindex):
        """设置当前汽车特殊属性"""
        self.player.vehicle.setSpecial(checkbox.checked, bitindex)

    def player_special_all(self, _=None):
        for cb in self.player_special_views:
            if not cb.checked:
                cb.checked = True
            cb.onchange(cb)

    def player_special_apply(self, _=None):
        for cb in self.player_special_views:
            if cb.checked:
                cb.onchange(cb)

    def vehicle_special_apply(self, _=None):
        for cb in self.vehicle_special_views:
            if cb.checked:
                cb.onchange(cb)

    def vehicle_special_all(self, _=None):
        for cb in self.vehicle_special_views:
            if not cb.checked:
                cb.checked = True
            cb.onchange(cb)

    def raise_up(self, _=None, speed=15):
        """升高(有速度)"""
        if self.isInVehicle:
            self.vehicle.speed[2] = 0.5
        else:
            self.player.speed[2] = 1

    def to_up(self, _=None):
        """升高(无速度)"""
        if self.isInVehicle:
            self.vehicle.coord[2] += 10
        else:
            self.player.coord[2] += 3

    def get_cheat_config(self):
        return cheat.version_config['V1.0']

    def toggle_cheat(self, checkbox, index):
        cheat_config = self.get_cheat_config()
        self.handler.write8(cheat_config['CHEATS_ADDR'][index], 1 if checkbox.checked else 0)

    def cheat_sync(self, _=None):
        cheat_config = self.get_cheat_config()
        for index, view in enumerate(self.cheat_views):
            view.checked = self.handler.read8(cheat_config['CHEATS_ADDR'][index]) == 1

    def turn_and_speed_up(self, _=None):
        self.dir_correct()
        self.speed_up()

    def get_weapon_prop(self, index):
        """武器熟练度"""
        addr = self.get_cheat_config()['WEAPON_PROF_ADDR'][index]
        return normalFloat(self.handler.readFloat(addr))

    def set_weapon_prop(self, value, index):
        addr = self.get_cheat_config()['WEAPON_PROF_ADDR'][index]
        return self.handler.writeFloat(addr, value)

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

    # def spawn_vehicle(self, model_id):
    #     self.handler.write32(cheat.SPAWN_VEHICLE_ID_BASE, model_id)

    def spawn_vehicle(self, model_id):
        self.load_model(model_id)
        self.script_call(0xa5, 'L3fP', model_id, *self.get_front_coord(), self.native_context.get_temp_addr())
        vehicle_handle = self.native_context.get_temp_value()
        if vehicle_handle:
            return self.vehicle_pool[vehicle_handle >> 8]

    def vehicle_lock_door(self, _=None, lock=True):
        car = self.player.vehicle
        if car:
            if lock:
                car.lock_door()
            else:
                car.unlock_door()

    def get_wanted_level(self):
        ptr = self.handler.read32(address.WANTED_LEVEL_ADDR)
        return self.handler.read8(ptr + 0x2C)

    def set_wanted_level(self, level):
        level = int(level)
        ptr = self.handler.read32(address.WANTED_LEVEL_ADDR)
        cops = (0, 1, 3, 5, 9, 1, 2)[level]
        wantedLevel = (0, 60, 200, 700, 1500, 3000, 5000)[level]
        self.handler.write32(ptr, wantedLevel)
        self.handler.write8(ptr + 0x19, cops)
        self.handler.write8(ptr + 0x2C, level)

    def get_objects(self):
        pool = models.Pool(address.OBJECT_POOL, self.handler, models.Object)
        return iter(pool)

    def get_near_objects(self, distance=100):
        """获取附近的物品"""
        coord = self.player.coord.values()
        for o in self.get_objects():
            if o.coord[2] > 0 and o.distance(coord) <= distance:
                yield o

    def near_objects_to_front(self, _=None):
        """附近的物品移到眼前"""
        coord = self.get_front_coord()
        for o in self.get_near_objects():
            o.coord = coord

    @property
    def system_time(self):
        return self.handler.read32(address.SYSTEM_TIME)

    def get_camera_rot(self):
        return (
            self.handler.readFloat(address.CAMERA + 0x10),
            self.handler.readFloat(address.CAMERA + 0x14),
            self.handler.readFloat(address.CAMERA + 0x18)
        )

    EXPLOSION_TYPE_GRENADE = 0
    EXPLOSION_TYPE_MOLOTOV = 1
    EXPLOSION_TYPE_ROCKET = 2
    EXPLOSION_TYPE_ROCKET_WEAK = 3
    EXPLOSION_TYPE_CAR = 4
    EXPLOSION_TYPE_CAR_QUICK = 5
    EXPLOSION_TYPE_BOAT = 6
    EXPLOSION_TYPE_HELI = 7
    EXPLOSION_TYPE_MINE = 8
    EXPLOSION_TYPE_OBJECT = 9
    EXPLOSION_TYPE_TANK_GRENADE = 10
    EXPLOSION_TYPE_SMALL = 11
    EXPLOSION_TYPE_TINY = 12
    def create_explosion(self, coord, explosionType=EXPLOSION_TYPE_ROCKET, fCameraShake=0.3):
        """产生爆炸"""
        # (pExplodingEntity, pOwner, explosionType, vecPosition, uiActivationDelay, bMakeSound, fCamShake, bNoDamage)
        self.native_call_auto(address.FUNC_AddExplosion, '2LL3fLLfL', 0, 0, explosionType, *coord, 0, 1, fCameraShake, 0)
        # self.script_call(0x20C, '3fL', *coord, explosionType)

    def fix_vehicle(self, vehicle):
        """修车"""
        vehicle.hp = 1000
        model_id = vehicle.model_id

        is_type = lambda addr: self.native_call_auto(addr, 'L', model_id) & 0xFF
        fix_addr = None

        if is_type(address.FUNC_IsCarModel) or is_type(address.FUNC_IsMonsterTruckModel) or is_type(address.FUNC_IsTrailerModel):
            fix_addr = address.FUNC_CAutomobile__Fix
        elif is_type(address.FUNC_IsPlaneModel):
            fix_addr = address.FUNC_CPlane__Fix
        elif is_type(address.FUNC_IsHeliModel):
            fix_addr = address.FUNC_CHeli__Fix
        elif is_type(address.FUNC_IsBikeModel):
            fix_addr = address.FUNC_CBike_Fix

        if fix_addr:
            self.native_call_auto(fix_addr, None, this=vehicle.addr)

    def clothes_rebuild(self, _=None):
        """洗衣服"""
        self.native_call_auto(address.FUNC_CClothes__RebuildPlayer, '2L', self.player.addr, 0)

    def get_enemys(self):
        """获取红色标记的peds"""
        for blip in self.get_target_blips():
            color = blip.color
            if blip.bright:
                color -= 7
            if color is 0:
                yield blip.entity

    def get_friends(self):
        """获取蓝色标记的peds"""
        for blip in self.get_target_blips():
            color = blip.color
            if color is 7 and not blip.bright:
                yield blip.entity

    def enemys_explode(self, _=None):
        """敌人爆炸"""
        for e in self.get_enemys():
            self.create_explosion(e.coord)