from lib import exui, fileutils
from lib.utils import float32
from styles import btn_xsm_style
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

            if parent.handler:
                self.handler = parent.handler
        self.render()
        if hasattr(self, 'view'):
            self.view.setOnDestroy(self.onDestroy)

    def __del__(self):
        pass

    def render(self):
        ui.Text(self.label, className="label_left expand")

    def render_btn(self):
        ui.Button(label="r", style=btn_xsm_style, onclick=lambda btn: self.read())
        ui.Button(label="w", style=btn_xsm_style, onclick=lambda btn: self.write())

    def read(self):
        pass

    def write(self):
        pass

    def onDestroy(self, view):
        del self.view

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

    @mem_value.deleter
    def mem_value(self):
        ins = self.ins
        if ins:
            prop = self.offsets
            if isinstance(prop, str):
                delattr(ins, prop)
            else:
                prop.__delete__(ins, value)
    

class Group(Widget):

    def __init__(self, name, label, addr, flexgrid=True, hasfootbar=True, handler=None):
        self.flexgrid = flexgrid
        self.hasfootbar = hasfootbar
        self.children = []
        self.handler = handler
        super().__init__(name, label, addr)

    def __del__(self):
        super().__del__()
        self.children.clear()

    def onDestroy(self, view):
        super().onDestroy(view)
        del self.root

    def render(self):
        with ui.Vertical() as root:
            with ui.ScrollView(className="fill container") as content:
                if self.flexgrid:
                    self.view = ui.FlexGridLayout(cols=2, vgap=10, className="fill")
                    self.view.AddGrowableCol(1)
                else:
                    self.view = content

            if self.hasfootbar:
                with ui.Horizontal(className="container"):
                    ui.Button(label="读取", className="button", onclick=lambda btn: self.read())
                    ui.Button(label="写入", className="button", onclick=lambda btn: self.write())
        ui.Item(root, caption=self.label)
        self.root = root

    def appendChild(self, child):
        self.children.append(child)

    def __enter__(self):
        self.view.__enter__()
        self.GROUPS.append(self)
        return self

    def __exit__(self, *args):
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


class StaticGroup(Group):
    def __init__(self, caption):
        return Group.__init__(self, None, caption, 0, False, False)


class BaseInputWidget(TwoWayWidget):
    def render(self):
        super().render()
        with ui.Horizontal(className="fill"):
            self.view = ui.TextInput(className="fill", wxstyle=0x0400)
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
        ret = self.handler.ptrsRead(self.addr, self.offsets, self.type, self.size)
        if self.type is float:
            ret = float32(ret)
        return ret

    @mem_value.setter
    def mem_value(self, value):
        self.handler.ptrsWrite(self.addr, self.offsets, self.type(value), self.size)


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


class SimpleCheckBoxWidget(Widget):
    """采用切换事件的立即模式"""
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
        self.handler.ptrsWrite(self.addr, self.offsets, data, len(data))


class BaseCheckBoxWidget(TwoWayWidget):
    def __init__(self, name, label, addr, offsets=(), enableData=None, disableData=None):
        """
        :param enableData: 激活时写入的数据
        :param disableData: 关闭时写入的数据
        """
        super().__init__(name, label, addr, offsets)
        self.enableData = enableData
        self.disableData = disableData
        self.type = type(enableData)

    def render(self):
        self.view = ui.CheckBox(self.label)

    @property
    def input_value(self):
        return self.enableData if self.view.checked else self.disableData

    @input_value.setter
    def input_value(self, value):
        if value == self.enableData:
            self.checked = True
        elif self.disableData is None or value == self.disableData:
            self.checked = False


class CheckBoxWidget(BaseCheckBoxWidget):

    @property
    def mem_value(self):
        ret = self.handler.ptrsRead(self.addr, self.offsets, self.type, self.size)
        if self.type is float:
            ret = float32(ret)
        return ret

    @mem_value.setter
    def mem_value(self, value):
        self.handler.ptrsWrite(self.addr, self.offsets, self.type(value), self.size)


class ModelCheckBoxWidget(ModelWidget, CheckBoxWidget):
    pass


class CoordWidget(TwoWayWidget):
    def __init__(self, name, label, addr, offsets=(), savable=False, preset=None):
        """
        :param saveble: 是否支持存取文件
        :param preset: 预设坐标模块(要读__file__属性)
        """
        self.savable = savable
        self.preset = preset
        if savable:
            self.data_list = []
            self.lastfile = None

        super().__init__(name, label, addr, offsets)

    def onDestroy(self, view):
        super().onDestroy(view)
        del self.views
        if self.savable:
            del self.listbox

    def render(self):
        super().render()
        if not self.savable:
            with ui.Horizontal(className="expand"):
                x_view = ui.TextInput(className="fill")
                y_view = ui.TextInput(className="fill")
                z_view = ui.TextInput(className="fill")
                self.render_btn()

        else:
            with ui.Vertical(className="fill") as root:
                with ui.Horizontal(className="fill"):
                    with ui.Vertical(className="fill"):
                        with ui.FlexGridLayout(cols=2, vgap=10, className="fill") as grid:
                            grid.AddGrowableCol(1)
                            ui.Text("X坐标", className="label_left expand")
                            x_view = ui.TextInput(className="fill")
                            ui.Text("Y坐标", className="label_left expand")
                            y_view = ui.TextInput(className="fill")
                            ui.Text("Z坐标", className="label_left expand")
                            z_view = ui.TextInput(className="fill")
                            ui.Text("名称", className="label_left expand")
                            self.name_view = ui.TextInput(className="fill")
                        with ui.Horizontal(className="container"):
                            self.render_btn()
                            ui.Button(label="添加", className="button", onclick=self.onAdd)
                            ui.Button(label="更新", className="button", onclick=self.onUpdate)
                            ui.Button(label="删除", className="button", onclick=self.onDel)
                            ui.Button(label="保存", className="button", onclick=self.onSave)
                            ui.Button(label="载入", className="button", onclick=self.onLoad)
                            if self.preset:
                                ui.Button(label="预设", className="button", onclick=self.choosePreset)
                    self.listbox = ui.ListBox(className="expand left_padding", onselect=self.onListBoxSel)
                    self.listbox.setOnKeyDown(self.onListBoxKey)

                with ui.ContextMenu() as contextmenu:
                    ui.MenuItem("复制(&C)", onselect=self.onCopy)
                    ui.MenuItem("粘贴(&V)", onselect=self.onPaste)
                    ui.MenuItem("清空列表(&E)", onselect=self.onClear)
                root.setContextMenu(contextmenu)

        self.views = (x_view, y_view, z_view)
        self.view = x_view

    @property
    def mem_value(self):
        offsets = list(self.offsets)
        ret = []
        for child in self.views:
            if offsets:
                value = self.handler.ptrsRead(self.addr, offsets, float)
                offsets[-1] += 4
            else:
                value = float32(self.handler.readFloat(self.addr))
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
                self.handler.ptrsWrite(self.addr, offsets, value)
                offsets[-1] += 4
            else:
                self.handler.writeFloat(self.addr, value)

    @property
    def input_value(self):
        return map(lambda v: v.value and float(v.value), self.views)

    @input_value.setter
    def input_value(self, values):
        it = iter(values)
        for child in self.views:
            child.value = str(next(it))

    def clear(self):
        self.data_list = []
        self.listbox.clear()
        self.lastfile = None

    def load(self, data_list):
        self.data_list = data_list
        self.listbox.clear()
        self.listbox.appendItems(tuple(data['name'] for data in self.data_list))

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
                # json.dump(self.data_list, file, ensure_ascii=False)
                content = json.dumps(self.data_list, ensure_ascii=False).replace('{', '\n\t{')[:-1] + '\n]'
                file.write(content)

    def onLoad(self, btn):
        path = fefactory_api.choose_file("选择要读取的文件", file=self.lastfile, wildcard='*.json')
        if path:
            self.lastfile = path
            with open(path, encoding="utf-8") as file:
                self.load(json.load(file))

    def choosePreset(self, btn):
        if self.preset:
            dialog = exui.ChoiceDialog("预设的坐标", (item[0] for item in self.preset.coords), onselect=self.onPreset)
            self.dialog = dialog
            dialog.showModal()

    def onPreset(self, lb):
        self.dialog.endModal()
        del self.dialog
        coords = self.preset.coords
        path = fileutils.brother(self.preset.__file__, coords[lb.index][1]) + '.json'
        with open(path, encoding="utf-8") as file:
            data = json.load(file)
            if data and isinstance(data, list):
                if isinstance(data[0], list):
                    name = coords[lb.index][0] + '%d'
                    data = [{'name': name % (i + 1), 'value': data[i]} for i in range(len(data))]
                self.load(data)

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

    def onClear(self, _=None):
        self.clear()

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
        return self.handler.ptrsRead(self.addr, self.offsets, self.type, self.size)

    @mem_value.setter
    def mem_value(self, value):
        self.handler.ptrsWrite(self.addr, self.offsets, self.type(value), self.size)


class ModelSelectWidget(ModelWidget, BaseSelectWidget):
    def __init__(self, name, label, ins, prop, choices):
        self.choices = choices
        super().__init__(name, label, ins, prop)


def render_tab_list(data):
    book = ui.Notebook(className="fill", wxstyle=0x0200)
    with book:
        for category in data:
            ui.Item(ui.ListBox(className="expand", choices=(item[0] for item in category[1])), caption=category[0])
    return book
