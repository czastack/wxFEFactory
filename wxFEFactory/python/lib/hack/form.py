from lib import exui, fileutils, utils, lazy
from lib.extypes import WeakBinder
from styles import styles, dialog_style, btn_xs_style
from __main__ import win as main_win
import json
import traceback
import types
import fefactory
import fefactory_api
ui = fefactory_api.ui


class Widget:
    GROUPS = []
    horizontal = True

    def __init__(self, name, label, addr, offsets=(), readonly=False):
        self.weak = WeakBinder(self)
        self.name = name
        self.label = name if label is None else label
        self.addr = addr
        self.offsets = offsets
        self.readonly = readonly

        parent = self.active_group()
        if parent:
            parent.appendChild(self)
            if self.addr is None:
                self.addr = getattr(parent, 'addr', None)

            if parent.handler:
                self.handler = parent.handler

        if isinstance(parent, Group) and not parent.horizontal:
            self.horizontal = False
            with ui.Vertical(className="expand"):
                self.render()
            del self.horizontal
        else:
            self.render()

    @classmethod
    def active_group(cls):
        return cls.GROUPS[-1] if len(cls.GROUPS) else None

    def render(self):
        ui.Text(self.label, className="input_label expand" if self.horizontal else "input_label_vertical")

    def render_btn(self):
        this = self.weak
        ui.Button(label="r", style=btn_xs_style, onclick=lambda btn: this.read())
        if not self.readonly:
            ui.Button(label="w", style=btn_xs_style, onclick=lambda btn: this.write())

    def onKey(self, v, event):
        mod = event.GetModifiers()
        code = event.GetKeyCode()
        if mod == 0:
            if code == event.getWXK('r'):
                self.read()
                return True
            elif code == event.getWXK('w') or code == 13:
                self.write()
                return True
        event.Skip()

    def read(self):
        pass

    def write(self):
        pass

    def __repr__(self):
        return '%s("%s", "%s")' % (self.__class__.__name__, self.name, self.label)


class TwoWayWidget(Widget):
    def read(self):
        value = self.mem_value
        if value is not None:
            self.input_value = value

    def write(self):
        if self.readonly:
            return
        value = self.input_value
        if value is not None:
            self.mem_value = value


class ModelWidget:
    def __init__(self, name, label=None, ins=None, prop=None, **kwargs):
        """
        :param ins: Model实例，或者返回Model实例的函数，在Widget中用addr占位
        :param prop: Widget对应Field的属性名称，在Widget中用offsets占位
        """
        super().__init__(name, label, addr=ins, offsets=prop or name, **kwargs)

    def render(self):
        if self.label is self.name and not callable(self.addr):
            # 从Field读取label
            field = self.addr.field(self.offsets)
            if field and field.label:
                self.label = field.label
        super().render()

    @property
    def ins(self):
        return self.addr() if callable(self.addr) else self.addr

    @property
    def mem_value(self):
        ins = self.ins
        if ins:
            return getattr(ins, self.offsets)

    @mem_value.setter
    def mem_value(self, value):
        ins = self.ins
        if ins:
            setattr(ins, self.offsets, value)

    @mem_value.deleter
    def mem_value(self):
        ins = self.ins
        if ins:
            delattr(ins, self.offsets)

    @property
    def field(self):
        # 尝试获取对应的模型字段
        ins = self.ins
        if ins and hasattr(ins, 'field'):
            return ins.field(self.offsets)


class OffsetsWidget:
    @property
    def mem_value(self):
        ret = self.handler.ptrsRead(self.addr, self.offsets, self.type, self.size)
        if self.type is float:
            ret = utils.float32(ret)
        return ret

    @mem_value.setter
    def mem_value(self, value):
        self.handler.ptrsWrite(self.addr, self.offsets, self.type(value), self.size)
    

class BaseGroup(Widget):
    cachable = True

    def __init__(self, name, label, addr, handler=None, cachable=True):
        """
        :param cachable: 子元素是ModelWidget时有用
        """
        self.children = []
        self.handler = handler
        cachable = cachable and callable(addr)
        if not cachable:
            self.cachable = False

        if cachable:
            self._ins_getter = addr
            self._ins_cached = False
            self._ins = None
            
        super().__init__(name, label, addr)

        if cachable:
            self.addr = self.weak.cached_ins_getter

    def __del__(self):
        self.children.clear()

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

    def cached_ins_getter(self):
        if self._ins_cached:
            if self._ins is None:
                # 获取Model实例并缓存
                self._ins = self._ins_getter()
            return self._ins

        return self._ins_getter()

    def start_ins_cache(self):
        if self.cachable:
            self._ins_cached = True

    def end_ins_cache(self):
        if self.cachable:
            self._ins_cached = False
            self._ins = None

    def read(self):
        self.start_ins_cache()
        for field in self.children:
            field.read()
        self.end_ins_cache()

    def write(self):
        self.start_ins_cache()
        for field in self.children:
            field.write()
        self.end_ins_cache()

    def load(self):
        data = fefactory.json_load_file(self)
        if data:
            for field in self.children:
                try:
                    value = data.get(field.name, None)
                    if value is not None:
                        field.input_value = value
                except Exception as e:
                    print("加载字段%s出错" % field.name, e.args)

    def export(self):
        data = {field.name: field.input_value for field in self.children if field.input_value is not None}
        fefactory.json_dump_file(self, data)

    def after_lazy(self):
        """lazy_group渲染后调用"""
        pass


class Group(BaseGroup):
    cols = 2
    horizontal = True

    def __init__(self, *args, flexgrid=True, hasheader=False, hasfooter=True, horizontal=True, cols=None, **kwargs):
        self.flexgrid = flexgrid
        self.hasheader = hasheader
        self.hasfooter = hasfooter
        if cols:
            self.cols = cols
        if not horizontal:
            self.horizontal = horizontal
        super().__init__(*args, **kwargs)

    def render(self):
        root = self.render_root()
        ui.Item(root, caption=self.label)
        self.root = root

    def render_root(self):
        this = self.weak
        with ui.Vertical(className="fill") as root:
            if self.hasheader:
                self.header = ui.Horizontal(className="expand container")

            with ui.ScrollView(className="fill container") as content:
                if self.flexgrid:
                    self.view = ui.FlexGridLayout(cols=self.cols, vgap=10, hgap=10, className="fill")
                    if self.horizontal:
                        for i in range(self.cols >> 1):
                            self.view.AddGrowableCol((i << 1) + 1)
                    else:
                        for i in range(self.cols):
                            self.view.AddGrowableCol(i)
                else:
                    self.view = content

            if self.hasfooter:
                with ui.Horizontal(className="expand container") as footer:
                    ui.Button(label="读取", className="btn_sm", onclick=lambda btn: this.read())
                    ui.Button(label="写入", className="btn_sm", onclick=lambda btn: this.write())
                    ui.Button(label="导入", className="btn_sm", onclick=lambda btn: this.load())
                    ui.Button(label="导出", className="btn_sm", onclick=lambda btn: this.export())
                self.footer = footer
        del self.flexgrid, self.hasheader, self.hasfooter
        return root

    def after_lazy(self):
        if isinstance(self.view, ui.FlexGridLayout):
            self.view.parent.reLayout()


class DialogGroup(Group):
    def __init__(self, *args, button=True, **kwargs):
        self.button = button
        self.dialog_style = kwargs.pop('dialog_style', None)
        super().__init__(*args, **kwargs)

    def render(self):
        if self.button:
            ui.Button(label=self.label, onclick=self.weak.show)
            
        style = dict(dialog_style, **self.dialog_style) if self.dialog_style else dialog_style
        with main_win:
            with exui.StdDialog(self.label, style=style, styles=styles) as root:
                self.render_root()

        self.root = root
        del self.button

    def show(self, _=None):
        self.root.show()

    def showModal(self, _=None):
        self.root.showModal()


class StaticGroup(Group):
    def __init__(self, caption):
        return Group.__init__(self, None, caption, 0, flexgrid=False, hasfooter=False)


class GroupBox(BaseGroup):
    def render(self):
        with ui.StaticBox(self.label, className="fill") as root:
            self.view = ui.ScrollView(className="fill container")

        self.root = root


class BaseInput(TwoWayWidget):
    def __init__(self, *args, hex=False, spin=False, size=4, max=None, **kwargs):
        """size: hex为True时有用"""
        self.hex = hex and not spin
        self.spin = spin
        self.size = size
        self.max = max
        super().__init__(*args, **kwargs)

    def render(self):
        super().render()
        with ui.Horizontal(className="fill") as container:
            if self.spin:
                self.view = ui.SpinCtrl(className="fill", wxstyle=0x4400, max=self.max or (1 << (self.size << 3) - 1) - 1)
            else:
                self.view = ui.TextInput(className="fill", wxstyle=0x0400, readonly=self.readonly)
            del self.max
            self.render_btn()
            self.view.setOnKeyDown(self.weak.onKey)
        self.container = container

    @property
    def input_value(self):
        value = self.view.value
        if not self.spin:
            if value == '':
                return None
            if self.hex or value.startswith('0x'):
                value = int(value, 16)
        return value

    @input_value.setter
    def input_value(self, value):
        if not self.spin:
            value = ("0x%0*X" % (self.size << 1, value)) if self.hex else str(value)
        self.view.value = value


class Input(BaseInput, OffsetsWidget):
    def __init__(self, *args, type=int, **kwargs):
        self.type = type
        super().__init__(*args, **kwargs)


class ModelInput(ModelWidget, BaseInput):
    pass


class ProxyInput(BaseInput):
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


class SimpleCheckBox(Widget):
    """采用切换事件的立即模式"""
    def __init__(self, name, label, addr, offsets=(), enableData=None, disableData=None, size=None):
        """
        :param enableData: 激活时写入的数据
        :param disableData: 关闭时写入的数据
        """
        super().__init__(name, label, addr, offsets)
        self.enableData = enableData
        self.disableData = disableData
        if size is None:
            if isinstance(enableData, bytes):
                size = len(enableData)
            else:
                size = 4
        self.size = size

    def render(self):
        self.view = ui.CheckBox(self.label, onchange=self.weak.onChange)

    def onChange(self, checkbox):
        data = self.enableData if checkbox.checked else self.disableData
        self.handler.ptrsWrite(self.addr, self.offsets, data, self.size)


class BaseCheckBox(TwoWayWidget):
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
        super().render()
        with ui.Horizontal(className="fill") as container:
            self.view = ui.CheckBox("", className="fill")
            self.render_btn()
        self.container = container

    @property
    def input_value(self):
        return self.enableData if self.view.checked else self.disableData

    @input_value.setter
    def input_value(self, value):
        if value == self.enableData:
            self.view.checked = True
        elif self.disableData is None or value == self.disableData:
            self.view.checked = False


class CheckBox(BaseCheckBox, OffsetsWidget):
    pass


class ModelCheckBox(ModelWidget, BaseCheckBox):
    @property
    def input_value(self):
        if self.enableData is None:
            return self.view.checked
        return super().input_value

    @input_value.setter
    def input_value(self, value):
        if self.enableData is None:
            self.view.checked = value
        else:
            super().input_value = value


class CoordWidget(TwoWayWidget):
    def __init__(self, name, label, addr, offsets=(), length=3, type=float, size=4, savable=False, preset=None):
        """
        :param length: 坐标维数
        :param saveble: 是否支持存取文件
        :param preset: 预设坐标模块(要读__file__属性)
        """
        self.length = length
        self.type = type
        self.size = size
        self.savable = savable
        self.preset = preset
        if savable:
            self.data_list = []
            self.lastfile = None

        super().__init__(name, label, addr, offsets)

    def render(self):
        this = self.weak
        super().render()
        if not self.savable:
            with ui.Horizontal(className="expand") as container:
                self.views = tuple(ui.TextInput(className="fill") for i in range(self.length))
                self.render_btn()

        else:
            views = []
            with ui.Vertical(className="fill") as root:
                with ui.Horizontal(className="fill"):
                    with ui.Vertical(style={'flex': 2}):
                        with ui.FlexGridLayout(cols=2, vgap=10, className="fill") as grid:
                            grid.AddGrowableCol(1)
                            for i, v in zip(range(self.length), ('X', 'Y', 'Z')):
                                ui.Text("%s坐标" % v, className="input_label expand")
                                views.append(ui.TextInput(className="fill"))
                            ui.Text("名称", className="input_label expand")
                            self.name_view = ui.TextInput(className="fill")
                        with ui.Horizontal(className="expand container") as container:
                            self.render_btn()
                            ui.Button(label="添加", className="button", onclick=this.onAdd)
                            ui.Button(label="更新", className="button", onclick=this.onUpdate)
                            ui.Button(label="删除", className="button", onclick=this.onDel)
                            ui.Button(label="保存", className="button", onclick=this.onSave)
                            ui.Button(label="载入", className="button", onclick=this.onLoad)
                            if self.preset:
                                ui.Button(label="预设", className="button", onclick=this.choosePreset)
                    self.listbox = ui.ListBox(className="fill left_padding", onselect=this.onListBoxSel)
                    self.listbox.setOnKeyDown(this.onListBoxKey)

                with ui.ContextMenu() as contextmenu:
                    ui.MenuItem("复制(&C)", onselect=this.onCopy)
                    ui.MenuItem("粘贴(&V)", onselect=this.onPaste)
                    ui.MenuItem("清空列表(&E)", onselect=this.onClear)
                root.setContextMenu(contextmenu)
            self.views = tuple(views)
        self.view = self.views[0]
        self.container = container

    @property
    def mem_value(self):
        offsets = list(self.offsets)
        addr = self.addr
        ret = []
        for child in self.views:
            if offsets:
                value = self.handler.ptrsRead(addr, offsets, self.type, self.size)
                offsets[-1] += self.size
            else:
                if self.type is float:
                    value = utils.float32(self.handler.readFloat(addr))
                else:
                    value = self.handler.read(addr, self.type, self.size)
                addr += self.size
            ret.append(value)
        return ret

    @mem_value.setter
    def mem_value(self, values):
        offsets = list(self.offsets)
        addr = self.addr
        it = iter(values)
        for child in self.views:
            value = next(it)
            if value is None or value == '':
                continue
            value = self.type(value)
            if offsets:
                self.handler.ptrsWrite(addr, offsets, value, self.size)
                offsets[-1] += self.size
            else:
                self.handler.write(addr, value, self.size)
                addr += self.size

    @property
    def input_value(self):
        return map(lambda v: v.value and self.type(v.value), self.views)

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
        def dumper(data, file):
            content = json.dumps(data, ensure_ascii=False).replace('{', '\n\t{')[:-1] + '\n]'
            file.write(content)

        fefactory.json_dump_file(self, self.data_list, dumper)

    def onLoad(self, btn):
        data = fefactory.json_load_file(self)
        if data:
            self.load(data)

    def choosePreset(self, btn):
        if self.preset:
            dialog = exui.ChoiceDialog("预设的坐标", (item[0] for item in self.preset.coords), onselect=self.weak.onPreset)
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

    def onCopy(self, v, m):
        fefactory_api.set_clipboard(str(tuple(self.input_value)))

    def onPaste(self, v, m):
        values = eval(fefactory_api.get_clipboard())
        self.input_value = values

    def onClear(self, v, m):
        self.clear()


class ModelCoordWidget(ModelWidget, CoordWidget):
    pass


class BaseSelect(TwoWayWidget):
    search_map = {}

    def __init__(self, *args, choices=None, values=None, onselect=None, **kwargs):
        # 预处理choices, values
        if values is None:
            list_tuple = (list, tuple)
            if not isinstance(choices, list_tuple):
                choices = tuple(choices)
            if choices and isinstance(choices[0], list_tuple):
                choices, values = utils.split_value_label(choices)
        self.choices = choices
        self.values = values
        self.onselect = onselect
        super().__init__(*args, **kwargs)

    def render(self):
        super().render()
        with ui.Horizontal(className="fill") as container:
            self.view = ui.Choice(className="fill", choices=self.choices, onselect=self.onselect)
            self.view.setContextMenu(self.contextmenu)
            self.view.setOnDestroy(self.weak.onDestroy)
            self.render_btn()
        self.container = container
        self.view.setOnKeyDown(self.weak.onKey)
        self.search_map[id(self.view)] = self
        del self.onselect

    def setItems(self, choices, values=0):
        self.choices = choices
        self.view.setItems(choices)
        if values is not 0:
            self.values = values

    @property
    def input_value(self):
        index = self.view.index
        if index is -1:
            return None
        return self.values[index] if self.values else index

    @input_value.setter
    def input_value(self, value):
        try:
            self.view.index = self.values.index(value) if self.values else value
        except ValueError:
            print(hex(value), "不在%s的可选值中" % self.label)

    @lazy.ClassLazy
    def contextmenu(cls):
        with ui.ContextMenu() as contextmenu:
            ui.MenuItem("搜索(&S)", onselect=cls.onSearch)
        return contextmenu

    @lazy.ClassLazy
    def search_dialog(cls):
        return exui.SearchDialog("搜索", onselect=cls.onsearch_select, onsearch=cls.onsearch)

    @classmethod
    def onSearch(cls, v, m):
        cls.active_ins = cls.search_map[id(v)]
        if getattr(cls, 'search_last_choices', None) is not cls.active_ins.choices:
            cls.search_dialog.listbox.clear()
        else:
            cls.search_dialog.listbox.index = -1
        cls.search_dialog.showModal()
        del cls.active_ins

    @classmethod
    def onsearch(cls, dialog, value):
        choices = []
        values = []
        i = 0
        for item in cls.active_ins.choices:
            if value in item:
                choices.append(item)
                values.append(i)
            i += 1
        cls.search_dialog.listbox.setItems(choices)
        cls.search_last_choices = cls.active_ins.choices # 上次搜索的内容集
        cls.search_values = values

    @classmethod
    def onsearch_select(cls, view):
        # 搜索结果选择后切换到对应的序号
        cls.active_ins.view.setSelection(cls.search_values[view.index], True)
        cls.search_dialog.endModal()

    def onDestroy(self, view):
        self.search_map.pop(id(view), None)

class Select(BaseSelect, OffsetsWidget):
    def __init__(self, *args, type=int, size=4, **kwargs):
        self.type = type
        self.size = size
        super().__init__(*args, **kwargs)


class ModelSelect(ModelWidget, BaseSelect):
    pass


class BaseFlagWidget(TwoWayWidget):
    def __init__(self, *args, labels=None, helps=None, values=None, checkbtn=False, cols=None, **kwargs):
        """size: hex为True时有用"""
        self.labels = labels
        self.helps = helps
        self.values = values or tuple(1 << i for i in range(len(labels)))
        self.checkbtn = checkbtn
        self.cols = cols
        super().__init__(*args, **kwargs)

    def render(self):
        ui.Text(self.label, className="form_label expand")
        with ui.Horizontal(className="fill") as container:
            if self.cols is not None:
                view = ui.GridLayout(cols=self.cols, vgap=10, className="fill")
            else:
                view = ui.Horizontal(className="fill")
            with view:
                self.views = tuple(
                    ui.CheckBox(label) for label in self.labels
                )
                if self.helps:
                    for view, help in zip(self.views, self.helps):
                        view.setToolTip(help)
            if self.checkbtn:
                ui.Button(label="全选", style=btn_xs_style, onclick=self.weak.check_all)
                ui.Button(label="不选", style=btn_xs_style, onclick=self.weak.uncheck_all)
            self.render_btn()
        self.view = view
        self.container = container
        self.helps, self.cols

    @property
    def input_value(self):
        value = 0
        for i in range(len(self.labels)):
            if self.views[i].checked:
                value |= self.values[i]
            
        return value

    @input_value.setter
    def input_value(self, value):
        for i in range(len(self.labels)):
            self.views[i].checked = value & self.values[i]

    def check_all(self, _=None):
        for view in self.views:
            view.checked = True

    def uncheck_all(self, _=None):
        for view in self.views:
            view.checked = False


class FlagWidget(BaseFlagWidget, OffsetsWidget):
    def __init__(self, *args, type=int, size=4, **kwargs):
        self.type = type
        self.size = size
        super().__init__(*args, **kwargs)


class ModelFlagWidget(ModelWidget, BaseFlagWidget):
    pass


def render_tab_list(data):
    book = ui.Notebook(className="fill", wxstyle=0x0200)
    with book:
        for category in data:
            ui.Item(ui.ListBox(className="expand", choices=(item[0] for item in category[1])), caption=category[0])
    return book
