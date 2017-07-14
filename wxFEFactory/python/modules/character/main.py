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
                listbox = ui.ListBox(options=['选项1', '选项2'], values=[11,22], className="listbox")
                with ui.Horizontal(className="footer"):
                    btnAdd = ui.Button(label="添加", key="add", className="button")
                    btnDel = ui.Button(label="删除", key="delete", className="button")
            pg = ui.PropertyGrid()
        ui.AuiItem(panel, caption=self.getTitle(), onclose=self.onclose)
        return panel

    def getMenu(self):
        with ui.Menu(self.getTitle()) as menu:
            ui.MenuItem("哈哈")
        return menu

    def onclose(self):
        print("close")
        return super().onclose()


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
        }
    }
}