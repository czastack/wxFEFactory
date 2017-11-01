from lib.hack.model import Model, Field, CoordField, ModelField, ArrayField
from lib.lazy import lazy
from lib.utils import float32
from ..gta_base import utils
from ..gta_base.models import Physicle, Pool
from .data import COLOR_LIST
import math
import time


class NativeModel:
    def __init__(self, handle, mgr):
        self.handle = handle
        self.mgr = mgr

    @property
    def native_context(self):
        return self.mgr.native_context

    @property
    def native_call(self):
        return self.mgr.native_call

    @property
    def script_call(self):
        return self.mgr.script_call

    def getter(name, ret_type=int, ret_size=4):
        def getter(self):
            return self.native_call(name, 'Q', self.handle, ret_type=ret_type, ret_size=ret_size)
        return getter

    def getter_ptr(name, ret_type=int, ret_size=4):
        def getter(self):
            self.native_call(name, '2Q', self.handle, self.native_context.get_temp_addr())
            return self.native_context.get_temp_value(type=ret_type, size=ret_size)
        return getter

    def setter(name, type_=int):
        if type_ is int:
            s = 'Q'
        elif type_ is float:
            s = 'f'
        elif type_ is bool:
            s = '?'
        else:
            raise ValueError('not support type: ' + type_.__name__)
        def setter(self, value):
            self.native_call(name, 'Q' + s, self.handle, type_(value))
        return setter

    builders = (getter, getter_ptr, setter)


class NativeEntity(NativeModel):
    distance = Physicle.distance

    EXPLOSION_TYPE_GRENADE = 0
    EXPLOSION_TYPE_MOLOTOV = 1
    EXPLOSION_TYPE_ROCKET = 2
    EXPLOSION_TYPE_HI_OCTANE = 3
    EXPLOSION_TYPE_CAR = 4
    EXPLOSION_TYPE_PLANE = 5

    getter, getter_ptr, setter = NativeModel.builders

    # 朝向
    heading = property(getter('GET_ENTITY_HEADING', float), setter('SET_ENTITY_HEADING', float))
    # 无敌
    invincible = property(None, setter('SET_ENTITY_INVINCIBLE', bool))
    existed = property(getter('DOES_ENTITY_EXIST', bool))
    hp = property(getter('GET_ENTITY_HEALTH'))

    @hp.setter
    def hp(self, value):
        value = int(value)
        if value < 100:
            value = 100
        self.native_call('SET_ENTITY_HEALTH', '2Q', self.handle, value)

    @property
    def coord(self):
        self.native_call('GET_ENTITY_COORDS', 'Q', self.handle)
        values = self.native_context.get_vector_result(8)
        return utils.CoordData(self, values)

    @coord.setter
    def coord(self, value):
        pos = tuple(value)
        self.script_call('SET_ENTITY_COORDS', 'Q3f4Q', self.handle, *pos, True, True, True, False, sync=False)

    def get_offset_coord(self, offset):
        self.native_call('GET_OFFSET_FROM_ENTITY_IN_WORLD_COORDS', 'Q3f', self.handle, *offset)
        return self.native_context.get_vector_result(8)

    @property
    def speed(self):
        self.native_call('GET_ENTITY_VELOCITY', 'Q', self.handle)
        values = self.native_context.get_vector_result(8)
        return utils.VectorField(self, values, 'speed')

    @speed.setter
    def speed(self, value):
        self.native_call('SET_ENTITY_VELOCITY', 'Q3f', self.handle, *value)

    # model hash
    model_id = property(getter('GET_ENTITY_MODEL'))

    @property
    def model(self):
        return IVModel(self.model_id, self.mgr)

    # 是否能被破坏
    can_be_damaged = property(None, setter('SET_ENTITY_CAN_BE_DAMAGED', bool))
    is_on_fire = property(getter('IS_ENTITY_ON_FIRE', bool))

    def create_fire(self):
        self._fire = self.mgr.create_fire(self.coord)
        return self._fire

    def delete_fire(self):
        if hasattr(self, '_fire'):
            self.mgr.delete_fire(self._fire)

    def create_explosion(self, *args, **kwargs):
        self.mgr.create_explosion(self.coord, *args, **kwargs)

    @property
    def rotation(self):
        return utils.degreeToRadian(self.heading)

    @rotation.setter
    def rotation(self, value):
        self.heading = utils.radianToDegree(value)

    @property
    def direction(self):
        return utils.headingToDirection(self.heading)

    @property
    def quaternion(self):
        ctx = self.native_context
        self.native_call('GET_ENTITY_QUATERNION', '5Q', self.handle, *ctx.get_temp_addrs(1, 4))
        values = ctx.get_temp_values(1, 4, float, mapfn=float32)
        return utils.VectorField(self, values, 'quaternion')

    @quaternion.setter
    def quaternion(self, value):
        self.native_call('SET_ENTITY_QUATERNION', 'Q4f', self.handle, *value)

    @property
    def rotation3f(self):
        x, y, z, w = self.quaternion
        pitch = math.atan2(2.0 * (y*z + w*x), w*w - x*x - y*y + z*z)
        yaw   = math.atan2(2.0 * (x*y + w*z), w*w + x*x - y*y - z*z)
        roll  = math.asin(-2.0 * (x*z - w*y))

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

    def stop(self):
        self.speed = (0, 0, 0)

    def freeze_position(self, value=True):
        """冻结位置"""
        self.script_call('FREEZE_ENTITY_POSITION', '2Q', self.handle, value)

    def add_marker(self):
        """添加标记"""
        return Blip.add_blip_for_entity(self)

    def get_offset_coord_m(self, offset):
        """手动获取偏移后的坐标"""
        coord = self.coord.values()
        coord[0] += offset[0]
        coord[1] += offset[1]
        coord[2] += offset[2]
        return coord

    get_offset_coord = get_offset_coord_m

    del getter, getter_ptr, setter


class Player(NativeEntity):
    # SIZE = 0xf00
    WEAPON_SLOT = 13

    getter, getter_ptr, setter = NativeEntity.builders

    def __init__(self, index, handle, mgr):
        super().__init__(handle, mgr)
        self.index = index

    def player_getter(name, ret_type=int, ret_size=4):
        def getter(self):
            return self.native_call(name, 'Q', self.index, ret_type=ret_type, ret_size=ret_size)
        return getter

    def player_getter_ptr(name, ret_type=int, ret_size=4):
        def getter(self):
            self.native_call(name, '2Q', self.index, self.native_context.get_temp_addr())
            return self.native_context.get_temp_value(type=ret_type, size=ret_size)
        return getter

    def player_setter(name, type_=int):
        if type_ is int:
            s = 'Q'
        elif type_ is float:
            s = 'f'
        elif type_ is bool:
            s = '?'
        else:
            raise ValueError('not support type: ' + type_.__name__)
        def setter(self, value):
            self.native_call(name, 'Q' + s, self.index, value)
        return setter

    @property
    def ped_index(self):
        return self.handle >> 8

    @property
    def addr(self):
        return self.mgr.ped_pool.addr_at(self.ped_index)

    ap = property(getter('GET_PED_ARMOUR'), setter('SET_PED_ARMOUR'))
    max_health = property(getter('GET_PED_MAX_HEALTH'), setter('SET_PED_MAX_HEALTH'))
    max_armor = property(player_getter('GET_PLAYER_MAX_ARMOUR'), player_setter('SET_PLAYER_MAX_ARMOUR'))

    money = property(getter('GET_PED_MONEY'))

    @money.setter
    def money(self, value):
        value = int(value)
        self.native_call('SET_PED_MONEY', '2Q', self.handle, value)

    gravity = property(None, setter('SET_PED_GRAVITY', bool))
    # 不会被拽出车
    can_be_dragged_out_of_vehicle = property(None, setter('SET_PED_CAN_BE_DRAGGED_OUT', bool))

    # 通缉等级
    wanted_level = property(player_getter('GET_PLAYER_WANTED_LEVEL'))
    @wanted_level.setter
    def wanted_level(self, level):
        level = int(level)
        if level > 0:
            self.native_call('SET_PLAYER_WANTED_LEVEL', '2Q', self.index, level)
        else:
            self.native_call('CLEAR_PLAYER_WANTED_LEVEL', 'Q', self.index)
        self.script_call('SET_PLAYER_WANTED_LEVEL_NOW', 'Q', self.index, sync=False)

    isInVehicle = property(getter('IS_PED_IN_ANY_VEHICLE', bool, 1))
    # 被其他角色忽略
    ignored_by_everyone = player_setter('SET_EVERYONE_IGNORE_PLAYER', bool)
    # 不会从车上摔下来
    keep_bike = property(None, setter('SET_PED_CAN_BE_KNOCKED_OFF_VEHICLE', bool))

    get_vehicle_handle = getter('GET_VEHICLE_PED_IS_USING')

    def get_last_vehicle_handle(self):
        return self.native_call('GET_PLAYERS_LAST_VEHICLE', None)

    @property
    def vehicle(self):
        handle = self.get_vehicle_handle()
        if handle:
            return Vehicle(handle, self.mgr)

    @property
    def last_vehicle(self):
        handle = self.get_last_vehicle_handle()
        if handle:
            return Vehicle(handle, self.mgr)

    # ----------------------------------------------------------------------
    # 武器相关
    # ----------------------------------------------------------------------
    def give_weapon(self, weapon, ammo, equipNow=True):
        self.native_call('GIVE_WEAPON_TO_PED', '5Q', self.handle, weapon, ammo, 0, equipNow)

    def get_weapon_in_slot(self, slot):
        """获取指定武器槽中的武器种类"""
        return self.native_call('GET_PED_WEAPONTYPE_IN_SLOT', '2Q', self.handle, slot)

    def remove_all_weapons(self, toggle=True):
        """移除所有武器"""
        self.native_call('REMOVE_ALL_PED_WEAPONS', '2Q', self.handle, toggle)
        
    def get_ammo(self, weapon):
        """获取指定武器的弹药数"""
        ctx = self.native_context
        self.native_call('GET_AMMO_IN_CLIP', '3Q', self.handle, weapon, ctx.get_temp_addr())
        return ctx.get_temp_value()
        
    def set_ammo(self, weapon, ammo):
        """设置指定武器的弹药数"""
        self.native_call('SET_AMMO_IN_CLIP', '3Q', self.handle, weapon, ammo)

    def get_max_ammo(self, weapon):
        """获取指定武器的最大弹药数"""
        ctx = self.native_context
        self.native_call('GET_MAX_AMMO', '3Q', self.handle, weapon, ctx.get_temp_addr())
        return ctx.get_temp_value()

    def max_ammo(self):
        """全部武器弹药全满"""
        for i in range(2, 8):
            weapon = self.get_weapon_in_slot(i)
            if weapon:
                self.set_ammo(weapon, 9999)

    def max_cur_ammo(self):
        """当前武器子弹全满"""
        self.set_ammo(self.weapon, 9999)

    # 当前武器种类
    weapon = property(getter_ptr('GET_CURRENT_PED_WEAPON'))

    @weapon.setter
    def weapon(self, weapon):
        """设置当前武器种类"""
        self.native_call('SET_CURRENT_PED_WEAPON', '3Q', self.handle, weapon, 1)

    @lazy
    def weapons(self):
        return WeaponSet(self, self.WEAPON_SLOT)

    def explode_head(self):
        """爆头"""
        self.script_call('EXPLODE_PED_HEAD', 'Q', self.handle)

    def explode(self, *args, **kwargs):
        """爆炸"""
        self.create_explosion(*args, **kwargs)

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
        return self.ped.get_weapon_in_slot(self.slot), 0

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
    # SIZE = 0x20d0
    
    getter, getter_ptr, setter = NativeEntity.builders

    @property
    def index(self):
        return self.handle >> 8

    @property
    def addr(self):
        return self.mgr.vehicle_pool.addr_at(self.index)

    engine_hp = property(getter('GET_VEHICLE_ENGINE_HEALTH', float), setter('SET_VEHICLE_ENGINE_HEALTH', float))

    def __bool__(self):
        return self.existed and self.engine_hp > 0

    # 损坏等级？
    dirtyness = property(
        getter('GET_VEHICLE_DIRT_LEVEL', float),
        setter('SET_VEHICLE_DIRT_LEVEL', float)
    )

    # 前进速度
    forard_speed = property(getter('GET_ENTITY_SPEED', float))
    @forard_speed.setter
    def forard_speed(self, value):
        if self.model.is_train:
            self.native_call('SET_TRAIN_SPEED', 'Qf', self.handle, value)
            self.native_call('SET_TRAIN_CRUISE_SPEED', 'Qf', self.handle, value)
        else:
            self.native_call('SET_VEHICLE_FORWARD_SPEED', 'Qf', self.handle, value)

    door_status = property(getter('GET_VEHICLE_DOOR_LOCK_STATUS'), setter('SET_VEHICLE_DOORS_LOCKED'))

    def lock_door(self):
        """锁车门"""
        door_status = 2

    def unlock_door(self):
        self.door_status = 1

    @property
    def driver(self):
        ped_handle = self.native_call('GET_PED_IN_VEHICLE_SEAT', '2Q', self.handle, 0)
        return Player(0, ped_handle, self.mgr) if ped_handle else None

    @property
    def name(self):
        addr = self.native_call('GET_DISPLAY_NAME_FROM_VEHICLE_MODEL', 'Q', self.model_id)
        data = self.mgr.handler.read(addr, bytes, 16)
        return data[:data.find(b'\x00')].decode()

    @property
    def colors(self):
        ctx = self.native_context
        self.native_call('GET_CAR_COLOURS', '3Q', self.handle, ctx.get_temp_addr(1), ctx.get_temp_addr(2))
        return float32(ctx.get_temp_value(1)), float32(ctx.get_temp_value(2))

    @colors.setter
    def colors(self, value):
        self.native_call('SET_VEHICLE_COLOURS', '3Q', self.handle, *value)

    @property
    def ext_colors(self):
        ctx = self.native_context
        self.native_call('GET_VEHICLE_EXTRA_COLOURS', '3Q', self.handle, ctx.get_temp_addr(1), ctx.get_temp_addr(2))
        return float32(ctx.get_temp_value(1)), float32(ctx.get_temp_value(2))

    @colors.setter
    def ext_colors(self, value):
        self.native_call('SET_VEHICLE_EXTRA_COLOURS', '3Q', self.handle, *value)

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

    def fix(self):
        self.native_call('SET_VEHICLE_FIXED', 'Q', self.handle)

    def explode(self):
        """爆炸"""
        self.script_call('EXPLODE_VEHICLE', '3Q', self.handle, 1, 0)

    del getter, getter_ptr, setter


class IVModel(NativeModel):
    getter, getter_ptr, setter = NativeEntity.builders

    is_bike = property(getter("IS_THIS_MODEL_A_BIKE", bool))
    is_bicycle = property(getter("IS_THIS_MODEL_A_BICYCLE", bool))
    is_boat = property(getter("IS_THIS_MODEL_A_BOAT", bool))
    is_car = property(getter("IS_THIS_MODEL_A_CAR", bool))
    is_heli = property(getter("IS_THIS_MODEL_A_HELI", bool))
    is_plane = property(getter("IS_THIS_MODEL_A_PLANE", bool))
    is_train = property(getter("IS_THIS_MODEL_A_TRAIN", bool))
    loaded = property(getter('HAS_MODEL_LOADED', bool))

    def request(self):
        if self.loaded:
            return True

        self.script_call('REQUEST_MODEL', 'Q', self.handle)
        try_count = 20
        while try_count:
            time.sleep(0.1)
            if self.loaded:
                return True

            try_count -= 1

    def release(self):
        self.script_call('SET_MODEL_AS_NO_LONGER_NEEDED', 'Q', self.handle)

    del getter, getter_ptr, setter


class Blip(NativeModel):
    BLIP_DESTINATION = 0
    BLIP_DESTINATION_1 = 1
    BLIP_DESTINATION_2 = 2
    BLIP_WAYPOINT = 8
    BLIP_BOSS = 93

    BLIP_TYPE_CAR = 1
    BLIP_TYPE_CHAR = 2             # ENEMY
    BLIP_TYPE_OBJECT = 3
    BLIP_TYPE_COORD = 4
    BLIP_TYPE_CONTACT = 5          # FRIEND
    BLIP_TYPE_PICKUP = 6

    BLIP_COLOR_ENEMY = 0x4
    BLIP_COLOR_FRIEND = 0x9

    color = property(NativeModel.getter('GET_BLIP_COLOUR'), NativeModel.setter('SET_BLIP_COLOUR'))
    blipType = property(NativeModel.getter('GET_BLIP_INFO_ID_TYPE'))
    sprite = property(NativeModel.getter('GET_BLIP_SPRITE'))
    existed = property(NativeModel.getter('DOES_BLIP_EXIST', bool))
    entity_index = property(NativeModel.getter('GET_BLIP_INFO_ID_ENTITY_INDEX'))
    pickup_index = property(NativeModel.getter('GET_BLIP_INFO_ID_PICKUP_INDEX'))
    
    def remove(self):
        self.script_call('REMOVE_BLIP', 'Q', self.handle, ret_type=None)

    @property
    def coord(self):
        ctx = self.native_context
        self.script_call('GET_BLIP_COORDS', 'Q', self.handle)
        return ctx.get_vector_result(8)

    @property
    def entity(self):
        blipType = self.blipType
        if blipType is self.BLIP_TYPE_CAR:
            return Vehicle(self.entity_index, self.mgr)
        elif blipType is self.BLIP_TYPE_CHAR:
            return Player(0, self.entity_index, self.mgr)

    @classmethod
    def add_blip_for_entity(cls, entity):
        return cls(entity.script_call('ADD_BLIP_FOR_ENTITY', '2L', entity.handle), entity.mgr)


class NativeRegistration(Model):
    nextRegistration = Field(0, size=8)
    handlers = ArrayField(8, 7, Field(0, size=8))
    numEntries = Field(0x40)
    hashes = ArrayField(0x48, 7, Field(0, size=8))

    def get_func(self, hash):
        registration = NativeRegistration(self.addr, self.handler)
        while registration.addr:
            for i in range(registration.numEntries):
                if hash == registration.hashes[i]:
                    return registration.handlers[i]
            registration.addr = registration.nextRegistration