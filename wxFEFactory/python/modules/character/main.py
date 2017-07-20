from lib.module import BaseModule
from mainframe import ui
from . import forms

class Module(BaseModule):

    def __init__(self):
        self.form = forms.CharacterForm()
        super().__init__()
        self.data_map = {}
        self._pg_inited = False

    def render(self):
        with ui.SplitterWindow(False, 220) as panel:
            with ui.Vertical(styles=styles):
                self.listbox = ui.RearrangeList(className="listbox", onselect=self.onselect)
                with ui.Horizontal(className="footer"):
                    ui.Text("Ctrl+↑↓ 上移/下移当前项")
                with ui.Horizontal(className="footer"):
                    btnAdd = ui.Button(label="添加", key="add", className="button", onclick=self.onAdd)
                    btnDel = ui.Button(label="删除", key="delete", className="button", onclick=self.onDel)
            self.pg = ui.PropertyGrid()
        ui.AuiItem(panel, caption=self.getTitle(), onclose=self.onclose)

        self.listbox.setOnKeyDown(self.onListBoxKey)
        self.pg.setTwowayBinding()
        return panel

    def getMenu(self):
        with ui.Menu(self.getTitle()) as menu:
            ui.MenuItem("哈哈")
        return menu

    def onclose(self):
        print("close")
        return super().onclose()

    def onAdd(self, btn):
        name = input("角色名称")
        if name:
            self.listbox.append([name])
            self.data_map[name] = {}

    def onDel(self, btn):
        pos = self.listbox.getSelection()
        if pos is not -1:
            self.data_map.pop(self.listbox.getText(pos), None)
            self.listbox.remove(pos)

    def getCurData(self):
        return self.data_map[self.listbox.getText()]

    def onselect(self, _):
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

    def itervalues(self):
        for text in self.listbox.getTexts():
            yield self.data_map[text]


styles = {
    'class': {
        'listbox': {
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