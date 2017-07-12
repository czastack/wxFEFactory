from . import forms
from mainframe import win, AuiItem, SplitterWindow, PropertyGrid, ListBox

form = forms.CharacterForm()

def run():
    with win.book:
        with SplitterWindow(False, 160) as panel:
            ListBox(options=['选项1', '选项2'], values=[11,22])
            PropertyGrid(key="pg")
        AuiItem(panel, caption=form.title)

    form.show(panel.pg)