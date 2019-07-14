import json
import time
import pyapi
from lib.win32.keys import VK
from pyapi import auto, ui
from tools.base.basetool import BaseTool


class Main(BaseTool):
    def attach(self, frame):
        super().attach(frame)
        self.win.register_hotkeys((
            (VK.MOD_ALT, VK.C, self.record_copy),
            (VK.MOD_ALT, VK('['), self.item_prev),
            (VK.MOD_ALT, VK(']'), self.item_next),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK('['), self.item_prev_input),
            (VK.MOD_ALT | VK.MOD_SHIFT, VK(']'), self.item_next_input),
        ))

    def render(self):
        with self.render_float_win() as win:
            with ui.Vertical(class_="padding"):
                with ui.Vertical(class_="fill padding"):
                    self.input = ui.TextInput(class_="expand", multiline=True, style={'height': 200})
                    self.listbox = ui.ListBox(class_="expand", onselect=self.on_select_change, style={'height': 200})
                    with ui.Horizontal(class_="expand padding_top"):
                        ui.Button("输入", onclick=self.input_text)
                    with ui.ScrollView(class_="fill padding"):
                        ui.Text("切换上一个: alt+[")
                        ui.Text("切换下一个: alt+]")
                        ui.Text("切换并粘贴上一个: alt+shift+[")
                        ui.Text("切换并粘贴下一个: alt+shift+]")
        return win

    def input_text(self, _=None):
        self.listbox.Set(self.input.value.split('\n'))

    def record_copy(self, _=None):
        self.input.AppendText('\n' + pyapi.get_clipboard())

    def item_prev(self, _=None):
        self.listbox.prev(False)
        self.on_select_change(self.listbox)

    def item_next(self, _=None):
        self.listbox.next(False)
        self.on_select_change(self.listbox)

    def item_prev_input(self, _=None):
        self.item_prev()
        time.sleep(0.5)
        self.paste()

    def item_next_input(self, _=None):
        self.item_next()
        time.sleep(0.5)
        self.paste()

    def on_select_change(self, listbox):
        pyapi.set_clipboard(listbox.text)

    def copy(self):
        auto.sendKey(auto.CombKey(VK.MOD_CONTROL, VK.C), 10)

    def paste(self):
        auto.sendKey(auto.CombKey(VK.MOD_CONTROL, VK.V), 10)


win_style = {
    'width': 640,
    'height': 820,
}
