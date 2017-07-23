from lib.module import BaseModule
from mainframe import ui
from . import forms
from . import config
import json

class Module(BaseModule):

    def __init__(self):
        self.form = forms.CharacterForm()
        super().__init__()
        self._pg_inited = False

        self.data_map = {}
        data_list = self.loadJson('characters', [])
        for item in data_list:
            self.data_map[item['name']] = item
            self.doAdd(item['name'])

    def render(self):
        with ui.SplitterWindow(False, 220, styles=styles) as panel:
            with ui.Vertical():
                self.listbox = ui.RearrangeList(className="fill", onselect=self.onListSelect)
                with ui.Horizontal(className="footer"):
                    ui.Text("Ctrl+↑↓ 上移/下移当前项")
                with ui.Horizontal(className="footer"):
                    ui.Button(label="添加", key="add", className="button", onclick=self.onAdd)
                    ui.Button(label="删除", key="delete", className="button", onclick=self.onDel)
            with ui.Vertical():
                self.pg = ui.PropertyGrid(className="fill")
                with ui.Horizontal(className="footer"):
                    ui.Button(label="保存", className="button", onclick=self.onSave)
        ui.AuiItem(panel, caption=self.getTitle(), onclose=self.onclose)

        with ui.ContextMenu() as listmenu:
            ui.MenuItem("重命名", onselect=self.onRename)

        self.listbox.setOnKeyDown(self.onListBoxKey)
        self.listbox.setContextMenu(listmenu)
        self.pg.setTwowayBinding()
        return panel

    def getMenu(self):
        with ui.Menu(self.getTitle()) as menu:
            ui.MenuItem("清空", onselect=self.onClear)
        return menu

    def onclose(self):
        if self.pg.changed:
            choice = self.confirm('保存修改', '有修改，是否保存？', self.CANCEL)
            if choice is self.CANCEL:
                return False
            elif choice is self.YES:
                self.onSave(None)
        return super().onclose()

    def onAdd(self, btn):
        name = input("角色名称")
        if name:
            self.doAdd(name)

    def doAdd(self, name):
        self.listbox.append([name])
        if name not in self.data_map:
            self.data_map[name] = {'name': name}

    def onDel(self, btn):
        pos = self.listbox.getSelection()
        if pos is not -1:
            self.data_map.pop(self.listbox.getText(pos), None)
            self.listbox.remove(pos)

    def onRename(self, m):
        name = self.listbox.getText()
        if name:
            newname = input("新名称", name)
            self.listbox.setText(newname)
            item = self.data_map[newname] = self.data_map.pop(name)
            item['name'] = newname
            self.pg.setValues({'name': newname})

    def onSave(self, btn):
        self.pg.changed = False
        self.dumpJson('characters', list(self.itervalues()))

    def getCurData(self):
        return self.data_map[self.listbox.getText()]

    def onListSelect(self, _):
        if self._pg_inited is False:
            self._pg_inited = True
            self.form.initPg(self.pg)

        self.pg.bindData(self.getCurData())

    def onListBoxKey(self, lb, event):
        mod = event.GetModifiers()
        if mod == event.CTRL:
            code = event.GetKeyCode()
            if code == event.UP:
                self.listbox.moveUp()
            elif code == event.DOWN:
                self.listbox.moveDown()
        event.Skip()

    def onClear(self, m):
        """清空列表"""
        if self.confirm('提示', '确认清空所有列表项？', self.NO) is self.YES:
            self.listbox.clear()
            self.data_map = {}

    def itervalues(self):
        for text in self.listbox.getTexts():
            yield self.data_map[text]

    def readFrom(self, reader):
        conf = config.ADDR_MAP[reader.key]
        


styles = {
    'class': {
        'fill': {
            'flex': 1,
            'expand': True,
        },
        'footer': {
            'expand': True,
        },
        'button': {
            'flex': 1,
            'width': 50,
        }
    }
}