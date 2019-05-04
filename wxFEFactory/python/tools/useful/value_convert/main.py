from lib import wxconst
from lib.hack.utils import bytes_beautify
from tools.base.basetool import BaseTool
from fefactory_api import ui
import struct


class Main(BaseTool):
    LABELS = ('bytes', 'byte(1字节)', 'word(2字节)', 'dword(4字节)', 'float(4字节)', 'double(8字节)')
    TYPES = tuple(s.split('(')[0] for s in LABELS)

    INT_FORMAT_CHOICES = ('有符号', '无符号', '16进制')
    INT_FORMAT_VALUES = ('signed', 'unsigned', 'hex')

    def render(self):
        self.text_inputs = []
        with self.render_float_win() as win:
            with ui.Vertical():
                ui.Text("按回车转换", className="padding")
                self.int_format = ui.RadioBox("整型格式", className="expand padding",
                    choices=self.INT_FORMAT_CHOICES).setSelection(1)
                with ui.FlexGridLayout(cols=2, vgap=10, className="fill padding") as container:
                    on_enter = self.weak.on_enter
                    for label in ('bytes', 'byte(1字节)', 'word(2字节)', 'dword(4字节)', 'float(4字节)', 'double(8字节)'):
                        ui.Text(label)
                        text_input = ui.TextInput(className="fill", wxstyle=wxconst.TE_PROCESS_ENTER)
                        text_input.setOnEnter(on_enter)
                        self.text_inputs.append(text_input)
                    container.AddGrowableCol(1)
        return win

    def on_enter(self, view):
        type = self.TYPES[self.text_inputs.index(view)]
        input_value = view.value
        int_format = self.INT_FORMAT_VALUES[self.int_format.index]

        # print(type, view.value)
        # 读取当前输入的值
        if type == 'bytes':
            value = bytes.fromhex(input_value)
        elif type == 'float':
            value = struct.pack('f', float(input_value))
        elif type == 'double':
            value = struct.pack('d', float(input_value))
        else:
            int_value = int(input_value, 16 if input_value.startswith('0x') else 10)
            if type == 'byte':
                size = 1
                int_value = int_value & 0xFF
            elif type == 'word':
                size = 2
                int_value = int_value & 0xFFFF
            elif type == 'dword':
                size = 4
                int_value = int_value & 0xFFFFFFFF
            else:  # qword
                size = 8
                int_value = int_value & 0xFFFFFFFFFFFFFFFF
            value = int_value.to_bytes(size, byteorder='little', signed=int_format == 'signed')

        value_len = len(value)
        for text_input, type in zip(self.text_inputs, self.TYPES):
            if type == 'bytes':
                input_value = bytes_beautify(value)
            elif type == 'float':
                if value_len < 4:
                    tmp_value = value + b'\x00' * (4 - value_len)
                elif value_len > 4:
                    tmp_value = value[:4]
                else:
                    tmp_value = value
                input_value = str(struct.unpack('f', tmp_value)[0])
            elif type == 'double':
                if value_len < 8:
                    tmp_value = value + b'\x00' * (8 - value_len)
                elif value_len > 8:
                    tmp_value = value[:8]
                else:
                    tmp_value = value
                input_value = str(struct.unpack('d', tmp_value)[0])
            else:
                if type == 'byte':
                    size = 1
                elif type == 'word':
                    size = 2
                elif type == 'dword':
                    size = 4
                else:  # qword
                    size = 8
                if int_format == 'hex':
                    input_value = "0x%0*X" % (size << 1, int.from_bytes(value[:size], byteorder='little'))
                else:
                    input_value = str(int.from_bytes(value[:size], byteorder='little', signed=int_format == 'signed'))

            text_input.value = input_value
