from .view import View, Control, EventFunctor, event_binder, value_property
from . import wx


class Button(Control):
    """普通按钮"""
    wxtype = wx.Button

    def __init__(self, label, onclick=None, **kwargs):
        self.onclick = onclick
        super().__init__(wxparams={'label': label}, **kwargs)

    def onready(self):
        super().onready()
        self.set_onclick(self.onclick)
        del self.onclick

    set_onclick = event_binder(wx.EVT_BUTTON)

    def click(self):
        self.post_event(wx.CommandEvent)


class BitmapButton(Button):
    """图像按钮"""
    def __init__(self, src, onclick=None, **kwargs):
        self.src = src
        self.onclick = onclick
        Control.__init__(self, **kwargs)

    def render(self, parent):
        bitmap = wx.Bitmap(self.src)
        self.bind_wx(wx.BitmapButton(parent, label=self.label, **self.wxparams))
        del self.src, self.onclick


class CheckableControl(Control):
    def onready(self):
        if self._checked:
            self.SetValue(True)
        self.set_onchange(self.onchange)
        del self._checked, self.onchange

    def set_onchange(self, fn, reset=True):
        self.bind_event(self.wxevent, fn, reset)

    def toggle(self):
        """切换状态"""
        self.SetValue(not self.GetValue())
        self.post_event(self.wxevent)

    checked = value = value_property


class ToggleButton(CheckableControl):
    """开关按钮"""
    wxtype = wx.ToggleButton
    wxevent = wx.EVT_TOGGLEBUTTON

    def __init__(self, label, checked=False, onchange=None, **kwargs):
        self._checked = checked
        self.onchange = onchange
        CheckableControl.__init__(self, wxparams={'label': label}, **kwargs)


class CheckBox(CheckableControl):
    """复选框"""
    wxtype = wx.CheckBox
    wxevent = wx.EVT_CHECKBOX

    def __init__(self, label="", checked=False, align_right=False, onchange=None, **kwargs):
        if align_right:
            kwargs['wxstyle'] = kwargs.get('wxstyle', 0) | wx.ALIGN_RIGHT
        kwargs['wxparams'] = {'label': label}
        self._checked = checked
        self.onchange = onchange
        CheckableControl.__init__(self, **kwargs)


class StaticBitmap(Control):
    """静态图片"""
    wxtype = wx.StaticBitmap

    def __init__(self, label, **kwargs):
        kwargs['wxparams'] = {'label': label}
        Control.__init__(self, **kwargs)

    def render(self, parent):
        bitmap = wx.Bitmap(self.label)
        self.bind_wx(wx.StaticBitmap(parent.wxwindow, label=bitmap, **self.wxparams))
        del self.label


class Text(Control):
    """静态文本"""
    wxtype = wx.StaticText

    def __init__(self, label, **kwargs):
        Control.__init__(self, wxparams={'label': label}, **kwargs)

    def apply_style(self):
        super().apply_style()
        align = self.computed_style.get('align', None)
        if align is not None:
            self.wxstyle |= align


class TextInput(Control):
    """文本输入框"""
    wxtype = wx.TextCtrl

    def __init__(self, value="", multiline=False, readonly=False, type=None, **kwargs):
        wxstyle = kwargs.get('wxstyle', 0)
        if multiline:
            wxstyle |= wx.TE_MULTILINE
        if readonly:
            wxstyle |= wx.TE_READONLY
        if type == "password":
            wxstyle |= wx.TE_PASSWORD
        if wxstyle:
            kwargs['wxstyle'] = wxstyle
        kwargs['wxparams'] = {'value': value}
        Control.__init__(self, **kwargs)

    set_onenter = event_binder(wx.EVT_TEXT_ENTER)
    set_onchar = event_binder(wx.EVT_CHAR)

    @property
    def selection(self):
        return self.GetSelection()

    @selection.setter
    def selection(self, value):
        self.SetSelection(value)

    value = value_property


class SearchCtrl(Control):
    """搜索框"""
    wxtype = wx.SearchCtrl

    def __init__(self, value="", search_button=True, cancel_button=False, **kwargs):
        self.search_button = search_button
        self.cancel_button = cancel_button
        Control.__init__(self, wxparams={'value': value}, **kwargs)

    def onready(self):
        super().onready()
        if not self.search_button:
            self.ShowSearchButton(False)
        if self.cancel_button:
            self.ShowCancelButton(True)
        del self.search_button, self.cancel_button

    set_onsubmit = event_binder(wx.EVT_SEARCH)
    set_oncancel = event_binder(wx.EVT_SEARCH_CANCEL)
    value = value_property


class SpinCtrl(Control):
    """数字输入框"""
    wxtype = wx.SpinCtrl

    def __init__(self, value="", min=0, max=100, initial=0, wxstyle=wx.SP_ARROW_KEYS | wx.ALIGN_RIGHT, **kwargs):
        kwargs['wxparams'] = dict(value=value, min=min, max=max, initial=initial)
        kwargs['wxstyle'] = wxstyle
        Control.__init__(self, **kwargs)

    set_onchange = event_binder(wx.EVT_SPINCTRL)
    set_onchar = event_binder(wx.EVT_TEXT_ENTER)


class ColorPicker(Control):
    """颜色选择器"""
    wxtype = wx.ColourPickerCtrl

    def __init__(self, color=None, onchange=None, **kwargs):
        Control.__init__(self, wxparams={'color': color}, **kwargs)
        self.onchange = onchange

    def onready(self):
        super().onready()
        self.set_onchange(self.onchange)
        del self.onchange

    set_onchange = event_binder(wx.EVT_SPINCTRL)


class ItemContainer(Control):
    pass


class ControlWithItems(ItemContainer):
    def onready(self):
        super().onready()
        self.set_onselect(self.onselect)
        del self.onselect

    def set_onselect(self, fn, reset=True):
        self.bind_event(self.wxevent, fn, reset)

    def post_select(self):
        self.post_event(self.wxevent)

    def set_selection(self, n, trigger=False):
        self.SetSelection(n)
        if trigger:
            self.post_select()
        return self

    @property
    def count(self):
        return self.GetCount()

    @property
    def index(self):
        return self.GetSelection()

    @index.setter
    def index(self, n):
        self.SetSelection(n)


class ListBox(ControlWithItems):
    """列表框"""
    wxtype = wx.ListBox
    wxevent = wx.EVT_LISTBOX

    def __init__(self, choices=None, onselect=None, **kwargs):
        self.onselect = onselect
        if choices is not None:
            kwargs['wxparams'] = {'choices': choices}
        Control.__init__(self, **kwargs)


class CheckListBox(ListBox):
    """带复选列表框"""
    wxtype = wx.CheckListBox


class RearrangeList(CheckListBox):
    """可排序复选列表框"""
    wxtype = wx.RearrangeList

    def __init__(self, order=None, **kwargs):
        super().__init__(self, wxparams={'order': order}, **kwargs)


class Choice(ControlWithItems):
    """简易下拉框"""
    wxtype = wx.Choice
    wxevent = wx.EVT_CHOICE

    def __init__(self, choices=None, onselect=None, **kwargs):
        self.onselect = onselect
        if choices is not None:
            kwargs['wxparams'] = {'choices': choices}
        Control.__init__(self, **kwargs)


class ComboBox(ControlWithItems):
    """下拉框"""
    wxtype = wx.ComboBox
    wxevent = wx.EVT_COMBOBOX

    def __init__(self, choices=None, value="", onselect=None, **kwargs):
        self.onselect = onselect
        wxparams = {'value': value}
        if choices is not None:
            wxparams['choices'] = choices
        kwargs['wxparams'] = wxparams
        Control.__init__(self, **kwargs)

    set_onenter = event_binder(wx.EVT_TEXT_ENTER)
    value = value_property


class RadioBox(ControlWithItems):
    """选择框"""
    wxtype = wx.RadioBox
    wxevent = wx.EVT_RADIOBOX

    def __init__(self, label="", choices=None, onselect=None, **kwargs):
        self.onselect = onselect
        wxparams = {'label': label}
        if choices:
            wxparams['choices'] = choices
        kwargs['wxparams'] = wxparams
        Control.__init__(self, **kwargs)

    def apply_style(self):
        super().apply_style()
        direction = self.computed_style.get('flex-direction', None)
        if direction is not None:
            if direction == 'row':
                self.wxstyle |= wx.RA_SPECIFY_ROWS
            elif direction == 'column':
                self.wxstyle |= wx.RA_SPECIFY_COLS


class Hr(Control):
    """静态线"""
    wxtype = wx.StaticLine

    def __init__(self, vertical=False, **kwargs):
        kwargs['wxstyle'] = wx.VERTICAL if vertical else wx.HORIZONTAL
        Control.__init__(self, **kwargs)


class FilePickerCtrl(Control):
    """文件选择器"""
    wxtype = wx.FilePickerCtrl

    def __init__(self, path=None, msg="", wildcard="", **kwargs):
        kwargs['wxparams'] = dict(path=path, msg=msg, wildcard=wildcard)
        Control.__init__(self, **kwargs)

    set_onchange = event_binder(wx.EVT_FILEPICKER_CHANGED)


class DirPickerCtrl(Control):
    """目录选择器"""
    wxtype = wx.DirPickerCtrl

    def __init__(self, path=None, msg="", **kwargs):
        kwargs['wxparams'] = dict(path=path, msg=msg)
        Control.__init__(self, **kwargs)

    set_onchange = event_binder(wx.EVT_DIRPICKER_CHANGED)


class TreeCtrl(Control):
    """树控件"""
    wxtype = wx.TreeCtrl

    def __init__(self, wxstyle=wx.TR_HAS_BUTTONS | wx.TR_SINGLE, **kwargs):
        Control.__init__(self, wxstyle=wxstyle, **kwargs)

    set_onchange = event_binder(wx.EVT_FILEPICKER_CHANGED, pass_event=True)


class StatusBar(Control):
    wxtype = wx.StatusBar

    def __init__(self, **kwargs):
        Control.__init__(self, **kwargs)
        self.wxparams.pop('pos')
        self.wxparams.pop('size')

    def onready(self):
        super().onready()
        self.GetParent().SetStatusBar(self.wxwindow)


# exui


def Label(text):
    return Text(text, class_="input_label expand")


class HotkeyCtrl(TextInput):
    def __init__(self, *args, **kwargs):
        self.value = None
        self.code = None
        self.mode = None
        kwargs['wxstyle'] = wx.TE_PROCESS_ENTER
        super().__init__(*args, **kwargs)

    def onready(self):
        super().onready()
        self.set_on_keydown(self.onkey)

    def onkey(self, _, event):
        code = event.GetKeyCode()
        if WXK.ismod(code):
            return
        mod = event.GetModifiers()
        self.handle_key(code, mod)
        return True

    def handle_key(self, code, mod):
        self.value = WXK.getname(code, mod)
        self.code = code
        self.mode = mod
