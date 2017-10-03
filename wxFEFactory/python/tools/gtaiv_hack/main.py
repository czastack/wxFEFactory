from functools import partial
from lib.hack.form import Group, InputWidget, CheckBoxWidget, CoordWidget, ModelInputWidget, ModelCoordWidget
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
from lib.win32.sendkey import auto, TextVK
from lib import utils
from commonstyle import dialog_style, styles
from ..gta_base.main import BaseGTATool
from ..gta_base.widgets import WeaponWidget
from . import address, models
from .data import SLOT_NO_AMMO, WEAPON_LIST, VEHICLE_LIST
from .models import Player, Vehicle
from .native import NativeContext
import math
import os
import json
import time
import __main__
import fefactory_api
ui = fefactory_api.ui


VERSION_101 = 0x831F7518
VERSION_102 = 0xC483FFE4
VERSION_103 = 0x280F0000
VERSION_104 = 0x110FF300
VERSION_105 = 0xf3385058
VERSION_106 = 0x00a42494
VERSION_106J = 0xda280f30
VERSION_107 = 0x1006e857
VERSION_EFLC1 = 0x0f14247c
VERSION_EFLC2 = 0x0d5c0ff3
VERSION_EFLC1R = 0x41110ff3
VERSION_RFG = 0x108b1874
VERSION_DR2 = 0x1B10044


class Tool(BaseGTATool):
    address = address
    models = models
    Player = Player
    Vehicle = Vehicle

    SAFE_SPEED_RATE = 15
    SAFE_SPEED_UP = 6
    jetPackSpeed = 3
    FLY_SPEED = 15

    def render(self):
        with self.render_win() as win:
            with ui.Vertical():
                with ui.Horizontal(className="expand container"):
                    ui.Button("检测", className="vcenter", onclick=self.checkAttach)
                    self.attach_status_view = ui.Text("", className="label_left grow")
                    ui.CheckBox("保持最前", onchange=self.swithKeeptop)
                with ui.Notebook(className="fill"):
                    self.render_main()

        win.setOnClose(self.onClose)

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
            for i in range(1, Player.WEAPON_SLOT):
                self.weapon_views.append(WeaponWidget("weapon%d" % i, "武器槽%d" % i, i, SLOT_NO_AMMO, WEAPON_LIST, self._player))

            ui.Button(label="一键最大", onclick=self.weapon_max)

        # with Group("global", "全局", 0, handler=self.handler):
        #     self.money_view = InputWidget("money", "金钱", address.MONEY, (), int)
            
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
                    ui.Text("附近车辆爆炸(使用秘籍BIGBANG): alt+enter")
        with Group(None, "测试", 0, handler=self.handler, flexgrid=False, hasfootbar=False):
            with ui.GridLayout(cols=4, vgap=10, className="fill container"):
                self.render_common_button()

        with Group(None, "工具", 0, flexgrid=False, hasfootbar=False):
            with ui.Vertical(className="fill container"):
                ui.Button("g3l坐标转json", onclick=self.g3l2json)

    def onClose(self, _=None):
        super().onClose()
        if self.handler.active:
            self.free_remote_function()

    def checkAttach(self, _=None):
        className = 'grcWindow'
        windowName = 'GTAIV'

        if self.handler.active:
            self.free_remote_function()
        else:
            # 确保重新生成 native_context
            self._playerins = None
            
        if self.handler.attachByWindowName(className, windowName):
            self.attach_status_view.label = windowName + ' 正在运行'
            self.MODULE_BASE = self.handler.base - 0x400000

            if not self.win.hotkeys:
                self.win.RegisterHotKeys((
                    ('jetPackTick', MOD_ALT, getVK('w'), self.jetPackTick),
                    ('jetPackTickLarge', MOD_ALT | MOD_SHIFT, getVK('w'), partial(self.jetPackTick, detal=4)),
                    ('jetPackTickSpeed', MOD_ALT, getVK('m'), partial(self.jetPackTick, useSpeed=True)),
                    ('raise_up', MOD_ALT, getVK(' '), self.raise_up),
                    ('go_down', MOD_ALT | MOD_SHIFT, getVK(' '), self.go_down),
                    ('to_up', MOD_ALT, getVK('.'), self.to_up),
                    ('stop', MOD_ALT, getVK('x'), self.stop),
                    ('restore_hp', MOD_ALT, getVK('h'), self.restore_hp),
                    ('restore_hp_large', MOD_ALT | MOD_SHIFT, getVK('h'), self.restore_hp_large),
                    # ('spawnVehicle', MOD_ALT, getVK('v'), self.spawnVehicle),
                    # ('spawnVehicleIdPrev', MOD_ALT, getVK('['), self.onSpawnVehicleIdPrev),
                    # ('spawnVehicleIdNext', MOD_ALT, getVK(']'), self.onSpawnVehicleIdNext),
                    ('jump_on_vehicle', MOD_ALT, getVK('j'), self.jump_on_vehicle),
                    ('near_persons_fly', MOD_ALT, getVK('f'), self.near_persons_fly),
                    ('near_fly', MOD_ALT | MOD_SHIFT, getVK('f'), self.near_fly),
                    ('vehicle_flip', MOD_ALT, getVK('k'), self.vehicle_flip),
                    ('near_vehicles_flip', MOD_ALT | MOD_SHIFT, getVK('k'), self.near_vehicles_flip),
                    ('move_near_vehicle_to_front', MOD_ALT, getVK('p'), partial(self.near_vehicles_to_front, zinc=2)),
                    ('move_near_person_to_front', MOD_ALT | MOD_SHIFT, getVK('p'), partial(self.near_persons_to_front, zinc=2.5)),
                    ('go_prev_pos', MOD_ALT | MOD_SHIFT, getVK(','), self.go_prev_pos),
                    ('go_next_pos', MOD_ALT | MOD_SHIFT, getVK('.'), self.go_next_pos),
                    ('max_cur_weapon', MOD_ALT, getVK('g'), self.max_cur_weapon),
                ))
            self.init_addr()
            self.init_remote_function()
        else:
            self.attach_status_view.label = '没有检测到 ' + windowName

    def get_addr(self, addr):
        return self.MODULE_BASE + addr

    def rel_addr(self, addr):
        return addr - self.MODULE_BASE

    def get_version(self):
        return self.handler.read32(self.get_addr(address.VERSION))

    def init_addr(self):
        version = self.get_version()
        if version == VERSION_104:
            address.PED_POOL     = self.get_addr(0x0175B77C)
            address.VEHICLE_POOL = self.get_addr(0x011F4F30)
            address.OBJECT_POOL  = self.get_addr(0x011FADD8)
            address.LOCAL_PLAYER_ID  = self.get_addr(0xEA68A8)
            address.PLAYER_INFO_ARRAY  = self.get_addr(0x1033058)
            # address.FindNativeAddress = self.get_addr(0x617280)
            address.SetMoveSpeed = 0 # TODO
        elif version == VERSION_107:
            address.PED_POOL     = self.get_addr(0x18A82AC)
            address.VEHICLE_POOL = self.get_addr(0x1619240)
            address.OBJECT_POOL  = self.get_addr(0x1350CE0)
            address.LOCAL_PLAYER_ID  = self.get_addr(0xF1CC68)
            address.PLAYER_INFO_ARRAY  = self.get_addr(0x11A7008)
            # address.FindNativeAddress = self.get_addr(0x5A76D0)
            address.SetMoveSpeed = self.get_addr(0xA47750)
            address.GetMoveSpeed = self.get_addr(0xA477F0)

            SPEED_FUNC = (
                b'\x55\x8B\xEC\x83\xEC\x08\x8B\x4D\x08\xC7\x45\xF8',
                b'\x8B\x41\x60\x89\x45\xFC\x8D\x41\x64\x89\x45\x08\xFF\x75\x08\x8B\x4D\xFC\xFF\x55\xF8\x8B\xE5\x5D\xC3'
            )
            self.FUNCTION_SET_SPEED = utils.u32bytes(address.SetMoveSpeed).join(SPEED_FUNC)
            self.FUNCTION_GET_SPEED = utils.u32bytes(address.GetMoveSpeed).join(SPEED_FUNC)

        # self.FUNCTION_FIND_NATIVE_ADDRESS = (
        #     b'\x55\x8B\xEC\x83\xEC\x08\x56\xC7\x45\xF8' + utils.u32bytes(address.FindNativeAddress) + 
        #     b'\xC7\x45\xFC\x00\x00\x00\x00\x56\x8B\x75\x08\xFF\x55\xF8\x5E\x89\x45\xFC\x8B\x45\xFC\x5E\x8B\xE5\x5D\xC3'
        # )

    def init_remote_function(self):
        # 现在Native方法对应的地址直接写在address.NATIVE_ADDRS中了
        # self.FindNativeAddress = self.handler.write_function(self.FUNCTION_FIND_NATIVE_ADDRESS)
        
        # TODO
        if address.SetMoveSpeed:
            self.SetMoveSpeed = self.handler.write_function(self.FUNCTION_SET_SPEED)
            self.GetMoveSpeed = self.handler.write_function(self.FUNCTION_GET_SPEED)

        # 初始化Native调用的参数环境
        context_addr = self.handler.alloc_memory(NativeContext.SIZE)
        self.native_context = NativeContext(context_addr, self.handler)

    def free_remote_function(self):
        # self.handler.free_memory(self.FindNativeAddress)
        if address.SetMoveSpeed:
            self.handler.free_memory(self.SetMoveSpeed)
            self.handler.free_memory(self.GetMoveSpeed)

        self.handler.free_memory(self.native_context.addr)
        self._playerins = None

    def native_call(self, name, arg_sign, *args, ret_type=int, ret_size=4):
        """ 远程调用GTAIV中的方法
        :param name: 方法名称，见address.NATIVE_ADDRS
        :param arg_sign: 函数签名
        """
        with self.native_context:
            fn_addr = self.get_addr(address.NATIVE_ADDRS[name])
            if arg_sign:
                self.native_context.push(arg_sign, *args)
            self.handler.remote_call(fn_addr, self.native_context.addr)
            if ret_type:
                return self.native_context.get_result(ret_type, ret_size)

    def _player(self):
        # player_addr = self.handler.read32(self.handler.read32(self.address.PLAYER_INFO_ARRAY) + 0x58C)
        # if player_addr is 0:
        #     return None
        player = getattr(self, '_playerins', None)
        player_index = self.get_player_id()

        if not player:
            player = self._playerins = self.Player(player_index, self.get_ped_index(player_index), self.native_call, self.native_context)
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

    # def get_player_index_of_pool(self):
    #     """获取当前ped在ped_pool中的index"""
    #     ped_addr = self.get_ped_addr()
    #     pool = self.ped_pool
    #     for i in range(pool.size):
    #         if pool.addr_at(i) == ped_addr:
    #             return i

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

    def get_persons(self):
        pool = self.ped_pool
        for i in range(pool.size):
            ped = pool[i]
            if ped.hp > 1:
                ped.index = i
                yield ped

    def get_near_persons(self, distance=100):
        """获取附近的人"""
        for ped in super().get_near_persons(distance):
            yield Player(0, self.ped_index_to_handle(ped.index), self.native_call, self.native_context)

    def get_vehicles(self):
        pool = self.vehicle_pool
        for i in range(pool.size):
            vehicle = pool[i]
            if vehicle.hp > 1:
                vehicle.index = i
                yield vehicle

    def get_near_vehicles(self, distance=100):
        """获取附近的载具"""
        for vehicle in super().get_near_vehicles(distance):
            yield Vehicle(self.vehicle_index_to_handle(vehicle.index), self.native_call, self.native_context)

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
        self.handler.write32(address.SPAWN_VEHICLE_ID_BASE, VEHICLE_LIST[lb.index][1])

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

    def set_ped_invincible(self, _=None):
        self.player.invincible = True

    def set_ped_block_switch_weapons(self, _=None):
        self.player.block_switch_weapons = False

    def set_ped_can_be_dragged_out_of_vehicle(self, _=None):
        self.player.can_be_dragged_out_of_vehicle = False

    def restore_hp(self, _=None):
        super().restore_hp()
        if self.isInVehicle:
            self.vehicle.engine_hp = 1000

    def max_cur_weapon(self, _=None):
        """当前武器子弹全满"""
        self.player.max_cur_ammo()

    def flash_weapon_icon(self):
        self.native_call('FLASH_WEAPON_ICON', 'L', 1, ret_type=None)

    def LoadEnvironmentNow(self, pos):
        self.native_call('REQUEST_COLLISION_AT_POSN', '3f', *pos)
        self.native_call('LOAD_ALL_OBJECTS_NOW', None)
        self.native_call('LOAD_SCENE', '3f', *pos)
        self.native_call('POPULATE_NOW', None)

    def GetGroundZ(self, pos, type=None):
        if type == 'highest' or type is None:
            self.native_call('GET_GROUND_Z_FOR_3D_COORD', '3fL', pos[0], pos[1], 1024.0, 
                self.native_context.get_temp_addr())
            return self.native_context.get_temp_value(float)
        elif type == 'nextBelowCurrent':
            self.native_call('GET_GROUND_Z_FOR_3D_COORD', '3fL', *pos, 
                self.native_context.get_temp_addr())
            return self.native_context.get_temp_value(float)