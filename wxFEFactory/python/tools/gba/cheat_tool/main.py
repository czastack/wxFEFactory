from styles import styles
from fefactory_api import auto, ui
from lib.gba import cheat
from tools.base.basetool import NestedTool


class Main(NestedTool):
    def render(self):
        self.code = cheat.CheatCode()
        self.code.batch_mode = True

        with self.render_win() as win:
            with ui.Vertical():
                with ui.Vertical(className="fill padding"):
                    self.textinput = ui.TextInput(className="expand fill", multiline=True, style=textstyle)
                    self.textoutput = ui.TextInput(className="expand fill", multiline=True, style=textstyle)
                with ui.Horizontal(className="padding"):
                    ui.Button("解析", onclick=self.weak.analyse)
        return win

    def analyse(self, _=None):
        self.code.clear()
        for line in self.textinput.value.split('\n'):
            line = line.strip()
            if line:
                self.code.from_string(line)
                if not self.code.wait_second:
                    self.code.set_cb()
        self.textoutput.value = self.code.get_text()


win_style = {'width': 640, 'height': 820}
textstyle = {'height': 200}
