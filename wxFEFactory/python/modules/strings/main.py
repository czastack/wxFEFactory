from ..module import BaseListBoxModuel
from mainframe import ui
from commonstyle import styles
import json
import fefactory_api

class Module(BaseListBoxModuel):

    def __init__(self):
        super().__init__()

    def attach(self):
        super().attach()
        self.data_list = self.loadJson('strings', [])

    def render_right(self):
        self.textarea = ui.TextInput(multiline=True, className="fill")
        with ui.Horizontal(className="footer"):
            ui.Button(label="保存", className="button", onclick=self.onSave)

    def onAdd(self, btn):
        text = self.longtext_dialog("输入内容")
        if text:
            count = self.listbox.getCount()
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

    def onSave(self, btn):
        self.pg.changed = False
        self.dumpJson('strings', self.data_list)

    def getCurData(self):
        return self.data_list[self.listbox.getSelection()]

    def onListSelect(self, _):
        self._lastpos = self.listbox.getSelection()
        self.textarea.value = self.data_list[self._lastpos]

    def onClear(self, m):
        """清空列表"""
        if super().onClear(m):
            self.data_list.clear()