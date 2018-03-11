from styles import styles, dialog_style
from lib.win32.keys import getWXK, getWXKName, isWXKMod
from lib.extypes import WeakBinder
import fefactory_api
ui = fefactory_api.layout


class StdDialog(ui.Dialog):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('style', dialog_style)
        kwargs.setdefault('styles', styles)
        super().__init__(*args, **kwargs)
        this = WeakBinder(self)

        super().__enter__()
        with ui.Vertical(className="fill"):
            self.view = ui.ScrollView(className="fill container")

            with ui.Horizontal(className="container right") as footer:
                ui.Button(label="取消", onclick=lambda btn: this.dismiss(False))
                ui.Button(label="确定", onclick=lambda btn: this.dismiss(True))
            self.footer = footer
        super().__exit__()

    def __enter__(self):
        self.view.__enter__()
        return self

    def __exit__(self, *args):
        self.view.__exit__(*args)


class ListDialog(ui.StdModalDialog):
    def __init__(self, *args, **kwargs):
        listbox_opt = kwargs.pop('listbox', {})
        kwargs.setdefault('style', dialog_style)
        super().__init__(*args, **kwargs)
        this = WeakBinder(self)

        with self:
            with ui.Vertical(styles=styles, style=styles['class']['fill']):
                self.listbox = ui.CheckListBox(className='fill', **listbox_opt)
                with ui.Horizontal(className="expand"):
                    ui.Button(label="全选", className="button", onclick=this.checkAll)
                    ui.Button(label="反选", className="button", onclick=this.reverseCheck)

    def checkAll(self, btn):
        self.listbox.checkAll()

    def reverseCheck(self, btn):
        self.listbox.reverseCheck()


class ChoiceDialog(ui.StdModalDialog):
    def __init__(self, title, choices, onselect, *args, **kwargs):
        kwargs.setdefault('style', dialog_style)
        super().__init__(title, *args, **kwargs)

        with self:
            with ui.Vertical(styles=styles, style=styles['class']['fill']):
                self.listbox = ui.ListBox(className='fill', choices=choices, onselect=onselect)


class CheckChoiceDialog(ListDialog):
    """
    选项对话框
    :param choices: [(name, label[, checked])], name会与序号绑定
    """
    def __init__(self, title, choices, *args, **kwargs):
        if 'listbox' in kwargs:
            listbox_opt = kwargs['listbox']
        else:
            listbox_opt = kwargs['listbox'] = {}
        listbox_opt['choices'] = (item[1] for item in choices)

        super().__init__(title, *args, **kwargs)

        i = 0

        # 默认选中的选项
        checked_list = []
        for item in choices:
            setattr(self, item[0], i)
            if len(item) is 3 and item[2] is True:
                checked_list.append(i)
            i += 1

        if checked_list:
            self.listbox.setCheckedItems(checked_list)

        self.fields = [item[0] for item in choices]

    def showModal(self):
        ret = super().showModal()
        if ret:
            checked_list = self.listbox.getCheckedItems()
            for name in self.fields:
                # 把对应的项的值从序号设为是否选中
                setattr(self, name, getattr(self, name) in checked_list)

        self.listbox = None
        return ret


class HotkeyCtrl(ui.TextInput):

    def __init__(self, *args, **kwargs):
        kwargs['wxstyle'] = 0x0400
        super().__init__(*args, **kwargs)
        self.setOnKeyDown(self.onKey)

    def onKey(self, v, event):
        code = event.GetKeyCode()
        if isWXKMod(code):
            return
        mod = event.GetModifiers()
        self.handleKey(code, mod)
        return True
        
    def handleKey(self, code, mod):
        self.value = getWXKName(code, mod)
        self.code = code
        self.mode = mod