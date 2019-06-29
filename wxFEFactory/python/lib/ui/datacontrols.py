from .view import View, Control
from . import wx


class PropertyGrid(Control):
    wxtype = wx.PropertyGrid

    def __init__(self, data=None, exstyle=wx.PG_EX_HELP_AS_TOOLTIPS, **kwargs):
        Control.__init__(self, **kwargs)
        self._data = data
        self._onchange = None
        self.exstyle = exstyle
        self.changed = False

    def onready(self):
        self.SetExtraStyle(self.exstyle)
        self.SetCaptionBackgroundColour(0xeeeeee)
        self.SetMarginColour(0xeeeeee)
        self.Bind(wx.EVT_PG_CHANGING, self.onchange)
    
    def onchange(self, event):
        self.changed = True
        if self.autosave:
            prop = event.GetProperty()
            name = prop.GetName()
            value = event.GetValue()

            if self._onchange is not None:
                ret = self._onchange(self, name, value)
                if ret is False:
                    event.Veto()
                    return
                elif not ret:
                    event.Skip()
            self._data[name] = value
        else:
            event.Skip()

    def set_onchange(self, fn):
        self._onchange = fn

    def set_onhighlight(self, fn):
        self.bind_event(wx.EVT_PG_HIGHLIGHTED, fn)

    def set_onselected(self, fn):
        self.bind_event(wx.EVT_PG_SELECTED, fn)


class ListView(Control):
    wxtype = wx.ListView

    def append_columns(self, columns, widths):
        widths_len = len(widths) if widths else 0
        i = 0
        for item in columns:
            self.AppendColumn(item, wx.LIST_FORMAT_LEFT,
                widths[i] if i < widths_len else -1)

    def insert_items(self, rows, pos=-1, create=False):
        info = wx.ListItem()
        info.m_mask = wx.LIST_MASK_TEXT
        info.m_itemId = pos if pos is not -1 else self.GetItemCount()
        if create and pos is -1:
            create = True

        for cols in rows:
            info.m_col = 0
            if create:
                self.InsertItem(info)
            for item in cols:
                info.m_text = item
                self.SetItem(info)
                info.m_col += 1

            info.m_itemId += 1

    def toggle_item(self, i):
        self.CheckItem(i, not self.IsItemChecked(i))

    def checkall(self, checked):
        for i in range(0, self.GetItemCount()):
            self.CheckItem(i, checked)

    def selectall(self, selected):
        for i in range(0, self.GetItemCount()):
            self.SelectItem(i, selected)

    def clear_selected(self):
        for i in self.get_selected_list():
            self.SelectItem(i, False)

    def check_selection(self, toogle):
        """勾选高亮选中的项"""
        for i in self.get_selected_list():
            self.CheckItem(i, self.IsItemChecked(i) if toogle else True)

    def get_checked_list(self):
        """勾选的序号"""
        for i in range(0, self.GetItemCount()):
            if self.IsItemChecked(i):
                yield i

    def get_selected_list(self):
        """高亮选中的序号"""
        i = self.GetFirstSelected()
        while i is not -1:
            yield i
            i = self.GetNextSelected(i)

    def set_checked_list(self, selection):
        """设置勾选列表"""
        self.checkall(False)
        for i in selection:
            self.CheckItem(i, True)

    def set_selected_list(self, selection):
        """设置高亮列表"""
        self.clear_selected()
        for i in selection:
            self.SelectItem(i, True)

    def set_on_item_selected(self, fn, reset=True):
        self.bind_event(wx.EVT_LIST_ITEM_SELECTED, fn, reset)

    def set_on_item_deselected(self, fn, reset=True):
        self.bind_event(wx.EVT_LIST_ITEM_DESELECTED, fn, reset)

    def set_on_item_checked(self, fn, reset=True):
        self.bind_event(wx.EVT_LIST_ITEM_CHECKED, fn, reset)

    def set_on_item_unchecked(self, fn, reset=True):
        self.bind_event(wx.EVT_LIST_ITEM_UNCHECKED, fn, reset)

    def set_on_item_activated(self, fn, reset=True):
        self.bind_event(wx.EVT_LIST_ITEM_ACTIVATED, fn, reset)

    def set_on_col_click(self, fn, reset=True):
        self.bind_event(wx.EVT_LIST_COL_CLICK, fn, reset)

    def set_on_col_right_click(self, fn, reset=True):
        self.bind_event(wx.EVT_LIST_COL_RIGHT_CLICK, fn, reset)
