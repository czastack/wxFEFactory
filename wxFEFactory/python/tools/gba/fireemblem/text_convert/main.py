from lib import ui
from tools.base.basetool import BaseTool
from tools.gba.fireemblem.fe.ferom import FeRomRW


class Main(BaseTool):
    def render(self):
        with self.render_float_win() as win:
            with ui.Vertical():
                with ui.FlexGridLayout(cols=2, vgap=10, class_="fill padding") as container:
                    ui.Text("Rom", class_="vcenter")
                    self.rom_picker = ui.FilePickerCtrl(wildcard="*.gba|*.gba", class_="fill")
                    ui.Text("码表", class_="vcenter")
                    self.dict_picker = ui.FilePickerCtrl(class_="fill")
                    ui.Text("文本")
                    self.text_view = ui.TextInput(class_="fill", multiline=True, wxstyle=ui.wx.TE_PROCESS_ENTER)
                    ui.Text("码表编码")
                    self.code_view = ui.TextInput(class_="fill", multiline=True, wxstyle=ui.wx.TE_PROCESS_ENTER)
                    ui.Text("哈夫曼编码  ")
                    self.haff_view = ui.TextInput(class_="fill", multiline=True, readonly=True,
                        wxstyle=ui.wx.TE_PROCESS_ENTER)
                    container.sizer.AddGrowableCol(1)
                    for i in (2, 3, 4):
                        container.sizer.AddGrowableRow(i)

        self.rom_picker.set_onchange(self.on_rom_change)
        self.dict_picker.set_onchange(self.on_dict_change)
        self.text_view.set_onenter(self.on_convert_text)
        self.code_view.set_onenter(self.on_convert_code)
        self.dict_picker.Enable(False)
        self.reader = None
        return win

    def on_rom_change(self, picker):
        self.reader = FeRomRW(picker.path)
        if not self.reader.closed:
            self.dict_picker.Enable(True)
            self.reader.open_dict()
            self.dict_picker.path = self.reader.dict_path
        else:
            self.dict_picker.Enable(False)

    def on_dict_change(self, picker):
        self.reader.open_dict(picker.path)

    def on_convert_text(self, tv):
        if not self.reader:
            print("请先选择Rom")
            return
        di = self.reader._dict
        text = tv.value
        codebytes = di.encode_text(text)
        haffbytes = di.encode_haffuman(text)
        self.code_view.value = ''.join(['%04X' % item for item in codebytes])
        self.haff_view.value = haffbytes.hex().upper()

    def on_convert_code(self, tv):
        if not self.reader:
            print("请先选择Rom")
            return
        di = self.reader._dict
        codebytes = bytes.fromhex(tv.value)
        codes = di.bytes_to_codes(codebytes)
        try:
            text = di.decode_text(codes)
        except KeyError as e:
            print("%04X" % e.args[0] + '不在码表中', '忽略文本转换')
            text = ''

        try:
            haffbytes = di.encode_haffuman_code(codes)
        except ValueError as e:
            print(e.args[0], '忽略哈夫曼编码转换')
            haffbytes = b''

        self.text_view.value = text
        self.haff_view.value = haffbytes.hex().upper()
