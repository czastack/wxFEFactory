from fefactory_api import ui
from lib.extypes import WeakBinder
from lib import exui, wxconst


class PresetDialog:
    def __init__(self, label, head, items, model, model_prop='item'):
        self.label = label
        self.head = head
        self.items = items
        self.model = model
        self.model_prop = model_prop

    @property
    def dialog(self):
        """对话框"""
        dialog = getattr(self, '_dialog', None)
        if dialog is None:
            weak = WeakBinder(self)
            with exui.StdDialog(self.label, style={'width': 1300, 'height': 900},
                    closable=False, cancel=False) as dialog:
                with ui.Horizontal(className="expand"):
                    dialog.search = ui.ComboBox(wxstyle=wxconst.CB_DROPDOWN, className="fill",
                        onselect=weak.on_search_select)
                    ui.Button("搜索", onclick=weak.on_search)
                dialog.listview = listview = ui.ListView(className="fill")
                dialog.listview.appendColumns(*self.head)
                listview.insertItems(self.items)
                listview.setOnItemActivated(weak.on_item_selected)
            self._dialog = dialog
        return dialog

    def show(self, index=-1):
        dialog = self.dialog
        if index is not -1:
            self.select(index)
        dialog.showModal()

    def select(self, index):
        dialog = self.dialog
        dialog.listview.clearSelected()
        dialog.listview.selectItem(index)
        dialog.listview.focused_item = index

    def on_item_selected(self, view, event):
        """物品预设选中处理"""
        setattr(self.model, self.model_prop, event.index)
        self.dialog.endModal()

    def on_search(self, _):
        """搜索"""
        dialog = self.dialog
        value = dialog.search.value
        choices = []
        values = []
        self.search_values = values
        i = 0
        for item in self.items:
            if value in item[0]:
                choices.append(item[0])
                values.append(i)
            i += 1
        dialog.search.setItems(choices)
        dialog.search.popup()

    def on_search_select(self, view):
        """点击搜索项定位"""
        self.select(self.search_values[view.index])
