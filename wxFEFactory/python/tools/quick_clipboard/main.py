from commonstyle import dialog_style, styles
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
from fefactory_api import auto
from ..tool import BaseTool
import json
import time
import fefactory_api
ui = fefactory_api.ui


class Tool(BaseTool):

    def __init__(self):
        pass

    def attach(self):
        self.render()
        self.win.RegisterHotKeys((
            ('item_prev', MOD_ALT, getVK('['), self.item_prev),
            ('item_next', MOD_ALT, getVK(']'), self.item_next),
            ('item_prev_input', MOD_ALT | MOD_SHIFT, getVK('['), self.item_prev_input),
            ('item_next_input', MOD_ALT | MOD_SHIFT, getVK(']'), self.item_next_input),
        ))


    def render(self):
        with ui.MenuBar() as menubar:
            with ui.Menu("窗口"):
                ui.MenuItem("关闭\tCtrl+W", onselect=self.closeWindow)

        with ui.HotkeyWindow(self.doGetTitle(), style=win_style, styles=styles, menuBar=menubar) as win:
            with ui.Vertical():
                self.textinput = ui.TextInput(className="expand", multiline=True, style={'height': 200})
                self.listbox = ui.ListBox(className="expand", onselect=self.onSelectChange, style={'height': 200})
                with ui.Horizontal(className="expand container"):
                    ui.Button("输入", onclick=self.input_text)


        self.win = win

    def closeWindow(self, m=None):
        self.win.close()

    def input_text(self, _=None):
        self.listbox.setItems(self.textinput.value.split('\n'))

    def item_prev(self, _=None):
        self.listbox.prev()

    def item_next(self, _=None):
        self.listbox.next()

    def item_prev_input(self, _=None):
        self.item_prev()
        time.sleep(0.8)
        auto.sendKey(auto.CombKey(MOD_CONTROL, getVK('v')), 10)

    def item_next_input(self, _=None):
        self.item_next()
        time.sleep(0.8)
        auto.sendKey(auto.CombKey(MOD_CONTROL, getVK('v')), 10)

    def onSelectChange(self, listbox):
        fefactory_api.set_clipboard(listbox.text)


win_style = {
    'width': 640,
    'height': 820,
}