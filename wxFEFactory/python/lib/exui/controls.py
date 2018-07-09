from fefactory_api import ui
from lib.win32.keys import WXK


class HotkeyCtrl(ui.TextInput):

    def __init__(self, *args, **kwargs):
        kwargs['wxstyle'] = 0x0400
        super().__init__(*args, **kwargs)
        self.setOnKeyDown(self.onKey)

    def onKey(self, v, event):
        code = event.GetKeyCode()
        if WXK.isMod(code):
            return
        mod = event.GetModifiers()
        self.handleKey(code, mod)
        return True
        
    def handleKey(self, code, mod):
        self.value = WXK.getName(code, mod)
        self.code = code
        self.mode = mod


def Label(text):
    return ui.Text(text, className="input_label expand")