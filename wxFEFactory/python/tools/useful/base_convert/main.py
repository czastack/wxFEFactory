from tools.tool import BaseTool
from fefactory_api import ui
import struct


class Main(BaseTool):
    BASES = (2, 8, 10, 16)
    FUNCS = (bin, oct, int, hex)
    BASES_CHOICES = ('2', '8', '10', '16')

    def render(self):
        with self.render_float_win() as win:
            with ui.Vertical():
                with ui.Horizontal(className="fill padding"):
                    with ui.Vertical(className="fill"):
                        with ui.Horizontal(className="expand padding"):
                            ui.Text('输入进制', className="padding_right")
                            self.base_in = ui.Choice(className="fill",
                                choices=self.BASES_CHOICES).setSelection(2)
                        self.text_input = ui.TextInput(className="fill", multiline=True)
                    with ui.Vertical(className="expand padding"):
                        ui.Button('<->', className='btn_sm', onclick=self.reverse_base)
                        with ui.Horizontal(className="fill"):
                            ui.Button('转换', className='btn_sm vcenter', onclick=self.convert)
                    with ui.Vertical(className="fill"):
                        with ui.Horizontal(className="expand padding"):
                            ui.Text('输出进制', className="padding_right")
                            self.base_out = ui.Choice(className="fill",
                                choices=self.BASES_CHOICES).setSelection(3)
                        self.text_output = ui.TextInput(className="fill", readonly=True, multiline=True)
        return win

    def reverse_base(self, _):
        self.base_in.index, self.base_out.index = self.base_out.index, self.base_in.index

    def convert(self, _):
        base_out_index = self.base_out.index
        base_in = self.BASES[self.base_in.index]
        base_out = self.BASES[base_out_index]
        trans_func = self.FUNCS[base_out_index]

        def handle_item(line):
            line = line.strip()
            if line:
                try:
                    return trans_func(int(line.strip(), base_in))
                except Exception as e:
                    print(line, '转换失败')
            return line

        lines = '\n'.join(handle_item(line) for line in self.text_input.value.splitlines())
        self.text_output.value = lines
