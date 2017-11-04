from functools import partial
from lib.hack.form import Group, InputWidget, CheckBoxWidget, CoordWidget, ModelInputWidget, ModelCoordWidget
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
from lib.win32.sendkey import auto, TextVK
from lib import utils
from commonstyle import dialog_style, styles
from ..gta_base.main import BaseGTATool
from ..gta_base.utils import degreeToRadian, Vector3
from . import address, models
from .data import VEHICLE_LIST, WEAPON_HASH, PLAYER_MODEL
from .models import Player, Vehicle
from .native import NativeContext
from .widgets import WeaponWidget
import math
import os
import json
import time
import __main__
import fefactory_api
ui = fefactory_api.ui


class Tool(BaseGTATool):
    CLASS_NAME = 'grcWindow'
    WINDOW_NAME = 'Grand Theft Auto V'
    address = address
    models = models
    Player = Player
    Vehicle = Vehicle
    NativeContext = NativeContext

    RAISE_UP_SPEED = 12
    SAFE_SPEED_RATE = 30
    SAFE_SPEED_UP = 6
    GO_FORWARD_COORD_RATE = 3
    FLY_SPEED = 15
    SLING_COORD_UP = 3
    SLING_SPEED_RATE = 60
    VEHICLE_LIST = VEHICLE_LIST

    from .data import WEAPON_LIST
    
    # use x64 native_call
    FUNCTION_NATIVE_CALL = BaseGTATool.FUNCTION_NATIVE_CALL_64

    def render_main(self):
        with Group("player", "角色", self._player, handler=self.handler):
            self.hp_view = ModelInputWidget("hp", "生命")
            self.ap_view = ModelInputWidget("ap", "防弹衣")
            self.coord_view = ModelCoordWidget("coord", "坐标", savable=True)
            # self.weight_view = ModelInputWidget("gravity", "重量")
            self.speed_view = ModelCoordWidget("speed", "速度")
            self.rot_view = ModelInputWidget("rotation", "旋转")
            self.wanted_level_view = ModelInputWidget("wanted_level", "通缉等级")
            self.money = ModelInputWidget("money", "金钱")
            ui.Hr()
            with ui.GridLayout(cols=4, vgap=10, className="expand"):
                ui.Button(label="车坐标->人坐标", onclick=self.from_vehicle_coord)
                ui.Button(label="开启无伤", onclick=self.set_ped_invincible)
                ui.Button(label="关闭无伤", onclick=partial(self.set_ped_invincible, value=False))
                ui.Button(label="可以切换武器", onclick=self.set_ped_block_switch_weapons)
                ui.Button(label="不会被拽出车", onclick=self.set_ped_can_be_dragged_out_of_vehicle)
                ui.Button(label="摩托车老司机", onclick=self.set_ped_keep_bike)
                ui.Button(label="切换无限弹药", onclick=self.set_ped_infinite_ammo_clip)
                ui.Button(label="切换不被警察注意", onclick=self.set_ped_ignored_by_police)

        with Group("vehicle", "汽车", self._vehicle, handler=self.handler):
            self.vehicle_hp_view = ModelInputWidget("hp", "HP")
            self.vehicle_roll_view = ModelCoordWidget("roll", "滚动")
            self.vehicle_dir_view = ModelCoordWidget("dir", "方向")
            self.vehicle_coord_view = ModelCoordWidget("coord", "坐标", savable=True)
            self.vehicle_speed_view = ModelCoordWidget("speed", "速度")
            self.weight_view = ModelInputWidget("weight", "重量")
            ui.Hr()
            with ui.GridLayout(cols=4, vgap=10, className="expand"):
                ui.Button(label="人坐标->车坐标", onclick=self.from_player_coord)
                ui.Button(label="开启无伤", onclick=self.set_vechile_invincible)
                ui.Button(label="关闭无伤", onclick=partial(self.set_vechile_invincible, value=False))
                ui.Button(label="锁车", onclick=self.vehicle_lock_door)
                ui.Button(label="开锁", onclick=partial(self.vehicle_lock_door, lock=False))

        with Group("weapon", "武器槽", None, handler=self.handler):
            self.weapon_views = []
            for item in self.WEAPON_LIST:
                if isinstance(item, str):
                    ui.Hr()
                    ui.Text(item)
                else:
                    self.weapon_views.append(WeaponWidget(self._player, *item))

            ui.Button(label="全部武器", onclick=self.give_all_weapon)
            ui.Button(label="一键最大", onclick=self.weapon_max)

        with Group("global", "全局", self, handler=self.handler):
            ModelInputWidget("game_hour", "当前小时")
            ModelInputWidget("game_minute", "当前分钟")
            ModelInputWidget("game_seconds", "当前秒数")
            ModelInputWidget("game_day", "当前日期")
            ModelInputWidget("game_month", "当前月份")
            ModelInputWidget("game_year", "当前年份")
            # self.money_view = InputWidget("money", "金钱", address.MONEY, (), int)

        with Group(None, "快捷键", 0, handler=self.handler, flexgrid=False, hasfootbar=False):
            with ui.Horizontal(className="fill container"):
                self.spawn_vehicle_id_view = ui.ListBox(className="expand", onselect=self.on_spawn_vehicle_id_change,
                    choices=(item[0] for item in VEHICLE_LIST))
                with ui.ScrollView(className="fill container"):
                    self.render_common_text()
                    ui.Text("大加速: alt+shift+m")
                    ui.Text("生成选中的载具并进入: alt+shift+v")
                    ui.Text("当前武器子弹全满: alt+g")
                    ui.Text("瞬移到标记点: alt+shift+g")
                    ui.Text("瞬移到目的地: alt+1")
                    ui.Text("根据摄像机朝向设置当前实体的朝向: alt+e")
                    ui.Text("爆破最近的车: alt+o")

        with Group(None, "角色模型", 0, handler=self.handler, flexgrid=False, hasfootbar=False):
            with ui.Horizontal(className="fill container"):
                self.player_model_view = ui.ListBox(className="expand",
                    choices=(item[0] for item in PLAYER_MODEL))
                with ui.ScrollView(className="fill container"):
                    ui.Text("1. 切换模型会失去武器")
                    ui.Text("2. 切换动物模型容易引发bug，请慎用")
                    ui.Text("3. 在陆地上切换鱼类模型会突然失去梦想，请注意")
                    ui.Button("切换模型", onclick=self.set_player_model)
                    ui.Button("生产人物", onclick=self.create_selected_ped)

        with Group(None, "测试", 0, handler=self.handler, flexgrid=False, hasfootbar=False):
            with ui.GridLayout(cols=4, vgap=10, className="fill container"):
                self.render_common_button()
                ui.Button("缴械", onclick=self.near_peds_remove_weapon)
                ui.Button("附近的人着火", onclick=self.near_peds_make_fire)
                ui.Button("附近的人爆炸", onclick=self.near_peds_explode)
                ui.Button("敌人着火", onclick=self.enemys_make_fire)
                ui.Button("敌人爆头", onclick=self.enemys_explode_head)
                ui.Button("敌人爆炸", onclick=self.enemys_explode)
                ui.Button("敌人缴械", onclick=self.enemys_remove_weapon)
                ui.Button("敌人定住", onclick=self.enemys_freeze_position)
                ui.Button("保存菜单", onclick=self.activate_save_menu)
                ui.Button("导弹攻击敌人", onclick=self.rocket_attack_enemy)
                ui.Button("导弹攻击所有标记", onclick=self.rocket_attack_target)
                # ui.Button("停止计时", onclick=self.freeze_timer)
                # ui.Button("恢复计时", onclick=partial(self.freeze_timer, freeze=False))

    def get_hotkeys(self):
        return (
            ('spawn_choosed_vehicle_and_enter', MOD_ALT | MOD_SHIFT, getVK('v'), self.spawn_choosed_vehicle_and_enter),
            ('max_cur_weapon', MOD_ALT, getVK('g'), self.max_cur_weapon),
            ('teleport_to_waypoint', MOD_ALT | MOD_SHIFT, getVK('g'), self.teleport_to_waypoint),
            ('dir_correct', MOD_ALT, getVK('e'), self.dir_correct),
            ('speed_large', MOD_ALT | MOD_SHIFT, getVK('m'), partial(self.speed_up, rate=30)),
            ('explode_nearest_vehicle', MOD_ALT, getVK('o'), self.explode_nearest_vehicle),
            ('shoot_vehicle_rocket', MOD_ALT, getVK('r'), self.shoot_vehicle_rocket),
            ('shoot_vehicle_rocket_more', MOD_ALT | MOD_SHIFT, getVK('r'), partial(self.shoot_vehicle_rocket, count=3)),
            ('rocket_attack_enemy', MOD_ALT, getVK("enter"), self.rocket_attack_enemy),
            ('special_ability_fill_meter', MOD_ALT, getVK("capslock"), self.special_ability_fill_meter),
        ) + self.get_common_hotkeys()

    def get_addr(self, addr):
        """原始地址转模块装载后的真实地址"""
        return self.MODULE_BASE + addr

    def orig_addr(self, addr):
        """模块装载后的真实地址转原始地址"""
        return addr - self.MODULE_BASE

    def get_offset_addr(self, addr):
        return addr + self.handler.read32(addr + 3) + 7

    def get_version(self):
        """获取版本码"""
        return self.handler.get_module_version()[1] >> 16

    def init_addr(self):
        """初始化地址信息"""
        self.MODULE_BASE = self.handler.base - 0x140000000

        version = self.get_version()
        version_depend = address.VERSION_DEPEND.get(version, None)
        if version_depend:
            # 装载针对当前版本的地址列表
            for name in version_depend:
                addr = version_depend[name]
                setattr(address, name, self.get_addr(addr) if addr else 0)
        
        address.REGISTRATION_TABLE = self.get_offset_addr(address.REGISTRATION_TABLE_BASE + 6)
        address.BLIP_LIST = self.get_offset_addr(address.BLIP_LIST_BASE)

        # 装载针对当前版本的native_hash
        name = 'hash_%d' % version
        module = getattr(__import__(__package__ + '.native_hash', fromlist=[name]), name)
        address.NATIVE_HASH = module.NATIVE_HASH

        # 检查是否加载了ScriptHook的帮助模块，因为部分script直接远程调用会crash
        # 要在ScriptHook的线程中才能安全运行
        self.ScriptHookHelper = self.handler.get_module(r'NativeHelper.asi')
        if self.ScriptHookHelper:
            self.ScriptHookHelperCtxPtr = self.ScriptHookHelper + 0x15A90

        # 此次运行的Native Script地址缓存
        address.NATIVE_ADDRS = {}
        
    def init_remote_function(self):
        """初始化远程函数"""
        self.init_addr()
        super().init_remote_function()
        self.near_entity_buff = self.handler.alloc_memory(8*40)

    def free_remote_function(self):
        """释放远程函数"""
        super().free_remote_function()
        self.handler.free_memory(self.near_entity_buff)    

    def get_native_addr(self, name):
        """根据脚本名称获取装载后原生函数地址"""
        addr = address.NATIVE_ADDRS.get(name, 0)
        if addr is 0:
            # 获取原生函数地址
            hash = address.NATIVE_HASH[name]
            registration = models.NativeRegistration(self.handler.read64(address.REGISTRATION_TABLE + (hash & 0xff) * 8), self.handler)
            addr = registration.get_func(hash)
            if addr:
                address.NATIVE_ADDRS[name] = addr
        return addr

    def native_call(self, name, arg_sign, *args, ret_type=int, ret_size=8):
        """ 远程调用GTAIV中的方法
        :param name: 方法名称，见address.NATIVE_HASH
        :param arg_sign: 函数签名
        """
        addr = self.get_native_addr(name) if isinstance(name, str) else name
        return super().native_call(addr, arg_sign, *args, ret_type=ret_type, ret_size=ret_size)

    def native_call_vector(self, *args, **kwargs):
        self.native_call(*args, **kwargs)
        return self.native_context.get_vector_result(8)

    def script_call(self, name, arg_sign, *args, ret_type=int, ret_size=8, sync=True):
        """通过ScriptHook的帮助模块远程调用脚本函数，通过计时器轮询的方式实现同步"""
        if self.ScriptHookHelper:
            with self.native_context:
                fn_addr = self.get_native_addr(name)
                if arg_sign:
                    self.native_context.push(arg_sign, *args)
                self.native_context.push('Q', fn_addr)
                self.handler.write64(self.ScriptHookHelperCtxPtr, self.native_context.addr)

                if sync:
                    # 在两秒内尝试同步
                    try_count = 20
                    while try_count:
                        time.sleep(0.1)
                        if self.handler.read64(self.ScriptHookHelperCtxPtr) == 0:
                            if ret_type:
                                return self.native_context.get_result(ret_type, ret_size)
                            return

                        try_count -= 1

                    print('获取script_call返回失败，超过尝试次数')

    def get_hash_key(self, name):
        return self.native_call('GET_HASH_KEY', 's', name)

    def _player(self):
        """获取当前角色"""
        player = getattr(self, '_playerins', None)
        player_index = self.get_player_index()

        if not player:
            player = self._playerins = self.Player(player_index, self.get_ped_id(), self)
        else:
            player.index = player_index
            player.handle = self.get_ped_id()
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
        return self.native_call('GET_PLAYER_INDEX', None)

    def get_ped_handle(self, player_index=0):
        """获取当前角色的句柄"""
        return self.native_call('GET_PLAYER_PED', 'Q', player_index or self.get_player_index())

    def get_ped_id(self, player_index=0):
        """获取当前角色的句柄"""
        return self.native_call('PLAYER_PED_ID', None)

    # def ped_index_to_handle(self, index):
    #     """角色序号转角色句柄"""
    #     handle = index << 8
    #     return handle | self.handler.read8(
    #         self.handler.read32(self.handler.read32(address.PED_POOL) + 4) + index
    #     )

    # def vehicle_index_to_handle(self, index):
    #     """载具序号转载具句柄"""
    #     handle = index << 8
    #     return handle | self.handler.read8(
    #         self.handler.read32(self.handler.read32(address.VEHICLE_POOL) + 4) + index
    #     )

    @property
    def ped_pool(self):
        """角色池"""
        # return models.Pool(self.address.PED_POOL, self.handler, models.MemPlayer)
        pass

    @property
    def vehicle_pool(self):
        """载具池"""
        # return models.Pool(self.address.VEHICLE_POOL, self.handler, models.MemVehicle)
        pass

    def get_peds(self, count=20):
        """获取角色池中的角色列表"""
        addr = self.near_entity_buff
        self.handler.write64(addr, count)
        real_count = self.script_call('GET_PED_NEARBY_PEDS', '2Ql', self.get_ped_id(), addr, -1)
        tmp_ped = Player(0, 0, self)
        my_handle = self.get_ped_id()
        for i in range(real_count):
            addr += 8
            tmp_ped.handle = self.handler.read64(addr)
            if tmp_ped.handle == my_handle:
                continue
            if tmp_ped.existed:
                yield Player(0, tmp_ped.handle, self)

    def get_near_peds(self, distance=100):
        """获取附近的人"""
        return self.get_peds(10)

    def get_vehicles(self, count=20):
        """载具池中的载具列表"""
        addr = self.near_entity_buff
        self.handler.write64(addr, count)
        real_count = self.script_call('GET_PED_NEARBY_VEHICLES', '2Q', self.get_ped_id(), addr)
        tmp_vehicle = Vehicle(0, self)
        my_handle = self.player.get_vehicle_handle()
        for i in range(real_count):
            addr += 8
            tmp_vehicle.handle = self.handler.read64(addr)
            if tmp_vehicle.handle == my_handle:
                continue
            if tmp_vehicle.handle and tmp_vehicle:
                yield Vehicle(tmp_vehicle.handle, self)

    def get_near_vehicles(self, distance=100):
        """获取附近的载具"""
        return self.get_vehicles()

    def get_nearest_ped(self, distance=50):
        """获取最近的人"""
        self.native_call('GET_CLOSEST_PED', '4f3Q', *self.entity.coord, distance, 1, 0, self.native_context.get_temp_addr())
        ped = self.native_context.get_temp_value()
        if ped:
            return Player(0, ped, self)

    def get_nearest_vehicle(self, distance=50):
        """获取最近的载具"""
        handle = self.native_call('GET_CLOSEST_VEHICLE', '4f2Q', *self.entity.coord, distance, 0, 70)
        if handle:
            vehicle = Vehicle(handle, self)
            if vehicle.existed:
                return vehicle

    def to_up(self, _=None):
        """升高(无速度)"""
        if self.isInVehicle:
            self.vehicle.coord[2] += 10
        else:
            self.player.coord[2] += 3

    def give_all_weapon(self, _=None):
        """获取全部武器并补充弹药"""
        for v in self.weapon_views:
            v.max_ammo()

    def weapon_max(self, _=None):
        """武器子弹数最大"""
        for v in self.weapon_views:
            if self.player.has_weapon(v.weapon):
                v.max_ammo()

    def set_ped_invincible(self, _=None, value=True):
        """当前角色无伤"""
        self.player.invincible = value

    def set_vechile_invincible(self, _=None, value=True):
        """当前载具无伤"""
        self.vehicle.set_invincible(value)

    def set_ped_block_switch_weapons(self, _=None):
        """解除当前角色武器切换限制"""
        self.player.block_switch_weapons = False

    def set_ped_can_be_dragged_out_of_vehicle(self, _=None):
        """当前角色不会被拖出载具"""
        self.player.can_be_dragged_out_of_vehicle = False

    def set_ped_keep_bike(self, _=None, value=True):
        """当前角色不会从摩托车上甩出去"""
        self.player.keep_bike = value

    def vehicle_fix(self, vehicle):
        """修车"""
        vehicle.engine_hp = 2000
        vehicle.fix()

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
        for blip in self.get_enemy_blips():
            self.create_fire(blip.coord)

    def enemys_explode_head(self, _=None):
        """敌人爆头"""
        for p in self.get_enemys():
            try:
                p.explode_head()
            except:
                pass

    def enemys_explode(self, _=None):
        """敌人爆炸"""
        for blip in self.get_enemy_blips():
            self.create_explosion(blip.coord)

    def enemys_remove_weapon(self, _=None):
        """敌人缴械"""
        for p in self.get_enemys():
            p.remove_all_weapons()

    def enemys_freeze_position(self, _=None):
        """敌人定住"""
        for p in self.get_enemys():
            p.freeze_position()

    def GetGroundZ(self, pos):
        """获取指定位置地面的z值"""
        self.native_call('GET_GROUND_Z_FOR_3D_COORD', '3f2Q', *pos, self.native_context.get_temp_addr(), 1)
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
        """获取目标的所有标记"""
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

    def get_enemy_blips(self):
        return self.get_target_blips(models.Blip.BLIP_COLOR_ENEMY)

    def get_friends(self):
        """获取蓝色标记的peds"""
        return [blip.entity for blip in self.get_target_blips(models.Blip.BLIP_COLOR_FRIEND)]

    def get_enemys(self):
        """获取红色标记的peds"""
        return [blip.entity for blip in self.get_enemy_blips() if blip.handle]

    def get_police_blips(self):
        """获取警察标记"""
        return self.get_blips(models.Blip.BLIP_COP)

    def get_police_helicopter_blips(self):
        """获取警察直升机标记"""
        return self.get_blips(models.Blip.BLIP_COPHELICOPTER)

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
        """瞬移到指定标记"""
        if blip:
            coord = list(blip.coord)
            if coord[0] != 0 or coord[1] != 0:
                if coord[2] < 3:
                    coord[2] = 40
                    coord[2] = self.GetGroundZ(coord) or 36
                self.entity.coord = coord
                return True

    def get_camera_rot(self):
        """ 获取摄像机朝向参数
        :return: (x分量, y分量, z方位角)
        """
        data = self.native_call_vector('GET_GAMEPLAY_CAM_ROT', 'Q', 2)
        tX = data[0] * 0.0174532924
        tZ = data[2] * 0.0174532924
        absX = abs(math.cos(tX))
        return (
            -math.sin(tZ) * absX,
            math.cos(tZ) * absX,
            math.sin(tX)
        )

    def get_camera_pos(self):
        """获取摄像机位置"""
        return self.native_call_vector('GET_GAMEPLAY_CAM_COORD', None)

    def get_camera_rotz(self):
        """获取xy面上的旋转量"""
        x, y, z = self.get_camera_rot()
        return math.atan2(-x, y)

    def dir_correct(self, _=None):
        """根据摄像机朝向设置当前实体的朝向"""
        rotz = self.get_camera_rotz()
        if rotz < 0:
            rotz += math.pi * 2
        entity = self.entity
        # entity.coord[2] += 2
        entity.rotation = rotz

    @property
    def game_hour(self):
        """当前小时"""
        return self.native_call('GET_CLOCK_HOURS', None)

    @game_hour.setter
    def game_hour(self, value):
        self.native_call('SET_CLOCK_TIME', '3L', int(value), self.game_minute, self.game_seconds)

    @property
    def game_minute(self):
        """当前分钟"""
        return self.native_call('GET_CLOCK_MINUTES', None)

    @game_minute.setter
    def game_minute(self, value):
        self.native_call('SET_CLOCK_TIME', '3L', self.game_hour, int(value), self.game_seconds)

    @property
    def game_seconds(self):
        """当前秒"""
        return self.native_call('GET_CLOCK_SECONDS', None)

    @game_seconds.setter
    def game_seconds(self, value):
        self.native_call('SET_CLOCK_TIME', self.game_hour, self.game_minute, int(value))

    @property
    def game_day(self):
        """当前日期"""
        return self.native_call('GET_CLOCK_DAY_OF_MONTH', None)

    @game_day.setter
    def game_day(self, value):
        self.native_call('SET_CLOCK_DATE', '3L', int(value), self.game_month, self.game_year)

    @property
    def game_month(self):
        """当前月份"""
        return self.native_call('GET_CLOCK_MONTH', None)

    @game_month.setter
    def game_month(self, value):
        self.native_call('SET_CLOCK_DATE', '3L', self.game_day, int(value), self.game_year)

    @property
    def game_year(self):
        """当前年"""
        return self.native_call('GET_CLOCK_YEAR', None)

    @game_year.setter
    def game_year(self, value):
        self.native_call('SET_CLOCK_DATE', self.game_day, self.game_month, int(value))

    @property
    def game_week(self):
        """当前星期几"""
        return self.native_call('GET_CLOCK_DAY_OF_WEEK', None)

    def spawn_vehicle(self, model):
        """生成载具"""
        m = models.VModel(model, self)
        m.request()
        handle = self.script_call('CREATE_VEHICLE', 'Q4f2Q', model, *self.get_front_coord(), self.player.heading, 0, 1)
        return Vehicle(handle, self)

    def create_ped(self, model, pedType=21):
        """生成载具"""
        m = models.VModel(model, self)
        m.request()
        handle = self.script_call('CREATE_PED', '2Q4f2Q', pedType, model, *self.get_front_coord(), self.player.heading, 0, 1)
        return Player(0, handle, self)

    def spawn_choosed_vehicle_and_enter(self, _=None):
        """生成选中的载具并进入"""
        car = self.spawn_choosed_vehicle()
        if car:
            self.script_call('TASK_WARP_PED_INTO_VEHICLE', '3Q', self.player.handle, car.handle, 0, sync=False)

    def create_fire(self, coord, maxChildren=10, isGasFire=1):
        """生成火焰"""
        return self.script_call('START_SCRIPT_FIRE', '3f2Q', *coord, maxChildren, isGasFire)

    def delete_fire(self, fire):
        """熄灭生成的火焰"""
        self.native_call('REMOVE_SCRIPT_FIRE', 'Q', fire)

    def create_explosion(self, coord, explosionType=models.NativeEntity.EXPLOSION_TYPE_ROCKET, fRadius=12, bSound=True, bInvisible=False, fCameraShake=0):
        """产生爆炸"""
        self.script_call('ADD_EXPLOSION', '3fLfLLf', *coord, explosionType, fRadius, bSound, bInvisible, fCameraShake)

    def shoot_between(self, v1, v2, demage, weapon, owner, speed, check_model=True):
        """ 武器把子弹从v1射向v2
        :param demage: 伤害值: int
        :param weapon: 武器hash
        :param owner: 行为人: ped
        :param speed: 子弹速度: float
        :param check_model: 是否检查武器model加载情况
        """
        if check_model:
            self.request_weapon_model(weapon)
        self.script_call('SHOOT_SINGLE_BULLET_BETWEEN_COORDS', '6f6Qf', *v1, *v2, demage, 1, weapon, owner, 1, 0, speed)

    def shoot_vehicle_rocket(self, _=None, ped_id=None, count=1):
        """发射车载火箭"""
        weapon = WEAPON_HASH['VEHICLE_ROCKET']
        self.request_weapon_model(weapon)
        coord = Vector3(self.get_cam_front_coord())
        rot = Vector3(self.get_camera_rot())
        if self.isInVehicle:
            rot.z *= 0.4

        # 目标坐标
        target = coord + rot * 100

        if ped_id is None:
            ped_id = self.get_ped_id()

        vertical_1, vertical_2 = rot.get_vetical_xy()
        vertical_1 *= 0.5
        vertical_2 *= 0.5

        for i in range(1, count + 1):
            self.shoot_between(coord + (vertical_1[0] * i, vertical_1[1] * i, 1), target, 250, weapon, ped_id, -1.0, False)
            self.shoot_between(coord + (vertical_2[1] * i, vertical_2[1] * i, 1), target, 250, weapon, ped_id, -1.0, False)

    def rocket_attack(self, entitys, speed=40, height=10):
        """天降正义(导弹攻击敌人)"""
        weapon = WEAPON_HASH['VEHICLE_ROCKET']
        self.request_weapon_model(weapon)
        for p in entitys:
            if p.handle:
                coord0 = p.coord.values()
                coord1 = tuple(coord0)
                coord0[2] += height
                self.shoot_between(coord0, coord1, 250, weapon, self.get_ped_id(), speed, False)

    def rocket_attack_enemy(self, _=None, *args, **kwargs):
        """天降正义(导弹攻击敌人)"""
        self.rocket_attack(self.get_enemy_blips(), *args, **kwargs)

    def rocket_attack_target(self, _=None, *args, **kwargs):
        """天降正义(导弹攻击敌人)"""
        self.rocket_attack(self.get_target_blips(), *args, **kwargs)

    def rocket_attack_police(self, _=None, *args, **kwargs):
        """乱世枭雄(导弹攻击警察)"""
        self.rocket_attack(self.get_police_blips(), *args, **kwargs)

    def rocket_attack_police_and_helicopter(self, _=None, *args, **kwargs):
        """乱世枭雄(导弹攻击警察和警用直升机)"""
        self.rocket_attack(tuple(self.get_police_blips()) + tuple(self.get_police_helicopter_blips()), *args, **kwargs)

    def activate_save_menu(self, _=None):
        """激活保存菜单"""
        self.native_call('SET_SAVE_MENU_ACTIVE', 'Q', 1)

    def request_weapon_model(self, weapon):
        """暂时还用不到好像"""
        if not self.script_call('HAS_WEAPON_ASSET_LOADED', 'Q', weapon):
            self.script_call('REQUEST_WEAPON_ASSET', '3Q', weapon, 31, 0)

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
        self.script_call('PAUSE_CLOCK', 'L', freeze)

    def create_enemy(self, count=1):
        for p in self.get_peds(count):
            p.as_enemy()

    def set_ped_infinite_ammo_clip(self, _=None):
        """角色无限弹药"""
        self.player.set_infinite_ammo_clip(self.toggle_setting('infinite_ammo_clip'))

    def set_ped_ignored_by_police(self, _=None):
        """角色不会被警察注意"""
        self.player.ignored_by_police = self.toggle_setting('ignored_by_police')

    def special_ability_fill_meter(self, _=None):
        """特殊能力能量充满"""
        self.native_call('SPECIAL_ABILITY_FILL_METER', '2Q', self.get_player_index(), 1)

    def set_player_model(self, _=None):
        """设置当前玩家模型"""
        model_name = PLAYER_MODEL[self.player_model_view.index][1]
        model = self.get_cache('player_model', model_name, self.get_hash_key)
        self.player.set_model(model)

    def create_selected_ped(self, _=None):
        """生产该模型的人物"""
        model_name = PLAYER_MODEL[self.player_model_view.index][1]
        model = self.get_cache('player_model', model_name, self.get_hash_key)
        self.create_ped(model)