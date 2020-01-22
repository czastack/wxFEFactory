from lib.extypes import WeakBinder
from lib import ui


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
            with ui.dialog.StdDialog(self.label, style={'width': 1300, 'height': 900},
                    closable=False, cancel=False) as dialog:
                with ui.Horizontal(class_="expand"):
                    dialog.search = ui.ComboBox(wxstyle=ui.wx.CB_DROPDOWN, class_="fill",
                        onselect=weak.on_search_select)
                    ui.Button("搜索", onclick=weak.on_search)
                dialog.listview = listview = ui.ListView(class_="fill")
                dialog.listview.append_columns(*self.head)
                listview.insert_items(self.items)
                listview.set_on_item_activated(weak.on_item_selected)
            self._dialog = dialog
        return dialog

    def show(self, index=-1):
        dialog = self.dialog
        if index != -1:
            self.select(index)
        dialog.ShowModal()

    def select(self, index):
        dialog = self.dialog
        dialog.listview.clear_selected()
        dialog.listview.Select(index)
        dialog.listview.Focus(index)

    def on_item_selected(self, view, event):
        """物品预设选中处理"""
        setattr(self.model, self.model_prop, event.GetSelection())
        self.dialog.EndModal()

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
        dialog.search.Set(choices)
        dialog.search.Popup()

    def on_search_select(self, view):
        """点击搜索项定位"""
        self.select(self.search_values[view.index])
