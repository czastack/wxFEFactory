import pyapi
from lib import ui
from ..module import BaseListBoxModuel
from . import forms
from . import config


class Module(BaseListBoxModuel):

    def __init__(self):
        super().__init__()
        self.form = forms.CharacterForm()
        self._pg_inited = False
        self.data_map = {}

    def attach(self, frame):
        super().attach(frame)

        data_list = self.load_json('characters', [])
        for item in data_list:
            self.data_map[item['name']] = item
            self.append(item['name'])

    def render_main(self):
        this = self.weak
        with ui.Horizontal(class_="padding expand") as infobar:
            ui.ComboBox(wxstyle=ui.wx.CB_READONLY, choices=('地址预览', *(key for key in config.ADDR_MAP)),
                        onselect=this.on_preview_addr_choice_change).set_selection(0, True)
            ui.Text("地址", class_="vcenter input_label")
            self.addr_view = ui.TextInput(readonly=True)
            ui.Text("说明", class_="vcenter input_label")
            self.help_view = ui.TextInput(readonly=True, class_="fill")

        self.pg = ui.PropertyGrid(class_="fill")
        with ui.Horizontal(class_="expand"):
            ui.CheckBox(label="自动保存", checked=True, onchange=this.on_swich_auto_save, class_="vcenter")
            ui.Button(label="保存该项", class_="button", onclick=this.on_saveIt)
            ui.Button(label="保存文件", class_="button", onclick=this.on_save)

        self.pg.autosave = True
        self.pg.set_onchange(this.on_pg_change)
        self.pg.set_on_selected(this.on_field_select)

    @property
    def title(self):
        return self.form.title

    def on_field_select(self, pg, name):
        # 预览地址
        addr = self.get_property_addr(name)
        if addr:
            self.addr_view.value = "%08X" % addr
        else:
            self.addr_view.value = ""

    def onclose(self, _=None):
        if self.pg.changed:
            choice = self.confirm('保存修改', '有修改，是否保存？', ui.wx.CANCEL)
            if choice is ui.wx.CANCEL:
                return False
            elif choice is ui.wx.YES:
                self.on_save(None)
        return super().onclose()

    def onadd(self, btn):
        name = input("角色名称")
        if name:
            self.append(name)

    def append(self, name, data=None):
        """
        添加列表项
        """
        super().append(name)
        if name not in self.data_map:
            self.data_map[name] = data or {'name': name}

    def ondelete(self, btn):
        pos, text = super().ondelete(btn)
        if text:
            self.data_map.pop(text, None)

    def on_rename(self, menu):
        args = super().on_rename(menu)
        if args:
            name, newname = args
            item = self.data_map[newname] = self.data_map.pop(name)
            item['name'] = newname
            self.pg.set_values({'name': newname})

    def on_saveIt(self, btn):
        item_data = self.get_cur_data()
        if item_data:
            item_data.update(self.pg.get_values())

    def on_save(self, btn):
        self.pg.changed = False
        self.dump_json('characters', list(self.itervalues()))

    def get_cur_data(self):
        text = self.listbox.text
        if text:
            return self.data_map[text]

    def on_list_select(self, _):
        if self._pg_inited is False:
            self._pg_inited = True
            self.form.init_pg(self.pg)

        self._lastpos = self.listbox.index
        self.pg.bind_data(self.get_cur_data())

    def on_pg_change(self, pg, name, value):
        if name == 'name':
            if value != self.listbox.text and value in self.listbox.get_texts():
                pyapi.alert('名称已存在')
                return False
            self.listbox[self._lastpos] = value

    def onclear(self, menu):
        """清空列表"""
        if super().onclear(menu):
            self.data_map = {}

    def on_swich_auto_save(self, checkbox):
        self.pg.autosave = checkbox.checked

    def on_preview_addr_choice_change(self, choice):
        """预览地址选项改变"""
        if choice.index:
            key = choice.text
            self.preview_addr_conf = config.ADDR_MAP[key]
        else:
            self.preview_addr_conf = None

    def get_property_addr(self, name):
        """获取某字段的预览地址"""
        if self.preview_addr_conf:
            field = self.form.cfield(name)
            if field:
                base = self.preview_addr_conf['addr']
                step = self.preview_addr_conf['step']
                return base + self.listbox.index * step + field.offset

    def itervalues(self):
        for text in self.listbox.get_texts():
            yield self.data_map[text]

    def read_from(self, reader):
        conf = config.ADDR_MAP[reader.key]
        count = 0xFF
        buff = reader.read(conf['addr'], count * conf['step'])
        ptr = self.form.ptr_from_bytes(buff, len(buff))
        texts = []
        for i in range(count):
            item = self.form.struct_to_dict(ptr[i])
            name = reader.get_text_entry_text(item['name'])
            item['name'] = name
            item['title'] = reader.get_text_entry_text(item['title'])
            self.data_map[name] = item
            texts.append(name)

        super().append(texts)
