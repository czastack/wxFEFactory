from lib import exui
from commonstyle import dialog_style, styles
from fefactory_api.emuhacker import ProcessHandler
import os
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
        ui.Text(self.label, className="label_left")

    def render_btn(self):
        ui.Button(label="r", style=btn_style, onclick=lambda btn: self.read(self.parent.handler))
        ui.Button(label="w", style=btn_style, onclick=lambda btn: self.write(self.parent.handler))

    def read(self, handler):
        pass

    def write(self, handler):
        pass

    def __repr__(self):
        return '%s("%s", "%s")' % (self.__class__.__name__, self.name, self.label)
    

class Group(Field):

    def __init__(self, name, label, addr, flexgrid=True, handler=None):
        super().__init__(name, label, addr)
        self.flexgrid = flexgrid
        self.children = []
        self.handler = handler

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

    def read(self, handler=None):
        if not handler:
            handler = self.handler
        for field in self.children:
            field.read(handler)

    def write(self, handler=None):
        if not handler:
            handler = self.handler
        for field in self.children:
            field.write(handler)


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

    def read(self, handler):
        self.view.value = str(handler.ptrsRead(self.addr, self.offsets, self.type_, self.size))

    def write(self, handler):
        handler.ptrsWrite(self.addr, self.offsets, self.type_(self.view.value), self.size)


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
        self.view = ui.CheckBox(self.label)


class CoordsField(Field):
    def __init__(self, name, label, addr, offsets):
        super().__init__(name, label, addr, offsets)

    def render(self):
        super().render()
        with ui.Horizontal(className="fill"):
            self.x_view = ui.TextInput(className="fill")
            self.y_view = ui.TextInput(className="fill")
            self.z_view = ui.TextInput(className="fill")
            self.render_btn()

        self.views = (self.x_view, self.y_view, self.z_view)

    def read(self, handler):
        offsets = list(self.offsets)
        for child in self.views:
            if offsets:
                child.value = str(handler.ptrsRead(self.addr, offsets, float))
                offsets[-1] += 4
            else:
                child.value = str(handler.readFloat(self.addr))

    def write(self, handler):
        offsets = list(self.offsets)
        for child in self.views:
            if offsets:
                handler.ptrsWrite(self.addr, offsets, float(child.value), float)
                offsets[-1] += 4
            else:
                handler.writeFloat(self.addr, float(child.value))


PLAYER_BASE  = 0x94AD28
VEHICLE_BASE = 0x7E49C0
MONEY_BASE   = 0x94ADC8
VEHICLE_BASE = 0x7E49C0


class GTA_VC_Cheat:

    def __init__(self):
        self.handler = ProcessHandler()
        self.render()

    def render(self):
        with ui.MenuBar() as menubar:
            with ui.Menu("文件"):
                with ui.Menu("新建"):
                    ui.MenuItem("新建工程\tCtrl+Shift+N", onselect=None)
            with ui.Menu("窗口"):
                ui.MenuItem("关闭\tCtrl+W", onselect=self.onclose)

        with ui.Window("罪恶都市Hack", style=win_style, styles=styles, menuBar=menubar) as win:
            with ui.Vertical():
                with ui.Horizontal(className="expand container"):
                    ui.Button("检测", className="vcenter", onclick=self.checkAtach)
                    self.attach_status_view = ui.Text("", className="vcenter grow")
                with ui.Notebook(className="fill"):
                    self.render_main()

        self.win = win

    def render_main(self):
        with Group("player", "角色", PLAYER_BASE, handler=self.handler):
            self.hp_view = InputField("hp", "HP", None, (0x354,), float)
            self.ap_view = InputField("ap", "AP", None, (0x358,), float)
            self.rot_view = InputField('rotation', '旋转', None, (0x378,), float)
            self.coord_view = CoordsField('coord', '坐标', None, (0x34,))
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

    def onclose(self, m=None):
        self.win.close()

    def checkAtach(self, btn):
        win_title = 'GTA: Vice City'
        if self.handler.attachByWindowName('Grand theft auto 3', win_title):
            label = win_title + ' 正在运行'
        else:
            label = '没有检测到 ' + win_title
        self.attach_status_view.label = label


ins = None
btn_style = {
    'width': 36,
}
win_style = {
    'width': 640,
    'height': 600,
}

def open():
    global ins
    ins = GTA_VC_Cheat()

if __name__ == 'testgta':
    open()