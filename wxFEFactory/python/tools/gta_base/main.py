from lib.win32.sendkey import auto, TextVK
import math
import time
import fefactory_api


class BaseGTATool:
    def swithKeeptop(self, cb):
        self.win.keeptop = cb.checked

    def inputCheat(self, text):
        auto.sendKey(TextVK(text), 10)

    def _player(self):
        player_addr = self.handler.read32(self.address.PLAYER_BASE)
        if player_addr is 0:
            return None
        player = getattr(self, '_playerins', None)
        if not player:
            player = self._playerins = self.Player(player_addr, self.handler)
        elif player.addr != player_addr:
            player.addr = player_addr
        return player

    def _vehicle(self):
        return self.Vehicle(self.handler.read32(self.address.VEHICLE_BASE), self.handler)

    player = property(_player)
    vehicle = property(_vehicle)

    @property
    def isInVehicle(self):
        return self.player.isInVehicle

    @property
    def player_entity(self):
        return self.vehicle if self.isInVehicle else self.player

    def get_rotz(self):
        PI = math.pi
        HALF_PI = PI / 2
        rotz = self.rot_view.mem_value
        rotz += HALF_PI
        if rotz > PI:
            rotz += PI * 2
        return rotz

    def jetPackTick(self, hotkeyId=None, useSpeed=False, detal=0):
        """弹射起步"""
        jetPackSpeed = detal or self.jetPackSpeed
        isInVehicle = self.isInVehicle

        if isInVehicle:
            coord_view = self.vehicle_coord_view
            speed_view = self.vehicle_speed_view
        else:
            coord_view = self.coord_view
            speed_view = self.speed_view
        
        rotz = self.get_rotz()
        xVal = math.cos(rotz)
        yVal = math.sin(rotz)

        if not useSpeed:
            target = coord_view
            values = target.mem_value.values()
            values[0] += xVal * jetPackSpeed
            values[1] += yVal * jetPackSpeed
        else:
            # speed up
            target = speed_view
            values = target.mem_value.values()
            speed_rate = getattr(self, 'safe_speed_rate', 0.5)
            values[0] += xVal * speed_rate
            values[1] += yVal * speed_rate
            if not isInVehicle:
                values[2] = 0.2
                self.raiseUp(speed=0.2)
                time.sleep(0.1)
        
        target.mem_value = values

    def raiseUp(self, hotkeyId=None, speed=1.0):
        self.player_entity.speed[2] = speed

    def goDown(self, hotkeyId=None, speed=0.5):
        self.player_entity.speed[2] = -speed

    def toUp(self, hotkeyId=None):
        self.player_entity.coord[2] += 10

    def stop(self, hotkeyId=None):
        speed_view = self.vehicle_speed_view if self.isInVehicle else self.speed_view
        speed_view.mem_value = (0, 0, 0)

    def restoreHp(self, hotkeyId=None):
        if self.isInVehicle:
            self.vehicle_hp_view.mem_value = 2000
        else:
            self.hp_view.mem_value = 200

    def restoreHpLarge(self, hotkeyId=None):
        if self.isInVehicle:
            self.vehicle_hp_view.mem_value = 2000
        else:
            self.hp_view.mem_value = 999
            self.ap_view.mem_value = 999

    def fromPlayerCoord(self, btn):
        self.vehicle_coord_view.input_value = self.coord_view.input_value

    def fromVehicleCoord(self, btn):
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

    def getNearPersons(self, distance=100):
        """获取附近的人"""
        coord = self.player.coord.values()
        myaddr = self.handler.read32(self.address.PLAYER_BASE)
        for p in self.getPersons():
            if p.hp != 0 and p.distance(coord) <= distance:
                if p.addr != myaddr:
                    yield p

    def getNearVehicles(self, distance=100):
        """获取附近的载具"""
        coord = self.player.coord.values()
        mycarAddr = self.handler.read32(self.address.VEHICLE_BASE)
        for v in self.getVehicles():
            if v.hp != 0 and v.distance(coord) <= distance:
                if v.addr != mycarAddr:
                    yield v

    def killNearPerson(self, btn=None):
        """杀死附近的人"""
        for p in self.getNearPersons():
            p.hp = 0

    def nearVehicleBoom(self, btn=None):
        """摧毁附近的载具"""
        for v in self.getNearVehicles():
            v.hp = 0

    def nearVehicleDown(self, btn=None):
        """获取附近的载具下陷"""
        for v in self.getNearVehicles():
            v.coord[2] -= 0.7

    def nearVehicleToFront(self, btn=None):
        """获取附近的载具移到眼前"""
        coord = self.get_front_coord()
        for p in self.getNearVehicles():
            p.coord = coord

    def nearPersonToFront(self, btn=None):
        """附近的人移到眼前"""
        coord = self.get_front_coord()
        for p in self.getNearPersons():
            p.coord = coord

    def jumpOnVehicle(self, btn=None):
        """跳上附近的一辆行驶中的车"""
        for v in self.getNearVehicles():
            # if v.numPassengers:
            v.stop()
            coord = v.coord.values()
            coord[2] += 1
            self.player.coord = coord
            break

    def nearVehicleFlip(self, _=None):
        """附近的载具上下翻转"""
        for v in self.getNearVehicles():
            v.flip()

    def nearPersonFly(self, _=None):
        """附近的人上天"""
        for p in self.getNearPersons():
            p.speed[2] = 1

    def nearVehicleFly(self, btn=None):
        """获取附近的载具上天"""
        for v in self.getNearVehicles():
            v.coord[2] += 1
            v.speed[2] = 1

    def nearFly(self, btn=None):
        """获取附近的人/载具上天"""
        self.nearPersonFly()
        self.nearVehicleFly()

    def vehicleFlip(self, _=None):
        """当前的载具翻转"""
        self.player.lastCar.flip()

    def callVehicle(self, _=None):
        """召唤上一辆车回来"""
        car = self.player.lastCar
        if car:
            car.coord = self.get_front_coord()

    def goVehicle(self, _=None):
        """回到上一辆车旁边"""
        car = self.player.lastCar
        if car:
            coord = car.coord.values()
            coord[2] += 5
            self.player.coord = coord

    def g3l2json(self, btn=None):
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