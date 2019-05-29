import math
from lib.extypes import WeakBinder
from fefactory_api import ui


class Pagination(ui.Horizontal):
    def __init__(self, onpagechange, total, page=1):
        super().__init__(className="expand center")
        this = WeakBinder(self)
        self.onpagechange = onpagechange
        self.total = total
        self.page = page
        with self:
            self.total_view = ui.Text(" 共%d页 " % total, className="vcenter")
            self.page_input = ui.SpinCtrl(className="expand", min=1, max=total, initial=page, wxstyle=0x4600)
            ui.Button(label="跳转", className="button", onclick=this.on_page)
            ui.Button(label="上页", className="button", onclick=this.on_prev)
            ui.Button(label="下页", className="button", onclick=this.on_next)
        self.page_input.setOnEnter(this.on_page)

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
