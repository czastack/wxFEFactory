from lib import ui
from lib.ui import wx
from lib.extypes import WeakBinder
from styles import styles, dialog_style


__ALL__ = ('StdDialog', 'ListDialog', 'ChoiceDialog', 'CheckChoiceDialog', 'SearchDialog')


class StdDialog(ui.Dialog):
    def __init__(self, *args, cancel=True, ok=True, closable=True, scrollable=False, **kwargs):
        kwargs.setdefault('style', dialog_style)
        kwargs.setdefault('styles', styles)
        super().__init__(*args, **kwargs)
        self.weak = WeakBinder(self)

        super().__enter__()
        with ui.Vertical(class_="fill"):
            self.view = (ui.ScrollView if scrollable else ui.Vertical)(class_="fill padding", keep_styles=True)
            with ui.Horizontal(class_="padding right") as footer:
                if cancel:
                    ui.Button(label="取消", id=wx.ID_CANCEL)
                if ok:
                    ui.Button(label="确定", id=wx.ID_OK)
            self.footer = footer
        super().__exit__(None, None, None)

        if not closable:
            self.set_onclose(self.prevent_close)

    def __enter__(self):
        self.view.__enter__()
        return self

    def __exit__(self, *args):
        self.view.__exit__(*args)

    def prevent_close(self, *args):
        self.dismiss()
        return False

    def EndModal(self, code=True):
        if code is True:
            code = wx.ID_OK
        elif code is False:
            code = wx.ID_CANCEL
        self.wxwindow.EndModal(code)


class ListDialog(StdDialog):
    def __init__(self, *args, **kwargs):
        listbox_opt = kwargs.pop('listbox', {})
        kwargs.setdefault('style', dialog_style)
        super().__init__(*args, **kwargs)

        with self:
            with ui.Vertical(styles=styles, style=styles['class']['fill']):
                self.listbox = ui.CheckListBox(class_='fill', **listbox_opt)
                with ui.Horizontal(class_="expand"):
                    ui.Button(label="全选", class_="button", onclick=self.weak.checkall)
                    ui.Button(label="反选", class_="button", onclick=self.weak.reverse_check)

    def checkall(self, btn):
        self.listbox.checkall()

    def reverse_check(self, btn):
        self.listbox.reverse_check()


class ChoiceDialog(StdDialog):
    def __init__(self, title, choices, onselect, *args, **kwargs):
        kwargs.setdefault('style', dialog_style)
        super().__init__(title, *args, **kwargs)

        with self:
            self.listbox = ui.ListBox(class_='fill', choices=choices, onselect=onselect)


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
            if len(item) == 3 and item[2] == True:
                checked_list.append(i)
            i += 1

        if checked_list:
            self.listbox.set_checked_list(checked_list)

        self.fields = [item[0] for item in choices]

    def ShowModal(self):
        ret = super().ShowModal()
        if ret:
            checked_list = self.listbox.GetCheckedItems()
            for name in self.fields:
                # 把对应的项的值从序号设为是否选中
                setattr(self, name, getattr(self, name) in checked_list)

        self.listbox = None
        return ret


class SearchDialog(StdDialog):
    """搜索对话框"""
    def __init__(self, title, onselect, onsearch=None, *args, **kwargs):
        kwargs.setdefault('style', dialog_style)
        self.onsearch = onsearch
        super().__init__(title, *args, **kwargs)

        with self:
            with ui.Horizontal(class_='expand'):
                self.input = ui.TextInput(class_='fill', wxstyle=wx.TE_PROCESS_ENTER)
                ui.Button(label="搜索", class_='btn_sm', onclick=self.weak.onenter)
            self.listbox = ui.ListBox(class_='fill', onselect=onselect)
            self.input.set_onenter(self.weak.onenter)

    def onenter(self, _):
        if self.onsearch:
            self.onsearch(self, self.input.value)
