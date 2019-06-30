import fefactory_api
from ..module import BaseListBoxModuel
from fefactory_api import ui
from styles import dialog_style
from lib import exui, wxconst


class Module(BaseListBoxModuel):

    def __init__(self):
        super().__init__()

    def attach(self, frame):
        super().attach(frame)
        self.data_list = self.load_json('strings', [])
        count = self.listbox.count
        for item in self.data_list:
            name = "%04X" % count
            super().doAdd(name)
            count += 1

    def render_main(self):
        with ui.FlexGridLayout(cols=2, vgap=10, class_="expand padding") as infobar:
            ui.Text("地址", class_="vcenter input_label")
            self.addr_view = ui.TextInput(readonly=True, class_="expand")
            ui.Text("代码", class_="vcenter input_label")
            self.code_view = ui.TextInput(readonly=True, multiline=True, class_="expand")

            infobar.AddGrowableCol(1)
            infobar.AddGrowableRow(1)

        self.textarea = ui.TextInput(multiline=True, class_="fill")
        with ui.Horizontal(class_="expand"):
            ui.ComboBox(wxstyle=wxconst.CB_READONLY, class_="fill")
            ui.Button(label="保存该项", class_="button", onclick=self.onSaveIt)
            ui.Button(label="保存文件", class_="button", onclick=self.onSave)
            ui.Button(label="另存为", class_="button", onclick=self.onSaveAs)

    def onAdd(self, btn):
        text = self.longtext_dialog("输入内容")
        if text:
            self.doAdd(text)

    def doAdd(self, text, unique=True):
        """ 添加列表项 """
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
        """保存当前项"""
        self.data_list[self.listbox.index]['text'] = self.textarea.value

    def onSave(self, btn):
        self.dump_json('strings', self.data_list, indent=0)

    def onSaveAs(self, btn):
        tpl = self.longtext_dialog("输入模板", "{i:04X} {addr:08X}\n{text}\n")
        path = fefactory_api.choose_file("选择保存文件", wildcard='*.txt')
        if path:
            result = []
            i = 0
            for item in self.data_list:
                result.append(tpl.format(i=i, **item))
                i += 1
            with open(path, 'w', encoding="utf-8") as file:
                file.write('\n'.join(result))
            print("保存成功: " + path)

    def getCurData(self):
        return self.data_list[self.listbox.index]

    def onListSelect(self, _):
        self._lastpos = self.listbox.index
        item = self.data_list[self._lastpos]
        self.textarea.value = item['text']
        addr = item.get('addr', '')
        if addr:
            addr = "%08X" % addr
        self.addr_view.value = addr
        code = item.get('code', '')
        if code:
            code = code
        self.code_view.value = code

    def move_up(self):
        """上移一项"""
        index = self.listbox.index
        if index != 0:
            self.data_list[index - 1], self.data_list[index] = self.data_list[index], self.data_list[index - 1]
            self.listbox.index = index - 1

    def move_down(self):
        """下移一项"""
        index = self.listbox.index
        if index != self.listbox.count - 1:
            self.data_list[index + 1], self.data_list[index] = self.data_list[index], self.data_list[index + 1]
            self.listbox.index = index + 1

    def onClear(self, m):
        """清空列表"""
        if super().onClear(m):
            self.data_list.clear()

    def readFrom(self, reader):
        unique = False

        choice = exui.CheckChoiceDialog(self.unique_title, (
            ('unique', '是否过滤重复文本？'),
            ('show_addr', '是否显示文本在rom中的地址'),
            ('show_code', '是否显示文本的码表代码'),
        ), style=dialog_style)

        if not choice.showModal():
            print("取消操作")
            return

        ptr = reader.text_table_start
        i = 0
        names = []  # ListBox中显示的列表项文本
        codes = None
        cur_count = self.listbox.count

        if choice.unique:
            added = {item['text'] for item in self.data_list}

        if choice.show_code:
            # 未压缩的代码缓冲区
            codes = bytearray()

        while True:
            addr = reader.read32(ptr)
            high = (addr >> 24) & 0xF

            if not (high is 8 or high is 9):
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
                names.append("%04X %08X" % (cur_count, addr))
                cur_count += 1

            ptr += 4
            i += 1

        super().doAdd(names)
