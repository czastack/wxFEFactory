from ..tool import BaseTool
from mainframe import ui
from commonstyle import styles, dialog_style
from fe.ferom import FeRomRW

class Tool(BaseTool):

    def attach(self):
        self.render()
    
    def render(self):
        input_style = {
            'height': 60,
        }

        with ui.MenuBar() as menubar:
            with ui.Menu("窗口"):
                ui.MenuItem("关闭\tCtrl+W", onselect=self.onclose)

        with ui.Window(self.getTitle(), styles=styles, style=dialog_style, menuBar=menubar) as win:
            with ui.Vertical():
                with ui.FlexGridLayout(cols=2, vgap=10, className="fill container") as container:
                    ui.Text("Rom", className="vcenter")
                    self.rom_picker = ui.FilePickerCtrl(className="fill")
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

        self.win = win
        self.rom_picker.setOnchange(self.onRomChange)
        self.dict_picker.setOnchange(self.onDictChange)
        self.text_view.setOnEnter(self.onConvertText)
        self.code_view.setOnEnter(self.onConvertCode)
        self.dict_picker.enabled = False

    def onclose(self, m=None):
        super().onclose()
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
        di = self.reader._dict
        text = tv.value
        codebytes = di.encode(text)
        haffbytes = di.encodeHaffuman(text)
        self.code_view.value = codebytes.hex().upper()
        self.haff_view.value = haffbytes.hex().upper()

    def onConvertCode(self, tv):
        di = self.reader._dict
        codebytes = bytes.fromhex(tv.value)
        try:
            text = di.decode(codebytes, True)
        except KeyError as e:
            print("%02X" % e.args[0] + '不在码表中')
            return

        haffbytes = di.encodeHaffuman(text)
        self.text_view.value = text
        self.haff_view.value = haffbytes.hex().upper()