import json
import fefactory
import pyapi
from pathlib import Path
from lib import ui, utils
from lib.win32.keys import WXK
from .widgets import ModelWidget, TwoWayWidget


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
            with ui.Horizontal(class_="expand") as container:
                if self.wrap:
                    with ui.Vertical(class_="fill"):
                        style = {'height': 54}
                        self.views = tuple(ui.TextInput(class_="fill padding_bottom", style=style)
                            for i in range(self.length))
                else:
                    self.views = tuple(ui.TextInput(class_="fill") for i in range(self.length))
                self.render_btn()
        else:
            views = []
            with ui.Vertical(class_="fill") as root:
                with ui.Horizontal(class_="fill"):
                    with ui.Vertical(style={'weight': 2}):
                        with ui.FlexGridLayout(cols=2, vgap=10, class_="fill") as grid:
                            grid.sizer.AddGrowableCol(1)
                            for label in self.labels or ('X坐标', 'Y坐标', 'Z坐标'):
                                ui.Label(label)
                                views.append(ui.TextInput(class_="fill"))
                            ui.Label("名称")
                            self.name_view = ui.TextInput(class_="fill")
                        with ui.Horizontal(class_="expand padding") as container:
                            self.render_btn()
                            ui.Button(label="添加", class_="button", onclick=this.onadd)
                            ui.Button(label="更新", class_="button", onclick=this.on_update)
                            ui.Button(label="删除", class_="button", onclick=this.ondelete)
                            ui.Button(label="保存", class_="button", onclick=this.on_save)
                            ui.Button(label="载入", class_="button", onclick=this.on_load)
                            if self.preset:
                                ui.Button(label="预设", class_="button", onclick=this.choose_preset)
                    self.listbox = ui.ListBox(class_="fill padding_left", onselect=this.on_listbox_sel)
                    self.listbox.set_on_keydown(this.on_listbox_key)

                with ui.ContextMenu() as contextmenu:
                    ui.MenuItem("复制(&C)", onselect=this.on_copy)
                    ui.MenuItem("粘贴(&V)", onselect=this.on_paste)
                    ui.MenuItem("清空列表(&E)", onselect=this.onclear)
            root.set_context_menu(contextmenu)
            self.views = tuple(views)
        self.view = self.views[0]
        self.container = container
        for view in self.views:
            view.set_on_keydown(self.onkey)

    @property
    def mem_value(self):
        offsets = list(self.offsets)
        addr = self.addr
        result = []
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
            result.append(value)
        return result

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
        self.listbox.Clear()
        self.lastfile = None

    def load(self, data_list):
        self.data_list = data_list
        self.listbox.Clear()
        self.listbox.Append(tuple(data['name'] for data in self.data_list))

    def onadd(self, btn):
        name = self.name_view.value
        if name:
            self.listbox.Append(name)
            self.data_list.append({'name': name, 'value': tuple(self.input_value)})

    def on_update(self, btn):
        pos = self.listbox.index
        if pos != -1:
            name = self.name_view.value
            if name:
                self.listbox.text = name
                self.data_list[pos] = {'name': name, 'value': tuple(self.input_value)}

    def ondelete(self, btn):
        pos = self.listbox.index
        if pos != -1:
            self.listbox.Delete(pos)
            self.data_list.pop(pos)

    def on_save(self, btn):
        def dumper(data, file):
            content = json.dumps(data, ensure_ascii=False).replace('{', '\n\t{')[:-1] + '\n]'
            file.write(content)

        fefactory.json_dump_file(self, self.data_list, dumper)

    def on_load(self, btn):
        data = fefactory.json_load_file(self)
        if data:
            self.load(data)

    def choose_preset(self, btn):
        if self.preset:
            dialog = ui.dialog.ChoiceDialog(
                "预设的坐标", (item[0] for item in self.preset.coords),
                onselect=self.weak.on_preset)
            self.dialog = dialog
            dialog.ShowModal()

    def on_preset(self, lb):
        self.dialog.EndModal()
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

    def on_listbox_sel(self, v):
        pos = self.listbox.index
        data = self.data_list[pos]
        self.name_view.value = data['name']
        self.input_value = data['value']

    def on_listbox_key(self, v, event):
        """按键监听"""
        mod = event.GetModifiers()
        code = event.GetKeyCode()
        if mod == WXK.MOD_CONTROL:
            if code == WXK.UP:
                self.move_up()
            elif code == WXK.DOWN:
                self.move_down()
        elif super().onkey(v, event):
            return True
        event.Skip()

    def move_up(self):
        """上移一项"""
        index = self.listbox.index
        if index != 0:
            self.data_list[index - 1], self.data_list[index] = self.data_list[index], self.data_list[index - 1]
            self.listbox.SetString(index, self.data_list[index]['name'])
            self.listbox.SetString(index - 1, self.data_list[index - 1]['name'])

    def move_down(self):
        """下移一项"""
        index = self.listbox.index
        if index != self.listbox.count - 1:
            self.data_list[index + 1], self.data_list[index] = self.data_list[index], self.data_list[index + 1]
            self.listbox.SetString(index, self.data_list[index]['name'])
            self.listbox.SetString(index + 1, self.data_list[index + 1]['name'])

    def on_copy(self, view, menu):
        pyapi.set_clipboard(str(tuple(self.input_value)))

    def on_paste(self, view, menu):
        values = eval(pyapi.get_clipboard())
        self.input_value = values

    def onclear(self, view, menu):
        self.clear()


class ModelCoordWidget(ModelWidget, CoordWidget):
    pass
