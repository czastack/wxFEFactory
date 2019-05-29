import json
import fefactory
import fefactory_api
from pathlib import Path
from lib import exui, utils
from lib.win32.keys import WXK
from .widgets import ModelWidget, TwoWayWidget
ui = fefactory_api.ui


class CoordWidget(TwoWayWidget):
    def __init__(self, name, label, addr, offsets=(), length=3, type=float, size=4,
            labels=None, savable=False, wrap=False, preset=None):
        """
        :param length: 坐标维数
        :param saveble: 是否支持存取文件
        :param wrap: saveble为False时是否折行
        :param preset: 预设坐标模块(要读__file__属性)
        """
        self.length = length
        self.type = type
        self.size = size
        self.labels = labels
        self.savable = savable
        self.wrap = wrap
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
                if self.wrap:
                    with ui.Vertical(className="fill"):
                        style = {'height': 54}
                        self.views = tuple(ui.TextInput(className="fill padding_bottom", style=style)
                            for i in range(self.length))
                else:
                    self.views = tuple(ui.TextInput(className="fill") for i in range(self.length))
                self.render_btn()
        else:
            views = []
            with ui.Vertical(className="fill") as root:
                with ui.Horizontal(className="fill"):
                    with ui.Vertical(style={'weight': 2}):
                        with ui.FlexGridLayout(cols=2, vgap=10, className="fill") as grid:
                            grid.AddGrowableCol(1)
                            for label in self.labels or ('X坐标', 'Y坐标', 'Z坐标'):
                                exui.Label(label)
                                views.append(ui.TextInput(className="fill"))
                            exui.Label("名称")
                            self.name_view = ui.TextInput(className="fill")
                        with ui.Horizontal(className="expand padding") as container:
                            self.render_btn()
                            ui.Button(label="添加", className="button", onclick=this.onAdd)
                            ui.Button(label="更新", className="button", onclick=this.onUpdate)
                            ui.Button(label="删除", className="button", onclick=this.onDel)
                            ui.Button(label="保存", className="button", onclick=this.onSave)
                            ui.Button(label="载入", className="button", onclick=this.onLoad)
                            if self.preset:
                                ui.Button(label="预设", className="button", onclick=this.choosePreset)
                    self.listbox = ui.ListBox(className="fill padding_left", onselect=this.onListBoxSel)
                    self.listbox.setOnKeyDown(this.onListBoxKey)

                with ui.ContextMenu() as contextmenu:
                    ui.MenuItem("复制(&C)", onselect=this.onCopy)
                    ui.MenuItem("粘贴(&V)", onselect=this.onPaste)
                    ui.MenuItem("清空列表(&E)", onselect=this.onClear)
                root.setContextMenu(contextmenu)
            self.views = tuple(views)
        self.view = self.views[0]
        self.container = container
        for view in self.views:
            view.setOnKeyDown(self.onKey)

    @property
    def mem_value(self):
        offsets = list(self.offsets)
        addr = self.addr
        ret = []
        for child in self.views:
            if offsets:
                value = self.handler.ptrs_read(addr, offsets, self.type, self.size)
                offsets[-1] += self.size
            else:
                if self.type is float:
                    value = utils.float32(self.handler.read_float(addr))
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
                self.handler.ptrs_write(addr, offsets, value, self.size)
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
        path = Path(self.preset.__file__).with_name(coords[lb.index][1] + '.json')
        with path.open(encoding="utf-8") as file:
            data = json.load(file)
            if data and isinstance(data, list):
                if isinstance(data[0], list):
                    name = coords[lb.index][0] + '%d'
                    data = [{'name': name % (i + 1), 'value': data[i]} for i in range(len(data))]
                self.load(data)

    def onListBoxSel(self, v):
        pos = self.listbox.index
        data = self.data_list[pos]
        self.name_view.value = data['name']
        self.input_value = data['value']

    def onListBoxKey(self, v, event):
        """按键监听"""
        mod = event.GetModifiers()
        code = event.GetKeyCode()
        if mod == WXK.MOD_CONTROL:
            if code == WXK.UP:
                self.move_up()
            elif code == WXK.DOWN:
                self.move_down()
        elif super().onKey(v, event):
            return True
        event.Skip()

    def move_up(self):
        """上移一项"""
        index = self.listbox.index
        if index != 0:
            self.data_list[index - 1], self.data_list[index] = self.data_list[index], self.data_list[index - 1]
            self.listbox.setText(self.data_list[index]['name'], index)
            self.listbox.setText(self.data_list[index - 1]['name'], index - 1)

    def move_down(self):
        """下移一项"""
        index = self.listbox.index
        if index != self.listbox.count - 1:
            self.data_list[index + 1], self.data_list[index] = self.data_list[index], self.data_list[index + 1]
            self.listbox.setText(self.data_list[index]['name'], index)
            self.listbox.setText(self.data_list[index + 1]['name'], index + 1)

    def onCopy(self, view, menu):
        fefactory_api.set_clipboard(str(tuple(self.input_value)))

    def onPaste(self, view, menu):
        values = eval(fefactory_api.get_clipboard())
        self.input_value = values

    def onClear(self, view, menu):
        self.clear()


class ModelCoordWidget(ModelWidget, CoordWidget):
    pass
