from styles import styles
from lib.win32.keys import getVK, MOD_ALT, MOD_CONTROL, MOD_SHIFT
from fefactory_api import auto
from ...tool import NestedTool
from lib.ndstool import ar
import fefactory_api
ui = fefactory_api.ui


class Main(NestedTool):
    def render(self):
        with self.render_win() as win:
            with ui.Vertical():
                with ui.Vertical(className="container fill"):
                    self.textinput = ui.TextInput(className="expand fill", multiline=True, style=textstyle)
                    self.textoutput = ui.TextInput(className="expand fill", multiline=True, style=textstyle)
                with ui.Horizontal(className="container"):
                    ui.Button("分析", onclick=self.weak.analyse)
        return win

    def analyse(self, _=None):
        self.textoutput.value = ar.analyse(self.textinput.value)


win_style = {'width': 640, 'height': 820}
textstyle = {'height': 200}