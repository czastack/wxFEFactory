import math
from lib.extypes import WeakBinder
from lib import ui
from . import wx


class Pagination(ui.Horizontal):
    def __init__(self, onpagechange, total, page=1):
        super().__init__(class_="expand center")
        this = WeakBinder(self)
        self.onpagechange = onpagechange
        self.total = total
        self.page = page
        with self:
            self.total_view = ui.Text(" 共%d页 " % total, class_="vcenter")
            self.page_input = ui.SpinCtrl(class_="expand", min=1, max=total, initial=page, wxstyle=0x4600)
            ui.Button(label="跳转", class_="button", onclick=this.on_page)
            ui.Button(label="上页", class_="button", onclick=this.on_prev)
            ui.Button(label="下页", class_="button", onclick=this.on_next)
        self.page_input.set_onenter(this.on_page)

    def set_total(self, total):
        self.total = total
        self.total_view.label = " 共%d页 " % total
        self.page_input.max = total
        if self.page > total:
            self.set_page(total)

    def asset_total(self, count, pagelen):
        """根据数据总条数和每页数量计算总页数"""
        self.set_total(math.ceil(count / pagelen))

    def set_page(self, page):
        self.page = page
        self.page_input.value = page
        self.onpagechange(self.page)

    def on_prev(self, btn):
        if self.page > 1:
            self.page -= 1
            self.page_input.value = self.page
            self.onpagechange(self.page)

    def on_next(self, btn):
        if self.page < self.total:
            self.page += 1
            self.page_input.value = self.page
            self.onpagechange(self.page)

    def on_page(self, btn):
        self.page = self.page_input.value
        self.onpagechange(self.page)


class SearchListBox(ui.Vertical):
    """带搜索功能列表框"""
    def __init__(self, choices, onselect, *args, **kwargs):
        if not extypes.is_list_tuple(choices):
            choices = tuple(choices)
        self.choices = choices
        super().__init__(*args, **kwargs)
        with self:
            self.input = ui.ComboBox(
                class_='expand', wxstyle=wx.CB_DROPDOWN | wx.TE_PROCESS_ENTER, onselect=self.onsearch_select)
            self.listbox = ui.ListBox(class_='fill', choices=choices, onselect=onselect)
            self.input.set_onenter(self.onsearch)

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
        self.input.Set(choices)
        self.input.value = value

    def onsearch_select(self, view):
        # 搜索结果选择后切换到对应的序号
        self.listbox.set_selection(self.search_values[view.index], True)
