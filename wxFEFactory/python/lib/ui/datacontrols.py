from .view import View, Control, event_binder
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
        super().onready()

    def set_prop_help(self, name, help):
        self.GetPropertyByName(name).SetHelpString(help)

    def set_readonly(self, name, readonly=True):
        self.GetPropertyByName(name).SetFlagRecursively(wx.PG_PROP_READONLY, readonly)

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

    set_onhighlight = event_binder(wx.EVT_PG_HIGHLIGHTED)

    set_onselected = event_binder(wx.EVT_PG_SELECTED)

    def append_property(self, prop, help=None):
        self.Append(prop)
        if help is not None:
            prop.SetHelpString(help)

    def add_category(self, title):
        self.append_property(wx.PropertyCategory(self.label))

    def add_string_property(title, name, help, value):
        self.append_property(wx.StringProperty(title, name, value), help)

    def add_int_property(title, name, help, value=0):
        self.append_property(wx.IntProperty(title, name, value), help)

    def add_uint_property(title, name, help, value=0):
        self.append_property(wx.UIntProperty(title, name, value), help)

    def add_hex_property(title, name, help, value=0):
        prop = wx.UIntProperty(title, name, value)
        prop.SetAttribute(wx.PG_UINT_BASE, wx.PG_BASE_HEX)
        # prop.SetAttribute(wx.PG_UINT_PREFIX, wx.PG_PREFIX_0x)
        self.append_property(prop, help)

    def add_float_property(title, name, help, value=0):
        self.append_property(wx.FloatProperty(title, name, value), help)

    def add_bool_property(title, name, help, value=False):
        prop = wx.BoolProperty(title, name, value)
        prop.SetAttribute(wx.PG_BOOL_USE_CHECKBOX, true)
        self.append_property(prop, help)

    def add_enum_property(title, name, help, labels, values, value=0):
        values = wx.ArrayInt() if values is None else values
        self.append_property(wx.EnumProperty(title, name, labels, values, value), help)

    def add_flags_property(title, name, help, items, values=None, value=0):
        if value is None:
            value = [1 << i for i in range(len(items))]
        prop = wx.FlagsProperty(title, name, labels, values, value)
        prop.SetAttribute(wx.PG_BOOL_USE_CHECKBOX, True)
        self.append_property(prop, help)

    def add_long_string_property(title, name, help, value):
        self.append_property(wx.LongStringProperty(title, name, value), help)

    def add_array_string_property(title, name, help, values):
        self.append_property(wx.ArrayStringProperty(title, name, values), help)

    def set_enum_choices(name, labels, values):
        prop = self.GetPropertyByName(name)
        if isinstance(prop, wx.EnumProperty):
            choices = wx.PGChoices(labels, wx.ArrayInt() if values is None else values)
            prop.SetChoices(choices)

    def _get_value(self, prop):
        variant = prop.GetValue()
        type = variant.GetType()
        if type == "long":
            return variant.GetLong()
        elif type == "string":
            return variant.GetString()
        elif type == "bool":
            return variant.GetBool()
        elif type == "arrstring":
            return variant.GetArrayString()

    def get_value(self, name):
        prop = self.GetPropertyByName(name)
        return self._get_value(prop)

    def _set_value(self, prop, value):
        type = prop.GetValueType()
        if value is None:
            variant = wx.Variant("")
        else:
            variant = wx.Variant(value)
        self.SetPropVal(prop, variant)

    def set_value(self, name, value):
        prop = self.GetPropertyByName(name)
        self._set_value(prop, value)

    def get_values(self, data=None):
        """批量获取值"""
        if data is None:
            data = {}
        it = self.GetIterator()
        while not it.AtEnd():
            prop = it.Get()
            data[prop.GetName()] = self._get_value(prop)
        return data

    def set_values(self, data, all):
        """批量设置值"""
        if all:
            it = self.GetIterator()
            while not it.AtEnd():
                prop = it.Get()
                self._set_value(prop, data.get(prop.GetName(), None))
        else:
            for name, value in data.items():
                self.set_value(name, value)


class ListView(Control):
    wxtype = wx.ListView

    def append_columns(self, columns, widths):
        widths_len = len(widths) if widths else 0
        i = 0
        for item in columns:
            self.AppendColumn(item, wx.LIST_FORMAT_LEFT, widths[i] if i < widths_len else -1)

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

    def reverse_check(self):
        """反选"""
        for i in range(0, self.GetItemCount()):
            self.toggle_item(i)

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

    set_on_item_selected = event_binder(wx.EVT_LIST_ITEM_SELECTED)

    set_on_item_deselected = event_binder(wx.EVT_LIST_ITEM_DESELECTED)

    set_on_item_checked = event_binder(wx.EVT_LIST_ITEM_CHECKED)

    set_on_item_unchecked = event_binder(wx.EVT_LIST_ITEM_UNCHECKED)

    set_on_item_activated = event_binder(wx.EVT_LIST_ITEM_ACTIVATED)

    set_on_col_click = event_binder(wx.EVT_LIST_COL_CLICK)

    set_on_col_right_click = event_binder(wx.EVT_LIST_COL_RIGHT_CLICK)
