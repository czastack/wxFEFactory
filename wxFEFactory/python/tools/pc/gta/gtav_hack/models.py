import math
import time
from lib.hack.models import Model, Field, CoordField, ArrayField
from lib.lazy import lazy
from lib.utils import float32, tuple2rgb, rgb2tuple
from ..gta_base import utils
from ..gta_base.models import Physicle, Pool, NativeModel64 as NativeModel


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
    # 是否能被破坏
    can_be_damaged = property(None, setter('SET_ENTITY_CAN_BE_DAMAGED', bool))
    existed = property(getter('DOES_ENTITY_EXIST', bool))
    hp = property(getter('GET_ENTITY_HEALTH'))
    height = property(getter('GET_ENTITY_HEIGHT_ABOVE_GROUND', float))
    # 是否悬空
    is_in_air = property(getter('IS_ENTITY_IN_AIR'))
    is_on_fire = property(getter('IS_ENTITY_ON_FIRE', bool))
    is_dead = property(getter('IS_ENTITY_DEAD', bool))
    is_ped = property(getter('IS_ENTITY_A_PED', bool))
    is_vehicle = property(getter('IS_ENTITY_A_VEHICLE', bool))
    is_object = property(getter('IS_ENTITY_AN_OBJECT', bool))

    # model hash
    model_id = property(getter('GET_ENTITY_MODEL'))

    @property
    def model(self):
        return VModel(self.model_id, self.context)

    @hp.setter
    def hp(self, value):
        value = int(value)
        if value < 100:
            value = 100
        self.native_call('SET_ENTITY_HEALTH', '2Q', self.handle, value)

    @property
    def coord(self):
        values = self.native_call_vector('GET_ENTITY_COORDS', 'Q', self.handle)
        return utils.CoordData(self, values)

    @coord.setter
    def coord(self, value):
        self.script_call('SET_ENTITY_COORDS', 'Q3f4Q', self.handle, *value, True, True, True, False)
        time.sleep(0.2)

    def get_offset_coord(self, offset):
        return self.native_call_vector('GET_OFFSET_FROM_ENTITY_IN_WORLD_COORDS', 'Q3f', self.handle, *offset)

    @property
    def speed(self):
        values = self.native_call_vector('GET_ENTITY_VELOCITY', 'Q', self.handle)
        return utils.VectorField(self, values, 'speed')

    @speed.setter
    def speed(self, value):
        self.script_call('SET_ENTITY_VELOCITY', 'Q3f', self.handle, *value)

    @property
    def turn_speed(self):
        values = self.native_call_vector('GET_ENTITY_ROTATION_VELOCITY', 'Q', self.handle)
        return utils.VectorField(self, values, 'turn_speed')

    @turn_speed.setter
    def turn_speed(self, value):
        # 结果还是speed...
        self.script_call('APPLY_FORCE_TO_ENTITY', '2Q6f6Q', self.handle, 3, *value,
            0, 0, 0, True, False, True, True, True, True)

    max_speed = property(None, setter('SET_ENTITY_MAX_SPEED', float))

    def start_fire(self):
        self.script_call('START_ENTITY_FIRE', 'Q', self.handle)

    def stop_fire(self):
        self.script_call('STOP_ENTITY_FIRE', 'Q', self.handle)

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
        return utils.degree_to_radian(self.heading)

    @rotation.setter
    def rotation(self, value):
        self.heading = utils.radian_to_degree(value)

    @property
    def direction(self):
        return utils.heading_to_direction(self.heading)

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
        return self.native_call_vector('GET_ENTITY_ROTATION', '2Q', self.handle, 2)

    @rotation3f.setter
    def rotation3f(self, value):
        self.native_call('SET_ENTITY_ROTATION', 'Q3f2Q', self.handle, *value, 2, True)

    def flip(self):
        """翻转"""
        x, y, z = self.rotation3f
        if y > 90 or y < -90:
            y = 0
        else:
            y = 180
        self.rotation3f = (x, y, z)

    def stop(self):
        self.speed = (0, 0, 0)
        # self.turn_speed = (0, 0, 0)

    def freeze_position(self, value=True):
        """冻结位置"""
        self.script_call('FREEZE_ENTITY_POSITION', '2Q', self.handle, value)

    def set_proofs(self, bp, fp, ep, cp, mp, un6, un7, dp):
        """设置实体的免疫 bulletProof, fireProof, explosionProof, collisionProof, meleeProof, p6, p7, drownProof"""
        self.native_call("SET_ENTITY_PROOFS", '9Q', self.handle,
            bp, fp, ep, cp, mp, un6, un7, dp)

    def add_marker(self):
        """添加标记"""
        return Blip.add_blip_for_entity(self)

    def get_offset_coord_m(self, offset):
        """手动获取偏移后的坐标"""
        coord = utils.Vector3(self.coord)
        coord += offset
        return coord

    get_offset_coord = get_offset_coord_m

    def go_to_entity(self, entity, speed=10):
        self.script_call('TASK_GO_TO_ENTITY', '2Ql3fl', self.handle, self.make_handle(entity),
            -1, 0.1, speed, 1073741824.0, 0)

    def attach_to_entity(self, entity, offset):
        """附上实体"""
        self.script_call('ATTACH_ENTITY_TO_ENTITY', '3Q6f6Q', self.handle, self.make_handle(entity), 0, *offset,
            0, 0, 0, False, True, True, True, 0, True)

    def detach_entity(self):
        self.script_call('DETACH_ENTITY', '3Q', self.handle, False, False)

    @property
    def entity_attached_to(self):
        entity = NativeEntity(self.native_call('GET_ENTITY_ATTACHED_TO', 'Q', self.handle), self.context)
        return entity.subtype_instance()

    def subtype_instance(self):
        if self.is_ped:
            return Player(0, self.handle, self.context)
        elif self.is_vehicle:
            return Vehicle(self.handle, self.context)
        elif self.is_object:
            return Object(self.handle, self.context)

    def fight_against(self, ped):
        self.script_call('TASK_COMBAT_PED', '4Q', self.handle, self.make_handle(ped), 0, 16)

    del getter, getter_ptr, setter


class Player(NativeEntity):
    WEAPON_SLOT = 13

    getter, getter_ptr, setter = NativeEntity.builders

    def __init__(self, index, handle, context):
        super().__init__(handle, context)
        self.index = index

    def player_getter(name, ret_type=int, ret_size=4):
        def _getter(self):
            return self.native_call(name, 'Q', self.index, ret_type=ret_type, ret_size=ret_size)
        return _getter

    def player_getter_ptr(name, ret_type=int, ret_size=4):
        def _getter(self):
            self.native_call(name, '2Q', self.index, self.native_context.get_temp_addr())
            return self.native_context.get_temp_value(type=ret_type, size=ret_size)
        return _getter

    def player_setter(name, type=int, default=None):
        if type is int:
            s = 'Q'
        elif type is float:
            s = 'f'
        elif type is bool:
            s = '?'
        else:
            raise ValueError('not support type: ' + type.__name__)
        if default is not None:
            def _setter(self, value=default):
                self.native_call(name, 'Q' + s, self.index, type(value))
        else:
            def _setter(self, value):
                self.native_call(name, 'Q' + s, self.index, type(value))
        return _setter

    @property
    def ped_index(self):
        return self.handle >> 8

    @property
    def addr(self):
        return self.context.ped_pool.addr_at(self.ped_index)

    is_player = property(getter('IS_PED_A_PLAYER'))
    type = property(getter('GET_PED_TYPE'))
    ap = property(getter('GET_PED_ARMOUR'), setter('SET_PED_ARMOUR'))
    max_health = property(getter('GET_PED_MAX_HEALTH'), setter('SET_PED_MAX_HEALTH'))
    max_armor = property(player_getter('GET_PLAYER_MAX_ARMOUR'), player_setter('SET_PLAYER_MAX_ARMOUR'))

    money = property(getter('GET_PED_MONEY'))

    @money.setter
    def money(self, value):
        value = int(value)
        self.native_call('SET_PED_MONEY', '2Q', self.handle, value)

    gravity = property(None, setter('SET_PED_GRAVITY', bool))
    # 能否被拽出车
    can_be_dragged_out_of_vehicle = property(None, setter('SET_PED_CAN_BE_DRAGGED_OUT', bool))
    # 能否在车中被射击
    can_be_shot_in_vehicle = property(None, setter('SET_PED_CAN_BE_SHOT_IN_VEHICLE', bool))

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

    def never_wanted(self, toggle):
        """不被通缉 只是把困难度调大"""
        if toggle:
            self.native_call('SET_WANTED_LEVEL_DIFFICULTY', 'Qf', self.index, 1000000)
        else:
            self.native_call('RESET_WANTED_LEVEL_DIFFICULTY', 'Q', self.index)

    in_vehicle = property(getter('IS_PED_IN_ANY_VEHICLE', bool, 1))
    # 被其他角色忽略
    ignored_by_everyone = player_setter('SET_EVERYONE_IGNORE_PLAYER', bool)
    # 被警察忽略
    ignored_by_police = player_setter('SET_POLICE_IGNORE_PLAYER', bool)
    # 变成敌人？
    set_as_enemy = player_setter('SET_PED_AS_ENEMY', bool)
    # 不会从车上摔下来
    keep_bike = property(None, setter('SET_PED_CAN_BE_KNOCKED_OFF_VEHICLE', bool))
    # 产生噪声比例 (默认1.0)
    noise_rate = property(None, player_setter('SET_PLAYER_NOISE_MULTIPLIER', float))
    # 射击比率
    shoot_rate = property(None, setter('SET_PED_SHOOT_RATE'))

    def _fast_run(self, toggle=True):
        """快速奔跑"""
        self.native_call('SET_RUN_SPRINT_MULTIPLIER_FOR_PLAYER', 'Qf', self.index, 1.49 if toggle else 1)

    def _fast_swim(self, toggle=True):
        """快速游泳"""
        self.native_call('SET_SWIM_MULTIPLIER_FOR_PLAYER', 'Qf', self.index, 1.49 if toggle else 1)

    fast_run = property(None, _fast_run)
    fast_swim = property(None, _fast_swim)

    def reset_skin(self):
        """使用初始衣服"""
        self.script_call('SET_PED_DEFAULT_COMPONENT_VARIATION', 'Q', self.handle)

    def reset_visible_damage(self):
        """修复可见损害"""
        self.native_call('RESET_PED_VISIBLE_DAMAGE', 'Q', self.handle)

    def set_model(self, model):
        """设置模型"""
        VModel(model, self.context).request()
        self.script_call('SET_PLAYER_MODEL', '2Q', self.index, model)
        self.script_call('SET_PED_DEFAULT_COMPONENT_VARIATION', 'Q', self.handle)

    create_fire = NativeEntity.start_fire
    stop_fire = NativeEntity.stop_fire

    # ----------------------------------------------------------------------
    # 载具相关
    # ----------------------------------------------------------------------

    get_vehicle_handle = getter('GET_VEHICLE_PED_IS_USING')

    def get_last_vehicle_handle(self):
        return self.native_call('GET_PLAYERS_LAST_VEHICLE', None)

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

    def into_vehicle(self, vehicle, seat=-1):
        """进入车辆"""
        self.script_call('TASK_WARP_PED_INTO_VEHICLE', '2Ql', self.handle, self.make_handle(vehicle), seat)

    def into_vehicle2(self, vehicle, seat=-1):
        """进入车辆"""
        self.script_call('SET_PED_INTO_VEHICLE', '2Ql', self.handle, self.make_handle(vehicle), seat)

    # ----------------------------------------------------------------------
    # 武器相关
    # ----------------------------------------------------------------------
    def give_weapon(self, weapon, ammo, equipNow=True):
        self.script_call('GIVE_WEAPON_TO_PED', '5Q', self.handle, weapon, ammo, 0, equipNow)

    def get_weapon_in_slot(self, slot):
        """获取指定武器槽中的武器种类"""
        return self.native_call('GET_PED_WEAPONTYPE_IN_SLOT', '2Q', self.handle, slot)

    def remove_weapon(self, weapon):
        """移除指定武器"""
        self.script_call('REMOVE_WEAPON_FROM_PED', '2Q', self.handle, weapon)

    def remove_all_weapons(self):
        """移除所有武器"""
        self.script_call('REMOVE_ALL_PED_WEAPONS', '2Q', self.handle, True)

    def get_ammo(self, weapon):
        """获取指定武器的弹药数"""
        return self.native_call('GET_AMMO_IN_PED_WEAPON', '2Q', self.handle, weapon)

    def set_ammo(self, weapon, ammo):
        """设置指定武器的弹药数"""
        self.native_call('SET_PED_AMMO', '3Q', self.handle, weapon, ammo)

    def get_max_ammo(self, weapon):
        """获取指定武器的最大弹药数"""
        ctx = self.native_context
        self.native_call('GET_MAX_AMMO', '3Q', self.handle, weapon, ctx.get_temp_addr())
        return ctx.get_temp_value(size=4)

    def has_weapon(self, weapon):
        return self.native_call('HAS_PED_GOT_WEAPON', '3Q', self.handle, weapon, 0)

    def max_ammo(self):
        """全部武器弹药全满"""
        for i in range(2, 8):
            weapon = self.get_weapon_in_slot(i)
            if weapon:
                self.set_ammo(weapon, 9999)

    def max_cur_ammo(self):
        """当前武器子弹全满"""
        self.set_ammo(self.weapon, 9999)

    def set_infinite_ammo(self, weapon, toggle=True):
        """无限弹药"""
        self.native_call('SET_PED_INFINITE_AMMO', '3Q', self.handle, weapon, toggle)

    # 全部武器无限弹药
    set_infinite_ammo_clip = setter('SET_PED_INFINITE_AMMO_CLIP')

    # 当前武器种类
    weapon = property(getter_ptr('GET_CURRENT_PED_WEAPON'))

    @weapon.setter
    def weapon(self, weapon):
        """设置当前武器种类"""
        self.script_call('SET_CURRENT_PED_WEAPON', '3Q', self.handle, weapon, 1)

    def get_vehicle_weapon(self):
        """当前车载武器种类"""
        self.script_call('GET_CURRENT_PED_VEHICLE_WEAPON', '2Q', self.handle, self.native_context.get_temp_addr())
        return self.native_context.get_temp_value(size=4)

    def set_vehicle_weapon(self, weapon):
        """设置当前车载武器种类"""
        self.script_call('SET_CURRENT_PED_VEHICLE_WEAPON', '2Q', self.handle, weapon)

    vehicle_weapon = property(get_vehicle_weapon, set_vehicle_weapon)

    def give_weapon_component(self, weapon, component):
        self.script_call('GIVE_WEAPON_COMPONENT_TO_PED', '3Q', self.handle, weapon, component)

    def remove_weapon_component(self, weapon, component):
        self.script_call('REMOVE_WEAPON_COMPONENT_FROM_PED', '3Q', self.handle, weapon, component)

    def explode_head(self):
        """爆头"""
        self.script_call('EXPLODE_PED_HEAD', '2Q', self.handle, 0x1B06D571)

    def explode(self, *args, **kwargs):
        """爆炸"""
        self.create_explosion(*args, **kwargs)

    def clear_tasks(self):
        """清除任务"""
        self.script_call('CLEAR_PED_TASKS', 'Q', self.handle)

    def clear_tasks_now(self):
        """清除任务，会下车"""
        self.script_call('CLEAR_PED_TASKS_IMMEDIATELY', 'Q', self.handle)

    def chase(self, entity):
        """追捕目标"""
        self.script_call('TASK_VEHICLE_CHASE', '2Q', self.handle, entity)

    def get_bone_coord(self, bone_id):
        """获取角色身体部分的坐标"""
        bone_index = self.native_call('GET_PED_BONE_INDEX', '2Q', self.handle, bone_id)
        values = self.native_call_vector('GET_WORLD_POSITION_OF_ENTITY_BONE', '2Q', self.handle, bone_index)
        return utils.Vector3(values)

    @property
    def head_coord(self):
        return self.get_bone_coord(12844)  # IK_Head

    def follow_to_entity(self, entity, speed=2, timeout=-1):
        """跟着实体"""
        self.script_call('TASK_FOLLOW_TO_OFFSET_OF_ENTITY', '2Q4flfq',
            self.handle, self.make_handle(entity), 1.5, 1.5, 1.5, speed, timeout, 2, 1)

    def go_straight_to_coord(self, coord, speed=2, timeout=-1):
        """径直走向坐标"""
        self.script_call('TASK_GO_STRAIGHT_TO_COORD', 'Q4fl2f',
            self.handle, *coord, speed, timeout, 0, 0)

    def parachute_to(self, coord):
        """降落到坐标"""
        self.script_call('TASK_PARACHUTE_TO_TARGET', 'Q3f', self.handle, *coord)

    def reset_stamina(self):
        self.script_call('RESET_PLAYER_STAMINA', 'Q', self.index)

    stamina = property(player_getter('GET_PLAYER_SPRINT_STAMINA_REMAINING', float),
        player_setter('RESTORE_PLAYER_STAMINA', float))

    del getter, getter_ptr, setter


class Vehicle(NativeEntity):
    getter, getter_ptr, setter = NativeEntity.builders

    @property
    def index(self):
        return self.handle >> 8

    @property
    def addr(self):
        return self.context.vehicle_pool.addr_at(self.index)

    vehicle_class = property(getter('GET_VEHICLE_CLASS'))
    engine_hp = property(getter('GET_VEHICLE_ENGINE_HEALTH', float), setter('SET_VEHICLE_ENGINE_HEALTH', float))

    def __bool__(self):
        return self.existed and self.engine_hp > 0

    tyres_can_burst = property(None, setter('SET_VEHICLE_TYRES_CAN_BURST'))
    wheels_can_break = property(None, setter('SET_VEHICLE_WHEELS_CAN_BREAK'))
    can_be_visibly_damaged = property(None, setter('SET_VEHICLE_CAN_BE_VISIBLY_DAMAGED'))
    has_strong_axles = property(None, setter('SET_VEHICLE_HAS_STRONG_AXLES'))

    # 车身脏的程度
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
        ped_handle = self.native_call('GET_PED_IN_VEHICLE_SEAT', 'Ql', self.handle, -1)
        return Player(0, ped_handle, self.context) if ped_handle else None

    @property
    def name(self):
        addr = self.native_call('GET_DISPLAY_NAME_FROM_VEHICLE_MODEL', 'Q', self.model_id)
        data = self.context.handler.read(addr, bytes, 16)
        return data[:data.find(b'\x00')].decode()

    @property
    def colors(self):
        ctx = self.native_context
        self.native_call('GET_VEHICLE_COLOURS', '3Q', self.handle, ctx.get_temp_addr(1), ctx.get_temp_addr(2))
        return ctx.get_temp_value(1), ctx.get_temp_value(2)

    @colors.setter
    def colors(self, value):
        self.native_call('SET_VEHICLE_COLOURS', '3Q', self.handle, *value)

    @property
    def ext_colors(self):
        ctx = self.native_context
        self.native_call('GET_VEHICLE_EXTRA_COLOURS', '3Q', self.handle, ctx.get_temp_addr(1), ctx.get_temp_addr(2))
        return ctx.get_temp_value(1), ctx.get_temp_value(2)

    @ext_colors.setter
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

    # 自定义颜色1
    is_primary_color_custom = property(getter("GET_IS_VEHICLE_PRIMARY_COLOUR_CUSTOM", bool))

    @property
    def custom_primary_color(self):
        ctx = self.native_context
        self.native_call('GET_VEHICLE_CUSTOM_PRIMARY_COLOUR', '4Q', self.handle, *ctx.get_temp_addrs(1, 4))
        return tuple2rgb(tuple(ctx.get_temp_values(1, 4, size=4)))

    @custom_primary_color.setter
    def custom_primary_color(self, rgb):
        rgbtuple = rgb2tuple(rgb)
        self.script_call('SET_VEHICLE_CUSTOM_PRIMARY_COLOUR', '4Q', self.handle, *rgbtuple)

    @custom_primary_color.deleter
    def custom_primary_color(self):
        self.script_call('CLEAR_VEHICLE_CUSTOM_PRIMARY_COLOUR', 'Q', self.handle)

    # 自定义颜色2
    is_secondary_color_custom = property(getter("GET_IS_VEHICLE_SECONDARY_COLOUR_CUSTOM", bool))

    @property
    def custom_secondary_color(self):
        ctx = self.native_context
        self.native_call('GET_VEHICLE_CUSTOM_SECONDARY_COLOUR', '4Q', self.handle, *ctx.get_temp_addrs(1, 4))
        return tuple2rgb(tuple(ctx.get_temp_values(1, 4, size=4)))

    @custom_secondary_color.setter
    def custom_secondary_color(self, rgb):
        rgbtuple = rgb2tuple(rgb)
        self.script_call('SET_VEHICLE_CUSTOM_SECONDARY_COLOUR', '4Q', self.handle, *rgbtuple)

    @custom_secondary_color.deleter
    def custom_secondary_color(self):
        self.script_call('CLEAR_VEHICLE_CUSTOM_SECONDARY_COLOUR', 'Q', self.handle)

    def fix(self):
        """修车"""
        self.script_call('SET_VEHICLE_FIXED', 'Q', self.handle)

    def wash(self):
        """洗车"""
        self.dirtyness = 0
        self.fix()

    def explode(self):
        """爆炸"""
        self.script_call('EXPLODE_VEHICLE', '3Q', self.handle, 1, 0)

    def set_invincible(self, toggle=True):
        """设置是否不可损坏"""
        not_toggle = not toggle
        self.invincible = toggle
        self.set_proofs(toggle, toggle, toggle, toggle, toggle, toggle, toggle, toggle)
        self.tyres_can_burst = not_toggle
        self.wheels_can_break = not_toggle
        self.can_be_damaged = not_toggle
        self.can_be_visibly_damaged = not_toggle

    def drive_to(self, coord, speed, driving_style):
        """驾驶到坐标"""
        self.script_call('TASK_VEHICLE_DRIVE_TO_COORD', '2Q4fl2Q2f',
            self.driver.handle, self.handle, *coord, speed, 1, self.model_id, driving_style, 10.0, -1.0)

    def drive_follow(self, entity, speed, driving_style):
        """跟着目标"""
        self.script_call('_TASK_VEHICLE_FOLLOW', '3Qf2Q',
            self.driver.handle, self.handle, self.make_handle(entity), speed, driving_style, 10)

    def clear_driver_tasks(self):
        """停止自动驾驶"""
        self.driver.clear_tasks()

    def chase(self, entity):
        """追捕目标"""
        self.driver.chase(self.make_handle(entity))

    def out_of_control(self, killDriver=False, explodeOnImpact=False):
        self.native_call('SET_VEHICLE_OUT_OF_CONTROL', '3Q', self.handle, killDriver, explodeOnImpact)

    del getter, getter_ptr, setter


class Object(NativeEntity):
    def place_on_ground(self):
        return self.script_call('PLACE_OBJECT_ON_GROUND_PROPERLY', 'Q', self.handle)


class VModel(NativeModel):
    getter, getter_ptr, setter = NativeEntity.builders

    is_bike = property(getter("IS_THIS_MODEL_A_BIKE", bool))
    is_bicycle = property(getter("IS_THIS_MODEL_A_BICYCLE", bool))
    is_boat = property(getter("IS_THIS_MODEL_A_BOAT", bool))
    is_car = property(getter("IS_THIS_MODEL_A_CAR", bool))
    is_heli = property(getter("IS_THIS_MODEL_A_HELI", bool))
    is_plane = property(getter("IS_THIS_MODEL_A_PLANE", bool))
    is_train = property(getter("IS_THIS_MODEL_A_TRAIN", bool))
    loaded = property(getter('HAS_MODEL_LOADED', bool))
    is_in_cdimage = property(getter('IS_MODEL_IN_CDIMAGE', bool))
    is_valid = property(getter('IS_MODEL_VALID', bool))

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

    def get_dimensions(self):
        ctx = self.native_context
        self.native_call('GET_MODEL_DIMENSIONS', '3Q', self.handle, ctx.get_temp_addr(6), ctx.get_temp_addr(3))
        v0 = ctx.get_temp_values(3, 1, float, mapfn=float32)
        v1 = ctx.get_temp_values(6, 4, float, mapfn=float32)
        return utils.Vector3(v0), utils.Vector3(v1)

    del getter, getter_ptr, setter


class Blip(NativeModel):
    BLIP_CIRCLE = 1
    BLIP_COP = 3
    BLIP_WAYPOINT = 8
    BLIP_COPHELICOPTER = 15

    BLIP_TYPE_CAR = 1
    BLIP_TYPE_CHAR = 2
    BLIP_TYPE_OBJECT = 3
    BLIP_TYPE_COORD = 4
    BLIP_TYPE_CONTACT = 5
    BLIP_TYPE_PICKUP = 6

    BLIP_COLOR_NONE = 0x0
    BLIP_COLOR_RED = 0x1
    BLIP_COLOR_GREEN = 0x2
    BLIP_COLOR_BLUE = 0x3
    BLIP_COLOR_PLAYER = 0x4
    BLIP_COLOR_YELLOWMISSION = 0x5
    BLIP_COLOR_FRIENDLYVEHICLE = 0x26
    BLIP_COLOR_MICHAEL = 0x2A
    BLIP_COLOR_FRANKLIN = 0x2B
    BLIP_COLOR_TREAVOR = 0x2C
    BLIP_COLOR_REDMISSION = 0x31
    BLIP_COLOR_MISSIONVEHICLE = 0x36
    BLIP_COLOR_REDMISSION2 = 0x3B
    BLIP_COLOR_YELLOWMISSION2 = 0x3C
    BLIP_COLOR_MISSION = 0x42
    BLIP_COLOR_WAYPOINT = 0x53

    BLIP_COLORS_ENEMY = (BLIP_COLOR_RED, BLIP_COLOR_REDMISSION)
    BLIP_COLORS_FRIEND = (BLIP_COLOR_BLUE, BLIP_COLOR_REDMISSION)

    color = property(NativeModel.getter('GET_BLIP_COLOUR'), NativeModel.setter('SET_BLIP_COLOUR'))
    hud_color = property(NativeModel.getter('GET_BLIP_HUD_COLOUR'))
    blip_type = property(NativeModel.getter('GET_BLIP_INFO_ID_TYPE'))
    sprite = property(NativeModel.getter('GET_BLIP_SPRITE'))
    existed = property(NativeModel.getter('DOES_BLIP_EXIST', bool))
    entity_index = property(NativeModel.getter('GET_BLIP_INFO_ID_ENTITY_INDEX'))
    pickup_index = property(NativeModel.getter('GET_BLIP_INFO_ID_PICKUP_INDEX'))

    def remove(self):
        self.script_call('REMOVE_BLIP', 'Q', self.handle, ret_type=None)

    @property
    def coord(self):
        values = self.native_call_vector('GET_BLIP_COORDS', 'Q', self.handle)
        return utils.CoordData(self, values)

    @coord.setter
    def coord(self, value):
        self.script_call('SET_BLIP_COORDS', 'Q3f', self.handle, *value)

    @property
    def entity(self):
        blip_type = self.blip_type
        if blip_type is self.BLIP_TYPE_CAR:
            return Vehicle(self.entity_index, self.context)
        elif blip_type is self.BLIP_TYPE_CHAR:
            return Player(0, self.entity_index, self.context)

    @classmethod
    def add_blip_for_entity(cls, entity):
        return cls(entity.script_call('ADD_BLIP_FOR_ENTITY', '2L', entity.handle), entity.context)

    def show_number(self, number):
        """显示数字"""
        self.native_call('SHOW_NUMBER_ON_BLIP', 'Ql', self.handle, number)

    def hide_number(self, number):
        """隐藏数字"""
        self.native_call('HIDE_NUMBER_ON_BLIP', 'Ql', self.handle, number)
