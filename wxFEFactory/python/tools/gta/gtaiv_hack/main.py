from functools import partial
from lib import utils
from lib.hack.forms import Group, StaticGroup, Input, CoordWidget, ModelInput, ModelCoordWidget
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
from lib.win32.sendkey import auto, TextVK
from lib.config.widgets import IntConfig, BoolConfig, FloatConfig, SelectConfig, ConfigGroup
from styles import dialog_style, styles
from ..gta_base.main import BaseGTATool
from ..gta_base.widgets import WeaponWidget
from ..gta_base.utils import degreeToRadian
from . import address, models, coords
from .datasets import VEHICLE_LIST
from .models import Player, Vehicle
from .native import NativeContext
import math
import os
import json
import time
import __main__
import fefactory_api
ui = fefactory_api.ui


class Main(BaseGTATool):
    CLASS_NAME = 'grcWindow'
    WINDOW_NAME = 'GTAIV'
    address = address
    models = models
    Player = Player
    Vehicle = Vehicle
    NativeContext = NativeContext

    RAISE_UP_SPEED = 15
    SAFE_SPEED_RATE = 15
    SAFE_SPEED_UP = 6
    GO_FORWARD_COORD_RATE = 3
    FLY_SPEED = 15
    SLING_SPEED_RATE = 60
    SLING_COORD_UP = 3

    from .datasets import WEAPON_LIST, SLOT_NO_AMMO

    def render_main(self):
        player = self.weak._player
        vehicle = self.weak._vehicle
        with Group("player", "角色", player):
            ModelInput("hp", "生命")
            ModelInput("ap", "防弹衣")
            self.coord_view = ModelCoordWidget("coord", "坐标", savable=True, preset=coords)
            # ModelInput("gravity", "重量")
            ModelCoordWidget("speed", "速度")
            ModelInput("rotation", "旋转")
            ModelInput("wanted_level", "通缉等级")
            self.money = ModelInput("money", "金钱")
            ui.Text("")
            with ui.GridLayout(cols=4, vgap=10, className="expand"):
                ui.Button(label="车坐标->人坐标", onclick=self.from_vehicle_coord)
                ui.Button(label="从标记点读取坐标", onclick=self.player_coord_from_waypoint)
                ui.ToggleButton(label="切换无伤状态", onchange=self.set_ped_invincible)
                ui.ToggleButton(label="可以切换武器", onchange=self.set_ped_block_switch_weapons)
                ui.ToggleButton(label="不会被拽出车", onchange=self.set_ped_can_be_dragged_out_of_vehicle)
                ui.ToggleButton(label="摩托车老司机", onchange=self.set_ped_keep_bike)
                ui.ToggleButton(label="不被通缉", onchange=self.set_never_wanted)

        with Group("vehicle", "汽车", vehicle):
            ModelInput("hp", "HP")
            ModelCoordWidget("roll", "滚动")
            ModelCoordWidget("dir", "方向")
            self.vehicle_coord_view = ModelCoordWidget("coord", "坐标", savable=True, preset=coords)
            ModelCoordWidget("speed", "速度")
            ModelInput("weight", "重量")
            ui.Text("")
            with ui.Horizontal(className="expand"):
                ui.Button(label="人坐标->车坐标", onclick=self.from_player_coord)
                ui.Button(label="从标记点读取坐标", onclick=self.vehicle_coord_from_waypoint)
                ui.Button(label="锁车", onclick=self.vehicle_lock_door)
                ui.Button(label="开锁", onclick=partial(self.vehicle_lock_door, lock=False))

        with Group("weapon", "武器槽", None):
            self.weapon_views = []
            for i in range(1, len(self.WEAPON_LIST)):
                self.weapon_views.append(WeaponWidget(player, "weapon%d" % i, "武器槽%d" % i, i, self.SLOT_NO_AMMO, self.WEAPON_LIST))

            ui.Button(label="一键最大", onclick=self.weapon_max)

        with Group("global", "全局", self):
            ModelInput("game_hour", "当前小时")
            ModelInput("game_minute", "当前分钟")
            ui.Text("日期", className="input_label expand")
            with ui.Horizontal(className="expand"):
                ui.Button("回退一天", onclick=self.day_back)
                ui.Button("前进一天", onclick=self.day_forward)

        with StaticGroup("快捷键"):
            with ui.ScrollView(className="fill"):
                self.render_common_text()
                ui.Text("大加速: alt+shift+m")
                ui.Text("生成选中的载具并进入: alt+shift+v")
                ui.Text("当前武器子弹全满: alt+g")
                ui.Text("瞬移到标记点: alt+shift+g")
                ui.Text("瞬移到目的地: alt+1")
                ui.Text("根据摄像机朝向设置当前实体的朝向: alt+e")
                ui.Text("爆破最近的车: alt+o")

        with StaticGroup("载具模型"):
            with ui.Horizontal(className="fill"):
                self.vehicle_model_book = ui.Notebook(className="fill", wxstyle=0x0200)
                with self.vehicle_model_book:
                    for category in VEHICLE_LIST:
                        ui.Item(ui.ListBox(className="expand", choices=(item[0] for item in category[1])), caption=category[0])

        with StaticGroup("测试"):
            with ui.GridLayout(cols=4, vgap=10, className="expand"):
                self.render_common_button()
                ui.Button("附近的人缴械", onclick=self.near_peds_remove_weapon)
                ui.Button("附近的人着火", onclick=self.near_peds_make_fire)
                ui.Button("附近的人爆炸", onclick=self.near_peds_explode)
                ui.Button("敌人着火", onclick=self.enemys_make_fire)
                ui.Button("敌人爆头", onclick=self.enemys_explode_head)
                ui.Button("敌人爆炸", onclick=self.enemys_explode)
                ui.Button("敌人缴械", onclick=self.enemys_remove_weapon)
                ui.Button("敌人定住", onclick=self.enemys_freeze_position)
                ui.Button("警车爆炸", onclick=self.police_car_explode)
                ui.Button("警察和直升机爆炸", onclick=self.police_and_helicopter_explode)
                ui.Button("保存菜单", onclick=self.activate_save_menu)
                ui.Button("停止计时", onclick=self.freeze_timer)
                ui.Button("恢复计时", onclick=partial(self.freeze_timer, freeze=False))
                ui.Button("附近的人吹飞", onclick=self.near_peds_go_away)
                ui.Button("附近的车吹飞", onclick=self.near_vehicles_go_away)
                # ui.Button("驾驶到到目的地", onclick=self.drive_to_destination)
                # ui.Button("驾驶到到标记点", onclick=self.drive_to_waypoint)
                ui.Button("停止自动驾驶", onclick=self.clear_driver_tasks)
                ui.Button("修复衣服", onclick=self.repair_cloth)
                ui.Button("清空区域内的载具", onclick=self.clear_area_of_vehicles)
                ui.Button("清空区域内的角色", onclick=self.clear_area_of_peds)
                ui.Button("清空区域内的警察", onclick=self.clear_area_of_cops)
                ui.Button("清空区域内的火焰", onclick=self.clear_area_of_fire)
                self.set_buttons_contextmenu()

        with Group(None, "设置", None, hasfooter=False):
            with ConfigGroup(self.config):
                FloatConfig('auto_driving_speed', '自动驾驶速度', 10)
            ui.Hr()
            ui.Button("放弃本次配置修改", onclick=self.discard_config)

    def get_hotkeys(self):
        return (
            ('spawn_choosed_vehicle_and_enter', MOD_ALT | MOD_SHIFT, getVK('v'), self.spawn_choosed_vehicle_and_enter),
            ('max_cur_weapon', MOD_ALT, getVK('g'), self.max_cur_weapon),
            ('teleport_to_waypoint', MOD_ALT | MOD_SHIFT, getVK('g'), self.teleport_to_waypoint),
            ('dir_correct', MOD_ALT, getVK('e'), self.dir_correct),
            ('speed_large', MOD_ALT | MOD_SHIFT, getVK('m'), partial(self.speed_up, rate=30)),
            ('explode_nearest_vehicle', MOD_ALT, getVK('o'), self.explode_nearest_vehicle),
            ('enemys_harmless', MOD_ALT, getVK('s'), self.enemys_harmless),
        ) + self.get_common_hotkeys()

    def get_addr(self, addr):
        """原始地址转模块装载后的真实地址"""
        return self.MODULE_BASE + addr

    def orig_addr(self, addr):
        """模块装载后的真实地址转原始地址"""
        return addr - self.MODULE_BASE

    def get_version(self):
        """获取版本码"""
        return self.handler.read32(self.get_addr(address.VERSION))

    def init_addr(self):
        """初始化地址信息"""
        self.MODULE_BASE = self.handler.base - 0x400000
        version = self.get_version()
        version_depend = address.VERSION_DEPEND.get(version, None)
        if version_depend:
            # 装载针对当前版本的地址列表
            for name in version_depend:
                addr = version_depend[name]
                setattr(address, name, self.get_addr(addr) if addr else 0)

        # script hash获取native函数地址的机器码
        self.FUNCTION_FIND_NATIVE_ADDRESS = (
            b'\x55\x8B\xEC\x83\xEC\x08\x56\xC7\x45\xF8' + utils.u32bytes(address.FindNativeAddress) +
            b'\xC7\x45\xFC\x00\x00\x00\x00\x56\x8B\x75\x08\xFF\x55\xF8\x5E\x89\x45\xFC\x8B\x45\xFC\x5E\x8B\xE5\x5D\xC3'
        )

        # 检查是否加载了ScriptHook的帮助模块，因为部分script直接远程调用会crash
        # 要在ScriptHook的线程中才能安全运行
        self.script_hook_helper = self.handler.get_module('NativeHelper.asi')
        if self.script_hook_helper:
            self.script_call_addr = self.script_hook_helper + 0x10A0

        # 此次运行的Native Script地址缓存
        address.NATIVE_ADDRS = {}

    def onattach(self):
        """初始化远程函数"""
        self.init_addr()
        super().onattach()
        self.FindNativeAddress = self.handler.write_function(self.FUNCTION_FIND_NATIVE_ADDRESS)

    def ondetach(self):
        """释放远程函数"""
        super().ondetach()
        self.handler.free_memory(self.FindNativeAddress)

    def get_native_addr(self, name):
        """根据脚本名称获取装载后原生函数地址"""
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
        addr = self.get_native_addr(name) if isinstance(name, str) else name
        return super().native_call(addr, arg_sign, *args, ret_type=ret_type, ret_size=ret_size)

    def script_call(self, name, arg_sign, *args, ret_type=int, ret_size=4, sync=True):
        """通过ScriptHook的帮助模块远程调用脚本函数，通过计时器轮询的方式实现同步"""
        if self.script_hook_helper:
            with self.native_context:
                fn_addr = self.get_native_addr(name)
                super().native_call(self.script_call_addr, (arg_sign or '') + 'L', *args, fn_addr)
                if ret_type:
                    return self.native_context.get_result(ret_type, ret_size)
        else:
            print("script_hook_helper未初始化，是否忘记了添加NativeHelper.asi？")

    def _player(self):
        """获取当前角色"""
        # player_addr = self.handler.read32(self.handler.read32(self.address.PLAYER_INFO_ARRAY) + 0x58C)
        # if player_addr is 0:
        #     return None
        player = getattr(self, '_playerins', None)
        player_index = self.get_player_index()

        if not player:
            player = self._playerins = self.Player(player_index, self.get_ped_handle(player_index), self)
        else:
            player.index = player_index
            player.handle = self.get_ped_handle(player_index)
        return player

    def _vehicle(self):
        """获取当前角色的上次使用的载具"""
        return self.player.last_vehicle

    player = property(_player)
    vehicle = property(_vehicle)

    def get_ped_addr(self):
        """获取当前角色的Ped结构地址"""
        return self.handler.read32(self.handler.read32(self.address.PLAYER_INFO_ARRAY) + 0x58C)

    def get_player_index(self):
        """获取当前角色的序号"""
        # return self.native_call('GET_PLAYER_ID', None)
        return self.handler.read32(address.LOCAL_PLAYER_ID)

    def get_ped_handle(self, player_index=0):
        """获取当前角色的句柄"""
        self.native_call('GET_PLAYER_CHAR', 'LL', player_index or self.get_player_index(), self.native_context.get_temp_addr())
        return self.native_context.get_temp_value()

    def ped_index_to_handle(self, index):
        """角色序号转角色句柄"""
        handle = index << 8
        return handle | self.handler.read8(
            self.handler.read32(self.handler.read32(address.PED_POOL) + 4) + index
        )

    def vehicle_index_to_handle(self, index):
        """载具序号转载具句柄"""
        handle = index << 8
        return handle | self.handler.read8(
            self.handler.read32(self.handler.read32(address.VEHICLE_POOL) + 4) + index
        )

    def player_has_ped(self, player_index):
        """指定序号是否有对应的角色句柄"""
        return self.native_call('PLAYER_HAS_CHAR', 'L', player_index, ret_type=bool)

    @property
    def ped_pool(self):
        """角色池"""
        return models.Pool(self.address.PED_POOL, self, models.MemPlayer)

    @property
    def vehicle_pool(self):
        """载具池"""
        return models.Pool(self.address.VEHICLE_POOL, self, models.MemVehicle)

    @property
    def object_pool(self):
        """物体池"""
        return models.Pool(self.address.OBJECT_POOL, self, models.MemObject)

    def get_peds(self):
        """获取角色池中的角色列表"""
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
        """载具池中的载具列表"""
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
        """获取最近的人"""
        self.native_call('GET_CLOSEST_CHAR', '4f3L', *self.entity.coord, distance, 1, 0, self.native_context.get_temp_addr())
        ped = self.native_context.get_temp_value()
        if ped:
            return Player(0, ped, self)

    def get_nearest_vehicle(self, distance=50):
        """获取最近的载具"""
        handle = self.native_call('GET_CLOSEST_CAR', '4f2L', *self.entity.coord, distance, 0, 70)
        if handle:
            vehicle = Vehicle(handle, self)
            if vehicle.existed:
                return vehicle

    def set_move_speed(self, entity_addr, value):
        """设置实体的移动速度"""
        ctx = self.native_context
        ctx.push_manual(-3, '3f', *value)
        self.native_call_auto(address.SetMoveSpeed, 'L', ctx.get_temp_addr(3), this=entity_addr)

    def get_move_speed(self, entity_addr):
        """获取实体的移动速度"""
        ctx = self.native_context
        self.native_call_auto(address.GetMoveSpeed, 'L', ctx.get_temp_addr(3), this=entity_addr)
        return tuple(ctx.get_temp_values(3, 1, float, mapfn=utils.float32))

    def set_turn_speed(self, entity_addr, value):
        """设置实体的转向速度"""
        ctx = self.native_context
        ctx.push_manual(-3, '3f', *value)
        self.native_call_auto(address.SetTurnSpeed, 'L', ctx.get_temp_addr(3), this=entity_addr)

    def get_turn_speed(self, entity_addr):
        """获取实体的转向速度"""
        ctx = self.native_context
        self.native_call_auto(address.GetTurnSpeed, 'L', ctx.get_temp_addr(3), this=entity_addr)
        return tuple(ctx.get_temp_values(3, 1, float, mapfn=utils.float32))

    def to_up(self, _=None):
        """升高(无速度)"""
        if self.isInVehicle:
            self.vehicle.coord[2] += 10
        else:
            self.player.coord[2] += 3

    def weapon_max(self, _=None):
        """武器子弹数最大"""
        for v in self.weapon_views:
            v.id_view.index = 1
            if v.has_ammo:
                v.ammo_view.value = 9999

    def player_coord_from_waypoint(self, _=None):
        # 从标记点读取坐标
        blip = self.get_first_blip(models.Blip.BLIP_WAYPOINT)
        if blip:
            self.coord_view.input_value = blip.coord

    def vehicle_coord_from_waypoint(self, _=None):
        # 从标记点读取坐标
        blip = self.get_first_blip(models.Blip.BLIP_WAYPOINT)
        if blip:
            self.vehicle_coord_view.input_value = blip.coord

    def set_ped_invincible(self, tb):
        """当前角色无伤"""
        self.player.invincible = tb.checked

    def set_ped_block_switch_weapons(self, tb):
        """解除当前角色武器切换限制"""
        self.player.block_switch_weapons = not tb.checked

    def set_ped_can_be_dragged_out_of_vehicle(self, tb):
        """当前角色不会被拖出载具"""
        self.player.can_be_dragged_out_of_vehicle = not tb.checked

    def set_ped_keep_bike(self, tb):
        """当前角色不会从摩托车上甩出去"""
        self.player.keep_bike = tb.checked

    def vehicle_fix(self, vehicle):
        """修车"""
        vehicle.engine_hp = 1000
        vehicle.fix()
        vehicle.wash()

    def set_never_wanted(self, tb):
        """不被通缉"""
        self.native_call('SET_WANTED_MULTIPLIER', 'f', 0 if tb.checked else 1)

    def max_cur_weapon(self, _=None):
        """当前武器子弹全满"""
        self.player.max_cur_ammo()

    def explode_nearest_vehicle(self, _=None):
        """爆破最近的车"""
        vehicle = self.get_nearest_vehicle()
        if vehicle:
            vehicle.explode()

    def near_peds_remove_weapon(self, _=None):
        """附近的人缴械"""
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
        for p in self.get_enemys():
            p.make_fire()

    def enemys_explode_head(self, _=None):
        """敌人爆头"""
        for p in self.get_enemys():
            try:
                p.explode_head()
            except:
                pass

    def enemys_explode(self, _=None):
        """敌人爆炸"""
        for p in self.get_enemys():
            p.create_explosion()

    def enemys_remove_weapon(self, _=None):
        """敌人缴械"""
        for p in self.get_enemys():
            if isinstance(p, self.Player):
                p.remove_all_weapons()

    def enemys_freeze_position(self, _=None):
        """敌人定住"""
        for p in self.get_enemys():
            p.freeze_position()
            if isinstance(p, self.Player):
                vehicle = p.vehicle
                if vehicle:
                    vehicle.freeze_position()

    def enemys_harmless(self, _=None):
        """敌人缴械+定住"""
        self.enemys_remove_weapon()
        self.enemys_freeze_position()

    def police_car_explode(self, _=None):
        """警车爆炸"""
        for blip in self.get_police_car_blips():
            blip.entity.create_explosion()

    def police_and_helicopter_explode(self, _=None):
        """警察和直升机爆炸"""
        for blip in self.get_cop_blips():
            blip.entity.create_explosion()

    # def LoadEnvironmentNow(self, pos):
    #     self.native_call('REQUEST_COLLISION_AT_POSN', '3f', *pos)
    #     self.native_call('LOAD_ALL_OBJECTS_NOW', None)
    #     self.native_call('POPULATE_NOW', None)
    #     self.script_call('LOAD_SCENE', '3f', *pos)

    def GetGroundZ(self, pos):
        """获取指定位置地面的z值"""
        self.native_call('GET_GROUND_Z_FOR_3D_COORD', '3fL', *pos, self.native_context.get_temp_addr())
        return self.native_context.get_temp_value(type=float)

    def get_first_blip(self, sprite):
        """获取指定类型的第一个标记"""
        blip_id = self.native_call('GET_FIRST_BLIP_INFO_ID', 'L', sprite)
        if blip_id:
            return models.Blip(blip_id, self)

    def get_next_blip(self, sprite):
        """获取指定类型的下一个标记"""
        blip_id = self.native_call('GET_NEXT_BLIP_INFO_ID', 'L', sprite)
        if blip_id:
            return models.Blip(blip_id, self)

    def get_blips(self, sprites, color=None, types=None):
        """根据sprite获取所有标记"""
        check_blip = lambda blip: blip.blipType and (
            (color is None or blip.color is color) and
            (types is None or blipType in types) )

        if isinstance(sprites, int):
            sprites = (sprites,)

        for i in sprites:
            blip = self.get_first_blip(i)
            if blip:
                if check_blip(blip):
                    yield blip

                while True:
                    blip = self.get_next_blip(i)
                    if blip:
                        if check_blip(blip):
                            yield blip
                    else:
                        break

    def get_target_blips(self, color=None):
        """获取目标的所有标记"""
        return self.get_blips(range(models.Blip.BLIP_DESTINATION, models.Blip.BLIP_DESTINATION_2 + 1), color=color)

    def get_friends(self):
        """获取蓝色标记的peds"""
        return [blip.entity for blip in self.get_target_blips(models.Blip.BLIP_COLOR_FRIEND)]

    def get_enemy_blips(self):
        """获取红色标记"""
        return self.get_target_blips(models.Blip.BLIP_COLOR_ENEMY)

    def get_enemys(self):
        """获取红色标记的peds"""
        return [blip.entity for blip in self.get_enemy_blips()]

    def get_police_car_blips(self):
        """获取警车标记"""
        return self.get_blips(models.Blip.BLIP_COP_CAR)

    def get_police_helicopter_blips(self):
        """获取警用直升机标记"""
        return self.get_blips(models.Blip.BLIP_COP_CHOPPER)

    def get_cop_blips(self):
        """获取所有警察标记"""
        for blip in self.get_police_car_blips():
            yield blip
        for blip in self.get_police_helicopter_blips():
            yield blip
        for blip in self.get_target_blips():
            if blip.is_short_range:
                yield blip

    def teleport_to_blip(self, blip):
        """瞬移到指定标记"""
        if blip:
            coord = list(blip.coord)
            # print(coord)
            entity = self.entity
            if coord[0] != 0 or coord[1] != 0:
                entity.coord = coord
                if coord[2] < 3:
                    coord[2] = 1024
                    coord[2] = self.GetGroundZ(coord) or 16
                entity.coord = coord
                return True

    def teleport_to_waypoint(self, _=None):
        """瞬移到标记点"""
        if not self.teleport_to_blip(self.get_first_blip(models.Blip.BLIP_WAYPOINT)):
            entity = self.entity
            coord = entity.coord.values()
            coord[2] = 1024
            coord[2] = self.GetGroundZ(coord)
            entity.coord = coord

    def teleport_to_destination(self, _=None):
        """瞬移到目的地"""
        for blip in self.get_target_blips():
            if self.teleport_to_blip(blip):
                break
        else:
            print('无法获取目的地坐标')

    def drive_to_blip(self, blip):
        """驾驶到到目的地"""
        if blip and self.vehicle:
            self.vehicle.drive_to(blip.coord, self.config.auto_driving_speed)

    def drive_to_destination(self, _=None):
        """驾驶到到目的地"""
        for blip in self.get_target_blips():
            if self.drive_to_blip(blip):
                break
        else:
            print('无法获取目的地坐标')

    def drive_to_waypoint(self, _=None):
        """驾驶到到标记点"""
        self.drive_to_blip(self.get_first_blip(models.Blip.BLIP_WAYPOINT))

    def clear_driver_tasks(self, _=None):
        """停止自动驾驶"""
        if self.vehicle:
            self.vehicle.clear_driver_tasks()

    def get_camera_rot_raw(self):
        """获取摄像机原始参数"""
        ctx = self.native_context
        self.native_call('GET_ROOT_CAM', 'L', ctx.get_temp_addr())
        cam = ctx.get_temp_value()
        self.native_call('GET_CAM_ROT', 'L3L', cam, *ctx.get_temp_addrs(1, 3))
        return tuple(ctx.get_temp_values(1, 3, float, mapfn=utils.float32))

    def get_camera_rot(self):
        """ 获取摄像机朝向参数
        :return: (x分量, y分量, z方位角)
        """
        data = self.get_camera_rot_raw()
        yaw = degreeToRadian(data[2]) + math.pi / 2
        return (math.cos(yaw), math.sin(yaw), degreeToRadian(data[0]))

    def get_camera_yaw(self):
        """获取xy面上的旋转量"""
        data = self.get_camera_rot_raw()
        return degreeToRadian(data[2])

    def dir_correct(self, _=None):
        """根据摄像机朝向设置当前实体的朝向"""
        yaw = self.get_camera_yaw()
        if yaw < 0:
            yaw += math.pi * 2
        entity = self.entity
        # entity.coord[2] += 2
        entity.rotation = yaw

    @property
    def game_hour(self):
        """当前小时"""
        return self.native_call('GET_HOURS_OF_DAY', None)

    @game_hour.setter
    def game_hour(self, value):
        self.native_call('SET_TIME_OF_DAY', '2L', int(value), self.game_minute)

    @property
    def game_minute(self):
        """当前分钟"""
        return self.native_call('GET_MINUTES_OF_DAY', None)

    @game_minute.setter
    def game_minute(self, value):
        return self.native_call('SET_TIME_OF_DAY', '2L', self.game_hour, int(value))

    def day_back(self, _=None):
        """回退一天"""
        return self.native_call('SET_TIME_ONE_DAY_BACK', None)

    def day_forward(self, _=None):
        """前进一天"""
        return self.native_call('TIME_ONE_DAY_FORWARD', None)

    def get_selected_vehicle_list(self):
        """当前刷车器活动的载具模型列表"""
        return VEHICLE_LIST[self.vehicle_model_book.index][1]

    # 兼容继承自BaseGTATool的方法
    VEHICLE_LIST = property(get_selected_vehicle_list)

    @property
    def spawn_vehicle_id_view(self):
        return self.vehicle_model_book.getPage()

    def get_selected_vehicle_model(self):
        """获取刷车器选中的载具模型"""
        page_index = self.vehicle_model_book.index
        item_index = self.vehicle_model_book.getPage(page_index).index
        if item_index is not -1:
            return VEHICLE_LIST[page_index][1][item_index][1]

    def spawn_vehicle(self, model_id, coord=None):
        """生成载具"""
        m = models.IVModel(model_id, self)
        if m.is_in_cdimage and m.is_vehicle:
            m.request()
            if m.loaded:
                self.script_call('CREATE_CAR', 'L3fLL', model_id, *(coord or self.get_front_coord()), self.native_context.get_temp_addr(), 1)
                return Vehicle(self.native_context.get_temp_value(), self)
            else:
                print("模型未加载", hex(model))
        else:
            print('该模型不支持或不是载具模型')

    def spawn_choosed_vehicle_and_enter(self, _=None):
        """生成选中的载具并进入"""
        car = self.spawn_choosed_vehicle()
        if car:
            self.script_call('TASK_WARP_CHAR_INTO_CAR_AS_DRIVER', '3L', self.player.handle, car.handle, 0, sync=False)

    def create_fire(self, coord, numGenerationsAllowed=0, strength=1):
        """生成火焰"""
        return self.native_call('START_SCRIPT_FIRE', '3f2L', *coord, numGenerationsAllowed, strength)

    def delete_fire(self, fire):
        """熄灭生成的火焰"""
        self.native_call('REMOVE_SCRIPT_FIRE', 'L', fire)

    def create_explosion(self, coord, uiExplosionType=models.NativeEntity.EXPLOSION_TYPE_ROCKET, fRadius=5, bSound=True, bInvisible=False, fCameraShake=0):
        """产生爆炸"""
        self.script_call('ADD_EXPLOSION', '3fLfLLf', *coord, uiExplosionType, fRadius, bSound, bInvisible, fCameraShake)

    def create_throwable_object(self, modelHash):
        self.script_call('CREATE_OBJECT', 'L3f2L', modelHash, *self.get_front_coord(), self.native_context.get_temp_addr(), 1)
        obj = models.Object(self.native_context.get_temp_value(), self)
        obj.invincible = False
        obj.dynamic = True
        obj.stealable = True
        obj.collision = True
        return obj

    def activate_save_menu(self, _=None):
        """激活保存菜单"""
        self.native_call('ACTIVATE_SAVE_MENU', None)

    def near_peds_to_front(self, _=None):
        super().near_peds_to_front(zinc=6)

    def near_vehicles_to_front(self, _=None):
        super().near_vehicles_to_front(zinc=5)

    def recal_markers(self, _=None):
        self._markers = tuple(self.get_target_blips(models.Blip.BLIP_COLOR_ENEMY))
        self._marker_index = 0

    def move_marker_to_front(self, _=None):
        super().move_marker_to_front(5)

    def freeze_timer(self, _=None, freeze=True):
        """停止计时"""
        self.script_call('FREEZE_ONSCREEN_TIMER', 'L', freeze)

    def near_peds_go_away(self, _=None):
        """附近的人吹飞"""
        self.launch_entity(self.get_near_peds(), False)

    def near_vehicles_go_away(self, _=None):
        """附近的车吹飞"""
        self.launch_entity(self.get_near_vehicles(), False)

    def repair_cloth(self, _=None):
        """修复衣服"""
        self.player.reset_visible_damage()

    def clear_area_of_vehicles(self, _=None):
        """清空区域内的载具"""
        self.script_call('CLEAR_AREA_OF_CARS', '4f?', *self.player.coord, 1000, False)

    def clear_area_of_peds(self, _=None):
        """清空区域内的角色"""
        self.script_call('CLEAR_AREA_OF_CHARS', '4f', *self.player.coord, 200)

    def clear_area_of_cops(self, _=None):
        """清空区域内的警察"""
        self.script_call('CLEAR_AREA_OF_COPS', '4f', *self.player.coord, 1000)

    def clear_area_of_cops(self, _=None):
        """清空区域内的警察"""
        self.script_call('CLEAR_AREA_OF_OBJECTS', '4f', *self.player.coord, 1000)

    def clear_area_of_fire(self, _=None):
        """清空区域内的火焰"""
        self.script_call('EXTINGUISH_FIRE_AT_POINT', '4f', *self.player.coord, 100)