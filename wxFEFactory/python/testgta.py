from lib import exui
from commonstyle import dialog_style, styles
from fefactory_api.emuhacker import ProcessHandler
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL
import math
import os
import json
import __main__
import fefactory_api
import fefactory
Path = os.path
ui = fefactory_api.ui


class Field:
    GROUPS = []

    def __init__(self, name, label, addr, offsets=()):
        self.name = name
        self.label = label
        self.addr = addr
        self.offsets = offsets

        parent = self.GROUPS[-1] if len(self.GROUPS) else None
        if parent:
            parent.appendChild(self)
            if self.addr is None:
                self.addr = parent.addr
        self.parent = parent
        self.render()

    def render(self):
        ui.Text(self.label, className="label_left expand")

    def render_btn(self):
        ui.Button(label="r", style=btn_style, onclick=lambda btn: self.read())
        ui.Button(label="w", style=btn_style, onclick=lambda btn: self.write())

    def read(self):
        pass

    def write(self):
        pass

    @property
    def _handler(self):
        return self.parent.handler if self.parent else None

    def __repr__(self):
        return '%s("%s", "%s")' % (self.__class__.__name__, self.name, self.label)
    

class Group(Field):

    def __init__(self, name, label, addr, flexgrid=True, handler=None):
        super().__init__(name, label, addr)
        self.flexgrid = flexgrid
        self.children = []
        self.handler = handler or (self._handler if self.parent else None)

    def render(self):
        self.view = ui.Vertical(className="fill container")
        ui.Item(self.view, caption=self.label)

    def appendChild(self, child):
        self.children.append(child)

    def __enter__(self):
        self.view.__enter__()
        if self.flexgrid:
            self.container = ui.FlexGridLayout(cols=2, vgap=10, className="fill container")
            self.container.AddGrowableCol(1)
            self.container.__enter__()

        self.GROUPS.append(self)
        return self

    def __exit__(self, *args):
        if self.flexgrid:
            self.container.__exit__(*args)
        with ui.Horizontal(className="container"):
            ui.Button(label="读取", className="button", onclick=lambda btn: self.read())
            ui.Button(label="写入", className="button", onclick=lambda btn: self.write())

        self.view.__exit__(*args)
        if self.GROUPS.pop() is not self:
            raise ValueError('GROUPS层次校验失败')

    def read(self):
        for field in self.children:
            field.read()

    def write(self):
        for field in self.children:
            field.write()


class GroupBox(Group):
    def render(self):
        self.view = ui.StaticBox(self.label, className="fill container")


class InputField(Field):
    def __init__(self, name, label, addr, offsets, type_=None, size=4):
        super().__init__(name, label, addr, offsets)
        self.type_ = type_
        self.size = size

    def render(self):
        super().render()
        with ui.Horizontal(className="fill"):
            self.view = ui.TextInput(className="fill", exstyle=0x0400)
            self.render_btn()

    @property
    def mem_value(self):
        return self._handler.ptrsRead(self.addr, self.offsets, self.type_, self.size)

    @mem_value.setter
    def mem_value(self, value):
        self._handler.ptrsWrite(self.addr, self.offsets, self.type_(value), self.size)

    def read(self):
        self.view.value = str(self.mem_value)

    def write(self):
        self.mem_value = self.view.value


class CheckBoxField(Field):
    def __init__(self, name, label, addr, offsets, enableData=None, disableData=None):
        """
        :param enableData: 激活时写入的数据
        :param disableData: 关闭时写入的数据
        """
        super().__init__(name, label, addr, offsets)
        self.enableData = enableData
        self.disableData = disableData

    def render(self):
        self.view = ui.CheckBox(self.label, onchange=self.onChange)

    def onChange(self, checkbox):
        data = self.enableData if checkbox.checked else self.disableData
        self._handler.ptrsWrite(self.addr, self.offsets, data, len(data))


class CoordsField(Field):
    def __init__(self, name, label, addr, offsets, savable=False):
        self.savable = savable
        super().__init__(name, label, addr, offsets)

        if savable:
            self.data_list = []
            self.lastfile = None

    def render(self):
        super().render()
        if not self.savable:
            with ui.Horizontal(className="expand"):
                self.x_view = ui.TextInput(className="fill")
                self.y_view = ui.TextInput(className="fill")
                self.z_view = ui.TextInput(className="fill")
                self.render_btn()

        else:
            with ui.Vertical(className="fill"):
                with ui.Horizontal(className="fill"):
                    with ui.Vertical(className="fill"):
                        with ui.FlexGridLayout(cols=2, vgap=10, className="fill container") as grid:
                            grid.AddGrowableCol(1)
                            ui.Text("X坐标", className="label_left expand")
                            self.x_view = ui.TextInput(className="fill")
                            ui.Text("Y坐标", className="label_left expand")
                            self.y_view = ui.TextInput(className="fill")
                            ui.Text("Z坐标", className="label_left expand")
                            self.z_view = ui.TextInput(className="fill")
                            ui.Text("名称", className="label_left expand")
                            self.name_view = ui.TextInput(className="fill")
                        with ui.Horizontal(className="container"):
                            self.render_btn()
                            ui.Button(label="添加", className="button", onclick=self.onAdd)
                            ui.Button(label="更新", className="button", onclick=self.onUpdate)
                            ui.Button(label="删除", className="button", onclick=self.onDel)
                            ui.Button(label="保存", className="button", onclick=self.onSave)
                            ui.Button(label="载入", className="button", onclick=self.onLoad)
                    self.listbox = ui.ListBox(className="expand", onselect=self.onListBoxSel)
                    self.listbox.setOnKeyDown(self.onListBoxKey)

        self.views = (self.x_view, self.y_view, self.z_view)

    @property
    def mem_value(self):
        offsets = list(self.offsets)
        ret = []
        for child in self.views:
            if offsets:
                value = self._handler.ptrsRead(self.addr, offsets, float)
                offsets[-1] += 4
            else:
                value = self._handler.readFloat(self.addr)
            ret.append(value)
        return ret

    @mem_value.setter
    def mem_value(self, values):
        offsets = list(self.offsets)
        it = iter(values)
        for child in self.views:
            if offsets:
                self._handler.ptrsWrite(self.addr, offsets, float(next(it)), float)
                offsets[-1] += 4
            else:
                self._handler.writeFloat(self.addr, float(next(it)))

    @property
    def input_value(self):
        return map(lambda v: float(v.value), self.views)

    @input_value.setter
    def input_value(self, values):
        it = iter(values)
        for child in self.views:
            child.value = str(next(it))

    def read(self):
        self.input_value = self.mem_value

    def write(self):
        self.mem_value = self.input_value

    def onAdd(self, btn):
        name = self.name_view.value
        if name:
            self.listbox.append(name)
            self.data_list.append({'name': name, 'value': tuple(self.input_value)})

    def onUpdate(self, btn):
        pos = self.listbox.index
        if pos != -1:
            name = self.name_view.value
            if name:
                self.listbox.text = name
                self.data_list[pos] = {'name': name, 'value': tuple(self.input_value)}

    def onDel(self, btn):
        pos = self.listbox.index
        if pos != -1:
            self.listbox.pop(pos)
            self.data_list.pop(pos)

    def onSave(self, btn):
        file = fefactory_api.choose_file("选择保存文件", file=self.lastfile, wildcard='*.json')
        if file:
            self.lastfile = file
            with open(file, 'w', encoding="utf-8") as file:
                json.dump(self.data_list, file, ensure_ascii=False)

    def onLoad(self, btn):
        file = fefactory_api.choose_file("选择要读取的文件", file=self.lastfile, wildcard='*.json')
        if file:
            self.lastfile = file
            with open(file, encoding="utf-8") as file:
                self.data_list = json.load(file)
                self.listbox.appendItems(tuple(data['name'] for data in self.data_list))

    def onListBoxSel(self, lb):
        pos = self.listbox.index
        data = self.data_list[pos]
        self.name_view.value = data['name']
        self.input_value = data['value']

    def onListBoxKey(self, lb, event):
        """按键监听"""
        mod = event.GetModifiers()
        code = event.GetKeyCode()
        if mod == event.CTRL:
            if code == event.UP:
                self.moveUp()
            elif code == event.DOWN:
                self.moveDown()
        elif code == event.getWXK('w'):
            self.write()
        event.Skip()

    def moveUp(self):
        """上移一项"""
        index = self.listbox.index
        if index != 0:
            self.data_list[index - 1], self.data_list[index] = self.data_list[index], self.data_list[index - 1]
            self.listbox.setText(self.data_list[index]['name'], index)
            self.listbox.setText(self.data_list[index - 1]['name'], index - 1)

    def moveDown(self):
        """下移一项"""
        index = self.listbox.index
        if index != self.listbox.count - 1:
            self.data_list[index + 1], self.data_list[index] = self.data_list[index], self.data_list[index + 1]
            self.listbox.setText(self.data_list[index]['name'], index)
            self.listbox.setText(self.data_list[index + 1]['name'], index + 1)


PLAYER_BASE  = 0x94AD28
VEHICLE_BASE = 0x7E49C0
MONEY_BASE   = 0x94ADC8
VEHICLE_BASE = 0x7E49C0


class GTA_VC_Cheat:

    def __init__(self):
        self.handler = ProcessHandler()
        self.render()
        self.jetPackSpeed = 2.0

    def render(self):
        with ui.MenuBar() as menubar:
            with ui.Menu("文件"):
                with ui.Menu("新建"):
                    ui.MenuItem("新建工程\tCtrl+Shift+N", onselect=None)
            with ui.Menu("窗口"):
                ui.MenuItem("关闭\tCtrl+W", onselect=self.closeWindow)

        with ui.HotkeyWindow("罪恶都市Hack", style=win_style, styles=styles, menuBar=menubar) as win:
            with ui.Vertical():
                with ui.Horizontal(className="expand container"):
                    ui.Button("检测", className="vcenter", onclick=self.checkAtach)
                    self.attach_status_view = ui.Text("", className="label_left grow")
                    ui.CheckBox("保持最前", onchange=self.swithKeeptop)
                with ui.Notebook(className="fill"):
                    self.render_main()

        win.setOnclose(self.onClose)
        self.win = win

    def render_main(self):
        with Group("player", "角色", PLAYER_BASE, handler=self.handler):
            self.hp_view = InputField("hp", "HP", None, (0x354,), float)
            self.ap_view = InputField("ap", "AP", None, (0x358,), float)
            self.rot_view = InputField('rotation', '旋转', None, (0x378,), float)
            self.coord_view = CoordsField('coord', '坐标', None, (0x34,), savable=True)
            self.speed_view = CoordsField('spped', '速度', None, (0x70,))
            self.weight_view = InputField("weight", "重量", None, (0xB8,), float)
            self.stamina_view = InputField("stamina", "体力", None, (0x600,), float)
            self.star_view = InputField("star", "通缉等级", None, (0x5f4, 0x20), int)
        with Group("vehicle", "汽车", VEHICLE_BASE, handler=self.handler):
            self.vehicle_hp_view = InputField("vehicle_hp", "HP", None, (0x204,), float)
            self.vehicle_roll_view = CoordsField('roll', '滚动', None, (0x04,))
            self.vehicle_dir_view = CoordsField('dir', '方向', None, (0x14,))
            self.vehicle_coord_view = CoordsField('coord', '坐标', None, (0x34,))
            self.vehicle_speed_view = CoordsField('spped', '速度', None, (0x70,))
            self.vehicle_turn_view = CoordsField('turn', 'Turn', None, (0x7C,))
            self.weight_view = InputField("weight", "重量", None, (0xB8,), float)
        with Group("global", "全局", 0, handler=self.handler):
            self.camera_view = CoordsField('camera', '摄像机', 0x7E46B8, ())
            self.camera_z_rot_view = InputField("camera_z_rot", "摄像机z_rot", 0x7E48CC, (), float)
            self.camera_x_rot_view = InputField("camera_x_rot", "摄像机x_rot", 0x7E48BC, (), float)
            CheckBoxField("god1", "角色无伤1", 0x5267DC, (), b'\xEB\x10', b'\x75\x15')
            CheckBoxField("god2", "角色无伤2", 0x5267D5, (), b'\x90\x90', b'\x75\x1C')
            CheckBoxField("vehicle_god1", "汽车无伤1", 0x5A9801, (), b'\xc7\x41\x04\x00\x00\x00\x00\xc2\x04', b'\x88\x41\x04\xc2\x04\x00\x00\x00\x00')
            CheckBoxField("vehicle_god2", "汽车无伤2", 0x588A77, (), b'\x90\x90', b'\x75\x09')
            CheckBoxField("infinite_run", "无限奔跑", 0x536F25, (), b'\xEB', b'\x75')
            CheckBoxField("drive_on_water", "水上开车", 0x593908, (), b'\x90\x90', b'\x74\x07')
            CheckBoxField("no_falling_off_the_bike", "摩托老司机", 0x61393D, (), b'\xE9\xBC\x0E\x00\x00\x90', b'\x0F\x84\xBB\x0E\x00\x90')
            CheckBoxField("disable_vehicle_explosions", "不会爆炸", 0x588A77, (), b'\x90\x90', b'\x75\x09')
            CheckBoxField("infinite_ammo1", "无限子弹1", 0x5D4ABE, (), b'\x90\x90\x90', b'\xFF\x4E\x08')
            CheckBoxField("infinite_ammo2", "无限子弹2", 0x5D4AF5, (), b'\x90\x90\x90', b'\xFF\x4E\x0C')

    def closeWindow(self, m=None):
        self.onClose()
        self.win.close()

    def onClose(self, _=None):
        global ins
        ins = None

    def checkAtach(self, btn):
        className = 'Grand theft auto 3'
        windowName = 'GTA: Vice City'
        if self.handler.attachByWindowName(className, windowName):
            self.attach_status_view.label = windowName + ' 正在运行'
            self.win.RegisterHotKey('jetPackTick', MOD_ALT, getVK('w'), self.jetPackTick)
            self.win.RegisterHotKey('raiseUp', MOD_ALT, getVK(' '), self.raiseUp)
            self.win.RegisterHotKey('stop', MOD_ALT, getVK('x'), self.stop)
        else:
            self.attach_status_view.label = '没有检测到 ' + windowName

    def swithKeeptop(self, cb):
        self.win.keeptop = cb.checked

    @property
    def isInVehicle(self):
        return self.vehicle_hp_view.mem_value >= 1

    @property
    def z_speed_ptr(self):
        speed_view = self.speed_view if self.isInVehicle else self.vehicle_speed_view
        offsets = list(speed_view.offsets)
        offsets[-1] += 8
        return self.handler.readLastPtr(self.speed_view.addr, offsets)

    def jetPackTick(self, hotkeyId=None):
        PI = math.pi
        HALF_PI = PI / 2
        jetPackSpeed = self.jetPackSpeed
        if self.isInVehicle:
            coord_view = self.vehicle_coord_view
            speed_view = self.vehicle_speed_view
            rotz = self.camera_z_rot_view.mem_value
        else:
            coord_view = self.coord_view
            speed_view = self.speed_view
            rotz = self.rot_view.mem_value
            rotz += HALF_PI
            if rotz > PI:
                rotz += PI * 2

        xVal = math.cos(rotz)
        yVal = math.sin(rotz)

        coords = coord_view.mem_value
        coords[0] += xVal * jetPackSpeed;
        coords[1] += yVal * jetPackSpeed;
        if False: # Z
            rotx = self.camera_x_rot_view.mem_value;
            coords[2] += rotx / HALF_PI * jetPackSpeed;
        
        coord_view.mem_value = coords
        speed_view.mem_value = (0, 0, 0.0066016)

        if False: # UP or FALSE
            speed_ptr = self.z_speed_ptr
            z_speed = jetPackSpeed * PI * 2
            if False: # Donw
                z_speed *= -1
            self.handler.writeFloat(speed_ptr, z_speed)

    def raiseUp(self, hotkeyId=None):
        self.handler.writeFloat(self.z_speed_ptr, 1.0)

    def stop(self, hotkeyId=None):
        speed_view = self.speed_view if self.isInVehicle else self.vehicle_speed_view
        speed_view.mem_value = (0, 0, 0)


ins = None
btn_style = {
    'width': 36,
}
win_style = {
    'width': 640,
    'height': 800,
}

def run():
    global ins
    ins = GTA_VC_Cheat()

if __name__ == 'testgta':
    run()