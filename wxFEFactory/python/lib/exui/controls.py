from lib import extypes, wxconst, ui
from lib.win32.keys import WXK


def Label(text):
    return ui.Text(text, className="input_label expand")


class HotkeyCtrl(ui.TextInput):
    def __init__(self, *args, **kwargs):
        kwargs['wxstyle'] = wxconst.TE_PROCESS_ENTER
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


class SearchListBox(ui.Vertical):
    """带搜索功能列表框"""
    def __init__(self, choices, onselect, *args, **kwargs):
        if not extypes.is_list_tuple(choices):
            choices = tuple(choices)
        self.choices = choices
        super().__init__(*args, **kwargs)
        with self:
            self.input = ui.ComboBox(className='expand', wxstyle=wxconst.CB_DROPDOWN | wxconst.TE_PROCESS_ENTER,
                onselect=self.onsearch_select)
            self.listbox = ui.ListBox(className='fill', choices=choices, onselect=onselect)
            self.input.setOnEnter(self.onsearch)

    def onsearch(self, input):
        value = input.value
        choices = []
        values = []
        i = 0
        if value:
            for item in self.choices:
                if value in item:
                    choices.append(item)
                    values.append(i)
                i += 1
        self.search_values = values
        self.input.setItems(choices)
        self.input.value = value

    def onsearch_select(self, view):
        # 搜索结果选择后切换到对应的序号
        self.listbox.setSelection(self.search_values[view.index], True)
