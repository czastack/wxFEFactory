import math
import os
import json
import time
import __main__
from functools import partial
from lib import utils
from lib.lazy import lazy
from lib.hack.forms import (Group, StaticGroup, ModelInput, ModelCoordWidget, TabList)
from lib.win32.keys import VK
from lib.win32.sendkey import auto, TextVK
from lib.config.widgets import IntConfig, BoolConfig, FloatConfig, SelectConfig, ConfigGroup
from lib import ui
from styles import dialog_style, styles
from ..gta_base.main import BaseGTATool
from ..gta_base.utils import degree_to_radian, Vector3
from ..gta_base.native import SafeScriptEnv
from ..gta_base.widgets import ColorWidget
from . import address, models, datasets, coords
from .models import Player, Vehicle
from .widgets import WeaponWidget, CustomColorWidget


class Main(BaseGTATool):
    CLASS_NAME = 'grcWindow'
    WINDOW_NAME = 'Grand Theft Auto V'
    address = address
    models = models
    Player = Player
    Vehicle = Vehicle

    RAISE_UP_SPEED = 12
    SAFE_SPEED_RATE = 30
    SAFE_SPEED_UP = 6
    GO_FORWARD_COORD_RATE = 8
    FLY_SPEED = 15
    SLING_COORD_DELTA = 10
    SLING_COORD_UP = 3
    SLING_SPEED_RATE = 70
    EXPLODE_DISTANCE_VEHICLE = 10

    def __init__(self):
        super().__init__()

    def render_main(self):
        with Group("player", "角色", self.weak._player):
            self.render_player()

        self.lazy_group(Group("vehicle", "汽车", self.weak._vehicle), self.render_vehicle)
        self.lazy_group(Group("weapon", "武器槽", None, flexgrid=False), self.render_weapon)
        self.lazy_group(Group("global", "全局", self), self.render_global)
        self.lazy_group(StaticGroup("快捷键"), self.render_hotkey)
        self.lazy_group(StaticGroup("角色模型"), self.render_ped_model)
        self.lazy_group(StaticGroup("载具模型"), self.render_vehicle_model)
        self.lazy_group(StaticGroup("物体模型"), self.render_object_model)
        self.lazy_group(StaticGroup("武器配件"), self.render_weapon_components)
        self.lazy_group(StaticGroup("测试"), self.render_functions)

        with Group(None, "设置", None, hasfooter=False):
            self.render_config()

    def render_player(self):
        ModelInput("hp", "生命")
        ModelInput("ap", "防弹衣")
        self.coord_view = ModelCoordWidget("coord", "坐标", savable=True, preset=coords)
        # ModelInput("gravity", "重量")
        ModelCoordWidget("speed", "速度")
        ModelInput("rotation", "旋转")
        ModelInput("wanted_level", "通缉等级")
        ui.Hr()
        with ui.GridLayout(cols=4, vgap=10, class_="expand"):
            ui.Button(label="车坐标->人坐标", onclick=self.from_vehicle_coord)
            ui.Button(label="从标记点读取坐标", onclick=self.player_coord_from_waypoint)
            ui.ToggleButton(label="切换无伤状态", onchange=self.set_ped_invincible)
            ui.ToggleButton(label="可以切换武器", onchange=self.set_ped_can_switch_weapons)
            ui.ToggleButton(label="不能被拽出载具", onchange=self.set_ped_canot_be_dragged_out)
            ui.ToggleButton(label="不能在车中被射击", onchange=self.set_ped_can_be_shot_in_vehicle)
            ui.ToggleButton(label="摩托车老司机", onchange=self.set_ped_keep_bike)
            ui.ToggleButton(label="切换无限弹药", onchange=self.set_ped_infinite_ammo_clip)
            ui.ToggleButton(label="不被警察注意", onchange=self.set_ped_ignored_by_police)
            ui.ToggleButton(label="快速奔跑", onchange=self.set_player_fast_run)
            ui.ToggleButton(label="快速游泳", onchange=self.set_player_fast_swim)
            ui.ToggleButton(label="不被通缉", onchange=self.set_never_wanted)
            ui.ToggleButton(label="没有噪声", onchange=self.set_no_noise)

    def render_vehicle(self):
        vehicle = self.weak._vehicle
        ModelInput("hp", "HP")
        ModelCoordWidget("roll", "滚动")
        ModelCoordWidget("dir", "方向")
        self.vehicle_coord_view = ModelCoordWidget("coord", "坐标", savable=True, preset=coords)
        ModelCoordWidget("speed", "速度")
        ModelInput("weight", "重量")
        ui.Hr()
        with ui.GridLayout(cols=4, vgap=10, class_="expand"):
            ui.Button(label="人坐标->车坐标", onclick=self.from_player_coord)
            ui.Button(label="从标记点读取坐标", onclick=self.vehicle_coord_from_waypoint)
            ui.ToggleButton(label="开启无伤", onchange=self.set_vechile_invincible)
            ui.Button(label="锁车", onclick=self.vehicle_lock_door)
            ui.Button(label="开锁", onclick=partial(self.vehicle_lock_door, lock=False))
        ui.Label("颜色")
        with ui.Horizontal(class_="fill"):
            ColorWidget("vehicle_color", "车身", self._vehicle, "color", datasets.COLOR_LIST)
            ColorWidget("vehicle_specular_color", "条纹", vehicle, "specular_color", datasets.COLOR_LIST)
            ColorWidget("vehicle_feature_color1", "边缘", vehicle, "feature_color1", datasets.COLOR_LIST)
            ColorWidget("vehicle_feature_color2", "轮胎", vehicle, "feature_color2", datasets.COLOR_LIST)
        CustomColorWidget("vehicle_custom_primary_color", "自定义颜色1", vehicle, "custom_primary_color")
        CustomColorWidget("vehicle_custom_secondary_color", "自定义颜色2", vehicle, "custom_secondary_color")

    def render_weapon(self):
        self.weapon_views = []
        player = self.weak._player
        with ui.Vertical(class_="fill padding"):
            self.weapon_model_book = ui.Notebook(class_="fill", wxstyle=0x0200)
            with self.weapon_model_book:
                for category in datasets.WEAPON_LIST:
                    with ui.Vertical():
                        with ui.FlexGridLayout(cols=2, vgap=10, class_="fill padding") as view:
                            view.sizer.AddGrowableCol(1)
                            for item in category[1]:
                                self.weapon_views.append(WeaponWidget(player, *item))
                    view.parent.extra = dict(caption=category[0])

            with ui.Horizontal():
                ui.Button(label="全部武器", onclick=self.give_all_weapon)
                ui.Button(label="一键最大", onclick=self.weapon_max)

    def render_global(self):
        ModelInput("game_hour", "当前小时")
        ModelInput("game_minute", "当前分钟")
        ModelInput("game_seconds", "当前秒数")
        ModelInput("game_day", "当前日期")
        ModelInput("game_month", "当前月份")
        ModelInput("game_year", "当前年份")
        ModelInput("money", "金钱")

        ModelInput("wind_speed", "风速")
        ui.Label("天气")
        with ui.Horizontal(class_="fill"):
            self.weather_view = ui.Choice(class_="fill", choices=(item[0] for item in datasets.WEATHER_LIST))
            ui.Button("短暂", onclick=self.apply_weather)
            ui.Button("持久", onclick=partial(self.apply_weather, persist=True))
            ui.ToggleButton("起风", onchange=self.set_wind)

    def render_hotkey(self):
        with ui.ScrollView(class_="fill"):
            self.render_common_text()
            ui.Text("大加速: alt+shift+m\n"
                "生成选中的载具并进入: alt+shift+v\n"
                "当前武器子弹全满: alt+g\n"
                "瞬移到标记点: alt+shift+g\n"
                "瞬移到目的地: alt+1\n"
                "根据摄像机朝向设置当前实体的朝向: alt+e\n"
                "爆破最近的车: alt+o\n"
                "发射车载火箭: alt+r\n"
                "发射多枚车载火箭: alt+shift+r\n"
                "天降正义(导弹攻击敌人): alt+enter\n"
                "特殊能力能量充满: alt+capslock")

    def render_ped_model(self):
        from .datasets.player_models import PLAYER_MODELS
        with ui.Horizontal(class_="fill padding"):
            self.player_model_book = TabList(PLAYER_MODELS)
            with ui.ScrollView(class_="fill padding"):
                ui.Text("1. 切换模型会失去武器")
                ui.Text("2. 切换动物模型容易引发bug，请慎用")
                ui.Text("3. 在陆地上使用鱼类模型会突然失去梦想，请注意")
                ui.Button("切换模型", onclick=self.set_player_model)
                ui.Button("生成人物", onclick=self.create_selected_ped)

    def render_vehicle_model(self):
        from .datasets.vehicle_models import VEHICLE_MODELS
        self.vehicle_model_book = TabList(VEHICLE_MODELS)

    def render_object_model(self):
        from .datasets.object_models import OBJECT_MODELS
        self.object_model_book = TabList(OBJECT_MODELS)

    def render_weapon_components(self):
        from .datasets.weapon_components import WEAPON_COMPONENTS

        weapon_map = {}
        for category in datasets.WEAPON_LIST:
            for item in category[1]:
                weapon_map[item[0]] = item

        self.weapon_components = weapon_components = []
        for item in WEAPON_COMPONENTS:
            weapon = weapon_map[item[0]]
            weapon_components.append((weapon[1], item[1], weapon[2]))

        with ui.Vertical(class_="fill padding"):
            self.weapon_component_book = TabList(weapon_components)
            # self.weapon_component_book.SetToolTip("选中后回车键给与配件")
            with ui.Horizontal():
                ui.Button("给予", onclick=self.give_weapon_component)
                ui.Button("移除", onclick=self.remove_weapon_component)

    def render_functions(self):
        with ui.GridLayout(cols=4, vgap=10, class_="expand"):
            self.render_common_button()
            # ui.Button("附近的车爆炸", onclick=self.near_vehicles_explode)
            ui.Button("附近的人缴械", onclick=self.near_peds_remove_weapon)
            ui.Button("附近的人着火", onclick=self.near_peds_make_fire)
            ui.Button("附近的人爆炸", onclick=self.near_peds_explode)
            ui.Button("附近的人下车", onclick=self.near_peds_exit_vehicle)
            ui.Button("敌人着火", onclick=self.enemys_make_fire)
            ui.Button("敌人爆头", onclick=self.enemys_explode_head)
            ui.Button("敌人爆炸", onclick=self.enemys_explode)
            ui.Button("敌人缴械", onclick=self.enemys_remove_weapon)
            ui.Button("敌人定住", onclick=self.enemys_freeze_position)
            ui.Button("圆形标记定住", onclick=self.target_freeze_position)
            ui.Button("保存菜单", onclick=self.activate_save_menu)
            ui.Button("导弹攻击敌人", onclick=self.rocket_attack_enemy)
            ui.Button("导弹攻击所有标记", onclick=self.rocket_attack_target)
            ui.Button("导弹攻击警察", onclick=self.rocket_attack_police)
            ui.Button("导弹攻击警用载具", onclick=self.rocket_attack_police_and_helicopter)
            ui.Button("导弹射向敌人", onclick=self.rocket_shoot_enemy)
            ui.Button("导弹射向所有标记", onclick=self.rocket_shoot_target)
            ui.Button("导弹射向警察", onclick=self.rocket_shoot_police)
            ui.Button("导弹射向警用载具", onclick=self.rocket_shoot_police_and_helicopter)
            ui.Button("停止计时", onclick=self.freeze_timer)
            ui.Button("恢复计时", onclick=partial(self.freeze_timer, freeze=False))
            ui.Button("附近的人吹飞", onclick=self.near_peds_go_away)
            ui.Button("附近的车吹飞", onclick=self.near_vehicles_go_away)
            ui.Button("驾驶到到目的地", onclick=self.drive_to_destination)
            ui.Button("驾驶到到标记点", onclick=self.drive_to_waypoint)
            ui.Button("驾驶到到黄色检查点", onclick=self.drive_to_yellow_checkpoint)
            ui.Button("瞬移到到黄色检查点", onclick=self.teleport_to_yellow_checkpoint)
            ui.Button("跟着敌人", onclick=self.drive_follow)
            ui.Button("追捕敌人", onclick=self.vehicle_chase)
            ui.Button("跟着蓝色标记", onclick=self.drive_follow_blue)
            ui.Button("停止自动驾驶", onclick=self.clear_driver_tasks)
            ui.Button("清空区域内的载具", onclick=self.clear_area_of_vehicles)
            ui.Button("清空区域内的角色", onclick=self.clear_area_of_peds)
            ui.Button("清空区域内的警察", onclick=self.clear_area_of_cops)
            ui.Button("熄灭区域内的火焰", onclick=self.clear_area_of_fire)
            ui.Button("修复衣服", onclick=self.repair_cloth)
            ui.Button("洗车", onclick=self.wash_vehicle)
            ui.Button("进入上一辆载具", onclick=self.into_last_vehicle)
            ui.Button("召唤火车", onclick=self.random_train)
            ui.Button("最近的车附上", onclick=self.nearest_vehicle_attach)
            ui.Button("附上敌人", onclick=self.attach_to_enemey)
            ui.Button("附上蓝色标记", onclick=self.attach_to_blue)
            ui.Button("取消附上", onclick=self.detach_entity)
            ui.Button("随机装扮", onclick=self.set_ped_random_component)
            ui.Button("生成所选物体", onclick=self.create_selected_object)
            ui.Button("生成多个物体", onclick=self.create_selected_objects_caller)
            ui.Button("发射生成物体", onclick=self.create_launch_object)
            ui.Button("前面起火", onclick=self.create_fire_at_front)
            ui.Button("打架", onclick=self.fight_against)
            ui.Button("导弹射向所瞄", onclick=self.rocket_shoot_entity_aiming_at)
            ui.Button("所瞄目标爆炸", onclick=self.entity_aiming_at_explode)
            # ui.Button("所射子弹爆炸", onclick=self.explode_projectiles_test)
            self.set_buttons_contextmenu()

    def render_config(self):
        with ConfigGroup(self.config):
            BoolConfig('mark_police_as_enemy', '把警察标记为敌人').set_help('对敌人的操作也会对警察有效')
            BoolConfig('explode_no_owner', '生成爆炸时不设置所有者(不会被通缉，但某些任务敌人打不死)')
            BoolConfig('rocket_attack_no_owner', '导弹攻击时不设置所有者(不会被通缉，但某些任务敌人打不死)')
            FloatConfig('rocket_attack_speed', '导弹攻击速度', 100)
            FloatConfig('rocket_shoot_speed', '导弹向前速度', -1.0)
            IntConfig('rocket_shoot_count_little', '导弹发射对数(少)', 0)
            IntConfig('rocket_shoot_count_more', '导弹发射对数(多)', 3)
            IntConfig('rocket_shoot_target_count', '射向目标导弹数', 1)
            IntConfig('rocket_damage', '导弹攻击伤害', 250)
            SelectConfig('shoot_weapon_hash', '射击武器种类', datasets.SHOOT_WEAPON_CHOICES).set_help('默认为上述的"导弹"')
            FloatConfig('auto_driving_speed', '自动驾驶速度', 300)
            SelectConfig('auto_driving_style', '自动驾驶风格', datasets.DRIVING_STYLE)
            SelectConfig('attach_direction', '附上目标方向', datasets.ATTACH_DIRECTION)
            FloatConfig('attach_distance_ped', '步行附上距离', 6).set_help('步行时附上目标距离')
            FloatConfig('attach_distance_vehilce', '驾车附上距离', 15).set_help('驾车时附上目标距离')
            IntConfig('create_objects_count', '批量生成物体个数', 5)
            FloatConfig('create_objects_spcae', '批量生成物体间隔', 5)
        ui.Hr()
        ui.Button("放弃本次配置修改", onclick=self.discard_config)

    def get_hotkeys(self):
        return (
            (VK.MOD_ALT | VK.MOD_SHIFT, VK.V, self.spawn_choosed_vehicle_and_enter),
            (VK.MOD_ALT, VK.G, self.max_cur_weapon),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK.G, self.teleport_to_waypoint),
            (VK.MOD_ALT, VK.E, self.dir_correct),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK.M, partial(self.speed_up, rate=30), 'speed_large'),
            (VK.MOD_ALT, VK.O, self.explode_nearest_vehicle),
            (VK.MOD_ALT, VK.R, self.shoot_vehicle_rocket_little),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK.R, self.shoot_vehicle_rocket_more),
            (VK.MOD_ALT, VK.ENTER, self.rocket_attack_enemy),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK.ENTER, self.rocket_shoot_enemy),
            (VK.MOD_ALT, VK.CAPSLOCK, self.special_ability_fill_meter),
        ) + self.get_common_hotkeys()

    def get_addr(self, addr):
        """原始地址转模块装载后的真实地址"""
        return self.MODULE_BASE + addr

    def orig_addr(self, addr):
        """模块装载后的真实地址转原始地址"""
        return addr - self.MODULE_BASE

    def get_offset_addr(self, addr):
        return addr + self.handler.read32(addr) + 4

    def get_version(self):
        """获取版本码"""
        return self.handler.get_module_version()[1] >> 16

    def init_addr(self):
        """初始化地址信息"""
        self.MODULE_BASE = self.handler.base_addr - 0x140000000

        version = self.get_version()
        version_depend = address.VERSION_DEPEND.get(version, None)
        if version_depend:
            # 装载针对当前版本的地址列表
            for name in version_depend:
                addr = version_depend[name]
                setattr(address, name, self.get_addr(addr) if addr else 0)

            # address.REGISTRATION_TABLE = self.get_offset_addr(address.REGISTRATION_TABLE_BASE + 9)
            # self.NativeRegistration = models.NativeRegistration1290 if version >= 1290 else models.NativeRegistration

        # 装载针对当前版本的native_hash
        # ==>
        # name = 'hash_%d' % version
        # module = getattr(__import__(__package__ + '.native_hash', fromlist=[name]), name)
        # address.NATIVE_HASH = module.NATIVE_HASH
        # ===
        from .native_hash.hash_universal import NATIVE_HASH
        address.NATIVE_HASH = NATIVE_HASH
        # <==

        # 检查是否加载了ScriptHook的帮助模块，因为部分script直接远程调用会crash
        # 要在ScriptHook的线程中才能安全运行
        self.script_hook_helper = self.handler.get_module('NativeHelper.asi')
        if self.script_hook_helper:
            # ==>
            # self.script_hook_helper_ctx_ptr = self.script_hook_helper + 0x15A90
            # ===
            self.script_call_addr = self.script_hook_helper + 0x1040
            # <==

        # 此次运行的Native Script地址缓存
        # address.NATIVE_ADDRS = {}

    def onattach(self):
        """初始化远程函数"""
        self.init_addr()
        super().onattach()
        self.near_entity_buff = self.handler.alloc_memory(8 * 40)

    def ondetach(self):
        """释放远程函数"""
        super().ondetach()
        self.handler.free_memory(self.near_entity_buff)

    # ==>
    # def get_native_addr(self, name):
    #     """根据脚本名称获取装载后原生函数地址"""
    #     addr = address.NATIVE_ADDRS.get(name, 0)
    #     if addr is 0:
    #         # 获取原生函数地址
    #         hash = address.NATIVE_HASH[name]
    #         registration = self.NativeRegistration(self.handler.read64(
    #             address.REGISTRATION_TABLE + (hash & 0xff) * 8), self.handler)
    #         addr = registration.get_func(hash)
    #         if addr:
    #             address.NATIVE_ADDRS[name] = addr
    #     return addr

    # def native_call(self, name, arg_sign, *args, ret_type=int, ret_size=8):
    #     """ 远程调用GTAIV中的方法
    #     :param name: 方法名称，见address.NATIVE_HASH
    #     :param arg_sign: 函数签名
    #     """
    #     addr = self.get_native_addr(name) if isinstance(name, str) else name
    #     if addr:
    #         return super().native_call(addr, arg_sign, *args, ret_type=ret_type, ret_size=ret_size)
    #     else:
    #         print('函数不存在', name)

    # def script_call(self, name, arg_sign, *args, ret_type=int, ret_size=8, sync=True):
    #     """通过ScriptHook的帮助模块远程调用脚本函数，通过计时器轮询的方式实现同步"""
    #     if self.script_hook_helper:
    #         with self.native_context:
    #             fn_addr = self.get_native_addr(name)
    #             if arg_sign:
    #                 self.native_context.push(arg_sign, *args)
    #             self.native_context.push('Q', fn_addr)
    #             self.handler.write64(self.script_hook_helper_ctx_ptr, self.native_context.addr)

    #             if sync:
    #                 # 在1秒内尝试同步
    #                 try_count = 20
    #                 time.sleep(0.02)
    #                 while try_count:
    #                     if self.handler.read64(self.script_hook_helper_ctx_ptr) == 0:
    #

    #                         return

    #                     try_count -= 1
    #                     time.sleep(0.05)

    #                 self.handler.write64(self.script_hook_helper_ctx_ptr, 0)
    #                 print('获取script_call返回失败，超过尝试次数')
    # ===

    def script_call(self, name, arg_sign, *args, loop=1, ret_type=int, ret_size=8, sync=True):
        """通过ScriptHook的帮助模块远程调用脚本函数，通过计时器轮询的方式实现同步"""
        context = self.native_context
        if self.script_hook_helper:
            with context:
                if arg_sign:
                    context.push(arg_sign, *args)
                context.push('Q', address.NATIVE_HASH.get(name, 0))
                if loop > 1:
                    context.push('L', 0xC0000000 | loop)
                self.handler.remote_call(self.script_call_addr, context.addr)
                if ret_type:
                    return self.native_context.get_result(ret_type, ret_size)
        else:
            print("script_hook_helper未初始化，是否忘记了添加NativeHelper.asi？")

    native_call = script_call
    # <==

    def script_call_vector(self, *args, **kwargs):
        fixed = 6 if kwargs.pop('fixed6', True) else -1
        self.native_call(*args, **kwargs)
        return self.native_context.get_vector_result(8, fixed)

    def script_hook_call_vector(self, *args, **kwargs):
        fixed = 6 if kwargs.pop('fixed6', True) else -1
        self.script_call(*args, **kwargs)
        return self.native_context.get_vector_result(8, fixed)

    def get_hash_key(self, name):
        return self.native_call('GET_HASH_KEY', 's', name)

    def _player(self):
        """获取当前角色"""
        player = getattr(self, '_player_ins', None)
        player_index = self.player_id

        if not player:
            player = self._player_ins = self.Player(player_index, self.ped_id, self)
        else:
            player.index = player_index
            player.handle = self.ped_id
        return player

    def _vehicle(self):
        """获取当前角色的上次使用的载具"""
        return self.player.last_vehicle

    player = property(_player)
    vehicle = property(_vehicle)

    @property
    def player_id(self):
        """获取当前角色的序号"""
        return self.native_call('GET_PLAYER_INDEX', None)

    @property
    def ped_id(self):
        """获取当前角色的句柄"""
        return self.native_call('PLAYER_PED_ID', None)

    @property
    def ped_pool(self):
        """角色池"""
        pass

    @property
    def vehicle_pool(self):
        """载具池"""
        pass

    def get_peds(self, count=20):
        """获取角色池中的角色列表"""
        addr = self.near_entity_buff
        self.handler.write64(addr, count)
        real_count = self.script_call('GET_PED_NEARBY_PEDS', '2Ql', self.ped_id, addr, -1)
        tmp_ped = Player(0, 0, self)
        my_handle = self.ped_id
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
        real_count = self.script_call('GET_PED_NEARBY_VEHICLES', '2Q', self.ped_id, addr)
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
        self.native_call('GET_CLOSEST_PED', '4f3Q3l', *self.entity.coord, distance, 1, 1,
            self.native_context.get_temp_addr(), 0, 1, -1)
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

    def restore_hp_large(self, _=None):
        """恢复大量HP"""
        if self.in_vehicle:
            self.vehicle.hp = 1000
            self.vehicle_fix(self.vehicle)
        self.player.hp = 200
        self.player.ap = 200

    def to_up(self, _=None):
        """升高(无速度)"""
        if self.in_vehicle:
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

    def get_waypoint_coord(self):
        blip = self.get_first_blip(models.Blip.BLIP_WAYPOINT)
        if blip:
            coord = list(blip.coord)
            if coord[2] < 3:
                coord[2] = 800.0
                coord[2] = self.GetGroundZ(coord) or 36
            return coord

    def player_coord_from_waypoint(self, _=None):
        # 从标记点读取坐标
        coord = self.get_waypoint_coord()
        if coord:
            self.coord_view.input_value = coord

    def vehicle_coord_from_waypoint(self, _=None):
        # 从标记点读取坐标
        coord = self.get_waypoint_coord()
        if coord:
            self.vehicle_coord_view.input_value = coord

    def set_ped_invincible(self, tb):
        """当前角色无伤"""
        self.player.invincible = tb.checked

    def set_vechile_invincible(self, tb):
        """当前载具无伤"""
        self.vehicle.set_invincible(tb.checked)

    def set_ped_can_switch_weapons(self, tb):
        """解除当前角色武器切换限制"""
        self.player.block_switch_weapons = not tb.checked

    def set_ped_canot_be_dragged_out(self, tb):
        """当前角色不能被拖出载具"""
        self.player.can_be_dragged_out_of_vehicle = not tb.checked

    def set_ped_can_be_shot_in_vehicle(self, tb):
        """当前角色不能否在车中被射击"""
        self.player.can_be_shot_in_vehicle = not tb.checked

    def set_ped_keep_bike(self, tb):
        """当前角色不会从摩托车上甩出去"""
        self.player.keep_bike = tb.checked

    def set_ped_infinite_ammo_clip(self, tb):
        """角色无限弹药"""
        self.player.set_infinite_ammo_clip(tb.checked)

    def set_ped_ignored_by_police(self, tb):
        """角色不会被警察注意"""
        self.player.ignored_by_police = tb.checked

    def set_player_fast_run(self, tb):
        """快速奔跑"""
        self.player.fast_run = tb.checked

    def set_player_fast_swim(self, tb):
        """快速游泳"""
        self.player.fast_swim = tb.checked

    def set_never_wanted(self, tb):
        """不被通缉"""
        # self.max_wanted_level = 0 if tb.checked else 5
        toggle = tb.checked
        if toggle:
            self.clear_wanted_level()
        self.script_call('SET_WANTED_LEVEL_MULTIPLIER', 'f', 0 if toggle else 1)

    def set_no_noise(self, tb):
        """不发出噪声"""
        self.player.noise_rate = 0 if tb.checked else 1.0

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

    def near_vehicles_boom(self, _=None):
        """摧毁附近的载具"""
        for v in self.get_near_vehicles():
            v.hp = 0
            v.engine_hp = -4000

    def near_vehicles_explode(self, _=None):
        """附近的车爆炸"""
        for v in self.get_near_vehicles():
            v.explode()

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
        # 0x22D8FE39 穿甲手枪
        weapon = 0x22D8FE39
        self.request_weapon_model(weapon)
        for p in self.get_enemys():
            if isinstance(p, Player):
                p.freeze_position()
                coord0 = p.head_coord
                coord1 = coord0.clone()
                coord0.x += 0.1
                self.shoot_between(coord0, coord1, 250, 0x22D8FE39, self.ped_id, -1.0, False)
                p.freeze_position(False)

    def enemys_explode(self, _=None):
        """敌人爆炸"""
        for blip in self.get_enemy_blips():
            self.create_explosion(blip.coord)

    def enemys_remove_weapon(self, _=None):
        """敌人缴械"""
        for p in self.get_enemys():
            if isinstance(p, Player):
                p.remove_all_weapons()

    def enemys_freeze_position(self, _=None):
        """敌人定住"""
        for p in self.get_enemys():
            if isinstance(p, Player):
                vehicle = p.vehicle
                if vehicle:
                    vehicle.freeze_position()
            else:
                p.freeze_position()

    def target_freeze_position(self, _=None):
        """目标定住"""
        for p in self.get_target_blips():
            p.entity and p.entity.freeze_position()

    def near_peds_exit_vehicle(self, _=None):
        """附近的人下车"""
        for p in self.get_near_peds():
            p.clear_tasks_now()

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
        """获取所有标记"""
        if isinstance(sprites, int):
            sprites = (sprites,)

        if isinstance(color, int):
            color = (color,)

        if isinstance(types, int):
            types = (types,)

        def check_blip(blip):
            blip_type = blip.blip_type
            return blip_type and (types is None or blip_type in types) and (color is None or blip.color in color)

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
        """获取所有的圆形标记"""
        return self.get_blips(models.Blip.BLIP_CIRCLE, color)

    def get_yellow_checkpoints(self):
        """获取所有的黄色检查点标记"""
        return self.get_blips(models.Blip.BLIP_CIRCLE, (models.Blip.BLIP_COLOR_YELLOWMISSION,
            models.Blip.BLIP_COLOR_YELLOWMISSION2, models.Blip.BLIP_COLOR_MISSION))

    def get_enemy_blips(self):
        """获取红色标记"""
        blips = (blip for blip in self.get_target_blips(models.Blip.BLIP_COLORS_ENEMY) if blip.hud_color == 6)
        if self.config.mark_police_as_enemy:
            blips = tuple(blips) + self.get_cop_blips()
        return blips

    def get_friends_blips(self):
        """获取蓝色标记"""
        return (blip for blip in self.get_target_blips(models.Blip.BLIP_COLORS_FRIEND) if blip.hud_color == 9)

    def get_enemys(self):
        """获取红色标记的entity"""
        return [blip.entity for blip in self.get_enemy_blips() if blip.handle]

    def get_friends(self):
        """获取蓝色标记的entity"""
        return [blip.entity for blip in self.get_friends_blips() if blip.entity]

    def get_police_blips(self):
        """获取警察标记"""
        return self.get_blips(models.Blip.BLIP_COP)

    def get_police_helicopter_blips(self):
        """获取警察直升机标记"""
        return self.get_blips(models.Blip.BLIP_COPHELICOPTER)

    def get_cop_blips(self):
        """获取所有警察标记"""
        return tuple(self.get_police_blips()) + tuple(self.get_police_helicopter_blips())

    def teleport_to_blip(self, blip):
        """瞬移到指定标记"""
        if blip:
            coord = list(blip.coord)
            if coord[0] != 0 or coord[1] != 0:
                if coord[2] < 3:
                    coord[2] = 1024
                    coord[2] = self.GetGroundZ(coord) or 36
                entity = self.entity
                self.last_coord = Vector3(entity.coord)  # 上次瞬移前的坐标
                self.last_teleport_coord = Vector3(coord)  # 上次瞬移后的坐标
                entity.coord = coord
                return True

    def teleport_to_destination(self, _=None):
        """瞬移到目的地"""
        if not self.teleport_to_blip(self.get_first_blip(models.Blip.BLIP_CIRCLE)):
            print('无法获取目的地坐标')

    def teleport_to_waypoint(self, _=None):
        """瞬移到标记点"""
        if not self.teleport_to_blip(self.get_first_blip(models.Blip.BLIP_WAYPOINT)):
            entity = self.entity
            coord = entity.coord.values()
            coord[2] = 1024
            coord[2] = self.GetGroundZ(coord)
            entity.coord = coord

    def teleport_to_yellow_checkpoint(self, _=None):
        """瞬移到到黄色检查点"""
        blips = tuple(self.get_yellow_checkpoints())
        if blips:
            self.teleport_to_blip(blips[0])

    def drive_to_blip(self, blip):
        """驾驶到到目的地"""
        if blip and self.vehicle:
            self.vehicle.drive_to(blip.coord, self.config.auto_driving_speed, self.config.auto_driving_style)

    def drive_to_destination(self, _=None):
        """驾驶到到目的地"""
        self.drive_to_blip(self.get_first_blip(models.Blip.BLIP_CIRCLE))

    def drive_to_waypoint(self, _=None):
        """驾驶到到标记点"""
        self.drive_to_blip(self.get_first_blip(models.Blip.BLIP_WAYPOINT))

    def drive_to_yellow_checkpoint(self, _=None):
        """驾驶到到黄色检查点"""
        blips = tuple(self.get_yellow_checkpoints())
        if blips:
            self.drive_to_blip(blips[0])

    def drive_follow(self, _=None):
        """跟着敌人"""
        vehicle = self.vehicle
        if vehicle:
            entitys = self.get_enemys()
            if entitys:
                vehicle.drive_follow(entitys[0], self.config.auto_driving_speed, self.config.auto_driving_style)

    def drive_follow_blue(self, _=None):
        """跟着蓝色标记"""
        vehicle = self.vehicle
        if vehicle:
            entitys = self.get_friends()
            if entitys:
                vehicle.drive_follow(entitys[0], self.config.auto_driving_speed, self.config.auto_driving_style)

    def vehicle_chase(self, _=None):
        """追捕敌人"""
        vehicle = self.vehicle
        if vehicle:
            enemys = self.get_enemys()
            if enemys:
                vehicle.chase(enemys[0])

    def clear_driver_tasks(self, _=None):
        """停止自动驾驶"""
        self.player.clear_tasks()

    def get_camera_rot(self):
        """ 获取摄像机朝向参数
        :return: (x, y, pitch)
        """
        data = self.script_call_vector('GET_GAMEPLAY_CAM_ROT', 'Q', 2)
        tx = data[0] * 0.0174532924
        tz = data[2] * 0.0174532924
        absx = abs(math.cos(tx))
        return (
            -math.sin(tz) * absx,
            math.cos(tz) * absx,
            math.sin(tx)
        )

    def get_camera_pos(self):
        """获取摄像机位置"""
        return self.script_call_vector('GET_GAMEPLAY_CAM_COORD', None)

    def get_camera_yaw(self):
        """获取xy面上的旋转量"""
        x, y, z = self.get_camera_rot()
        return math.atan2(-x, y)

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
        self.native_call('SET_CLOCK_TIME', '3L', self.game_hour, self.game_minute, int(value))

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
        self.native_call('SET_CLOCK_DATE', '3L', self.game_day, self.game_month, int(value))

    @property
    def game_week(self):
        """当前星期几"""
        return self.native_call('GET_CLOCK_DAY_OF_WEEK', None)

    @lazy
    def player_models(self):
        return tuple(map(self.get_hash_key, ['player_zero', 'player_one', 'player_two']))

    @lazy
    def money_keys(self):
        return tuple(self.get_hash_key("SP%d_TOTAL_CASH" % i) for i in range(3))

    @property
    def money(self):
        """当前金钱"""
        try:
            i = self.player_models.index(self.player.model_id)
            self.native_call('STAT_GET_INT', '2Ql', self.money_keys[i], self.native_context.get_temp_addr(), -1)
            return self.native_context.get_temp_value(size=4)
        except Exception:
            print('请确保当前人物模型是三主角之一')

    @money.setter
    def money(self, value):
        try:
            i = self.player_models.index(self.player.model_id)
            self.native_call('STAT_SET_INT', 'Q2l', self.money_keys[i], int(value), 1)
        except Exception:
            print('请确保当前人物模型是三主角之一')

    @property
    def max_wanted_level(self):
        """最大通缉等级"""
        return self.native_call('GET_MAX_WANTED_LEVEL', None)

    @max_wanted_level.setter
    def max_wanted_level(self, value):
        self.native_call('SET_MAX_WANTED_LEVEL', 'Q', value)

    def get_selected_vehicle_list(self):
        """当前刷车器活动的载具模型列表"""
        from .datasets.vehicle_models import VEHICLE_MODELS
        return VEHICLE_MODELS[self.vehicle_model_book.index][1]

    # 兼容继承自BaseGTATool的方法
    VEHICLE_LIST = property(get_selected_vehicle_list)

    @property
    def spawn_vehicle_id_view(self):
        return self.vehicle_model_book.get_page()

    def get_selected_vehicle_model(self):
        """获取刷车器选中的载具模型"""
        from .datasets.vehicle_models import VEHICLE_MODELS
        page_index = self.vehicle_model_book.index
        item_index = self.vehicle_model_book.get_page(page_index).index
        if item_index is not -1:
            model_name = VEHICLE_MODELS[page_index][1][item_index][1]
            if isinstance(model_name, int):
                return model_name
            return self.get_cache('vehicle_model', model_name, self.get_hash_key)

    def spawn_vehicle(self, model_id, coord=None):
        """生成载具"""
        model = models.VModel(model_id, self)
        model.request()
        handle = self.script_call('CREATE_VEHICLE', 'Q4f2Q', model_id, *(coord or self.get_front_coord()),
            self.player.heading, 0, 1)
        return Vehicle(handle, self)

    def spawn_choosed_vehicle_and_enter(self, _=None):
        """生成选中的载具并进入"""
        vehicle = self.spawn_choosed_vehicle()
        if vehicle:
            self.player.into_vehicle(vehicle)

    def into_last_vehicle(self, _=None):
        """进入上一辆载具"""
        vehicle = self.last_vehicle
        if vehicle:
            self.player.into_vehicle(vehicle)

    def create_ped(self, model_id, coord=None, pedType=21):
        """生成角色"""
        model = models.VModel(model_id, self)
        model.request()
        handle = self.script_call('CREATE_PED', '2Q4f2Q', pedType, model_id, *(coord or self.get_front_coord()),
            self.player.heading, 0, 1)
        return Player(0, handle, self)

    def create_object(self, model_id, coord=None, on_ground=True):
        """生成物体"""
        if isinstance(model_id, str):
            model_id = self.get_hash_key(model_id)
        model = model_ids.VModel(model_id, self)
        model.request()
        handle = self.script_call('CREATE_OBJECT', 'Q3f3Q', model_id, *(coord or self.get_front_coord()), 0, 1, 1)
        if handle:
            obj = models.Object(handle, self)
            if on_ground:
                obj.place_on_ground()
            return obj

    def create_pickup(self, type, coord=None, value=100, model=0):
        """生成可拾取物
        :param type: PICKUP_TYPE
        """
        self.script_call('CREATE_PICKUP', 'Q3f4Q', type, *(coord or self.get_front_coord()), 0, value, True, model)

    def create_fire(self, coord, maxChildren=20, isGasFire=0):
        """生成火焰"""
        return self.script_call('START_SCRIPT_FIRE', '3f2Q', *coord, maxChildren, isGasFire)

    def delete_fire(self, fire):
        """熄灭生成的火焰"""
        self.native_call('REMOVE_SCRIPT_FIRE', 'Q', fire)

    def create_fire_at_front(self, _=None):
        """前面起火"""
        self._fire = self.create_fire(self.get_front_coord())

    def _create_explosion(self, coord, explosionType=models.NativeEntity.EXPLOSION_TYPE_ROCKET,
            fRadius=12, bSound=True, bInvisible=False, fCameraShake=0):
        """产生爆炸"""
        self.script_call('ADD_EXPLOSION', '3fLfLLf', *coord, explosionType, fRadius, bSound, bInvisible, fCameraShake)

    def create_owned_explosion(self, ped, coord, explosionType=models.NativeEntity.EXPLOSION_TYPE_ROCKET,
            fRadius=12, bSound=True, bInvisible=False, fCameraShake=0):
        """产生有所有者的爆炸"""
        self.script_call('ADD_OWNED_EXPLOSION', 'Q3fLfLLf', ped, *coord, explosionType, fRadius, bSound, bInvisible,
            fCameraShake)

    def create_explosion(self, *args, **kwargs):
        """产生爆炸适配"""
        if self.config.explode_no_owner:
            self._create_explosion(*args, **kwargs)
        else:
            self.create_owned_explosion(self.ped_id, *args, **kwargs)

    def get_weapon_hash(self, name):
        """通过武器名称获取hash"""
        for group in datasets.WEAPON_LIST:
            for item in group[1]:
                if item[0] == name:
                    return item[2]

    def get_shoot_weapon(self):
        """获取要射击的武器模型"""
        weapon = self.config.shoot_weapon_hash
        if weapon:
            self.request_weapon_model(weapon)
        else:
            weapon = self.player.weapon
        return weapon

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

    def shoot_vehicle_rocket(self, ped=0, count=1):
        """发射车载火箭"""
        weapon = self.get_shoot_weapon()
        in_vehicle = self.in_vehicle
        rot = Vector3(self.get_camera_rot())
        coord = Vector3(self.player.get_bone_coord(12844)) + rot * 2
        coord.z -= 0.1
        # if rot.z > 0.2:
        #     rot.z += 0.015
        # 目标坐标
        target = coord + rot * 100
        if in_vehicle:
            vehicle = self.vehicle
            coord += Vector3(vehicle.speed) * 0.5
            height = vehicle.height
            if vehicle.model.is_car:
                driver_height = vehicle.driver.height
                if driver_height > height:
                    height = driver_height + 0.2
                coord.z += height
                target.z += 1
            elif height > 15:
                # 在飞机上
                coord += rot * 5

        speed = self.config.rocket_shoot_speed or -1.0
        damage = self.config.rocket_damage

        if count > 1:
            vertical_1, vertical_2 = rot.get_vetical_xy()
            if not in_vehicle:
                vertical_1 *= 0.5
                vertical_2 *= 0.5
            for i in range(1, count + 1):
                self.shoot_between(coord + (vertical_1[0] * i, vertical_1[1] * i, 1),
                    target, damage, weapon, ped, speed, False)
                self.shoot_between(coord + (vertical_2[1] * i, vertical_2[1] * i, 1),
                    target, damage, weapon, ped, speed, False)
        else:
            self.shoot_between(coord, target, damage, weapon, ped, speed, False)

    def shoot_vehicle_rocket_little(self, _=None):
        """发射少量车载火箭"""
        ped = 0 if self.config.rocket_attack_no_owner else self.ped_id
        self.shoot_vehicle_rocket(ped, self.config.rocket_shoot_count_little)

    def shoot_vehicle_rocket_more(self, _=None):
        """发射多量车载火箭"""
        ped = 0 if self.config.rocket_attack_no_owner else self.ped_id
        self.shoot_vehicle_rocket(ped, self.config.rocket_shoot_count_more)

    def rocket_attack_coords(self, coords, speed=100, height=10):
        """天降正义(导弹攻击坐标)"""
        weapon = self.get_shoot_weapon()
        damage = self.config.rocket_damage
        if self.config.rocket_attack_no_owner:
            ped = 0
        else:
            ped = self.ped_id
        for coord in coords:
            coord0 = list(coord)
            coord1 = coord
            coord0[0] += 0.1
            coord0[2] += height
            self.shoot_between(coord0, coord1, damage, weapon, ped, speed, False)

    def rocket_attack(self, entitys, speed=100, height=10):
        """天降正义(导弹攻击敌人)"""
        weapon = self.get_shoot_weapon()
        damage = self.config.rocket_damage
        if self.config.rocket_attack_no_owner:
            ped = 0
        else:
            ped = self.ped_id

        speed = self.config.rocket_attack_speed or speed

        for p in entitys:
            if p.handle:
                coord0 = p.coord.values()
                coord1 = tuple(coord0)
                coord0[0] += 0.1  # 如果xy坐标一样，有些武器子弹会无法移动
                coord0[2] += height
                self.shoot_between(coord0, coord1, damage, weapon, ped, speed, False)

    def rocket_shoot(self, entitys, speed=100):
        """导弹射向目标"""
        weapon = self.get_shoot_weapon()
        if self.config.rocket_attack_no_owner:
            ped = 0
        else:
            ped = self.ped_id

        speed = self.config.rocket_shoot_speed or speed

        coord = Vector3(self.player.coord)

        count = self.config.rocket_shoot_target_count
        damage = self.config.rocket_damage
        rot = None

        for p in entitys:
            if p.handle:
                coord1 = Vector3(p.coord)
                coord0 = (coord + coord1) * 0.5
                if count is 1:
                    self.shoot_between(coord0, coord1, damage, weapon, ped, speed, False)
                else:
                    if rot is None:
                        rot = Vector3(self.get_camera_rot())
                    vertical_1, vertical_2 = rot.get_vetical_xy()
                    for i in range(1, count + 1):
                        self.shoot_between(coord0 + (vertical_1[0] * i, vertical_1[1] * i, 1), coord1, damage, weapon,
                            ped, speed, False)
                        self.shoot_between(coord0 + (vertical_2[1] * i, vertical_2[1] * i, 1), coord1, damage, weapon,
                            ped, speed, False)

    def rocket_attack_enemy(self, _=None, *args, **kwargs):
        """天降正义(导弹攻击敌人)"""
        self.rocket_attack(self.get_enemy_blips(), *args, **kwargs)

    def rocket_attack_target(self, _=None, *args, **kwargs):
        """天降正义(导弹攻击所有圆形标记)"""
        self.rocket_attack(self.get_target_blips(), *args, **kwargs)

    def rocket_attack_police(self, _=None, *args, **kwargs):
        """乱世枭雄(导弹攻击警察)"""
        self.rocket_attack(self.get_police_blips(), *args, **kwargs)

    def rocket_attack_police_and_helicopter(self, _=None, *args, **kwargs):
        """乱世枭雄(导弹攻击警用载具)"""
        self.rocket_attack(self.get_cop_blips(), *args, **kwargs)

    def rocket_attack_waypint(self, _=None, *args, **kwargs):
        """导弹攻击标记点"""
        blip = self.get_first_blip(self.models.Blip.BLIP_WAYPOINT)
        if blip:
            coord = list(blip.coord)
            coord[2] = 1024
            coord[2] = self.GetGroundZ(coord)
            self.rocket_attack_coords((coord,), *args, **kwargs)

    def rocket_shoot_enemy(self, _=None, *args, **kwargs):
        """导弹射向敌人"""
        self.rocket_shoot(self.get_enemy_blips(), *args, **kwargs)

    def rocket_shoot_target(self, _=None, *args, **kwargs):
        """导弹射向所有圆形标记"""
        self.rocket_shoot(self.get_target_blips(), *args, **kwargs)

    def rocket_shoot_police(self, _=None, *args, **kwargs):
        """导弹射向警察"""
        self.rocket_shoot(self.get_police_blips(), *args, **kwargs)

    def rocket_shoot_police_and_helicopter(self, _=None, *args, **kwargs):
        """导弹射向警用载具"""
        self.rocket_shoot(tuple(self.get_police_blips()) + tuple(self.get_police_helicopter_blips()), *args, **kwargs)

    def activate_save_menu(self, _=None):
        """激活保存菜单"""
        self.native_call('SET_SAVE_MENU_ACTIVE', 'Q', 1)

    def request_weapon_model(self, weapon):
        """加载武器模型"""
        if not self.script_call('HAS_WEAPON_ASSET_LOADED', 'Q', weapon):
            self.script_call('REQUEST_WEAPON_ASSET', '3Q', weapon, 31, 0)

    def near_vehicles_to_front(self, _=None):
        super().near_vehicles_to_front(zinc=2)

    def recal_markers(self, _=None):
        self._markers = tuple(self.get_target_blips(models.Blip.BLIP_COLORS_ENEMY))
        self._marker_index = 0

    def move_marker_to_front(self, _=None):
        super().move_marker_to_front(5)

    def freeze_timer(self, _=None, freeze=True):
        """停止计时"""
        self.script_call('PAUSE_CLOCK', 'L', freeze)

    def special_ability_fill_meter(self, _=None):
        """特殊能力能量充满"""
        self.native_call('SPECIAL_ABILITY_FILL_METER', '2Q', self.player_id, 1)

    def get_selected_ped_model(self):
        """获取选中的角色模型"""
        from .datasets.player_models import PLAYER_MODELS
        page_index = self.player_model_book.index
        item_index = self.player_model_book.get_page(page_index).index
        if item_index is not -1:
            model_name = PLAYER_MODELS[page_index][1][item_index][1]
            return self.get_cache('player_model', model_name, self.get_hash_key)

    def set_player_model(self, _=None):
        """设置当前玩家模型"""
        model = self.get_selected_ped_model()
        if model:
            self.player.set_model(self.get_selected_ped_model())

    def create_selected_ped(self, _=None):
        """生成该模型的人物"""
        model = self.get_selected_ped_model()
        if model:
            return self.create_ped(self.get_selected_ped_model())

    def get_selected_object_model(self):
        """获取选中的物体模型"""
        from .datasets.object_models import OBJECT_MODELS
        page_index = self.object_model_book.index
        item_index = self.object_model_book.get_page(page_index).index
        if item_index is not -1:
            model_name = OBJECT_MODELS[page_index][1][item_index][1]
            return self.get_cache('object_model', model_name, self.get_hash_key)

    def create_selected_object(self, _=None, on_ground=True):
        """生成该模型的物体"""
        model = self.get_selected_object_model()
        if model:
            return self.create_object(self.get_selected_object_model(), on_ground=on_ground)

    def create_launch_object(self, _=None):
        """生成该模型的物体并发射"""
        obj = self.create_selected_object(on_ground=False)
        if obj:
            self.launch_entity(obj)

    def create_selected_objects(self, count, space):
        """生成多个该模型的物体"""
        model = self.get_selected_object_model()
        if model:
            objs = []
            for coord in self.iter_cam_dir_coords(count, space):
                objs.append(self.create_object(model, coord))
            return objs

    def create_selected_objects_caller(self, _=None):
        """生成多个该模型的物体"""
        self.create_selected_objects(self.config.create_objects_count, self.config.create_objects_spcae)

    def near_peds_go_away(self, _=None):
        """附近的人吹飞"""
        self.launch_entity(self.get_near_peds(), False)

    def near_vehicles_go_away(self, _=None):
        """附近的车吹飞"""
        self.launch_entity(self.get_near_vehicles(), False)

    def repair_cloth(self, _=None):
        """修复衣服"""
        self.player.reset_visible_damage()

    def wash_vehicle(self, _=None):
        """洗车"""
        self.vehicle.fix()
        self.vehicle.wash()

    def clear_area_of_vehicles(self, _=None):
        """清空区域内的载具"""
        self.script_call('CLEAR_AREA_OF_VEHICLES', '4f5Q', *self.player.coord, 1000, False, False, False, False, False)

    def clear_area_of_peds(self, _=None):
        """清空区域内的角色"""
        self.script_call('CLEAR_AREA_OF_PEDS', '4fQ', *self.player.coord, 200, True)

    def clear_area_of_cops(self, _=None):
        """清空区域内的警察"""
        self.script_call('CLEAR_AREA_OF_COPS', '4fQ', *self.player.coord, 1000, True)

    def clear_area_of_fire(self, _=None):
        """熄灭区域内的火焰"""
        self.script_call('STOP_FIRE_IN_RANGE', '4f', *self.player.coord, 100)

    def jump_on_vehicle(self, _=None):
        with SafeScriptEnv(self):
            super().jump_on_vehicle()

    def apply_weather(self, _=None, persist=False):
        """ 应用所选天气
        :param persist: 是否持久
        """
        self.native_call('CLEAR_OVERRIDE_WEATHER', None)
        index = self.weather_view.index
        if index != -1:
            weather = datasets.WEATHER_LIST[index][1]
            if persist:
                self.native_call('CLEAR_OVERRIDE_WEATHER', 's', weather)
            else:
                self.native_call('SET_WEATHER_TYPE_NOW_PERSIST', 's', weather)
                self.native_call('CLEAR_WEATHER_TYPE_PERSIST', None)

    def set_wind(self, tb):
        if tb.checked:
            self.native_call('SET_WIND', 'f', 1.0)
            self.native_call('SET_WIND_SPEED', 'f', 11.99)
            self.native_call('SET_WIND_DIRECTION', 'f', self.entity.heading)
        else:
            self.native_call('SET_WIND', 'f', 0)
            self.native_call('SET_WIND_SPEED', 'f', 0)

    @property
    def wind_speed(self):
        return self.native_call('SET_WIND_SPEED', None, ret_type=float)

    @wind_speed.setter
    def wind_speed(self, value):
        self.native_call('SET_WIND_SPEED', 'f', float(value))

    def random_train(self, _=None):
        self.script_call('SET_RANDOM_TRAINS', 'L', 1)

    def set_ped_random_component(self, _=None):
        self.script_call('SET_PED_RANDOM_COMPONENT_VARIATION', '2Q', self.ped_id, 1)

    def entitys_attach(self, entitys, distance):
        """附上当前实体"""
        if not hasattr(entitys, '__iter__'):
            entitys = (entitys,)

        me = self.entity
        for entity in entitys:
            entity.attach_to_entity(me, (0, distance, 0))

    def nearest_ped_attach(self, _=None):
        """最近的角色附上当前角色"""
        ped = self.get_nearest_ped()
        if ped:
            self.entitys_attach(ped, self.config.attach_distance_ped)

    def nearest_vehicle_attach(self, _=None):
        """最近的车附上当前实体"""
        vehicle = self.get_nearest_vehicle()
        if vehicle:
            self.entitys_attach(vehicle, self.config.attach_distance_vehilce)

    def vehilce_attach_to(self, entity):
        """当前车附上目标"""
        distance = (self.config.attach_distance_vehilce if isinstance(entity, Vehicle)
            else self.config.attach_distance_ped)
        direction = self.config.attach_direction
        if direction is datasets.DIRECTION_FRONT:
            offset = (0, distance, 0)
        elif direction is datasets.DIRECTION_BACK:
            offset = (0, -distance, 0)
        elif direction is datasets.DIRECTION_LEFT:
            offset = (-distance, 0, 0)
        elif direction is datasets.DIRECTION_RIGHT:
            offset = (distance, 0, 0)
        elif direction is datasets.DIRECTION_ABOVE:
            offset = (0, 0, distance)
        self.vehicle.attach_to_entity(entity, offset)

    def attach_to_enemey(self, _=None):
        """附上敌人"""
        vehicle = self.vehicle
        if vehicle:
            entitys = self.get_enemys()
            if entitys:
                self.vehilce_attach_to(entitys[0])

    def attach_to_blue(self, _=None):
        """附上蓝色标记"""
        vehicle = self.vehicle
        if vehicle:
            entitys = self.get_friends()
            if entitys:
                self.vehilce_attach_to(entitys[0])

    def detach_entity(self, _=None):
        """取消附上"""
        vehicle = self.vehicle
        if vehicle:
            vehicle.detach_entity()

    def fight_against(self, _=None):
        """打架"""
        me = self.ped_id
        for p in self.get_near_peds():
            p.fight_against(me)

    @property
    def entity_aiming_at(self):
        self.native_call('GET_ENTITY_PLAYER_IS_FREE_AIMING_AT', '2Q', self.player_id,
            self.native_context.get_temp_addr())
        entity = models.NativeEntity(self.native_context.get_temp_value(), self)
        return entity.subtype_instance()

    def rocket_shoot_entity_aiming_at(self, _):
        entity = self.entity_aiming_at
        if entity is not None:
            self.rocket_shoot((entity,))

    def entity_aiming_at_explode(self, _):
        entity = self.entity_aiming_at
        if entity is not None:
            entity.create_explosion()

    # def entity_aiming_at_test(self, _):
    #     entity = self.entity_aiming_at
    #     if entity:
    #         print(entity, entity.coord)

    def get_selected_weapon_component(self):
        page_index = self.weapon_component_book.index
        item_index = self.weapon_component_book.get_page(page_index).index
        if item_index is not -1:
            data = self.weapon_components[page_index]
            weapon_hash = data[2]
            component_hash = data[1][item_index][1]
            return weapon_hash, component_hash

    def give_weapon_component(self, _):
        data = self.get_selected_weapon_component()
        if data:
            self.player.give_weapon_component(*data)

    def remove_weapon_component(self, _):
        data = self.get_selected_weapon_component()
        if data:
            self.player.remove_weapon_component(*data)

    # def explode_projectiles_test(self, _):
    #     self.script_call('EXPLODE_PROJECTILES', '3Q', self.ped_id, self.config.shoot_weapon_hash, True)
