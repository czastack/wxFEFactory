from styles import dialog_style, styles
from lib.win32.keys import VK
from fefactory_api import auto, ui
from tools.tool import BaseTool
import json
import time
import fefactory_api


class Main(BaseTool):
    def attach(self, frame):
        super().attach(frame)
        self.win.RegisterHotKeys((
            (VK.MOD_ALT, VK.C, self.record_copy),
            (VK.MOD_ALT, VK.getCode('['), self.item_prev),
            (VK.MOD_ALT, VK.getCode(']'), self.item_next),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK.getCode('['), self.item_prev_input),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK.getCode(']'), self.item_next_input),
        ))

    def render(self):
        with ui.HotkeyWindow(self.title, style=win_style, styles=styles, menubar=self.render_menu()) as win:
            with ui.Vertical(className="container"):
                with ui.Vertical(className="container fill"):
                    self.input = ui.TextInput(className="expand", multiline=True, style={'height': 200})
                    self.listbox = ui.ListBox(className="expand", onselect=self.onSelectChange, style={'height': 200})
                    with ui.Horizontal(className="expand top_padding"):
                        ui.Button("输入", onclick=self.input_text)
                    with ui.ScrollView(className="fill container"):
                        ui.Text("切换上一个: alt+[")
                        ui.Text("切换下一个: alt+]")
                        ui.Text("切换并粘贴上一个: alt+shift+[")
                        ui.Text("切换并粘贴下一个: alt+shift+]")
        # win.keeptop = True
        return win

    def input_text(self, _=None):
        self.listbox.setItems(self.input.value.split('\n'))

    def record_copy(self, _=None):
        self.input.appendText('\n' + fefactory_api.get_clipboard())

    def item_prev(self, _=None):
        self.listbox.prev(False)
        self.onSelectChange(self.listbox)

    def item_next(self, _=None):
        self.listbox.next(False)
        self.onSelectChange(self.listbox)

    def item_prev_input(self, _=None):
        self.item_prev()
        time.sleep(0.5)
        self.paste()

    def item_next_input(self, _=None):
        self.item_next()
        time.sleep(0.5)
        self.paste()

    def onSelectChange(self, listbox):
        fefactory_api.set_clipboard(listbox.text)

    def copy(self):
        auto.sendKey(auto.CombKey(VK.MOD_CONTROL, VK.C), 10)

    def paste(self):
        auto.sendKey(auto.CombKey(VK.MOD_CONTROL, VK.V), 10)


win_style = {
    'width': 640,
    'height': 820,
}
