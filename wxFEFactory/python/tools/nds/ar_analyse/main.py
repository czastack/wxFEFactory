from styles import styles
from lib import ui
from lib.ndstool import ar
from tools.base.basetool import NestedTool


class Main(NestedTool):
    def render(self):
        with self.render_win() as win:
            with ui.Vertical():
                with ui.Vertical(class_="fill padding"):
                    self.textinput = ui.TextInput(class_="expand fill", multiline=True, style=textstyle)
                    self.textoutput = ui.TextInput(class_="expand fill", multiline=True, style=textstyle)
                with ui.Horizontal(class_="padding"):
                    ui.Button("分析", onclick=self.weak.analyse)
        return win

    def analyse(self, _=None):
        self.textoutput.value = ar.analyse(self.textinput.value)


win_style = {'width': 640, 'height': 820}
textstyle = {'height': 200}
