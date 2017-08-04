from ..module import BaseListBoxModuel
from mainframe import ui
from commonstyle import dialog_style
from lib import exui


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
        with ui.FlexGridLayout(cols=2, vgap=10, className="expand container") as infobar:
            ui.Text("地址", className="vcenter label_left")
            self.addr_view = ui.TextInput(readonly=True, className="expand")
            ui.Text("代码", className="vcenter label_left")
            self.code_view = ui.TextInput(readonly=True, multiline=True, className="expand")

            infobar.AddGrowableCol(1)
            infobar.AddGrowableRow(1)
            
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
        self.data_list[self.listbox.index]['text'] = self.textarea.value

    def onSave(self, btn):
        self.dumpJson('strings', self.data_list, indent=0)

    def getCurData(self):
        return self.data_list[self.listbox.index]

    def onListSelect(self, _):
        self._lastpos = self.listbox.index
        item =self.data_list[self._lastpos]
        self.textarea.value = item['text']
        addr = item.get('addr', '')
        if addr:
            addr = "%08X" % addr
        self.addr_view.value = addr
        code = item.get('code', '')
        if code:
            code = code
        self.code_view.value = code

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
        
        choice = exui.CheckChoiceDialog(self.getTitle(), (
            ('unique', '是否过滤重复文本？'),
            ('show_addr', '是否显示文本在rom中的地址'),
            ('show_code', '是否显示文本的码表代码'),
        ), style=dialog_style)

        if not choice.showOnce():
            print("取消操作")
            return

        ptr = reader.text_table_start
        if choice.unique:
            added = {item['text'] for item in self.data_list}
        i = 0

        codes = None

        if choice.show_code:
            # 未压缩的代码缓冲区
            codes = bytearray()

        while True:
            addr = reader.read32(ptr)
            high = addr >> 24
            
            if not (high is 8 or high is 9) or i > 0xF:
                # 读取结束
                break

            if codes is not None:
                codes.clear()

            text = reader.readText(addr, codes)
            if not choice.unique or text not in added:
                item = {'text': text, 'addr': addr}

                if codes is not None:
                    item['code'] = codes.hex().upper()

                self.data_list.append(item)
            ptr += 4
            i += 1

        count = self.listbox.count
        super().doAdd("%04X" % count for count in range(count, count + i))
