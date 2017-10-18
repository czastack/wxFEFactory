from ..tool import BaseTool
from mainframe import ui
from commonstyle import styles, dialog_style
from fe.ferom import FeRomRW

class Tool(BaseTool):
    def render(self):
        input_style = {
            'height': 60,
        }

        with ui.MenuBar() as menubar:
            with ui.Menu("窗口"):
                ui.MenuItem("关闭\tCtrl+W", onselect=self.onClose)

        with ui.Window(self.getTitle(), styles=styles, style=dialog_style, menuBar=menubar) as win:
            with ui.Vertical():
                with ui.FlexGridLayout(cols=2, vgap=10, className="fill container") as container:
                    ui.Text("Rom", className="vcenter")
                    self.rom_picker = ui.FilePickerCtrl(wildcard="*.gba|*.gba", className="fill")
                    ui.Text("码表", className="vcenter")
                    self.dict_picker = ui.FilePickerCtrl(className="fill")
                    ui.Text("文本")
                    self.text_view = ui.TextInput(className="fill", multiline=True, exstyle=0x0400)
                    ui.Text("码表编码")
                    self.code_view = ui.TextInput(className="fill", exstyle=0x0400, multiline=True)
                    ui.Text("哈夫曼编码  ")
                    self.haff_view = ui.TextInput(className="fill", multiline=True, readonly=True, exstyle=0x0400)
                    container.AddGrowableCol(1)
                    for i in (2, 3, 4):
                        container.AddGrowableRow(i)

        self.rom_picker.setOnChange(self.onRomChange)
        self.dict_picker.setOnChange(self.onDictChange)
        self.text_view.setOnEnter(self.onConvertText)
        self.code_view.setOnEnter(self.onConvertCode)
        self.dict_picker.enabled = False
        self.reader = None
        return win

    def onClose(self, m=None):
        super().onClose()
        self.win.close()

    def onRomChange(self, picker):
        self.reader = FeRomRW(picker.path)
        if not self.reader.closed:
            self.dict_picker.enabled = True
            self.reader.openDict()
            self.dict_picker.path = self.reader.dict_path
        else:
            self.dict_picker.enabled = False

    def onDictChange(self, picker):
        self.reader.openDict(picker.path)

    def onConvertText(self, tv):
        if not self.reader:
            print("请先选择Rom")
            return
        di = self.reader._dict
        text = tv.value
        codebytes = di.encodeText(text)
        haffbytes = di.encodeHaffuman(text)
        self.code_view.value = ''.join(['%04X' % item for item in codebytes])
        self.haff_view.value = haffbytes.hex().upper()

    def onConvertCode(self, tv):
        if not self.reader:
            print("请先选择Rom")
            return
        di = self.reader._dict
        codebytes = bytes.fromhex(tv.value)
        codes = di.bytes_to_codes(codebytes)
        try:
            text = di.decodeText(codes)
        except KeyError as e:
            print("%04X" % e.args[0] + '不在码表中', '忽略文本转换')
            text = ''

        try:
            haffbytes = di.encodeHaffumanCode(codes)
        except ValueError as e:
            print(e.args[0], '忽略哈夫曼编码转换')
            haffbytes = b''

        self.text_view.value = text
        self.haff_view.value = haffbytes.hex().upper()