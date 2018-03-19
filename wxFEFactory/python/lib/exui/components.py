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
            ui.Button(label="上页", className="button", onclick=this.on_prev)
            ui.Text(" 共%d页 " % total, className="vcenter")
            self.page_input = ui.SpinCtrl(className="expand", min=1, max=total, initial=page)
            ui.Button(label="跳转", className="button", onclick=this.on_page)
            ui.Button(label="下页", className="button", onclick=this.on_next)

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