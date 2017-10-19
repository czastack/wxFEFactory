from functools import partial
from lib.hack.form import Group, InputWidget, CheckBoxWidget, CoordWidget, ModelInputWidget, ModelCoordWidget
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
from lib.win32.sendkey import auto, TextVK
from lib import utils
from commonstyle import dialog_style, styles
from ..gta_base.main import BaseGTATool
from ..gta_base.widgets import WeaponWidget
from ..gta_base.utils import degreeToRadian
from . import address, models
from .data import VEHICLE_LIST
from .models import Player, Vehicle
from .native import NativeContext
import math
import os
import json
import time
import __main__
import fefactory_api
ui = fefactory_api.ui


class Tool(BaseGTATool):
    address = address
    models = models
    Player = Player
    Vehicle = Vehicle

    SAFE_SPEED_RATE = 15
    SAFE_SPEED_UP = 6
    GO_FORWARD_COORD_RATE = 3
    FLY_SPEED = 15
    SLING_SPEED_RATE = 60
    SLING_COORD_UP = 3
    from .data import WEAPON_LIST, SLOT_NO_AMMO

    def render_main(self):
        with Group("player", "角色", self._player, handler=self.handler):
            self.hp_view = ModelInputWidget("hp", "生命")
            self.ap_view = ModelInputWidget("ap", "防弹衣")
            self.coord_view = ModelCoordWidget("coord", "坐标", savable=True)
            # self.weight_view = ModelInputWidget("gravity", "重量")
            self.speed_view = ModelCoordWidget("speed", "速度")
            self.rot_view = ModelInputWidget("rotation", "旋转")
            self.wanted_level = ModelInputWidget("wanted_level", "通缉等级")
            self.money = ModelInputWidget("money", "金钱")
            ui.Text("")
            with ui.GridLayout(cols=4, vgap=10, className="expand"):
                ui.Button(label="车坐标->人坐标", onclick=self.from_vehicle_coord)
                ui.Button(label="开启无伤", onclick=self.set_ped_invincible)
                ui.Button(label="可以切换武器", onclick=self.set_ped_block_switch_weapons)
                ui.Button(label="不会被拽出车", onclick=self.set_ped_can_be_dragged_out_of_vehicle)
                ui.Button(label="摩托车老司机", onclick=self.set_ped_keep_bike)

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
            for i in range(1, len(self.WEAPON_LIST)):
                self.weapon_views.append(WeaponWidget("weapon%d" % i, "武器槽%d" % i, i, self.SLOT_NO_AMMO, self.WEAPON_LIST, self._player))

            ui.Button(label="一键最大", onclick=self.weapon_max)

        with Group("global", "全局", self, handler=self.handler):
            ModelInputWidget("game_hour", "当前小时")
            ModelInputWidget("game_minute", "当前分钟")
            ModelInputWidget("game_week", "当前星期")
            # self.money_view = InputWidget("money", "金钱", address.MONEY, (), int)

        with Group(None, "快捷键", 0, handler=self.handler, flexgrid=False, hasfootbar=False):
            with ui.Horizontal(className="fill container"):
                self.spawn_vehicle_id_view = ui.ListBox(className="expand", onselect=self.onSpawnVehicleIdChange,
                    choices=(item[0] for item in VEHICLE_LIST))
                with ui.ScrollView(className="fill container"):
                    self.render_common_text()

        with Group(None, "测试", 0, handler=self.handler, flexgrid=False, hasfootbar=False):
            with ui.GridLayout(cols=4, vgap=10, className="fill container"):
                self.render_common_button()
                ui.Button("缴械", onclick=self.remove_near_peds_weapon)
                ui.Button("附近的人着火", onclick=self.near_peds_make_fire)
                ui.Button("附近的人爆炸", onclick=self.near_peds_explode)
                ui.Button("敌人着火", onclick=self.enemys_make_fire)
                ui.Button("敌人爆头", onclick=self.enemys_explode_head)
                ui.Button("敌人爆炸", onclick=self.enemys_explode)
                ui.Button("爆炸就是艺术", onclick=self.explode_art)
                ui.Button("保存菜单", onclick=self.activate_save_menu)

        with Group(None, "工具", 0, flexgrid=False, hasfootbar=False):
            with ui.Vertical(className="fill container"):
                ui.Button("g3l坐标转json", onclick=self.g3l2json)

    def onClose(self, _=None):
        if self.handler.active:
            self.free_remote_function()
        return super().onClose()

    def checkAttach(self, _=None):
        className = 'grcWindow'
        windowName = getattr(self, 'WINDOW_NAME', 'GTAIV')

        if self.handler.active:
            self.free_remote_function()
        else:
            # 确保重新生成 native_context
            self._playerins = None

        if self.handler.attachByWindowName(className, windowName):
            self.attach_status_view.label = windowName + ' 正在运行'
            self.MODULE_BASE = self.handler.base - 0x400000

            if not self.win.hotkeys:
                self.win.RegisterHotKeys(
                    (
                        ('spawnVehicleIdPrev', MOD_ALT, getVK('['), self.onSpawnVehicleIdPrev),
                        ('spawnVehicleIdNext', MOD_ALT, getVK(']'), self.onSpawnVehicleIdNext),
                        ('spawn_choosed_vehicle', MOD_ALT, getVK('v'), self.spawn_choosed_vehicle),
                        ('spawn_choosed_vehicle_and_enter', MOD_ALT | MOD_SHIFT, getVK('v'), self.spawn_choosed_vehicle_and_enter),
                        ('max_cur_weapon', MOD_ALT, getVK('g'), self.max_cur_weapon),
                        ('teleport_to_waypoint', MOD_ALT | MOD_SHIFT, getVK('g'), self.teleport_to_waypoint),
                        ('teleport_to_destination', MOD_ALT, getVK('1'), self.teleport_to_destination),
                        ('dir_correct', MOD_ALT, getVK('e'), self.dir_correct),
                        ('speed_large', MOD_ALT | MOD_SHIFT, getVK('m'), partial(self.speed_up, rate=30)),
                        ('clear_wanted_level', MOD_ALT, getVK('0'), self.clear_wanted_level),
                        ('explode_nearest_vehicle', MOD_ALT, getVK('o'), self.explode_nearest_vehicle),
                        ('explode_art', MOD_ALT, getVK('`'), self.explode_art),
                    ) + self.get_common_hotkeys()
                )
            self.init_addr()
            self.init_remote_function()
        else:
            self.attach_status_view.label = '没有检测到 ' + windowName

    def get_addr(self, addr):
        return self.MODULE_BASE + addr

    def orig_addr(self, addr):
        return addr - self.MODULE_BASE

    def get_version(self):
        return self.handler.read32(self.get_addr(address.VERSION))

    def init_addr(self):
        version = self.get_version()
        version_depend = address.VERSION_DEPEND.get(version, None)
        if version_depend:
            for name in version_depend:
                addr = version_depend[name]
                setattr(address, name, self.get_addr(addr) if addr else 0)

        if address.SetMoveSpeed:
            SPEED_FUNC = (
                b'\x55\x8B\xEC\x83\xEC\x08\x8B\x4D\x08\xC7\x45\xF8',
                b'\x8B\x41\x60\x89\x45\xFC\x8D\x41\x64\x89\x45\x08\xFF\x75\x08\x8B\x4D\xFC\xFF\x55\xF8\x8B\xE5\x5D\xC3'
            )
            self.FUNCTION_SET_SPEED = utils.u32bytes(address.SetMoveSpeed).join(SPEED_FUNC)
            self.FUNCTION_GET_SPEED = utils.u32bytes(address.GetMoveSpeed).join(SPEED_FUNC)

        # if address.LoadWorldAtPosition:
        #     self.FUNC_LOAD_WORLD_AT_POSITION = (
        #         b'\x55\x8B\xEC\x51\x83\x45\x08\x60\xC7\x45\xFC' + utils.u32bytes(address.LoadWorldAtPosition) +
        #         b'\xFF\x75\x08\xB9' + utils.u32bytes(0x11DC444) + b'\xFF\x55\xFC\x83\xC4\x04\x8B\xE5\x5D\xC3'
        #     )

        self.FUNCTION_FIND_NATIVE_ADDRESS = (
            b'\x55\x8B\xEC\x83\xEC\x08\x56\xC7\x45\xF8' + utils.u32bytes(address.FindNativeAddress) +
            b'\xC7\x45\xFC\x00\x00\x00\x00\x56\x8B\x75\x08\xFF\x55\xF8\x5E\x89\x45\xFC\x8B\x45\xFC\x5E\x8B\xE5\x5D\xC3'
        )

        self.ScriptHookHelper = self.handler.get_module(r'Test.asi')
        if self.ScriptHookHelper:
            self.ScriptHookHelperCtxPtr = self.ScriptHookHelper + 0x141EC

        # 使用新的地址表
        address.NATIVE_ADDRS = {}

    def init_remote_function(self):
        self.FindNativeAddress = self.handler.write_function(self.FUNCTION_FIND_NATIVE_ADDRESS)

        # TODO
        if address.SetMoveSpeed:
            self.SetMoveSpeed = self.handler.write_function(self.FUNCTION_SET_SPEED)
            self.GetMoveSpeed = self.handler.write_function(self.FUNCTION_GET_SPEED)

        # 初始化Native调用的参数环境
        context_addr = self.handler.alloc_memory(NativeContext.SIZE)
        self.native_context = NativeContext(context_addr, self.handler)

    def free_remote_function(self):
        self.handler.free_memory(self.FindNativeAddress)
        if address.SetMoveSpeed:
            self.handler.free_memory(self.SetMoveSpeed)
            self.handler.free_memory(self.GetMoveSpeed)

        self.handler.free_memory(self.native_context.addr)
        self._playerins = None

    def get_native_addr(self, name):
        addr = address.NATIVE_ADDRS.get(name, 0)
        if addr is 0:
            # 获取原生函数地址
            addr = address.NATIVE_ADDRS[name] = self.handler.remote_call(self.FindNativeAddress, address.NATIVE_HASH[name])
        return addr

    def native_call(self, name, arg_sign, *args, ret_type=int, ret_size=4):
        """ 远程调用GTAIV中的方法
        :param name: 方法名称，见address.NATIVE_HASH
        :param arg_sign: 函数签名
        """
        with self.native_context:
            fn_addr = self.get_native_addr(name)
            if arg_sign:
                self.native_context.push(arg_sign, *args)
            self.handler.remote_call(fn_addr, self.native_context.addr)
            if ret_type:
                return self.native_context.get_result(ret_type, ret_size)

    def script_hook_call(self, name, arg_sign, *args, ret_type=int, ret_size=4, sync=True):
        if self.ScriptHookHelper:
            with self.native_context:
                fn_addr = self.get_native_addr(name)
                if arg_sign:
                    self.native_context.push(arg_sign, *args)
                self.native_context.push('L', fn_addr)
                self.handler.write32(self.ScriptHookHelperCtxPtr, self.native_context.addr)

                if sync:
                    try_count = 20
                    while try_count:
                        time.sleep(0.1)
                        if self.handler.read32(self.ScriptHookHelperCtxPtr) == 0:
                            if ret_type:
                                return self.native_context.get_result(ret_type, ret_size)
                            return

                        try_count -= 1

                    print('获取script_hook_call返回失败，超过尝试次数')

    def _player(self):
        # player_addr = self.handler.read32(self.handler.read32(self.address.PLAYER_INFO_ARRAY) + 0x58C)
        # if player_addr is 0:
        #     return None
        player = getattr(self, '_playerins', None)
        player_index = self.get_player_id()

        if not player:
            player = self._playerins = self.Player(player_index, self.get_ped_index(player_index), self)
        else:
            player.index = player_index
            player.handle = self.get_ped_index(player_index)
        return player

    def _vehicle(self):
        return self.player.vehicle
        # return self.Vehicle(self.handler.read32(self.address.VEHICLE_PTR), self.handler)

    player = property(_player)
    vehicle = property(_vehicle)

    def get_ped_addr(self):
        return self.handler.read32(self.handler.read32(self.address.PLAYER_INFO_ARRAY) + 0x58C)

    def get_player_id(self):
        # return self.native_call('GET_PLAYER_ID', None)
        return self.handler.read32(address.LOCAL_PLAYER_ID)

    def get_ped_index(self, player_index=0):
        # 方法一
        # player_id = (index or self.get_player_index_of_pool()) << 8
        # return player_id | self.handler.read8(
        #     self.handler.read32(self.handler.read32(address.PED_POOL) + 4) + (player_id >> 8)
        # )

        # 方法二
        self.native_call('GET_PLAYER_CHAR', 'LL', player_index or self.get_player_id(), self.native_context.get_temp_addr())
        return self.native_context.get_temp_value()

    def ped_index_to_handle(self, index):
        handle = index << 8
        return handle | self.handler.read8(
            self.handler.read32(self.handler.read32(address.PED_POOL) + 4) + index
        )

    def vehicle_index_to_handle(self, index):
        handle = index << 8
        return handle | self.handler.read8(
            self.handler.read32(self.handler.read32(address.VEHICLE_POOL) + 4) + index
        )

    def player_has_ped(self, player_index):
        return self.native_call('PLAYER_HAS_CHAR', 'L', player_index, ret_type=bool)

    @property
    def ped_pool(self):
        return models.Pool(self.address.PED_POOL, self.handler, models.MemPlayer)

    @property
    def vehicle_pool(self):
        return models.Pool(self.address.VEHICLE_POOL, self.handler, models.MemVehicle)

    def get_peds(self):
        pool = self.ped_pool
        for i in range(pool.size):
            ped = pool[i]
            if ped.hp > 1:
                ped.index = i
                yield ped

    def get_near_peds(self, distance=100):
        """获取附近的人"""
        for ped in super().get_near_peds(distance):
            yield Player(0, self.ped_index_to_handle(ped.index), self)

    def get_vehicles(self):
        pool = self.vehicle_pool
        for i in range(pool.size):
            vehicle = pool[i]
            if vehicle.engine_hp > 1:
                vehicle.index = i
                yield vehicle

    def get_near_vehicles(self, distance=100):
        """获取附近的载具"""
        for vehicle in super().get_near_vehicles(distance):
            yield Vehicle(self.vehicle_index_to_handle(vehicle.index), self)

    def get_nearest_ped(self, distance=50):
        self.native_call('GET_CLOSEST_CHAR', '4f3L', *self.entity.coord, distance, 1, 0, self.native_context.get_temp_addr())
        ped = self.native_context.get_temp_value()
        if ped:
            return Player(0, ped, self)

    def get_nearest_vehicle(self, distance=50):
        handle = self.native_call('GET_CLOSEST_CAR', '4f2L', *self.entity.coord, distance, 0, 70)
        if handle:
            vehicle = Vehicle(handle, self)
            if vehicle.existed:
                return vehicle

    def set_move_speed(self, entity_addr, value):
        ctx = self.native_context
        with ctx:
            ctx.push('L3f', entity_addr, *value)
            self.handler.remote_call(self.SetMoveSpeed, ctx.addr)

    def get_move_speed(self, entity_addr):
        ctx = self.native_context
        with ctx:
            ctx.push('L', entity_addr)
            self.handler.remote_call(self.GetMoveSpeed, ctx.addr)
            return (
                round(ctx.get_stack_value(1, float), 3),
                round(ctx.get_stack_value(2, float), 3),
                round(ctx.get_stack_value(3, float), 3)
            )

    def raise_up(self, _=None, speed=15):
        self.entity.speed[2] = speed

    def to_up(self, _=None):
        if self.isInVehicle:
            self.vehicle.coord[2] += 10
        else:
            self.player.coord[2] += 3

    def onSpawnVehicleIdChange(self, lb):
        self.spwan_vehicle_id = VEHICLE_LIST[lb.index][1]

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

    def set_ped_invincible(self, _=None, value=True):
        self.player.invincible = value

    def set_ped_block_switch_weapons(self, _=None):
        self.player.block_switch_weapons = False

    def set_ped_can_be_dragged_out_of_vehicle(self, _=None):
        self.player.can_be_dragged_out_of_vehicle = False

    def set_ped_keep_bike(self, _=None, value=True):
        self.player.keep_bike = value

    def restore_hp(self, _=None):
        super().restore_hp()
        if self.isInVehicle:
            vehicle = self.vehicle
            vehicle.engine_hp = 1000
            vehicle.fix()
            vehicle.wash()

    def max_cur_weapon(self, _=None):
        """当前武器子弹全满"""
        self.player.max_cur_ammo()

    def explode_nearest_vehicle(self, _=None):
        """爆破最近的车"""
        vehicle = self.get_nearest_vehicle()
        if vehicle:
            vehicle.explode()

    def remove_near_peds_weapon(self, _=None):
        """缴械"""
        for p in self.get_near_peds():
            p.remove_all_weapons()

    def near_peds_make_fire(self, _=None):
        """附近的人着火"""
        for p in self.get_near_peds():
            p.create_fire()

    def near_peds_explode(self, _=None):
        """附近的人爆炸"""
        for p in self.get_near_peds():
            p.explode()

    def enemys_make_fire(self, _=None):
        """敌人着火"""
        for p in self.get_near_peds():
            p.make_fire()

    def enemys_explode_head(self, _=None):
        """敌人爆头"""
        for p in self.get_near_peds():
            try:
                p.explode_head()
            except:
                pass

    def enemys_explode(self, _=None):
        """敌人爆炸"""
        for p in self.get_near_peds():
            p.create_explosion()

    def flash_weapon_icon(self):
        self.native_call('FLASH_WEAPON_ICON', 'L', 1, ret_type=None)

    # def LoadEnvironmentNow(self, pos):
    #     self.native_call('REQUEST_COLLISION_AT_POSN', '3f', *pos)
    #     self.native_call('LOAD_ALL_OBJECTS_NOW', None)
    #     self.native_call('POPULATE_NOW', None)
    #     self.script_hook_call('LOAD_SCENE', '3f', *pos)

    def GetGroundZ(self, pos):
        """获取指定位置地面的z值"""
        self.native_call('GET_GROUND_Z_FOR_3D_COORD', '3fL', *pos, self.native_context.get_temp_addr())
        return self.native_context.get_temp_value(type=float)

    def get_first_blip(self, blipType):
        blip_id = self.native_call('GET_FIRST_BLIP_INFO_ID', 'L', blipType)
        if blip_id:
            return models.Blip(blip_id, self)

    def get_next_blip(self, blipType):
        blip_id = self.native_call('GET_NEXT_BLIP_INFO_ID', 'L', blipType)
        if blip_id:
            return models.Blip(blip_id, self)

    def get_target_blips(self, color=0):
        for i in range(models.Blip.BLIP_DESTINATION, models.Blip.BLIP_DESTINATION_2 + 1):
            blip = self.get_first_blip(i)
            if blip:
                if color is 0 or blip.color == color:
                    yield blip

                while True:
                    blip = self.get_next_blip(models.Blip.BLIP_DESTINATION_1)
                    if blip:
                        if color is 0 or blip.color == color:
                            yield blip
                    else:
                        break

    def get_friends(self):
        """获取蓝色标记的peds"""
        return [blip.entity for blip in self.get_target_blips(models.Blip.BLIP_COLOR_FRIEND)]

    def get_enemys(self):
        """获取红色标记的peds"""
        return [blip.entity for blip in self.get_target_blips(models.Blip.BLIP_COLOR_ENEMY)]

    def teleport_to_waypoint(self, _=None):
        """瞬移到标记点"""
        if not self.teleport_to_blip(self.get_first_blip(models.Blip.BLIP_WAYPOINT)):
            print('无法获取标记坐标')

    def teleport_to_destination(self, _=None):
        """瞬移到目的地"""
        for i in range(models.Blip.BLIP_DESTINATION, models.Blip.BLIP_DESTINATION_2 + 1):
            if self.teleport_to_blip(self.get_first_blip(i)):
                break
        else:
            print('无法获取目的地坐标')

    def teleport_to_blip(self, blip):
        if blip:
            coord = list(blip.coord)
            print(coord)

            if coord[0] != 0 or coord[1] != 0:
                self.player.coord = coord
                if coord[2] == 0.0:
                    coord[2] = self.GetGroundZ(coord) or 16
                self.player.coord = coord
                return True

    def clear_wanted_level(self, _=None):
        self.player.wanted_level = 0

    def get_camera_rot_raw(self):
        ctx = self.native_context
        self.native_call('GET_ROOT_CAM', 'L', ctx.get_temp_addr())
        cam = ctx.get_temp_value()
        self.native_call('GET_CAM_ROT', 'L3L', cam, *ctx.get_temp_addrs(1, 3))
        return tuple(ctx.get_temp_values(1, 3, float, mapfn=utils.normalFloat))

    def get_camera_rot(self):
        data = self.get_camera_rot_raw()
        rotz = degreeToRadian(data[2]) + math.pi / 2
        return (math.cos(rotz), math.sin(rotz), degreeToRadian(data[0]))

    def get_camera_rotz(self):
        data = self.get_camera_rot_raw()
        return degreeToRadian(data[2])

    def dir_correct(self, _=None):
        rotz = self.get_camera_rotz()
        if rotz < 0:
            rotz += math.pi * 2
        entity = self.entity
        # entity.coord[2] += 2
        entity.rotation = rotz

    @property
    def game_hour(self):
        """当前小时"""
        return self.handler.read32(address.CClock__Hour)

    @game_hour.setter
    def game_hour(self, value):
        return self.handler.write32(address.CClock__Hour, int(value))

    @property
    def game_minute(self):
        """当前分钟"""
        return self.handler.read32(address.CClock__Minute)

    @game_minute.setter
    def game_minute(self, value):
        return self.handler.write32(address.CClock__Minute, int(value))

    @property
    def game_week(self):
        """当前星期"""
        return self.handler.read32(address.CClock__DayOfWeek)

    @game_week.setter
    def game_week(self, value):
        return self.handler.write32(address.CClock__DayOfWeek, int(value))

    def spawn_vehicle(self, model):
        """生成载具"""
        m = models.IVModel(model, self)
        m.request()
        self.script_hook_call('CREATE_CAR', 'L3fLL', model, *self.player.get_offset_coord((2, 0, 0)), self.native_context.get_temp_addr(), 1)
        return Vehicle(self.native_context.get_temp_value(), self)

    def spawn_choosed_vehicle(self, _=None):
        """生成选中的载具"""
        model = getattr(self, 'spwan_vehicle_id', None)
        if model:
            return self.spawn_vehicle(model)

    def spawn_choosed_vehicle_and_enter(self, _=None):
        """生成选中的载具并进入"""
        car = self.spawn_choosed_vehicle()
        if car:
            self.script_hook_call('TASK_WARP_CHAR_INTO_CAR_AS_DRIVER', '3L', self.player.handle, car.handle, 0, sync=False)

    def create_fire(self, coord, numGenerationsAllowed=0, strength=1):
        """生成火焰"""
        return self.native_call('START_SCRIPT_FIRE', '3f2L', *coord, numGenerationsAllowed, strength)

    def delete_fire(self, fire):
        """熄灭生成的火焰"""
        self.native_call('REMOVE_SCRIPT_FIRE', 'L', fire)

    def create_explosion(self, coord, uiExplosionType=models.NativeEntity.EXPLOSION_TYPE_ROCKET, fRadius=5, bSound=True, bInvisible=True, fCameraShake=0):
        """产生爆炸"""
        self.script_hook_call('ADD_EXPLOSION', '3fLfLLf', *coord, uiExplosionType, fRadius, bSound, bInvisible, fCameraShake)

    def explode_art(self, _=None, count=10):
        """爆炸就是艺术"""
        cam_x, cam_y, cam_z = self.get_camera_rot()
        offset = (cam_x * 5, cam_y * 5, cam_z * 5)
        coord = self.player.get_offset_coord_m(offset)

        # fires = []

        for i in range(count):
            coord[0] += offset[0]
            coord[1] += offset[1]
            coord[2] += offset[2]
            self.create_explosion(coord)
            # fires.append(self.create_fire(coord))

        # 5秒后移除火焰
        # time.sleep(5)
        # for fire in fires:
        #     self.delete_fire(fire)

    def activate_save_menu(self, _=None):
        self.native_call('ACTIVATE_SAVE_MENU', None)