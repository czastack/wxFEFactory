from functools import partial
from lib.hack.handlers import MemHandler
from lib.win32.keys import VK
from lib.win32.sendkey import auto, TextVK
from tools.native_hacktool import NativeHacktool
from .models import Pool
import math
import time
import traceback
import fefactory_api
ui = fefactory_api.ui


class BaseGTATool(NativeHacktool):
    RAISE_UP_SPEED = 1.0
    GO_DOWN_SPEED = 0.5
    TO_UP_DELTA = 10
    TO_DOWN_DELTA = 6

    def __init__(self):
        super().__init__()
        self.handler = MemHandler()

    def get_hotkeys(self):
        """重写这个函数，返回要注册的热键列表"""
        return self.get_common_hotkeys()

    def inputCheat(self, text):
        auto.sendKey(TextVK(text), 10)

    def _player(self):
        player_addr = self.handler.read32(self.address.PLAYER_PTR)
        if player_addr is 0:
            return None
        player = getattr(self, '_playerins', None)
        if not player:
            player = self._playerins = self.Player(player_addr, self)
        elif player.addr != player_addr:
            player.addr = player_addr
        return player

    def _vehicle(self):
        addr = self.handler.read32(self.address.VEHICLE_PTR)
        if addr >= self.vehicle_pool.start:
            return self.Vehicle(self.handler.read32(self.address.VEHICLE_PTR), self) or None

    player = property(_player)
    vehicle = property(_vehicle)

    @property
    def last_vehicle(self):
        return self.player.vehicle or self.vehicle

    @property
    def isInVehicle(self):
        """当前是否在乘车"""
        return self.player.isInVehicle

    @property
    def entity(self):
        """在车中则返回载具对象，否则返回角色对象"""
        return self.vehicle if self.isInVehicle else self.player

    @property
    def ped_pool(self):
        """角色池"""
        return self.models.Pool(self.address.PED_POOL, self, self.Player)

    @property
    def vehicle_pool(self):
        """载具池"""
        return self.models.Pool(self.address.VEHICLE_POOL, self, self.Vehicle)

    @property
    def object_pool(self):
        """物体池"""
        return self.models.Pool(self.address.OBJECT_POOL, self, self.models.Object)

    def get_yaw(self):
        """获取偏航角"""
        PI = math.pi
        HALF_PI = PI / 2
        yaw = self.player.rotation
        yaw += HALF_PI
        if yaw > PI:
            yaw += PI * 2
        return yaw

    def get_camera_rot(self):
        """获取摄像机朝向参数 (pitch, yaw, roll)"""
        yaw = self.get_yaw()
        return (math.cos(yaw), math.sin(yaw), 0.1)

    def get_front_coord(self, delta=5):
        """获取前面一点的坐标"""
        yaw = self.get_yaw()

        x = math.cos(yaw)
        y = math.sin(yaw)
        coord = self.player.coord.values()
        coord[0] += x * delta
        coord[1] += y * delta
        return coord

    def get_cam_front_coord(self, delta=5):
        """根据摄像机朝向获取前面一点的坐标"""
        rot = self.get_camera_rot()
        coord = self.player.coord.values()
        coord[0] += rot[0] * delta
        coord[1] += rot[1] * delta
        return coord

    def go_forward(self, _=None, rate=0):
        """前进"""
        rate = rate or self.GO_FORWARD_COORD_RATE

        yaw = self.get_yaw()
        x = math.cos(yaw)
        y = math.sin(yaw)

        entity = self.entity
        coord = entity.coord.values()
        coord[0] += x * rate
        coord[1] += y * rate

        entity.coord = coord

    def speed_up(self, _=None, rate=0):
        """弹射起步"""
        speed_rate = rate or getattr(self, 'SAFE_SPEED_RATE', 0.5)

        yaw = self.get_yaw()
        x = math.cos(yaw)
        y = math.sin(yaw)

        entity = self.entity
        speed = entity.speed.values()
        speed[0] += x * speed_rate
        speed[1] += y * speed_rate

        if not self.isInVehicle:
            safe_speed_up = getattr(self, 'SAFE_SPEED_UP', 0.2)
            speed[2] = safe_speed_up
            self.raise_up(speed=safe_speed_up)
            time.sleep(0.1)
        entity.speed = speed

    def raise_up(self, _=None, speed=0):
        """上天（有速度）"""
        self.entity.speed[2] = speed or self.RAISE_UP_SPEED

    def go_down(self, _=None, speed=0):
        """向下（有速度）"""
        self.entity.speed[2] = -(speed or self.GO_DOWN_SPEED)

    def to_up(self, _=None, delta=0):
        """往上（无速度）"""
        self.entity.coord[2] += delta or self.TO_UP_DELTA

    def to_down(self, _=None, delta=0):
        """向下（无速度）"""
        self.entity.coord[2] -= delta or self.TO_DOWN_DELTA

    def stop(self, _=None):
        """停止移动"""
        self.entity.stop()

    def restore_hp(self, _=None):
        """恢复HP"""
        if self.isInVehicle:
            self.vehicle.hp = 1000
            self.vehicle_fix(self.vehicle)
        else:
            self.player.hp = 200
            self.player.ap = 200

    def restore_hp_large(self, _=None):
        """恢复大量HP"""
        if self.isInVehicle:
            self.vehicle.hp = 2000
            self.vehicle_fix(self.vehicle)
        else:
            self.player.hp = 999
            self.player.ap = 999

    def vehicle_fix(self, vehicle):
        """修车"""
        pass

    def from_player_coord(self, btn):
        """车坐标从人坐标取值"""
        self.vehicle_coord_view.input_value = self.coord_view.input_value

    def from_vehicle_coord(self, btn):
        """人坐标从车坐标取值"""
        self.coord_view.input_value = self.vehicle_coord_view.input_value

    def go_prev_pos(self, _=None):
        """瞬移到上一处地点"""
        view = self.vehicle_coord_view if self.isInVehicle else self.coord_view
        view.listbox.prev()
        view.write()

    def go_next_pos(self, _=None):
        """瞬移到下一处地点"""
        view = self.vehicle_coord_view if self.isInVehicle else self.coord_view
        view.listbox.next()
        view.write()

    def iter_cam_dir_coords(self, count, space, first_double=False):
        """往视角方向迭代坐标
        :param first_double: 第一个坐标是否是双倍距离
        """
        cam_x, cam_y, cam_z = self.get_camera_rot()
        offset = (cam_x * space, cam_y * space, cam_z * space)
        coord = self.player.get_offset_coord_m(offset)
        if first_double:
            coord += offset

        for i in range(count):
            yield coord
            coord += offset

    def get_peds(self):
        """获取角色池中的角色列表"""
        return iter(self.ped_pool)

    def get_near_peds(self, distance=100):
        """获取附近的人"""
        coord = self.player.coord.values()
        myaddr = self.player.addr
        for p in self.get_peds():
            if p.hp > 0 and p.coord[2] > 0 and p.distance(coord) <= distance and p.addr != myaddr:
                yield p

    def get_vehicles(self):
        """载具池中的载具列表"""
        return iter(self.vehicle_pool)

    def get_near_vehicles(self, distance=100):
        """获取附近的载具"""
        coord = self.player.coord.values()
        mycar = self.vehicle
        myaddr = mycar.addr if mycar else 0
        for v in self.get_vehicles():
            if v.coord[2] > 0 and v.distance(coord) <= distance and v.addr != myaddr:
                yield v

    def collect_vehicles(self):
        """暂存附近的载具"""
        self._vehicles = self.get_near_vehicles()

    def next_collected_vehicle(self, is_retry=False, recollect=False):
        """获取下一辆暂存的载具"""
        vehicles = None if recollect else getattr(self, '_vehicles', None)
        flag = False
        if vehicles:
            try:
                if getattr(self, 'iter_vehicle_locked', False):
                    vehicle = getattr(self, 'last_iter_vehicle', None)
                    if vehicle:
                        flag = True

                if not flag:
                    vehicle = next(vehicles)
                    self.last_iter_vehicle = vehicle
                    flag = True
            except StopIteration:
                if is_retry:
                    # 大概是附近没有车了
                    return

        if not flag:
            self.collect_vehicles()
            return self.next_collected_vehicle(is_retry=True)

        return vehicle

    def iter_vehicle_lock(self, _=None):
        """锁住载具迭代（接下来只操作上一个返回的已收集载具）"""
        self.iter_vehicle_locked = not getattr(self, 'iter_vehicle_locked', False)

    def kill_near_peds(self, _=None):
        """杀死附近的人"""
        for p in self.get_near_peds():
            p.hp = 0

    def near_vehicles_boom(self, _=None):
        """摧毁附近的载具"""
        for v in self.get_near_vehicles():
            v.hp = 0

    def near_vehicles_down(self, _=None):
        """获取附近的载具下陷"""
        for v in self.get_near_vehicles():
            v.coord[2] -= 0.7

    def near_vehicles_to_front(self, _=None, zinc=0):
        """ 获取附近的载具移到眼前
        :param zinc: 下一个目标的z坐标增加
        """
        coord = self.get_front_coord()
        for p in self.get_near_vehicles():
            p.coord = coord
            if zinc:
                coord[2] += zinc

    def near_peds_to_front(self, _=None, zinc=0):
        """附近的人移到眼前"""
        coord = self.get_front_coord()
        for p in self.get_near_peds():
            p.coord = coord
            if zinc:
                coord[2] += zinc

    def jump_on_vehicle(self, _=None):
        """跳上附近的一辆行驶中的车"""
        for v in self.get_near_vehicles():
            if v.driver:
                v.stop()
                coord = v.coord.values()
                coord[2] += 1
                self.entity.coord = coord
                break

    def near_vehicles_flip(self, _=None):
        """附近的载具上下翻转"""
        for v in self.get_near_vehicles():
            v.flip()

    def near_vehicle_unlock(self, _=None):
        """附近的载具解锁"""
        for v in self.get_near_vehicles():
            v.unlock_door()

    def near_peds_fly(self, _=None):
        """附近的人上天"""
        fly_speed = getattr(self, 'FLY_SPEED', 1)
        for p in self.get_near_peds():
            p.speed[2] = fly_speed

    def near_vehicles_fly(self, _=None):
        """获取附近的载具上天"""
        fly_speed = getattr(self, 'FLY_SPEED', 1)
        for v in self.get_near_vehicles():
            v.coord[2] += fly_speed
            v.speed[2] = fly_speed

    def near_fly(self, _=None):
        """获取附近的人/载具上天"""
        self.near_peds_fly()
        self.near_vehicles_fly()

    def vehicle_flip(self, _=None):
        """当前的载具翻转"""
        self.last_vehicle.flip()

    def call_vehicle(self, _=None):
        """召唤上一辆车回来"""
        car = self.last_vehicle
        if car:
            car.coord = self.get_front_coord()

    def go_vehicle(self, _=None):
        """回到上一辆车旁边"""
        car = self.last_vehicle
        if car:
            coord = car.coord.values()
            coord[2] += 5
            self.player.coord = coord

    def bring_one_vehicle(self, _=None):
        """ 把一辆车移到眼前 """
        vehicle = self.next_collected_vehicle()

        if not vehicle:
            return

        cam_x, cam_y, cam_z = self.get_camera_rot()
        coord = self.player.coord.values()
        coord[0] += cam_x * 5
        coord[1] += cam_y * 5
        coord[2] += cam_z * 5
        vehicle.stop()
        vehicle.coord = coord

    def vehicle_lock_door(self, _=None, lock=True):
        """锁车门"""
        vehicle = self.last_vehicle
        if vehicle:
            if lock:
                vehicle.lock_door()
            else:
                vehicle.unlock_door()

    def vehicle_toggle_door(self, tb):
        """切换锁车状态"""
        self.vehicle_lock_door(lock=tb.checked)

    # ----------------------------------------------------------------------
    # MARKER
    # ----------------------------------------------------------------------
    def get_blips(self, color=None, types=None, sprite=None):
        """获取所有标记"""
        Marker = self.models.Marker
        addr = self.address.BLIP_LIST
        it = Marker(addr, self)

        for i in range(self.MARKER_RANGE):
            blipType = it.blipType
            if (it.blipType and (types is None or blipType in types) and (color is None or it.color is color)
                    and (sprite is None or it.sprite is sprite)):
                yield Marker(it.addr, self)
            it.next()

    def get_first_blip(self, *args, **kwargs):
        try:
            return next(self.get_blips(*args, **kwargs))
        except StopIteration:
            pass

    def get_target_blips(self, color=None, types=None, sprite=0):
        """获取目标的所有标记"""
        return self.get_blips(color, types or self.models.Marker.AVAILABLE_TYPE)

    def recal_markers(self, _=None):
        """重新获取人/车标记点"""
        self._markers = tuple(self.get_target_blips())
        self._marker_index = 0

    def go_next_marker(self, _=None):
        """到下一处 人/车标记点"""
        if not hasattr(self, '_markers'):
            self.recal_markers()

        while True:
            try:
                entity = self._markers[self._marker_index].entity
            except IndexError:
                self.recal_markers()
                return
            if entity:
                self.entity.coord = entity.coord
                break
            self._marker_index += 1

    def move_marker_to_front(self, _=None, zinc=0):
        """人/车标记点目标移到眼前"""
        if not hasattr(self, '_markers'):
            self.recal_markers()

        moved_car_addr = []
        coord = self.get_front_coord()

        for marker in self._markers:
            entity = marker.entity
            if isinstance(entity, self.Player):
                car = entity.vehicle
                if car and car.hp > 1:
                    if car.addr not in moved_car_addr:
                        moved_car_addr.append(car.addr)
                        car.coord = coord
                else:
                    entity.coord = coord
            elif isinstance(entity, self.Vehicle):
                entity.coord = coord
            if zinc:
                coord[2] += zinc

    def teleport_to_blip(self, blip):
        """瞬移到指定标记"""
        if blip:
            blipType = blip.blipType
            if blipType is self.models.Marker.MARKER_TYPE_COORDS:
                coord = blip.coord
            else:
                entity = blip.entity
                self.en = entity
                if entity:
                    coord = entity.coord
                else:
                    return False
            self.entity.coord = coord
            return True
        return False

    def teleport_to_destination(self, _=None, color=None, types=None):
        """瞬移到目的地"""
        Marker = self.models.Marker

        if color is None:
            color = getattr(self, '_last_dest_color', self.DEST_DEFAULT_COLOR)
        else:
            self._last_dest_color = color

        if types is None:
            types = (Marker.MARKER_TYPE_CAR, Marker.MARKER_TYPE_PED, Marker.MARKER_TYPE_COORDS)

        for blip in self.get_blips(color, types):
            if blip.sprite is 0:
                if self.teleport_to_blip(blip):
                    break

    def get_selected_vehicle_model(self):
        """获取刷车器选中的载具模型"""
        return getattr(self, 'spwan_vehicle_id', None)

    def spawn_choosed_vehicle(self, _=None, coord=None):
        """生成选中的载具"""
        model = self.get_selected_vehicle_model()
        if model:
            return self.spawn_vehicle(model, coord)

    def on_spawn_vehicle_id_change(self, lb):
        """刷车器listbox回调"""
        self.spwan_vehicle_id = self.VEHICLE_LIST[lb.index][1]

    def spawn_vehicle_id_prev(self, _=None):
        """选中上一个载具"""
        pos = self.spawn_vehicle_id_view.index
        if pos == 0:
            pos = len(self.VEHICLE_LIST)
        self.spawn_vehicle_id_view.setSelection(pos - 1, True)

    def spawn_vehicle_id_next(self, _=None):
        """选中下一个载具"""
        pos = self.spawn_vehicle_id_view.index
        if pos == len(self.VEHICLE_LIST) - 1:
            pos = -1
        self.spawn_vehicle_id_view.setSelection(pos + 1, True)

    def lock_door(self, _=None):
        """锁最近使用的载具的车门"""
        vehicle = self.last_vehicle
        if vehicle:
            vehicle.lock_door()

    def unlock_door(self, _=None):
        """解锁最近使用的载具的车门"""
        vehicle = self.last_vehicle
        if vehicle:
            vehicle.unlock_door()

    def launch_entity(self, entitys, need_set_coord=True):
        """朝前方发射载具"""
        if not hasattr(entitys, '__iter__'):
            entitys = (entitys,)

        for entity in entitys:
            cam_x, cam_y, cam_z = self.get_camera_rot()
            speed_rate = getattr(self, 'SLING_SPEED_RATE', 3)
            speed = (cam_x * speed_rate, cam_y * speed_rate, cam_z * speed_rate)
            if need_set_coord:
                coord_up = getattr(self, 'SLING_COORD_UP', 1)
                coord_delta = getattr(self, 'SLING_COORD_DELTA', 5)
                if self.isInVehicle:
                    coord_delta *= 1.5
                coord = self.player.coord.values()
                coord[0] += cam_x * coord_delta
                coord[1] += cam_y * coord_delta
                coord[2] += cam_z * coord_delta + coord_up
                entity.stop()
                entity.coord = coord
            entity.speed = speed

    def sling(self, _=None, recollect=False):
        """载具发射台"""
        vehicle = self.next_collected_vehicle(recollect=recollect)
        if vehicle:
            self.launch_entity(vehicle)
            self._last_launch_vehicle = vehicle

    def spawn_and_launch(self, _=None, recreate=False):
        """生产载具并发射"""
        vehicle = None
        if not recreate:
            vehicle = getattr(self, '_last_spawn_and_launch_vehicle', None)
        if not vehicle or vehicle.model_id != self.get_selected_vehicle_model():
            coord_delta = getattr(self, 'SLING_COORD_DELTA', 5)
            if self.isInVehicle:
                coord_delta *= 1.5
            vehicle = self.spawn_choosed_vehicle(coord=self.get_cam_front_coord(coord_delta))
            self._last_spawn_and_launch_vehicle = vehicle
        if vehicle:
            self.launch_entity(vehicle)
            self._last_launch_vehicle = vehicle

    def explode_last_launch_vehicle(self, _=None):
        """爆破上次发射的载具"""
        vehicle = getattr(self, '_last_launch_vehicle', None)
        if vehicle:
            vehicle.explode()

    def clear_wanted_level(self, _=None):
        """清除通缉等级"""
        self.set_wanted_level(0)

    def set_wanted_level(self, value):
        self.player.wanted_level = value

    def explode_art(self, _=None, count=10):
        """焰之炼金术 (向前生成数个爆炸)"""
        distance = (getattr(self, 'EXPLODE_DISTANCE_VEHICLE', 8) if self.isInVehicle
            else getattr(self, 'EXPLODE_DISTANCE', 6))
        for coord in self.iter_cam_dir_coords(count, distance, True):
            self.create_explosion(coord)

    def g3l2json(self, _=None):
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

    def render_common_button(self):
        ui.Button("杀掉附近的人", onclick=self.kill_near_peds)
        ui.Button("附近的车摧毁", onclick=self.near_vehicles_boom)
        ui.Button("附近的车下陷", onclick=self.near_vehicles_down)
        ui.Button("附近的车移到眼前", onclick=self.near_vehicles_to_front)
        ui.Button("附近的人移到眼前", onclick=self.near_peds_to_front)
        ui.Button("附近的车上天", onclick=self.near_vehicles_fly)
        ui.Button("附近的人上天", onclick=self.near_peds_fly)
        ui.Button("附近的车翻转", onclick=self.near_vehicles_flip)
        ui.Button("跳上一辆车", onclick=self.jump_on_vehicle)
        ui.Button("召唤上一辆车回来", onclick=self.call_vehicle)
        ui.Button("回到上一辆车旁边", onclick=self.go_vehicle)
        ui.Button("附近的载具解锁", onclick=self.near_vehicle_unlock)
        ui.Button("锁定载具迭代", onclick=self.iter_vehicle_lock)

    def render_common_text(self):
        ui.Text("生产选中的载具: alt+v")
        ui.Text("选中上一个载具: alt+[")
        ui.Text("选中下一个载具: alt+]")
        ui.Text("向前穿墙: alt+w")
        ui.Text("向前穿墙大: alt+shift+w")
        ui.Text("弹射起步: alt+m")
        ui.Text("上天（有速度）: alt+空格")
        ui.Text("往上（无速度）: alt+.")
        ui.Text("下坠: alt+shift+空格")
        ui.Text("停止移动: alt+x")
        ui.Text("恢复HP: alt+h")
        ui.Text("恢复大量HP: alt+shift+h")
        ui.Text("跳上一辆车: alt+j")
        ui.Text("附近的人上天: alt+f")
        ui.Text("附近的人和载具上天: alt+shift+f")
        ui.Text("自己的载具翻转: alt+k")
        ui.Text("附近的载具翻转: alt+shift+k")
        ui.Text("附近的人移到眼前: alt+shift+p")
        ui.Text("附近的载具移到眼前: alt+p")
        ui.Text("瞬移到上一个地点: alt+shift+,")
        ui.Text("瞬移到下一个地点: alt+shift+.")
        ui.Text("重新获取雷达上标记的目标: alt+'")
        ui.Text("瞬移到下一个标记目标处: alt+/")
        ui.Text("把获取到的标记目标移到眼前: alt+shift+/")
        ui.Text("上一辆车锁门: alt+l")
        ui.Text("上一辆车解锁: alt+shift+l")
        ui.Text("载具发射台(扫描附件的车，依次把一辆车发射出去): alt+d")
        ui.Text("载具发射台(重新扫描): alt+shift+d")
        ui.Text("生产载具并发射: alt+a")
        ui.Text("爆破上次发射的载具: alt+shift+a")
        ui.Text("把一辆车移到眼前: alt+b")
        ui.Text("清除通缉等级: alt+0")
        ui.Text("红莲之炼金术 (向前生成数个爆炸): alt+`")
        ui.Text("红莲之炼金术 (长): alt+shift+`")
        ui.Text("瞬移到目的地: alt+1")
        ui.Text("自定义临时热键(执行tool.cfn): alt+c")

    def get_common_hotkeys(self):
        return (
            (VK.MOD_ALT, VK.W, self.go_forward),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK.W, partial(self.go_forward, rate=10), 'go_forward_large'),
            (VK.MOD_ALT, VK.M, self.speed_up),
            (VK.MOD_ALT, VK.SPACE, self.raise_up),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK.SPACE, self.go_down),
            (VK.MOD_ALT, VK.getCode(','), self.to_up),
            (VK.MOD_ALT, VK.getCode('.'), self.to_down),
            (VK.MOD_ALT, VK.X, self.stop),
            (VK.MOD_ALT, VK.H, self.restore_hp),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK.H, self.restore_hp_large),
            (VK.MOD_ALT, VK.J, self.jump_on_vehicle),
            (VK.MOD_ALT, VK.F, self.near_peds_fly),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK.F, self.near_fly),
            (VK.MOD_ALT, VK.K, self.vehicle_flip),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK.K, self.near_vehicles_flip),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK.P, self.near_peds_to_front),
            (VK.MOD_ALT, VK.P, self.near_vehicles_to_front),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK.getCode(','), self.go_prev_pos),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK.getCode('.'), self.go_next_pos),
            (VK.MOD_ALT, VK.getCode("'"), self.recal_markers),
            (VK.MOD_ALT, VK.getCode('/'), self.go_next_marker),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK.getCode('/'), self.move_marker_to_front),
            (VK.MOD_ALT, VK.L, self.lock_door),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK.L, self.unlock_door),
            (VK.MOD_ALT, VK.D, self.sling),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK.D, partial(self.sling, recollect=True), 'resling'),
            (VK.MOD_ALT, VK.A, self.spawn_and_launch),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK.A, partial(self.spawn_and_launch, recreate=True), 'respawn_and_launch'),
            (VK.MOD_ALT, VK.Z, self.explode_last_launch_vehicle),
            (VK.MOD_ALT, VK.B, self.bring_one_vehicle),
            (VK.MOD_ALT, VK._0, self.clear_wanted_level),
            (VK.MOD_ALT, VK.getCode('`'), self.explode_art),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK.getCode('`'), partial(self.explode_art, count=24), 'explode_art_long'),
            (VK.MOD_ALT, VK.Q, partial(self.explode_art, count=1), 'explode_art_one'),
            (VK.MOD_ALT, VK._1, self.teleport_to_destination),
            (VK.MOD_ALT, VK.getCode('['), self.spawn_vehicle_id_prev),
            (VK.MOD_ALT, VK.getCode(']'), self.spawn_vehicle_id_next),
            (VK.MOD_ALT, VK.V, self.spawn_choosed_vehicle),
            (VK.MOD_ALT, VK.C, self.custom_hotkey),
        )
