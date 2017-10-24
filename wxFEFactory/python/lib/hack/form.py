from lib.utils import float32
import json
import types
import fefactory_api
ui = fefactory_api.ui


class Widget:
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


class TwoWayWidget(Widget):
    def read(self):
        value = self.mem_value
        if value is not None:
            self.input_value = self.mem_value

    def write(self):
        self.mem_value = self.input_value


class ModelWidget:
    def __init__(self, name, label, ins=None, prop=None, **kwargs):
        """
        :param ins: Model实例，或者返回Model实例的函数，在Widget中用addr占位
        :param prop: Widget对应Field的属性对象或者名称，在Widget中用offsets占位
        """
        super().__init__(name, label, addr=ins, offsets=prop or name, **kwargs)

    @property
    def ins(self):
        if callable(self.addr):
            return self.addr()
        return self.addr

    @property
    def mem_value(self):
        ins = self.ins
        if ins:
            prop = self.offsets
            return (
                getattr(ins, prop) if isinstance(prop, str) else 
                prop.__get__(ins, ins.__class__)
            )

    @mem_value.setter
    def mem_value(self, value):
        ins = self.ins
        if ins:
            prop = self.offsets
            if isinstance(prop, str):
                setattr(ins, prop, value)
            else:
                prop.__set__(ins, value)
    

class Group(Widget):

    def __init__(self, name, label, addr, flexgrid=True, hasfootbar=True, handler=None):
        super().__init__(name, label, addr)
        self.flexgrid = flexgrid
        self.hasfootbar = hasfootbar
        self.children = []
        self.handler = handler or (self._handler if self.parent else None)

    def render(self):
        with ui.ScrollView(className="fill") as root:
            self.view = ui.Vertical(className="fill container")
        ui.Item(root, caption=self.label)

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
        if self.hasfootbar:
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


class BaseInputWidget(TwoWayWidget):
    def render(self):
        super().render()
        with ui.Horizontal(className="fill"):
            self.view = ui.TextInput(className="fill", exstyle=0x0400)
            self.render_btn()

            self.view.setOnKeyDown(self.onKey)

    @property
    def input_value(self):
        return self.view.value

    @input_value.setter
    def input_value(self, value):
        self.view.value = str(value)

    def onKey(self, v, event):
        mod = event.GetModifiers()
        code = event.GetKeyCode()
        if mod == 0:
            if code == event.getWXK('r'):
                self.read()
                return True
            elif code == event.getWXK('w'):
                self.write()
                return True
        event.Skip()


class InputWidget(BaseInputWidget):
    def __init__(self, name, label, addr, offsets=(), type_=int, size=4):
        super().__init__(name, label, addr, offsets)
        self.type = type_
        self.size = size

    @property
    def mem_value(self):
        ret = self._handler.ptrsRead(self.addr, self.offsets, self.type, self.size)
        if self.type is float:
            ret = float32(ret)
        return ret

    @mem_value.setter
    def mem_value(self, value):
        self._handler.ptrsWrite(self.addr, self.offsets, self.type(value), self.size)


class ProxyInputWidget(BaseInputWidget):
    def __init__(self, name, label, read, write):
        super().__init__(name, label, None, None)
        self.doRead = read
        self.doWrite = write

    @property
    def mem_value(self):
        return self.doRead()

    @mem_value.setter
    def mem_value(self, value):
        self.doWrite(value)


class ModelInputWidget(ModelWidget, BaseInputWidget):
    pass


class CheckBoxWidget(Widget):
    def __init__(self, name, label, addr, offsets=(), enableData=None, disableData=None):
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


class CoordWidget(TwoWayWidget):
    def __init__(self, name, label, addr, offsets=(), savable=False):
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
            with ui.Vertical(className="fill") as root:
                with ui.Horizontal(className="fill"):
                    with ui.Vertical(className="fill"):
                        with ui.FlexGridLayout(cols=2, vgap=10, className="fill") as grid:
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
                    self.listbox = ui.ListBox(className="expand left_padding", onselect=self.onListBoxSel)
                    self.listbox.setOnKeyDown(self.onListBoxKey)

                with ui.ContextMenu() as contextmenu:
                    ui.MenuItem("复制(&C)", onselect=self.onCopy)
                    ui.MenuItem("粘贴(&V)", onselect=self.onPaste)
                root.setContextMenu(contextmenu)

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
                value = float32(self._handler.readFloat(self.addr))
            ret.append(value)
        return ret

    @mem_value.setter
    def mem_value(self, values):
        offsets = list(self.offsets)
        it = iter(values)
        for child in self.views:
            value = next(it)
            if value is None or value == '':
                continue
            value = float(value)
            if offsets:
                self._handler.ptrsWrite(self.addr, offsets, value)
                offsets[-1] += 4
            else:
                self._handler.writeFloat(self.addr, value)

    @property
    def input_value(self):
        return map(lambda v: v.value and float(v.value), self.views)

    @input_value.setter
    def input_value(self, values):
        it = iter(values)
        for child in self.views:
            child.value = str(next(it))

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
        path = fefactory_api.choose_file("选择保存文件", file=self.lastfile, wildcard='*.json')
        if path:
            self.lastfile = path
            with open(path, 'w', encoding="utf-8") as file:
                json.dump(self.data_list, file, ensure_ascii=False)

    def onLoad(self, btn):
        path = fefactory_api.choose_file("选择要读取的文件", file=self.lastfile, wildcard='*.json')
        if path:
            self.lastfile = path
            with open(path, encoding="utf-8") as file:
                self.data_list = json.load(file)
                self.listbox.clear()
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

    def onCopy(self, _=None):
        fefactory_api.set_clipboard(str(tuple(self.input_value)))

    def onPaste(self, _=None):
        values = eval(fefactory_api.get_clipboard())
        self.input_value = values

class ModelCoordWidget(ModelWidget, CoordWidget):
    pass


class BaseSelectWidget(TwoWayWidget):
    def render(self):
        super().render()
        with ui.Horizontal(className="fill"):
            self.view = ui.Choice(className="fill", choices=self.choices)
            self.render_btn()

    @property
    def input_value(self):
        return self.view.index

    @input_value.setter
    def input_value(self, value):
        self.view.index = value


class SelectWidget(BaseSelectWidget):
    def __init__(self, name, label, addr, offsets, choices, type_=int, size=4):
        self.choices = choices
        self.type = type_
        self.size = size
        super().__init__(name, label, addr, offsets)

    @property
    def mem_value(self):
        return self._handler.ptrsRead(self.addr, self.offsets, self.type, self.size)

    @mem_value.setter
    def mem_value(self, value):
        self._handler.ptrsWrite(self.addr, self.offsets, self.type(value), self.size)


class ModelSelectWidget(ModelWidget, BaseSelectWidget):
    def __init__(self, name, label, ins, prop, choices):
        self.choices = choices
        super().__init__(name, label, ins, prop)


btn_style = {
    'width': 36,
}