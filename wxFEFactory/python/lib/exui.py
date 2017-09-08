import fefactory_api
from commonstyle import styles

ui = fefactory_api.layout

class ListDialog(ui.StdModalDialog):
    def __init__(self, *args, **kwargs):
        listbox_opt = kwargs.pop('listbox', {})
        super().__init__(*args, **kwargs)

        with self:
            with ui.Vertical(styles=styles, style=styles['class']['fill']):
                self.listbox = ui.CheckListBox(className='fill', **listbox_opt)
                with ui.Horizontal(className="expand"):
                    ui.Button(label="全选", className="button", onclick=self.checkAll)
                    ui.Button(label="反选", className="button", onclick=self.reverseCheck)

    def checkAll(self, btn):
        self.listbox.checkAll()

    def reverseCheck(self, btn):
        self.listbox.reverseCheck()


class ChoiceDialog(ui.StdModalDialog):
    def __init__(self, *args, **kwargs):
        combobox_opt = kwargs.pop('combobox', {})
        super().__init__(*args, **kwargs)

        with self:
            with ui.Vertical(styles=styles, style=styles['class']['fill']):
                self.combobox = ui.ComboBox(type="simple", className='fill', **combobox_opt)


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
        kwargs['readonly'] = True
        kwargs['exstyle'] = 0x0400
        super().__init__(*args, **kwargs)
        self.setOnKeyDown(self.onKey)

    def onKey(self, v, event):
        mod = event.GetModifiers()
        code = event.GetKeyCode()
        if mod == event.CTRL:
            if code == event.UP:
                pass
            elif code == event.DOWN:
                pass
        event.Skip()