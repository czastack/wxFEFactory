from .view import View, Control
from . import wx


class Button(Control):
    """普通按钮"""
    wxtype = wxButton

    def __init__(self, label, onclick=None, **kwargs):
        super().__init__(**kwargs)
        self.wxparams['label'] = label
        self.onclick = onclick

    def onready(self):
        self.set_onclick(self.onclick)
        del self.onclick

    def set_onclick(self, onclick, reset=true):
        self.bind_event(wxEVT_BUTTON, onclick, reset)

    def click(self):
        self.post_event(wxCommandEvent)


class BitmapButton(Button):
    """图像按钮"""
    def __init__(self, src, onclick=None, **kwargs):
        Control.__init__(self, **kwargs)
        self.src = src
        self.onclick = onclick

    def render(self, parent):
        bitmap = wxBitmap(self.src)
        self.bind_wx(wxBitmapButton(parent, label=self.label, **self.wxparams))
        del self.src, self.onclick


class ToggleButton(Control):
    """开关按钮"""
    wxtype = wxToggleButton

    def __init__(self, label, checked=False, onchange=None, **kwargs):
        Control.__init__(self, **kwargs)
        self.wxparams['label'] = label
        self.checked = checked
        self.onchange = onchange

    def onready(self):
        if self.checked:
            self.SetValue(True)
        self.set_onchange(self.change)
        del self.checked, self.onchange

    def set_onchange(self, onchange, reset=True):
        self.bind_event(wxEVT_TOGGLEBUTTON, onchange, reset)

    def toggle(self):
        """切换状态"""
        self.SetValue(not self.GetValue())
        self.post_event(wxEVT_TOGGLEBUTTON)


class CheckBox(Control):
    """复选框"""
    wxtype = wxCheckBox

    def __init__(self, label="", checked=False, align_right=False, onchange=None, **kwargs):
        Control.__init__(self, **kwargs)
        self.wxparams['label'] = label
        self.checked = checked
        self.onchange = onchange

        if align_right:
            self.wxparams['style'] |= wx.ALIGN_RIGHT

    def render(self, parent):
        self.bind_wx(wxCheckBox(parent, **self.wxparams))
        if self.checked:
            self.SetValue(True)
        self.set_onchange(self.change)
        del self.checked, self.onchange

    def set_onchange(self, onchange):
        pass

    def toggle(self):
        """切换状态"""
        self.SetValue(not self.GetValue())
        self.post_event(wx.EVT_CHECKBOX)


class StaticBitmap(Control):
    """静态图片"""
    wxtype = wxStaticBitmap

    def __init__(self, label, **kwargs):
        Control.__init__(self, **kwargs)
        self.label = label

    def render(self, parent):
        bitmap = wxBitmap(self.label)
        self.bind_wx(wxStaticBitmap(parent, label=bitmap, **self.wxparams))
        del self.label


class Text(Control):
    """静态文本"""
    wxtype = wxStaticText

    def __init__(self, label, **kwargs):
        Control.__init__(self, **kwargs)
        self.wxparams['label'] = label

    def apply_style_own(self, styles):
        align = styles.get('align', None)
        if align is not None:
            self.wxstyle |= align


class TextInput(Control):
    """文本输入框"""
    wxtype = wxTextCtrl

    def __init__(self, value="", multiline=False, readonly=False, type=None, **kwargs):
        Control.__init__(self, **kwargs)
        wxstyle = 0
        if multiline:
            wxstyle |= wx.TE_MULTILINE
        if readonly:
            wxstyle |= wx.TE_READONLY
        if type == "password":
            wxstyle |= wx.TE_PASSWORD
        if wxstyle:
            self.wxparams['style'] |= wxstyle
        self.wxparams['value'] = value

    def set_onenter(self, fn, reset=True):
        self.bind_event(wxEVT_TEXT_ENTER, fn, reset)

    def set_onchar(self, fn, reset=True):
        self.bind_event(wxEVT_CHAR, fn, reset)


class SearchCtrl(Control):
    """搜索框"""
    wxtype = wxSearchCtrl

    def __init__(self, value="", search_button=True, cancel_button=False, **kwargs):
        Control.__init__(self, **kwargs)
        self.wxparams['value'] = value
        self.search_button = search_button
        self.cancel_button = cancel_button

    def onready(self):
        if not self.search_button:
            self.ShowSearchButton(False)
        if self.cancel_button:
            self.ShowCancelButton(True)
        del self.search_button, self.cancel_button

    def set_onsubmit(self, fn, reset=True):
        self.bind_event(wxEVT_SEARCHCTRL_SEARCH_BTN, fn, reset)

    def set_oncancel(self, fn, reset=True):
        self.bind_event(wxEVT_SEARCHCTRL_CANCEL_BTN, fn, reset)


class SpinCtrl(Control):
    """数字输入框"""
    wxtype = wxSpinCtrl

    def __init__(self, value="", min=0, max=100, initial=0, wxstyle=wx.SP_ARROW_KEYS | wx.ALIGN_RIGHT, **kwargs):
        Control.__init__(self, **kwargs)
        self.wxparams.update(value=value, min=min, max=max, initial=initial)

    def set_onchange(self, fn, reset=True):
        self.bind_event(wxEVT_SPINCTRL, fn, reset)

    def set_onchar(self, fn, reset=True):
        self.bind_event(wxEVT_TEXT_ENTER, fn, reset)


class ColorPicker(Control):
    """颜色选择器"""
    wxtype = wxColourPickerCtrl

    def __init__(self, color=None, onchange=None, **kwargs):
        Control.__init__(self, **kwargs)
        self.wxparams['color'] = color
        self.onchange = onchange

    def onready(self):
        self.set_onchange(self.onchange)
        del self.onchange

    def set_onchange(self, fn, reset=True):
        self.bind_event(wxEVT_SPINCTRL, fn, reset)


class ItemContainer(Control):
    pass


class ControlWithItems(ItemContainer):
    def onready(self):
        self.set_onselect(self.onselect)
        del self.onselect

    def set_onselect(self, fn, reset=True):
        self.bind_event(self.wxevent, fn, reset)

    def post_select(self):
        self.post_event(self.wxevent)


class ListBox(ControlWithItems):
    """列表框"""
    wxtype = wxListBox
    wxevent = wxEVT_LISTBOX

    def __init__(self, choices=None, onselect=None, **kwargs):
        Control.__init__(self, **kwargs)
        if choices:
            self.wxparams['choices'] = choices
        self.onselect = onselect


class CheckListBox(ListBox):
    """带复选列表框"""
    wxtype = wxCheckListBox


class RearrangeList(CheckListBox):
    """可排序复选列表框"""
    wxtype = wxRearrangeListPatched

    def __init__(self, order=None, **kwargs):
        super().__init__(self, **kwargs)
        self.wxparams['order'] = choices


class Choice(ControlWithItems):
    """简易下拉框"""
    wxtype = wxChoice
    wxevent = wxEVT_CHOICE

    def __init__(self, choices=None, onselect=None, **kwargs):
        Control.__init__(self, **kwargs)
        if choices:
            self.wxparams['choices'] = choices
        self.onselect = onselect


class ComboBox(ControlWithItems):
    """下拉框"""
    wxtype = wxComboBox
    wxevent = wxEVT_COMBOBOX

    def __init__(self, choices=None, value="", onselect=None, **kwargs):
        Control.__init__(self, **kwargs)
        if choices:
            self.wxparams['choices'] = choices
        self.wxparams['value'] = value
        self.onselect = onselect

    def set_onenter(self, fn, reset=True):
        self.bind_event(wxEVT_TEXT_ENTER, fn, reset)


class RadioBox(ControlWithItems):
    """选择框"""
    wxtype = wxRadioBox
    wxevent = wxEVT_RADIOBOX

    def __init__(self, label="", choices=None, onselect=None, **kwargs):
        Control.__init__(self, **kwargs)
        if choices:
            self.wxparams['choices'] = choices
        self.wxparams['label'] = label
        self.onselect = onselect

    def apply_style_own(self, styles):
        direction = styles.get('flex-direction', None)
        if direction is not None:
            if direction == 'row':
                self.wxstyle |= wx.RA_SPECIFY_ROWS
            elif direction == 'column':
                self.wxstyle |= wx.RA_SPECIFY_COLS


class Hr(Control):
    """静态线"""
    wxtype = wxStaticLine

    def __init__(self, vertical=Flase, **kwargs):
        Control.__init__(self, **kwargs)
        self.wxparams['wxstyle'] = wx.VERTICAL if vertical else wx.HORIZONTAL


class FilePickerCtrl(Control):
    """文件选择器"""
    wxtype = wxFilePickerCtrl

    def __init__(self, path=None, msg="", wildcard="", **kwargs):
        Control.__init__(self, **kwargs)
        self.wxparams.update(path=path, msg=msg, wildcard=wildcard)

    def set_onchange(self, onchange, reset=True):
        self.bind_event(wxEVT_FILEPICKER_CHANGED, onchange, reset)


class DirPickerCtrl(Control):
    """目录选择器"""
    wxtype = wxDirPickerCtrl

    def __init__(self, path=None, msg="", **kwargs):
        Control.__init__(self, **kwargs)
        self.wxparams.update(path=path, msg=msg)

    def set_onchange(self, onchange, reset=True):
        self.bind_event(wxEVT_DIRPICKER_CHANGED, onchange, reset)


class TreeCtrl(Control):
    """树控件"""
    wxtype = wxTreeCtrl

    def __init__(self, wxstyle=wx.TR_HAS_BUTTONS | wx.TR_SINGLE, **kwargs):
        Control.__init__(self, wxstyle=wxstyle, **kwargs)

    def set_on_item_activated(self, fn, reset=True):
        self.bind_event(wxEVT_TREE_ITEM_ACTIVATED, fn, reset)
