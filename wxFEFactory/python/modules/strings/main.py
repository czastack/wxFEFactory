from ..module import BaseListBoxModuel
from mainframe import ui
from commonstyle import styles


class Module(BaseListBoxModuel):

    def __init__(self):
        super().__init__()

    def attach(self):
        super().attach()
        self.data_list = self.loadJson('strings', [])
        count = self.listbox.count
        for item in self.data_list:
            name = "%04X" % count
            super().doAdd(name)
            count += 1

    def render_right(self):
        with ui.GridLayout(cols=4, key="infobar", className="container"):
            ui.Text("地址", className="vcenter")
            ui.TextInput(readonly=True)
        self.textarea = ui.TextInput(multiline=True, className="fill")
        with ui.Horizontal(className="footer"):
            ui.ComboBox(type="readonly", className="fill")
            ui.Button(label="保存该项", className="button", onclick=self.onSaveIt)
            ui.Button(label="保存文件", className="button", onclick=self.onSave)

    def onAdd(self, btn):
        text = self.longtext_dialog("输入内容")
        if text:
            self.doAdd(text)

    def doAdd(self, text, unique=True):
        """
        添加列表项
        """
        if not unique or text not in self.data_list:
            count = self.listbox.count
            name = "%04X" % count
            super().doAdd(name)
            self.data_list.append(text)

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
        self.dumpJson('strings', self.data_list, indent=0)

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

    def readFrom(self, reader):
        unique = False
        choice = self.confirm('确认', '是否过滤重复文本？')
        if choice is self.YES:
            unique = True
        elif choice is self.CANCEL:
            print("取消操作")
            return

        ptr = reader.text_table_start
        texts = []
        i = 0
        while True:
            addr = reader.read32(ptr)
            high = addr >> 24
            if not (high is 8 or high is 9) or i > 0xF:
                # 读取结束
                break
            text = reader.readText(addr)
            if not unique or text not in texts:
                texts.append(text)
            ptr += 4
            i += 1

        count = self.listbox.count
        super().doAdd("%04X" % count for count in range(count, len(texts) + count))
        self.data_list.extend(texts)
