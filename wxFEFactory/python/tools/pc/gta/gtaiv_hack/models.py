import math
import time
from lib.hack.models import Model, Field, CoordField, ManagedModelPtrField
from lib.lazy import lazy
from lib.utils import float32
from ..gta_base import utils
from ..gta_base.models import Physicle, Pool, NativeModel


class Pos(Model):
    grad = CoordField(0)
    looking = CoordField(0x10)
    coord = CoordField(0x30)


class Entity(Physicle):
    # speed = CoordField(0x78)
    # weight = Field(0xc0, float)
    model_id = Field(0x2e, int, 2)

    @property
    def pos(self):
        return Pos(self.handler.read32(self.addr + 0x20), self.handler)

    @property
    def coord(self):
        return self.pos.coord

    @coord.setter
    def coord(self, value):
        self.pos.coord = value


class MemVehicle(Entity):
    SIZE = 0x20d0

    hp = Field(0x200, float)
    engine_hp = Field(0x10FC, float)
    roll = CoordField(0x04)
    dir = CoordField(0x14)
    numPassengers = Field(0x1c8, int, 1)
    maxPassengers = Field(0x1cc, int, 1)
    door_status = Field(0x224, int, 1)
    flags = Field(0x1f5, int, 1)
    primaryColor = Field(0x19c, int, 1)
    secondaryColor = Field(0x19d, int, 1)
    type = Field(0x284, int, 4)


class MemPlayer(Entity):
    SIZE = 0xf00

    hp = Field(0x1f0, float)
    ap = Field(0x2c4, float)
    rotation = Field(0x2dc, float)
    isInVehicle = Field(0x314, bool, 1)
    cur_weapon = Field(0x504, int)
    vehicle = ManagedModelPtrField(0x310, MemVehicle)
    cur_weapon_slop = Field(0x498, int, 1)


class MemObject(Entity):
    SIZE = 0x320


class NativeEntity(NativeModel):
    distance = Physicle.distance

    @property
    def speed(self):
        values = self.context.get_move_speed(self.addr)
        return utils.VectorField(self, values, 'speed')

    @speed.setter
    def speed(self, value):
        self.context.set_move_speed(self.addr, value)

    @property
    def turn_speed(self):
        values = self.context.get_move_turn_speed(self.addr)
        return utils.VectorField(self, values, 'turn_speed')

    @turn_speed.setter
    def turn_speed(self, value):
        self.context.set_move_speed(self.addr, value)

    def create_fire(self):
        self._fire = self.context.create_fire(self.coord)
        return self._fire

    def delete_fire(self):
        if hasattr(self, '_fire'):
            self.context.delete_fire(self._fire)

    def create_explosion(self, *args, **kwargs):
        self.context.create_explosion(self.coord, *args, **kwargs)

    @property
    def rotation(self):
        return utils.degreeToRadian(self.heading)

    @rotation.setter
    def rotation(self, value):
        self.heading = utils.radianToDegree(value)

    @property
    def direction(self):
        return utils.headingToDirection(self.heading)

    def stop(self):
        self.speed = (0, 0, 0)

    def get_offset_coord_m(self, offset):
        """手动获取偏移后的坐标"""
        coord = utils.Vector3(self.coord)
        coord += offset
        return coord

    get_offset_coord = get_offset_coord_m


class Player(NativeEntity):
    WEAPON_SLOT = 13

    getter, getter_ptr, setter = NativeModel.builders

    def __init__(self, index, handle, context):
        super().__init__(handle, context)
        self.index = index

    def player_getter(name, ret_type=int, ret_size=4):
        def getter(self):
            return self.native_call(name, 'L', self.index, ret_type=ret_type, ret_size=ret_size)
        return getter

    def player_getter_ptr(name, ret_type=int, ret_size=4):
        def getter(self):
            self.native_call(name, '2L', self.index, self.native_context.get_temp_addr())
            return self.native_context.get_temp_value(type=ret_type, size=ret_size)
        return getter

    def player_setter(name, type=int):
        if type is int:
            s = 'L'
        elif type is float:
            s = 'f'
        elif type is bool:
            s = '?'
        else:
            raise ValueError('not support type: ' + type.__name__)

        def setter(self, value):
            self.native_call(name, 'L' + s, self.index, value)

        return setter

    @property
    def ped_index(self):
        return self.handle >> 8

    @property
    def addr(self):
        return self.context.ped_pool.addr_at(self.ped_index)

    @property
    def memobj(self):
        return MemPlayer(self.addr, self.context)

    existed = property(getter('DOES_CHAR_EXIST', bool))
    hp = property(getter_ptr('GET_CHAR_HEALTH'), setter('SET_CHAR_HEALTH'))
    ap = property(getter_ptr('GET_CHAR_ARMOUR'), setter('ADD_ARMOUR_TO_CHAR'))
    max_health = property(None, player_getter_ptr('INCREASE_PLAYER_MAX_HEALTH'))
    max_armor = property(None, player_getter_ptr('INCREASE_PLAYER_MAX_ARMOUR'))
    # 射击比率
    shoot_rate = property(None, setter('SET_CHAR_SHOOT_RATE'))

    money = property(player_getter_ptr('STORE_SCORE'))

    @money.setter
    def money(self, value):
        value = int(value)
        if value < 0:
            value = 0
        else:
            value -= self.money
        self.native_call('ADD_SCORE', '2L', self.index, value)

    gravity = property(getter('GET_CHAR_GRAVITY', float), setter('SET_CHAR_GRAVITY', float))
    # 朝向
    heading = property(getter_ptr('GET_CHAR_HEADING', float), setter('SET_CHAR_HEADING', float))
    # 无敌
    invincible = property(None, setter('SET_CHAR_INVINCIBLE', bool))
    # 限制切换武器
    block_switch_weapons = property(None, setter('BLOCK_PED_WEAPON_SWITCHING', bool))
    # 不会被拽出车
    can_be_dragged_out_of_vehicle = property(None, setter('SET_CHAR_CANT_BE_DRAGGED_OUT', bool))

    # 通缉等级
    wanted_level = property(player_getter_ptr('STORE_WANTED_LEVEL'))

    @wanted_level.setter
    def wanted_level(self, level):
        level = int(level)
        if level > 0:
            self.native_call('ALTER_WANTED_LEVEL', '2L', self.index, level)
        else:
            self.native_call('CLEAR_WANTED_LEVEL', 'L', self.index)
        self.script_call('APPLY_WANTED_LEVEL_CHANGE_NOW', 'L', self.index, sync=False)

    isInVehicle = property(getter('IS_CHAR_IN_ANY_CAR', bool, 1))
    # 被其他角色忽略
    ignored_by_everyone = player_setter('SET_EVERYONE_IGNORE_PLAYER', bool)
    # 不会累
    never_gets_tired = player_setter('SET_PLAYER_NEVER_GETS_TIRED', bool)
    # 不会从摩托车上摔下来
    keep_bike = property(None, setter('SET_CHAR_CAN_BE_KNOCKED_OFF_BIKE', bool))

    @property
    def coord(self):
        ctx = self.native_context
        self.native_call('GET_CHAR_COORDINATES', '4L', self.handle, *ctx.get_temp_addrs(1, 3))
        values = ctx.get_temp_values(1, 3, float, mapfn=float32)
        return utils.CoordData(self, values)

    @coord.setter
    def coord(self, value):
        pos = tuple(value)
        self.script_call('SET_CHAR_COORDINATES', 'L3f', self.handle, *pos, sync=False)

    def get_offset_coord(self, offset):
        self.native_call('GET_OFFSET_FROM_CHAR_IN_WORLD_COORDS', 'L3f3L',
            self.handle, *offset, *self.native_context.get_temp_addrs(1, 3))
        return self.native_context.get_temp_values(1, 3, float, mapfn=float32)

    get_vehicle_handle = getter_ptr('GET_CAR_CHAR_IS_USING')

    def get_last_vehicle_handle(self):
        self.native_call('GET_PLAYERS_LAST_CAR_NO_SAVE', 'L', self.native_context.get_temp_addr())
        return self.native_context.get_temp_value()

    @property
    def vehicle(self):
        handle = self.get_vehicle_handle()
        if handle:
            return Vehicle(handle, self.context)

    @property
    def last_vehicle(self):
        handle = self.get_last_vehicle_handle()
        if handle:
            return Vehicle(handle, self.context)

    def reset_visible_damage(self):
        """修复可见损害"""
        self.native_call('RESET_VISIBLE_PED_DAMAGE', 'Q', self.handle)

    # ----------------------------------------------------------------------
    # 武器相关
    # ----------------------------------------------------------------------
    def give_weapon(self, weapon, ammo):
        self.native_call('GIVE_WEAPON_TO_CHAR', '4L', self.handle, weapon, ammo, 0)

    def get_weapon_in_slot(self, slot):
        """获取指定武器槽中的武器种类和弹药数"""
        ctx = self.native_context
        self.native_call('GET_CHAR_WEAPON_IN_SLOT', '5L', self.handle, slot,
            ctx.get_temp_addr(1), ctx.get_temp_addr(2), ctx.get_temp_addr(3))
        return (
            ctx.get_temp_value(1),  # weapon_type
            ctx.get_temp_value(2),  # ammo
        )

    def remove_all_weapons(self):
        """移除所有武器"""
        self.native_call('REMOVE_ALL_CHAR_WEAPONS', 'L', self.handle)

    def get_ammo(self, weapon):
        """获取指定武器的弹药数"""
        ctx = self.native_context
        self.native_call('GET_AMMO_IN_CHAR_WEAPON', '3L', self.handle, weapon, ctx.get_temp_addr())
        return ctx.get_temp_value()

    def set_ammo(self, weapon, ammo):
        """设置指定武器的弹药数"""
        self.native_call('SET_CHAR_AMMO', '3L', self.handle, weapon, ammo)

    def get_max_ammo(self, weapon):
        """获取指定武器的最大弹药数"""
        ctx = self.native_context
        self.native_call('GET_MAX_AMMO', '3L', self.handle, weapon, ctx.get_temp_addr())
        return ctx.get_temp_value()

    def max_ammo(self):
        """全部武器弹药全满"""
        for i in range(2, 8):
            weapon, ammo = self.get_weapon_in_slot(i)
            if weapon:
                self.set_ammo(weapon, 9999)

    def max_cur_ammo(self):
        """当前武器子弹全满"""
        self.set_ammo(self.weapon, 9999)

    # 当前武器种类"
    weapon = property(getter_ptr('GET_CURRENT_CHAR_WEAPON'))

    @weapon.setter
    def weapon(self, weapon):
        """设置当前武器种类"""
        self.native_call('SET_CURRENT_CHAR_WEAPON', '3L', self.handle, weapon, 1)

    @lazy
    def weapons(self):
        return WeaponSet(self, self.WEAPON_SLOT)

    def explode_head(self):
        """爆头"""
        self.script_call('EXPLODE_CHAR_HEAD', 'L', self.handle)

    def explode(self, *args, **kwargs):
        """爆炸"""
        self.create_explosion(*args, **kwargs)

    def add_marker(self):
        """添加标记"""
        return Blip.add_blip_for_char(self)

    def freeze_position(self, value=True):
        """冻结位置"""
        self.script_call('FREEZE_CHAR_POSITION', '2L', self.handle, value)

    def clear_tasks(self):
        """清除任务"""
        self.script_call('CLEAR_CHAR_TASKS', 'L', self.handle)

    def clear_tasks_now(self):
        """清除任务，会下车"""
        self.script_call('CLEAR_CHAR_TASKS_IMMEDIATELY', 'L', self.handle)

    def attach_to_object(self, obj):
        """附上一个物体"""
        self.script_call('ATTACH_PED_TO_OBJECT', '3L5f2L',
            self.handle, self.make_handle(obj), 0, -2.5, 0.0, 0, 0, 0, 0, 0)

    def attach_to_vehicle(self, vehicle):
        """附上一辆车"""
        self.script_call('ATTACH_PED_TO_CAR', '3L5f2L',
            self.handle, self.make_handle(vehicle), 0, -2.5, 0.0, 0, 0, 0, 1, 1)

    def create_fire(self):
        self._fire = self.script_call('START_CHAR_FIRE', 'L', self.handle)
        return self._fire

    del getter, getter_ptr, setter


class WeaponSet:
    def __init__(self, ped, size):
        self.ped = ped
        self.size = size

    def __getitem__(self, i):
        if i < 0 or i >= self.size:
            print("not available i")
            return
        return WeaponItem(self.ped, i)

    def __setitem__(self, i, item):
        if i < 0 or i >= self.size:
            print("not available i")
            return
        self[i].set(item)


class WeaponItem:
    def __init__(self, ped, slot):
        self.ped = ped
        self.slot = slot

    @property
    def data(self):
        return self.ped.get_weapon_in_slot(self.slot)

    @property
    def id(self):
        return self.data[0]

    @property
    def ammo(self):
        return self.data[1]

    @ammo.setter
    def ammo(self, ammo):
        self.ped.set_ammo(self.id, ammo)

    def set(self, other):
        if isinstance(other, WeaponItem):
            # self.id = other.id
            # self.ammo = other.ammo
            id = other.id
            ammo = other.ammo
        elif isinstance(other, (tuple, list)):
            # self.id, self.ammo = other
            id, ammo = other

        self.ped.give_weapon(id, ammo)


class Vehicle(NativeEntity):
    getter, getter_ptr, setter = NativeModel.builders

    @property
    def index(self):
        return self.handle >> 8

    @property
    def addr(self):
        return self.context.vehicle_pool.addr_at(self.index)

    @property
    def memobj(self):
        return MemVehicle(self.addr, self.context)

    hp = property(getter_ptr('GET_CAR_HEALTH'), setter('SET_CAR_HEALTH'))
    engine_hp = property(getter('GET_ENGINE_HEALTH', float), setter('SET_ENGINE_HEALTH', float))
    heading = property(getter_ptr('GET_CAR_HEADING', float), setter('SET_CAR_HEADING', float))
    model_id = property(getter_ptr('GET_CAR_MODEL'))

    @property
    def model(self):
        return IVModel(self.model_id, self.context)

    existed = property(getter('DOES_VEHICLE_EXIST', bool))

    def __bool__(self):
        return self.existed and self.engine_hp > 0

    is_freeze = property(None, setter('FREEZE_CAR_POSITION', bool))
    can_be_damaged = property(None, setter('SET_CAR_CAN_BE_DAMAGED', bool))
    # 损坏等级？
    dirtyness = property(
        getter_ptr('GET_VEHICLE_DIRT_LEVEL', float),
        setter('SET_VEHICLE_DIRT_LEVEL', float)
    )

    # 前进速度
    forard_speed = property(getter_ptr('GET_CAR_SPEED', float))

    @forard_speed.setter
    def forard_speed(self, value):
        if self.model.is_train:
            self.native_call('SET_TRAIN_SPEED', 'Lf', self.handle, value)
            self.native_call('SET_TRAIN_CRUISE_SPEED', 'Lf', self.handle, value)
        else:
            self.native_call('SET_CAR_FORWARD_SPEED', 'Lf', self.handle, value)

    @property
    def coord(self):
        ctx = self.native_context
        self.native_call('GET_CAR_COORDINATES', '4L', self.handle, *ctx.get_temp_addrs(1, 3))
        values = ctx.get_temp_values(1, 3, float, mapfn=float32)
        return utils.CoordData(self, values)

    @coord.setter
    def coord(self, value):
        pos = tuple(value)
        mycar = self.context.player.get_vehicle_handle()
        if self.handle == mycar:
            self.script_call('SET_CAR_COORDINATES', 'L3f', self.handle, *pos, sync=False)
        else:
            self.native_call('SET_CAR_COORDINATES', 'L3f', self.handle, *pos)

    @property
    def quaternion(self):
        ctx = self.native_context
        self.native_call('GET_VEHICLE_QUATERNION', '5L', self.handle, *ctx.get_temp_addrs(1, 4))
        values = ctx.get_temp_values(1, 4, float, mapfn=float32)
        return utils.VectorField(self, values, 'quaternion')

    @quaternion.setter
    def quaternion(self, value):
        self.native_call('SET_VEHICLE_QUATERNION', 'L4f', self.handle, *value)

    @property
    def rotation3f(self):
        x, y, z, w = self.quaternion
        pitch = math.atan2(2.0 * (y * z + w * x), w * w - x * x - y * y + z * z)
        yaw = math.atan2(2.0 * (x * y + w * z), w * w + x * x - y * y - z * z)
        roll = math.asin(-2.0 * (x * z - w * y))

        return utils.VectorField(self, (pitch, roll, yaw), 'rotation3f')

    @rotation3f.setter
    def rotation3f(self, value):
        self.quaternion = utils.Quaternion.from_rotation(utils.Vector3(value))

    def flip(self):
        """翻转"""
        x, y, z = self.rotation3f
        x = -x
        y = -y
        self.rotation3f = (x, y, z)

    is_on_fire = property(getter('IS_CAR_ON_FIRE', bool))

    door_status = property(getter_ptr('GET_CAR_DOOR_LOCK_STATUS'), setter('LOCK_CAR_DOORS'))

    def lock_door(self):
        """锁车门"""
        door_status = 2

    def unlock_door(self):
        self.door_status = 1

    @property
    def driver(self):
        self.native_call('GET_DRIVER_OF_CAR', '2L', self.handle, self.native_context.get_temp_addr())
        ped_handle = self.native_context.get_temp_value()
        return Player(0, ped_handle, self.context) if ped_handle else None

    @property
    def name(self):
        addr = self.native_call('GET_DISPLAY_NAME_FROM_VEHICLE_MODEL', 'L', self.model_id)
        data = self.context.handler.read(addr, bytes, 16)
        return data[:data.find(b'\x00')].decode()

    @property
    def colors(self):
        ctx = self.native_context
        self.native_call('GET_CAR_COLOURS', '3L', self.handle, ctx.get_temp_addr(1), ctx.get_temp_addr(2))
        return float32(ctx.get_temp_value(1)), float32(ctx.get_temp_value(2))

    @colors.setter
    def colors(self, value):
        self.native_call('CHANGE_CAR_COLOUR', '3L', self.handle, *value)

    @property
    def ext_colors(self):
        ctx = self.native_context
        self.native_call('GET_EXTRA_CAR_COLOURS', '3L', self.handle, ctx.get_temp_addr(1), ctx.get_temp_addr(2))
        return float32(ctx.get_temp_value(1)), float32(ctx.get_temp_value(2))

    @colors.setter
    def ext_colors(self, value):
        self.native_call('SET_EXTRA_CAR_COLOURS', '3L', self.handle, *value)

    @property
    def color(self):
        c1, c2 = self.colors
        return c1

    @color.setter
    def color(self, value):
        c1, c2 = self.colors
        c1 = value
        self.colors = c1, c2

    @property
    def specular_color(self):
        c1, c2 = self.colors
        return c2

    @specular_color.setter
    def specular_color(self, value):
        c1, c2 = self.colors
        c2 = value
        self.colors = c1, c2

    @property
    def feature_color1(self):
        c1, c2 = self.ext_colors
        return c1

    @feature_color1.setter
    def feature_color1(self, value):
        c1, c2 = self.ext_colors
        c1 = value
        self.ext_colors = c1, c2

    @property
    def feature_color2(self):
        c1, c2 = self.ext_colors
        return c2

    @feature_color2.setter
    def feature_color2(self, value):
        c1, c2 = self.ext_colors
        c2 = value
        self.ext_colors = c1, c2

    def wash(self):
        self.dirtyness = 0
        self.native_call('WASH_VEHICLE_TEXTURES', '2L', self.handle, 255)

    def fix(self):
        self.script_call('FIX_CAR', 'L', self.handle)

    def explode(self):
        """爆炸"""
        self.script_call('EXPLODE_CAR', '3L', self.handle, 1, 0)

    def add_marker(self):
        """添加标记"""
        return Blip.add_blip_for_car(self)

    def freeze_position(self, value=True):
        """冻结位置"""
        self.script_call('FREEZE_CAR_POSITION', '2L', self.handle, value)

    def drive_to(self, coord, speed):
        """驾驶到坐标"""
        self.script_call('TASK_CAR_DRIVE_TO_COORD', '2Q4f3lfl',
            self.driver.handle, self.handle, *coord, speed, 1, 0, 0, 10.0, -1)

    def clear_driver_tasks(self):
        """停止自动驾驶"""
        self.driver.clear_tasks()

    def attach_to_object(self, obj):
        """附上一个物体"""
        self.script_call('ATTACH_PED_TO_OBJECT', '3L6f', self.handle, self.make_handle(obj), 0, -2.5, 0.0, 0, 0, 0, 0)

    def attach_to_vehicle(self, vehicle):
        """附上一辆车"""
        self.script_call('ATTACH_PED_TO_CAR', '3L6f', self.handle, self.make_handle(vehicle), 0, -2.5, 0.0, 0, 0, 0, 0)

    del getter, getter_ptr, setter


class Object(NativeEntity):

    invincible = property(None, NativeModel.setter('SET_OBJECT_INVINCIBLE', bool))
    dynamic = property(None, NativeModel.setter('SET_OBJECT_DYNAMIC', bool))
    stealable = property(None, NativeModel.setter('SET_OBJECT_AS_STEALABLE', bool))
    collision = property(None, NativeModel.setter('SET_OBJECT_COLLISION', bool))
    hp = property(NativeModel.getter_ptr('GET_OBJECT_HEALTH', float), NativeModel.setter('SET_OBJECT_HEALTH', float))
    heading = property(NativeModel.getter_ptr('GET_CAR_HEADING', float), NativeModel.setter('SET_CAR_HEADING', float))

    @property
    def coord(self):
        ctx = self.native_context
        self.native_call('GET_OBJECT_COORDINATES', '4L', self.handle, *ctx.get_temp_addrs(1, 3))
        values = ctx.get_temp_values(1, 3, float, mapfn=float32)
        return utils.CoordData(self, values)

    @coord.setter
    def coord(self, value):
        pos = tuple(value)
        self.script_call('SET_OBJECT_COORDINATES', 'L3f', self.handle, *pos, sync=False)

    def freeze_position(self, value=True):
        """冻结位置"""
        self.script_call('FREEZE_OBJECT_POSITION', '2L', self.handle, value)


class IVModel(NativeModel):
    getter, getter_ptr, setter = NativeModel.builders

    is_bike = property(getter("IS_THIS_MODEL_A_BIKE", bool))
    is_boat = property(getter("IS_THIS_MODEL_A_BOAT", bool))
    is_car = property(getter("IS_THIS_MODEL_A_CAR", bool))
    is_heli = property(getter("IS_THIS_MODEL_A_HELI", bool))
    is_ped = property(getter("IS_THIS_MODEL_A_PED", bool))
    is_plane = property(getter("IS_THIS_MODEL_A_PLANE", bool))
    is_train = property(getter("IS_THIS_MODEL_A_TRAIN", bool))
    is_vehicle = property(getter("IS_THIS_MODEL_A_VEHICLE", bool))
    loaded = property(getter('HAS_MODEL_LOADED', bool))
    is_in_cdimage = property(getter('IS_MODEL_IN_CDIMAGE', bool))

    def request(self):
        if self.loaded:
            return True

        self.script_call('REQUEST_MODEL', 'L', self.handle)
        try_count = 20
        while try_count:
            time.sleep(0.1)
            if self.loaded:
                return True

            try_count -= 1

    def release(self):
        self.script_call('MARK_MODEL_AS_NO_LONGER_NEEDED', 'L', self.handle)

    del getter, getter_ptr, setter


class Blip(NativeModel):
    BLIP_DESTINATION = 0
    BLIP_DESTINATION_1 = 1
    BLIP_DESTINATION_2 = 2
    BLIP_WAYPOINT = 8
    BLIP_COP_CAR = 68
    BLIP_COP_CHOPPER = 73

    BLIP_TYPE_CAR = 1
    BLIP_TYPE_CHAR = 2             # ENEMY
    BLIP_TYPE_OBJECT = 3
    BLIP_TYPE_COORD = 4
    BLIP_TYPE_CONTACT = 5          # FRIEND
    BLIP_TYPE_PICKUP = 6

    BLIP_COLOR_ENEMY = 0x4
    BLIP_COLOR_FRIEND = 0x9

    color = property(NativeModel.getter_ptr('GET_BLIP_COLOUR'), NativeModel.setter('CHANGE_BLIP_COLOUR'))
    blipType = property(NativeModel.getter('GET_BLIP_INFO_ID_TYPE'))
    sprite = property(NativeModel.getter('GET_BLIP_SPRITE'))
    existed = property(NativeModel.getter('DOES_BLIP_EXIST', bool))
    car_index = property(NativeModel.getter('GET_BLIP_INFO_ID_CAR_INDEX'))
    ped_index = property(NativeModel.getter('GET_BLIP_INFO_ID_PED_INDEX'))
    object_index = property(NativeModel.getter('GET_BLIP_INFO_ID_OBJECT_INDEX'))
    pickup_index = property(NativeModel.getter('GET_BLIP_INFO_ID_PICKUP_INDEX'))
    is_short_range = property(NativeModel.getter('IS_BLIP_SHORT_RANGE'))

    def remove(self):
        self.script_call('REMOVE_BLIP', 'L', self.handle, ret_type=None)

    @property
    def coord(self):
        ctx = self.native_context
        self.script_call('GET_BLIP_COORDS', '2L', self.handle, ctx.get_temp_addr(3), ret_type=None)
        return ctx.get_temp_values(3, 1, float, mapfn=float32)

    @property
    def entity(self):
        blipType = self.blipType
        if blipType is self.BLIP_TYPE_CAR:
            return Vehicle(self.car_index, self.context)
        elif blipType is self.BLIP_TYPE_CHAR:
            return Player(0, self.ped_index, self.context)

    @classmethod
    def add_blip_for_car(cls, vehicle):
        vehicle.script_call('ADD_BLIP_FOR_CAR', '2L', vehicle.handle, vehicle.native_context.get_temp_addr())
        return cls(vehicle.native_context.get_temp_value(), vehicle.context)

    @classmethod
    def add_blip_for_char(cls, ped):
        ped.script_call('ADD_BLIP_FOR_CHAR', '2L', ped.handle, ped.native_context.get_temp_addr())
        return cls(ped.native_context.get_temp_value(), ped.context)
