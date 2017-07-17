from lib.module import BaseModule
from mainframe import ui
from . import forms

class Module(BaseModule):

    def __init__(self):
        self.form = forms.CharacterForm()
        super().__init__()

    def render(self):
        with ui.SplitterWindow(False, 220) as panel:
            with ui.Vertical(styles=styles):
                self.listbox = ui.ListBox(className="listbox", onselect=self.onselect)
                with ui.Horizontal(className="footer"):
                    btnAdd = ui.Button(label="添加", key="add", className="button", onclick=self.onAdd)
                    btnDel = ui.Button(label="删除", key="delete", className="button", onclick=self.onDel)
            self.pg = ui.PropertyGrid()
        ui.AuiItem(panel, caption=self.getTitle(), onclose=self.onclose)
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
            print(self.listbox.className)
            self.listbox.append([name])

    def onDel(self, btn):
        pos = self.listbox.getSelection()
        if pos is not -1:
            self.listbox.remove(pos)

    def onselect(self, _):
        print(self.listbox.getValue())


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