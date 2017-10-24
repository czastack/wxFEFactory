from functools import partial
from fefactory_api.emuhacker import ProcessHandler
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
from lib.win32.sendkey import auto, TextVK
from commonstyle import styles
from ..tool import BaseTool
from .models import Pool
from .native import NativeContext
import math
import time
import fefactory_api
import fefactory_api
ui = fefactory_api.ui

win_style = {
    'width': 700,
    'height': 820,
    # 'width': 640,
    # 'height': 700,
}


class BaseGTATool(BaseTool):
    nested = True

    FUNCTION_NATIVE_CALL = (
        b'\x55\x8B\xEC\x83\xEC\x0C\x56\x8B\x75\x08\x57\x8B\x56\x08\x8B\x02\x8B\x7A\x04\x83\x46\x04\xFE\x8B\x4E\x04\x41\x89\x45'
        b'\xF4\x89\x7D\xF8\x83\xF9\x01\x7E\x0F\x8B\x04\x8A\x89\x45\xFC\xFF\x75\xFC\x49\x83\xF9\x01\x7F\xF1\x85\xFF\x74\x03\x8B'
        b'\x4D\xF8\xFF\x55\xF4\x89\x45\x08\x85\xFF\x75\x0C\x8B\x46\x04\xC1\xE0\x02\x89\x45\xF4\x03\x65\xF4\x8B\x0E\x8B\x45\x08'
        b'\x5F\x5E\x89\x01\x8B\xE5\x5D\xC3'
    )

    def __init__(self):
        super().__init__()
        self.handler = ProcessHandler()

    def attach(self, frame):
        super().attach(frame)
        self.check_attach()

    def render(self):
        with self.render_win() as win:
            with ui.Vertical():
                with ui.Horizontal(className="expand container"):
                    ui.Button("检测", className="vcenter", onclick=self.check_attach)
                    self.attach_status_view = ui.Text("", className="label_left grow")
                    ui.CheckBox("保持最前", onchange=self.swithKeeptop)
                with ui.Notebook(className="fill"):
                    self.render_main()

        return win

    def render_win(self):
        menubar = self.render_menu()
        self.win = ui.HotkeyWindow(self.doGetTitle(), style=win_style, styles=styles, menuBar=menubar, exstyle=0x80804)
        self.win.position = (70, 4)
        return self.win

    def check_attach(self, _=None):
        """检查运行GTA主程序状态"""
        if self.handler.active:
            self.free_remote_function()

        if self.handler.attachByWindowName(self.CLASS_NAME, self.WINDOW_NAME):
            self.attach_status_view.label = self.WINDOW_NAME + ' 正在运行'

            if not self.win.hotkeys:
                self.win.RegisterHotKeys(self.get_hotkeys())
            self.init_remote_function()
        else:
            self.attach_status_view.label = '没有检测到 ' + self.WINDOW_NAME

    def get_hotkeys(self):
        """重写这个函数，返回要注册的热键列表"""
        return self.get_common_hotkeys()

    def swithKeeptop(self, cb):
        self.win.keeptop = cb.checked

    def onClose(self, _=None):
        if self.handler.active:
            self.free_remote_function()
        return super().onClose()

    def read_vector(self, addr):
        """ 在addr读三个float类型
        :return: (x, y, z)
        """
        r = self.handler.readFloat
        return (r(addr), r(addr + 4), r(addr + 8))

    def init_remote_function(self):
        """初始化远程函数"""
        self.NativeCall = self.handler.write_function(self.FUNCTION_NATIVE_CALL)
        # 初始化Native调用的参数环境
        context_addr = self.handler.alloc_memory(NativeContext.SIZE)
        self.native_context = NativeContext(context_addr, self.handler)

    def free_remote_function(self):
        """释放远程函数"""
        self.handler.free_memory(self.NativeCall)
        self.handler.free_memory(self.native_context.addr)

    def native_call(self, addr, arg_sign, *args, ret_type=int, ret_size=4):
        """ 远程调用参数为NativeContext*的函数
        :param arg_sign: 函数签名
        """
        with self.native_context:
            if arg_sign:
                self.native_context.push(arg_sign, *args)
            self.handler.remote_call(addr, self.native_context.addr)
            if ret_type:
                return self.native_context.get_result(ret_type, ret_size)

    def native_call_auto(self, addr, arg_sign, *args, this=0, ret_type=int, ret_size=4):
        """ 以cdcel或thiscall形式调用远程函数
        :param addr: 目标函数地址
        :param this: this指针，若不为0，则以thiscall形式调用，否则以cdcel形式调用
        :param arg_sign: 参数签名
        """
        self.native_call(self.NativeCall, '2L' + (arg_sign if arg_sign is not None else ''), addr, this, *args, ret_type=ret_type, ret_size=ret_size)
        return self.handler.read32(self.native_context.m_pReturn)

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
        """当前是否在乘车"""
        return self.player.isInVehicle

    @property
    def entity(self):
        """在车中则返回载具对象，否则返回角色对象"""
        return self.vehicle if self.isInVehicle else self.player

    @property
    def ped_pool(self):
        """角色池"""
        return self.models.Pool(self.address.PED_POOL, self.handler, self.Player)

    @property
    def vehicle_pool(self):
        """载具池"""
        return self.models.Pool(self.address.VEHICLE_POOL, self.handler, self.Vehicle)

    @property
    def object_pool(self):
        """物体池"""
        return self.models.Pool(self.address.OBJECT_POOL, self.handler, self.Object)

    def get_rotz(self):
        """获取xy面旋转量"""
        PI = math.pi
        HALF_PI = PI / 2
        rotz = self.rot_view.mem_value
        rotz += HALF_PI
        if rotz > PI:
            rotz += PI * 2
        return rotz

    def get_camera_rot(self):
        """获取摄像机朝向参数 (x分量, y分量, z仰角)"""
        rotz = self.get_rotz()
        return (math.cos(rotz), math.sin(rotz), 0.1)

    def get_front_coord(self):
        """获取前面一点的坐标"""
        rotz = self.get_rotz()

        xVal = math.cos(rotz)
        yVal = math.sin(rotz)
        coord = self.player.coord.values()
        coord[0] += xVal * 5
        coord[1] += yVal * 5
        return coord

    def go_forward(self, _=None, rate=0):
        """前进"""
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
        """上天（有速度）"""
        self.entity.speed[2] = speed

    def go_down(self, _=None, speed=0.5):
        """向下（有速度）"""
        self.entity.speed[2] = -speed

    def to_up(self, _=None):
        """往上（无速度）"""
        self.entity.coord[2] += 10

    def to_down(self, _=None):
        """向下（无速度）"""
        self.entity.coord[2] -= 6

    def stop(self, _=None):
        """停止移动"""
        speed_view = self.vehicle_speed_view if self.isInVehicle else self.speed_view
        speed_view.mem_value = (0, 0, 0)

    def restore_hp(self, _=None):
        """恢复HP"""
        if self.isInVehicle:
            self.vehicle_hp_view.mem_value = 2000
            self.vehicle_fix(self.vehicle)
        else:
            self.hp_view.mem_value = 200
            self.ap_view.mem_value = 200

    def restore_hp_large(self, _=None):
        """恢复大量HP"""
        if self.isInVehicle:
            self.vehicle_hp_view.mem_value = 2000
            self.vehicle_fix(self.vehicle)
        else:
            self.hp_view.mem_value = 999
            self.ap_view.mem_value = 999

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

    def get_peds(self):
        """获取角色池中的角色列表"""
        pool = Pool(self.address.PED_POOL, self.handler, self.Player)
        return iter(pool)

    def get_near_peds(self, distance=100):
        """获取附近的人"""
        coord = self.player.coord.values()
        myaddr = self.player.addr
        for p in self.get_peds():
            if p.hp > 0 and p.coord[2] > 0 and p.distance(coord) <= distance and p.addr != myaddr:
                yield p

    def get_vehicles(self):
        """载具池中的载具列表"""
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

    def collect_vehicles(self):
        """暂存附近的载具"""
        self._vehicles = self.get_near_vehicles(distance=100)

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
        vehicle = self.player.vehicle
        if vehicle:
            if lock:
                vehicle.lock_door()
            else:
                vehicle.unlock_door()

    #----------------------------------------------------------------------
    # MARKER
    #----------------------------------------------------------------------
    def get_blips(self, color=None, types=None):
        """获取所有标记"""
        Marker = self.models.Marker
        addr = self.address.BLIP_LIST
        it = Marker(addr, self)

        for i in range(self.MARKER_RANGE):
            blipType = it.blipType
            if it.blipType and (types is None or blipType in types) and (color is None or it.color is color):
                yield Marker(it.addr, self)
            it.next()

    def get_target_blips(self, color=None, types=None):
        """获取目标的所有标记"""
        return self.get_blips(color, self.models.Marker.AVAILABLE_TYPE)

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
    
    def teleport_to_destination(self, _=None, color=None, types=None):
        """瞬移到目的地"""
        Marker = self.models.Marker

        if color is None:
            color = self.DEST_DEFAULT_COLOR

        if types is None:
            types = (Marker.MARKER_TYPE_CAR, Marker.MARKER_TYPE_PED, Marker.MARKER_TYPE_COORDS)

        for blip in self.get_blips(color, types):
            if blip.sprite is 0:
                blipType = blip.blipType
                if blipType is Marker.MARKER_TYPE_COORDS:
                    coord = blip.coord
                else:
                    entity = blip.entity
                    if entity:
                        coord = entity.coord
                    else:
                        continue
                self.entity.coord = coord
                break

    def spawn_choosed_vehicle(self, _=None):
        """生成选中的载具"""
        model = getattr(self, 'spwan_vehicle_id', None)
        if model:
            return self.spawn_vehicle(model)

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
        car = self.player.vehicle
        if car:
            car.lock_door()

    def unlock_door(self, _=None):
        """解锁最近使用的载具的车门"""
        car = self.player.vehicle
        if car:
            car.unlock_door()

    def sling(self, _=None, recollect=False):
        """载具发射台"""
        vehicle = self.next_collected_vehicle(recollect=recollect)
        
        if not vehicle:
            return

        cam_x, cam_y, cam_z = self.get_camera_rot()
        coord_up = getattr(self, 'SLING_COORD_UP', 1)
        coord = self.player.coord.values()
        coord[0] += cam_x * 5
        coord[1] += cam_y * 5
        coord[2] += cam_z * 5 + coord_up
        speed_rate = getattr(self, 'SLING_SPEED_RATE', 3)
        speed = (cam_x * speed_rate, cam_y * speed_rate, cam_z * speed_rate)
        vehicle.stop()
        vehicle.coord = coord
        vehicle.speed = speed

    def clear_wanted_level(self, _=None):
        """清除通缉等级"""
        self.wanted_level_view.mem_value = 0
    
    def explode_art(self, _=None, count=10):
        """焰之炼金术 (向前生成数个爆炸)"""
        cam_x, cam_y, cam_z = self.get_camera_rot()
        offset = (cam_x * 6, cam_y * 6, cam_z * 6)
        coord = self.player.get_offset_coord_m(offset)

        for i in range(count):
            coord[0] += offset[0]
            coord[1] += offset[1]
            coord[2] += offset[2]
            self.create_explosion(coord)

    def custom_hotkey(self, _=None):
        """用于自定义的临时热键功能"""
        fn = getattr(self, 'hotkey_cfn', None)
        if fn:
            fn()

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
        ui.Button("附近的车起火", onclick=self.near_vehicles_boom)
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
        ui.Text("根据左边列表生产载具: alt+v")
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
        ui.Text("把一辆车移到眼前: alt+b")
        ui.Text("清除通缉等级: alt+0")
        ui.Text("红莲之炼金术 (向前生成数个爆炸): alt+`")
        ui.Text("红莲之炼金术 (长): alt+shift+`")
        ui.Text("瞬移到目的地: alt+1")
        ui.Text("自定义临时热键(执行tool.hotkey_cfn): alt+c")

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
            ('near_peds_fly', MOD_ALT, getVK('f'), self.near_peds_fly),
            ('near_fly', MOD_ALT | MOD_SHIFT, getVK('f'), self.near_fly),
            ('vehicle_flip', MOD_ALT, getVK('k'), self.vehicle_flip),
            ('near_vehicles_flip', MOD_ALT | MOD_SHIFT, getVK('k'), self.near_vehicles_flip),
            ('move_near_ped_to_front', MOD_ALT | MOD_SHIFT, getVK('p'), self.near_peds_to_front),
            ('move_near_vehicle_to_front', MOD_ALT, getVK('p'), self.near_vehicles_to_front),
            ('go_prev_pos', MOD_ALT | MOD_SHIFT, getVK(','), self.go_prev_pos),
            ('go_next_pos', MOD_ALT | MOD_SHIFT, getVK('.'), self.go_next_pos),
            ('recal_markers', MOD_ALT, getVK("'"), self.recal_markers),
            ('go_next_marker', MOD_ALT, getVK('/'), self.go_next_marker),
            ('move_marker_to_front', MOD_ALT | MOD_SHIFT, getVK('/'), self.move_marker_to_front),
            ('lock_door', MOD_ALT, getVK('l'), self.lock_door),
            ('unlock_door', MOD_ALT | MOD_SHIFT, getVK('l'), self.unlock_door),
            ('sling', MOD_ALT, getVK('d'), self.sling),
            ('resling', MOD_ALT | MOD_SHIFT, getVK('d'), partial(self.sling, recollect=True)),
            ('bring_one_vehicle', MOD_ALT, getVK('b'), self.bring_one_vehicle),
            ('clear_wanted_level', MOD_ALT, getVK('0'), self.clear_wanted_level),
            ('explode_art', MOD_ALT, getVK('`'), self.explode_art),
            ('explode_art_long', MOD_ALT | MOD_SHIFT, getVK('`'), partial(self.explode_art, count=24)),
            ('teleport_to_destination', MOD_ALT, getVK('1'), self.teleport_to_destination),
            ('spawn_vehicle_id_prev', MOD_ALT, getVK('['), self.spawn_vehicle_id_prev),
            ('spawn_vehicle_id_next', MOD_ALT, getVK(']'), self.spawn_vehicle_id_next),
            ('spawn_choosed_vehicle', MOD_ALT, getVK('v'), self.spawn_choosed_vehicle),
            ('custom_hotkey', MOD_ALT, getVK('c'), self.custom_hotkey),
        )