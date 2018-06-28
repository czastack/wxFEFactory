from styles import styles, dialog_style
from lib.win32.keys import getWXK, getWXKName, isWXKMod
from lib.extypes import WeakBinder
from fefactory_api import ui


__ALL__ = ('StdDialog', 'ListDialog', 'ChoiceDialog', 'CheckChoiceDialog', 'SearchDialog')


class StdDialog(ui.Dialog):
    def __init__(self, *args, cancel=True, ok=True, scrollable=False, **kwargs):
        kwargs.setdefault('style', dialog_style)
        kwargs.setdefault('styles', styles)
        super().__init__(*args, **kwargs)
        self.weak = WeakBinder(self)

        super().__enter__()
        with ui.Vertical(className="fill"):
            self.view = (ui.ScrollView if scrollable else ui.Vertical)(className="fill container")

            with ui.Horizontal(className="container right") as footer:
                if cancel:
                    ui.Button(label="取消").id = ui.ID_CANCEL
                if ok:
                    ui.Button(label="确定").id = ui.ID_OK
            self.footer = footer
        super().__exit__()

    def __enter__(self):
        self.view.__enter__()
        return self

    def __exit__(self, *args):
        self.view.__exit__(*args)


class ListDialog(StdDialog):
    def __init__(self, *args, **kwargs):
        listbox_opt = kwargs.pop('listbox', {})
        kwargs.setdefault('style', dialog_style)
        super().__init__(*args, **kwargs)

        with self:
            with ui.Vertical(styles=styles, style=styles['class']['fill']):
                self.listbox = ui.CheckListBox(className='fill', **listbox_opt)
                with ui.Horizontal(className="expand"):
                    ui.Button(label="全选", className="button", onclick=self.weak.checkAll)
                    ui.Button(label="反选", className="button", onclick=self.weak.reverseCheck)

    def checkAll(self, btn):
        self.listbox.checkAll()

    def reverseCheck(self, btn):
        self.listbox.reverseCheck()


class ChoiceDialog(StdDialog):
    def __init__(self, title, choices, onselect, *args, **kwargs):
        kwargs.setdefault('style', dialog_style)
        super().__init__(title, *args, **kwargs)

        with self:
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


class SearchDialog(StdDialog):
    """搜索对话框"""
    def __init__(self, title, onselect, onsearch=None, *args, **kwargs):
        kwargs.setdefault('style', dialog_style)
        self.onsearch = onsearch
        super().__init__(title, *args, **kwargs)

        with self:
            with ui.Horizontal(className='expand'):
                self.input = ui.TextInput(className='fill', wxstyle=0x0400)
                ui.Button(label="搜索", className='btn_sm', onclick=self.weak.onenter)
            self.listbox = ui.ListBox(className='fill', onselect=onselect)
            self.input.setOnEnter(self.weak.onenter)

    def onenter(self, _):
        if self.onsearch:
            self.onsearch(self, self.input.value)