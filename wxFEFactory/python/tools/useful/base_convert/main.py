import struct
from tools.base.basetool import BaseTool
from lib import ui


class Main(BaseTool):
    BASES = (2, 8, 10, 16)
    FUNCS = (bin, oct, int, hex)
    BASES_CHOICES = ('2', '8', '10', '16')

    def render(self):
        with self.render_float_win() as win:
            with ui.Vertical():
                with ui.Horizontal(class_="fill padding"):
                    with ui.Vertical(class_="fill"):
                        with ui.Horizontal(class_="expand padding"):
                            ui.Text('输入进制', class_="padding_right")
                            self.base_in = ui.Choice(class_="fill",
                                choices=self.BASES_CHOICES).set_selection(2)
                        self.text_input = ui.TextInput(class_="fill", multiline=True)
                    with ui.Vertical(class_="expand padding"):
                        ui.Button('<->', class_='btn_sm', onclick=self.reverse_base)
                        with ui.Horizontal(class_="fill"):
                            ui.Button('转换', class_='btn_sm vcenter', onclick=self.convert)
                    with ui.Vertical(class_="fill"):
                        with ui.Horizontal(class_="expand padding"):
                            ui.Text('输出进制', class_="padding_right")
                            self.base_out = ui.Choice(class_="fill",
                                choices=self.BASES_CHOICES).set_selection(3)
                        self.text_output = ui.TextInput(class_="fill", readonly=True, multiline=True)
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
