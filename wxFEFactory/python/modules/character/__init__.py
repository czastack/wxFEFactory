from . import forms
from mainframe import win, ui

form = forms.CharacterForm()

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

def run():
    with win.book:
        with ui.SplitterWindow(False, 220) as panel:
            with ui.Vertical(styles=styles):
                listbox = ui.ListBox(options=['选项1', '选项2'], values=[11,22], className="listbox")
                with ui.Horizontal(className="footer"):
                    btnAdd = ui.Button(label="添加", key="add", className="button")
                    btnDel = ui.Button(label="删除", key="delete", className="button")
            pg = ui.PropertyGrid()
        ui.AuiItem(panel, caption=form.title)

    with win.menubar:
        with ui.Menu(form.title) as menu:
            ui.MenuItem("哈哈")

    global m
    m = menu
    form.show(pg)