from functools import partial
from fefactory_api.emuhacker import ProcessHandler
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
from lib.win32.sendkey import auto, TextVK
from commonstyle import styles
from ..tool import BaseTool
from .models import Pool
import math
import time
import fefactory_api
import fefactory_api
ui = fefactory_api.ui

win_style = {
    # 'width': 680,
    # 'height': 920,
    'width': 640,
    'height': 700,
}


class BaseGTATool(BaseTool):
    def __init__(self):
        super().__init__()
        self.handler = ProcessHandler()

    def attach(self):
        self.render()
        self.checkAttach()

    def render_win(self):
        menubar = self.render_menu()
        self.win = ui.HotkeyWindow(self.doGetTitle(), style=win_style, styles=styles, menuBar=menubar)
        self.win.position = (70, 4)
        return self.win

    def swithKeeptop(self, cb):
        self.win.keeptop = cb.checked

    def inputCheat(self, text):
        auto.sendKey(TextVK(text), 10)

    def _player(self):
        player_addr = self.handler.read32(self.address.PLAYER_PTR)
        if player_addr is 0:
            return None
        player = getattr(self, '_playerins', None)
        if not player:
            player = self._playerins = self.Player(player_addr, self.handler)
        elif player.addr != player_addr:
            player.addr = player_addr
        return player

    def _vehicle(self):
        return self.Vehicle(self.handler.read32(self.address.VEHICLE_PTR), self.handler)

    player = property(_player)
    vehicle = property(_vehicle)

    @property
    def isInVehicle(self):
        return self.player.isInVehicle

    @property
    def entity(self):
        return self.vehicle if self.isInVehicle else self.player

    @property
    def ped_pool(self):
        return self.models.Pool(self.address.PED_POOL, self.handler, self.Player)

    @property
    def vehicle_pool(self):
        return self.models.Pool(self.address.VEHICLE_POOL, self.handler, self.Vehicle)

    def get_rotz(self):
        PI = math.pi
        HALF_PI = PI / 2
        rotz = self.rot_view.mem_value
        rotz += HALF_PI
        if rotz > PI:
            rotz += PI * 2
        return rotz

    def go_forward(self, _=None, rate=0):
        rate = rate or self.GO_FORWARD_COORD_RATE
        
        rotz = self.get_rotz()
        xVal = math.cos(rotz)
        yVal = math.sin(rotz)

        entity = self.entity
        coord = entity.coord.values()
        coord[0] += xVal * rate
        coord[1] += yVal * rate
        
        entity.coord = coord

    def speed_up(self, _=None, rate=0):
        """弹射起步"""
        speed_rate = rate or getattr(self, 'SAFE_SPEED_RATE', 0.5)

        rotz = self.get_rotz()
        xVal = math.cos(rotz)
        yVal = math.sin(rotz)

        entity = self.entity
        speed = entity.speed.values()
        speed[0] += xVal * speed_rate
        speed[1] += yVal * speed_rate

        if not self.isInVehicle:
            safe_speed_up = getattr(self, 'SAFE_SPEED_UP', 0.2)
            speed[2] = safe_speed_up
            self.raise_up(speed=safe_speed_up)
            time.sleep(0.1)
        entity.speed = speed

    def raise_up(self, _=None, speed=1.0):
        self.entity.speed[2] = speed

    def go_down(self, _=None, speed=0.5):
        self.entity.speed[2] = -speed

    def to_up(self, _=None):
        self.entity.coord[2] += 10

    def to_down(self, _=None):
        self.entity.coord[2] -= 6

    def stop(self, _=None):
        speed_view = self.vehicle_speed_view if self.isInVehicle else self.speed_view
        speed_view.mem_value = (0, 0, 0)

    def restore_hp(self, _=None):
        if self.isInVehicle:
            self.vehicle_hp_view.mem_value = 2000
        else:
            self.hp_view.mem_value = 200

    def restore_hp_large(self, _=None):
        if self.isInVehicle:
            self.vehicle_hp_view.mem_value = 2000
        else:
            self.hp_view.mem_value = 999
            self.ap_view.mem_value = 999

    def from_player_coord(self, btn):
        self.vehicle_coord_view.input_value = self.coord_view.input_value

    def from_vehicle_coord(self, btn):
        self.coord_view.input_value = self.vehicle_coord_view.input_value

    def go_prev_pos(self, _=None):
        view = self.vehicle_coord_view if self.isInVehicle else self.coord_view
        view.listbox.prev()
        view.write()

    def go_next_pos(self, _=None):
        view = self.vehicle_coord_view if self.isInVehicle else self.coord_view
        view.listbox.next()
        view.write()

    def get_front_coord(self):
        """获取前面一点的坐标"""
        rotz = self.get_rotz()

        xVal = math.cos(rotz)
        yVal = math.sin(rotz)
        coord = self.player.coord.values()
        coord[0] += xVal * 5
        coord[1] += yVal * 5
        return coord

    def get_persons(self):
        pool = Pool(self.address.PED_POOL, self.handler, self.Player)
        return iter(pool)

    def get_near_persons(self, distance=100):
        """获取附近的人"""
        coord = self.player.coord.values()
        myaddr = self.player.addr
        for p in self.get_persons():
            if p.hp > 0 and p.coord[2] > 0 and p.distance(coord) <= distance and p.addr != myaddr:
                yield p

    def get_vehicles(self):
        pool = Pool(self.address.VEHICLE_POOL, self.handler, self.Vehicle)
        return iter(pool)

    def get_near_vehicles(self, distance=100):
        """获取附近的载具"""
        coord = self.player.coord.values()
        mycar = self.vehicle
        myaddr = mycar.addr if mycar else 0
        for v in self.get_vehicles():
            if v.coord[2] > 0 and v.distance(coord) <= distance and v.addr != myaddr:
                yield v

    def kill_near_persons(self, _=None):
        """杀死附近的人"""
        for p in self.get_near_persons():
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

    def near_persons_to_front(self, _=None, zinc=0):
        """附近的人移到眼前"""
        coord = self.get_front_coord()
        for p in self.get_near_persons():
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

    def near_persons_fly(self, _=None):
        """附近的人上天"""
        fly_speed = getattr(self, 'FLY_SPEED', 1)
        for p in self.get_near_persons():
            p.speed[2] = fly_speed

    def near_vehicles_fly(self, _=None):
        """获取附近的载具上天"""
        fly_speed = getattr(self, 'FLY_SPEED', 1)
        for v in self.get_near_vehicles():
            v.coord[2] += fly_speed
            v.speed[2] = fly_speed

    def near_fly(self, _=None):
        """获取附近的人/载具上天"""
        self.near_persons_fly()
        self.near_vehicles_fly()

    def vehicle_flip(self, _=None):
        """当前的载具翻转"""
        self.player.vehicle.flip()

    def call_vehicle(self, _=None):
        """召唤上一辆车回来"""
        car = self.player.vehicle
        if car:
            car.coord = self.get_front_coord()

    def go_vehicle(self, _=None):
        """回到上一辆车旁边"""
        car = self.player.vehicle
        if car:
            coord = car.coord.values()
            coord[2] += 5
            self.player.coord = coord

    #----------------------------------------------------------------------
    # MARKER
    #----------------------------------------------------------------------
    def re_cal_markers(self, _=None):
        """重新获取人/车标记点"""
        Marker = self.models.Marker
        addr = self.address.MARKER_ARRAY
        it = Marker(addr, self.handler)
        self._markers = []

        for i in range(self.MARKER_RANGE):
            blipType = it.blipType
            if blipType in Marker.AVAILABLE_TYPE:
                self._markers.append(Marker(it.addr, self.handler))

            it.next()

        self._marker_index = 0

    def go_next_marker(self, _=None):
        """到下一处 人/车标记点"""
        if not hasattr(self, '_markers'):
            self.re_cal_markers()

        while True:
            try:
                entity = self._markers[self._marker_index].entity
            except IndexError:
                self.re_cal_markers()
                return
            if entity:
                self.entity.coord = entity.coord
                break
            self._marker_index += 1

    def move_marker_to_front(self, _=None, zinc=0):
        """人/车标记点目标移到眼前"""
        if not hasattr(self, '_markers'):
            self.re_cal_markers()

        moved_car_addr = []
        front_coord = self.get_front_coord()

        for marker in self._markers:
            entity = marker.entity
            if isinstance(entity, self.Player):
                car = entity.vehicle
                if car and car.hp > 1: 
                    if car.addr not in moved_car_addr:
                        moved_car_addr.append(car.addr)
                        car.coord = front_coord
                else:
                    entity.coord = front_coord
            elif isinstance(entity, self.Vehicle):
                entity.coord = front_coord
            if zinc:
                coord[2] += zinc

    def lock_door(self, _=None):
        car = self.player.vehicle
        if car:
            car.lock_door()

    def unlock_door(self, _=None):
        car = self.player.vehicle
        if car:
            car.unlock_door()

    def get_camera_rot(self):
        rotz = self.get_rotz()
        return (math.cos(rotz), math.sin(rotz), 0.1)

    def collect_sling_balls(self):
        self._sling_balls = self.get_near_vehicles(distance=60)

    def sling(self, _=None, is_retry=False, force_recollect=False):
        cam_x, cam_y, cam_z = self.get_camera_rot()

        sling_balls = None if force_recollect else getattr(self, '_sling_balls', None)
        flag = False
        if sling_balls:
            try:
                ball = next(sling_balls)
                flag = True
            except StopIteration:
                if is_retry:
                    # 大概是附近没有车了
                    return

        if not flag:
            self.collect_sling_balls()
            self.sling(is_retry=True)
            return

        coord_up = getattr(self, 'SLING_COORD_UP', 1)
        coord = self.player.coord.values()
        coord[0] += cam_x * 5
        coord[1] += cam_y * 5
        coord[2] += cam_z * 5 + coord_up
        speed_rate = getattr(self, 'SLING_SPEED_RATE', 3)
        speed = (cam_x * speed_rate, cam_y * speed_rate, cam_z * speed_rate)
        ball.stop()
        ball.coord = coord
        ball.speed = speed

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
        ui.Button("杀掉附近的人", onclick=self.kill_near_persons)
        ui.Button("附近的车起火", onclick=self.near_vehicles_boom)
        ui.Button("附近的车下陷", onclick=self.near_vehicles_down)
        ui.Button("附近的车移到眼前", onclick=self.near_vehicles_to_front)
        ui.Button("附近的人移到眼前", onclick=self.near_persons_to_front)
        ui.Button("附近的车上天", onclick=self.near_vehicles_fly)
        ui.Button("附近的人上天", onclick=self.near_persons_fly)
        ui.Button("附近的车翻转", onclick=self.near_vehicles_flip)
        ui.Button("跳上一辆车", onclick=self.jump_on_vehicle)
        ui.Button("召唤上一辆车回来", onclick=self.call_vehicle)
        ui.Button("回到上一辆车旁边", onclick=self.go_vehicle)

    def render_common_text(self):
        ui.Text("向前穿墙: alt+w")
        ui.Text("向前穿墙大: alt+shift+w")
        ui.Text("弹射起步: alt+m")
        ui.Text("上天（有速度）: alt+空格")
        ui.Text("往上（无速度）: alt+.")
        ui.Text("下坠: alt+shift+空格")
        ui.Text("恢复HP: alt+h")
        ui.Text("恢复大量HP: alt+shift+h")
        ui.Text("跳上一辆车: alt+j")
        ui.Text("附近的人上天: alt+f")
        ui.Text("附近的人和载具上天: alt+shift+f")
        ui.Text("自己的车翻转: alt+k")
        ui.Text("附近的人和载具翻转: alt+shift+k")
        ui.Text("附近的人移到眼前: alt+shift+p")
        ui.Text("附近的载具移到眼前: alt+p")
        ui.Text("瞬移到上一个地点: alt+shift+,")
        ui.Text("瞬移到下一个地点: alt+shift+.")
        ui.Text("重新获取雷达上标记的目标: alt+'")
        ui.Text("瞬移到下一个标记目标处: alt+/")
        ui.Text("把获取到的标记目标移到眼前: alt+shift+/")
        ui.Text("上一辆车锁门: alt+l")
        ui.Text("上一辆车解锁: alt+shift+l")

    def get_common_hotkeys(self):
        return (
            ('go_forward', MOD_ALT, getVK('w'), self.go_forward),
            ('go_forward_large', MOD_ALT | MOD_SHIFT, getVK('w'), partial(self.go_forward, rate=10)),
            ('speed_up', MOD_ALT, getVK('m'), self.speed_up),
            ('raise_up', MOD_ALT, getVK(' '), self.raise_up),
            ('go_down', MOD_ALT | MOD_SHIFT, getVK(' '), self.go_down),
            ('to_up', MOD_ALT, getVK('.'), self.to_up),
            ('stop', MOD_ALT, getVK('x'), self.stop),
            ('restore_hp', MOD_ALT, getVK('h'), self.restore_hp),
            ('restore_hp_large', MOD_ALT | MOD_SHIFT, getVK('h'), self.restore_hp_large),
            ('jump_on_vehicle', MOD_ALT, getVK('j'), self.jump_on_vehicle),
            ('near_persons_fly', MOD_ALT, getVK('f'), self.near_persons_fly),
            ('near_fly', MOD_ALT | MOD_SHIFT, getVK('f'), self.near_fly),
            ('vehicle_flip', MOD_ALT, getVK('k'), self.vehicle_flip),
            ('near_vehicles_flip', MOD_ALT | MOD_SHIFT, getVK('k'), self.near_vehicles_flip),
            ('move_near_vehicle_to_front', MOD_ALT, getVK('p'), self.near_vehicles_to_front),
            ('move_near_person_to_front', MOD_ALT | MOD_SHIFT, getVK('p'), self.near_persons_to_front),
            ('go_prev_pos', MOD_ALT | MOD_SHIFT, getVK(','), self.go_prev_pos),
            ('go_next_pos', MOD_ALT | MOD_SHIFT, getVK('.'), self.go_next_pos),
            ('re_cal_markers', MOD_ALT, getVK("'"), self.re_cal_markers),
            ('go_next_marker', MOD_ALT, getVK('/'), self.go_next_marker),
            ('move_marker_to_front', MOD_ALT | MOD_SHIFT, getVK('/'), self.move_marker_to_front),
            ('lock_door', MOD_ALT, getVK('l'), self.lock_door),
            ('unlock_door', MOD_ALT | MOD_SHIFT, getVK('l'), self.unlock_door),
            ('sling', MOD_ALT, getVK('d'), self.sling),
            ('resling', MOD_ALT | MOD_SHIFT, getVK('d'), partial(self.sling, force_recollect=True)),
        )