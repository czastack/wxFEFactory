from lib import wxconst
from ..module import BaseListBoxModuel
from . import forms
from . import config
from mainframe import ui
import fefactory_api


class Module(BaseListBoxModuel):

    def __init__(self):
        super().__init__()
        self.form = forms.CharacterForm()
        self._pg_inited = False
        self.data_map = {}

    def attach(self, frame):
        super().attach(frame)

        data_list = self.loadJson('characters', [])
        for item in data_list:
            self.data_map[item['name']] = item
            self.doAdd(item['name'])

    def render_main(self):
        this = self.weak
        with ui.Horizontal(className="container expand") as infobar:
            ui.ComboBox(type="readonly", choices=('地址预览', *(key for key in config.ADDR_MAP)), 
                onselect=this.onPreviewAddrChoiceChange).setSelection(0, True)
            ui.Text("地址", className="vcenter input_label")
            self.addr_view = ui.TextInput(readonly=True)
            ui.Text("说明", className="vcenter input_label")
            self.help_view = ui.TextInput(readonly=True, className="fill")

        self.pg = ui.PropertyGrid(className="fill")
        with ui.Horizontal(className="expand"):
            ui.CheckBox(label="自动保存", checked=True, onchange=this.onSwichAutoSave, className="vcenter")
            ui.Button(label="保存该项", className="button", onclick=this.onSaveIt)
            ui.Button(label="保存文件", className="button", onclick=this.onSave)

        self.pg.autosave = True
        self.pg.setOnChange(this.onPgChange)
        self.pg.setOnSelected(this.onFieldSelect)

    @property
    def title(self):
        return self.form.title

    def onFieldSelect(self, pg, name):
        # 预览地址
        addr = self.get_property_addr(name)
        if addr:
            self.addr_view.value = "%08X" % addr
        else:
            self.addr_view.value = ""

    def onClose(self, _=None):
        if self.pg.changed:
            choice = self.confirm('保存修改', '有修改，是否保存？', wxconst.CANCEL)
            if choice is wxconst.CANCEL:
                return False
            elif choice is wxconst.YES:
                self.onSave(None)
        return super().onClose()

    def onAdd(self, btn):
        name = input("角色名称")
        if name:
            self.doAdd(name)

    def doAdd(self, name, data=None):
        """
        添加列表项
        """
        super().doAdd(name)
        if name not in self.data_map:
            self.data_map[name] = data or {'name': name}

    def onDel(self, btn):
        pos, text = super().onDel(btn)
        if text:
            self.data_map.pop(text, None)

    def onRename(self, m):
        args = super().onRename(m)
        if args:
            name, newname = args
            item = self.data_map[newname] = self.data_map.pop(name)
            item['name'] = newname
            self.pg.setValues({'name': newname})

    def onSaveIt(self, btn):
        item_data = self.getCurData()
        if item_data:
            item_data.update(self.pg.getValues())

    def onSave(self, btn):
        self.pg.changed = False
        self.dumpJson('characters', list(self.itervalues()))

    def getCurData(self):
        text = self.listbox.text
        if text:
            return self.data_map[text]

    def onListSelect(self, _):
        if self._pg_inited is False:
            self._pg_inited = True
            self.form.initPg(self.pg)

        self._lastpos = self.listbox.index
        self.pg.bindData(self.getCurData())

    def onPgChange(self, pg, name, value):
        if name == 'name':
            if value != self.listbox.text and value in self.listbox.getTexts():
                fefactory_api.alert('名称已存在')
                return False
            self.listbox[self._lastpos] = value

    def onClear(self, m):
        """清空列表"""
        if super().onClear(m):
            self.data_map = {}

    def onSwichAutoSave(self, checkbox):
        self.pg.autosave = checkbox.checked

    def onPreviewAddrChoiceChange(self, choice):
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
        for text in self.listbox.getTexts():
            yield self.data_map[text]

    def readFrom(self, reader):
        conf = config.ADDR_MAP[reader.key]
        count = 0xFF
        buff = reader.read(conf['addr'], count * conf['step'])
        ptr = self.form.ptr_from_bytes(buff, len(buff))
        texts = []
        for i in range(count):
            item = self.form.struct_to_dict(ptr[i])
            name = reader.getTextEntryText(item['name'])
            item['name'] = name
            item['title'] = reader.getTextEntryText(item['title'])
            self.data_map[name] = item
            texts.append(name)

        super().doAdd(texts)
