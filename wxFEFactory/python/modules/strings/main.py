from ..module import BaseListBoxModuel
from mainframe import ui
from commonstyle import styles


class Module(BaseListBoxModuel):

    def __init__(self):
        super().__init__()

    def attach(self):
        super().attach()
        self.data_list = self.loadJson('strings', [])

    def render_right(self):
        self.textarea = ui.TextInput(multiline=True, className="fill")
        with ui.Horizontal(className="footer"):
            ui.Button(label="保存该项", className="button", onclick=self.onSaveIt)
            ui.Button(label="保存文件", className="button", onclick=self.onSave)

    def onAdd(self, btn):
        text = self.longtext_dialog("输入内容")
        if text:
            count = self.listbox.count
            self.doAdd("%04X" % count, text)

    def doAdd(self, name, data=None):
        """
        添加列表项
        """
        super().doAdd(name)
        if data not in self.data_list:
            self.data_list.append(data)

    def onDel(self, btn):
        pos, text = super().onDel(btn)
        if text:
            self.data_list.pop(pos)

    def onRename(self, m):
        # args = super().onRename(m)
        # if args:
        #     name, newname = args
        #     item = self.data_map[newname] = self.data_map.pop(name)
        #     item['name'] = newname
        #     self.pg.setValues({'name': newname})
        pass

    def onSaveIt(self, btn):
        self.data_list[self.listbox.index] = self.textarea.value

    def onSave(self, btn):
        self.dumpJson('strings', self.data_list)

    def getCurData(self):
        return self.data_list[self.listbox.index]

    def onListSelect(self, _):
        self._lastpos = self.listbox.index
        self.textarea.value = self.data_list[self._lastpos]

    def moveUp(self):
        """上移一项"""
        index = self.listbox.index
        if index != 0:
            self.data_list[index - 1], self.data_list[index] = self.data_list[index], self.data_list[index - 1]
            self.listbox.setSelection(index - 1)

    def moveDown(self):
        """下移一项"""
        index = self.listbox.index
        if index != self.listbox.count - 1:
            self.data_list[index + 1], self.data_list[index] = self.data_list[index], self.data_list[index + 1]
            self.listbox.setSelection(index + 1)

    def onClear(self, m):
        """清空列表"""
        if super().onClear(m):
            self.data_list.clear()