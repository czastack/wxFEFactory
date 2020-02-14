from lib.win32.keys import WXK
from .view import View, Control, EventFunctor, event_binder, value_property
from . import wx


class Button(Control):
    """普通按钮"""
    wxtype = wx.Button

    def __init__(self, label, onclick=None, **kwargs):
        super().__init__(wxparams={'label': label}, **kwargs)
        if onclick:
            self.set_onclick(onclick)

    set_onclick = event_binder(wx.EVT_BUTTON)

    def click(self):
        self.post_event(wx.CommandEvent)


class BitmapButton(Button):
    """图像按钮"""
    def __init__(self, src, **kwargs):
        self.src = src
        super().__init__(**kwargs)

    def render(self, parent):
        bitmap = wx.Bitmap(self.src)
        self.bind_wx(wx.BitmapButton(parent, label=bitmap, **self.wxparams))
        del self.src, self.onclick


class CheckableControl(Control):
    def __init__(self, checked=False, onchange=None, **kwargs):
        super().__init__(**kwargs)
        if checked:
            self.SetValue(True)
        if onchange:
            self.set_onchange(onchange)

    def set_onchange(self, fn, reset=True):
        self.bind_event(self.wxevent, fn, reset)

    def toggle(self, value=None, post=True):
        """切换状态"""
        if value is None:
            value = not self.GetValue()
        self.SetValue(value)
        if post:
            self.post_event(self.wxevent)
        else:
            self.call_event(self.wxevent)

    checked = value = value_property


class ToggleButton(CheckableControl):
    """开关按钮"""
    wxtype = wx.ToggleButton
    wxevent = wx.EVT_TOGGLEBUTTON

    def __init__(self, label, **kwargs):
        super().__init__(wxparams={'label': label}, **kwargs)


class CheckBox(CheckableControl):
    """复选框"""
    wxtype = wx.CheckBox
    wxevent = wx.EVT_CHECKBOX

    def __init__(self, label="", align_right=False, **kwargs):
        if align_right:
            kwargs['wxstyle'] = kwargs.get('wxstyle', 0) | wx.ALIGN_RIGHT
        kwargs['wxparams'] = {'label': label}
        super().__init__(**kwargs)


class StaticBitmap(Control):
    """静态图片"""
    wxtype = wx.StaticBitmap

    def __init__(self, label, **kwargs):
        kwargs['wxparams'] = {'label': label}
        super().__init__(**kwargs)

    def render(self, parent):
        bitmap = wx.Bitmap(self.label)
        self.bind_wx(wx.StaticBitmap(parent.wxwindow, label=bitmap, **self.wxparams))
        del self.label


class Text(Control):
    """静态文本"""
    wxtype = wx.StaticText

    def __init__(self, label, **kwargs):
        super().__init__(wxparams={'label': label}, **kwargs)

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
        super().__init__(**kwargs)

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
        super().__init__(wxparams={'value': value}, **kwargs)
        if not search_button:
            self.ShowSearchButton(False)
        if cancel_button:
            self.ShowCancelButton(True)

    set_onsubmit = event_binder(wx.EVT_SEARCH)
    set_oncancel = event_binder(wx.EVT_SEARCH_CANCEL)
    value = value_property


class SpinCtrl(Control):
    """数字输入框"""
    wxtype = wx.SpinCtrl

    def __init__(self, value="", min=0, max=100, initial=0, wxstyle=wx.SP_ARROW_KEYS | wx.ALIGN_RIGHT, **kwargs):
        kwargs['wxparams'] = dict(value=value, min=min, max=max, initial=initial)
        kwargs['wxstyle'] = wxstyle
        super().__init__(**kwargs)

    set_onchange = event_binder(wx.EVT_SPINCTRL)
    set_onenter = event_binder(wx.EVT_TEXT_ENTER)


class ColorPicker(Control):
    """颜色选择器"""
    wxtype = wx.ColourPickerCtrl

    def __init__(self, color=None, onchange=None, **kwargs):
        super().__init__(wxparams={'color': color}, **kwargs)
        self.set_onchange(onchange)

    set_onchange = event_binder(wx.EVT_COLOURPICKER_CHANGED)


class ItemContainer(Control):
    @property
    def count(self):
        return self.GetCount()

    @property
    def index(self):
        return self.GetSelection()

    @index.setter
    def index(self, n):
        self.SetSelection(n)

    @property
    def text(self):
        return self.GetString(self.GetSelection())


class ControlWithItems(ItemContainer):
    def __init__(self, onselect=None, **kwargs):
        super().__init__(**kwargs)
        self.set_onselect(onselect)

    def set_onselect(self, fn, reset=True):
        self.bind_event(self.wxevent, fn, reset)

    def post_select(self):
        self.post_event(self.wxevent)

    def set_selection(self, n, trigger=False):
        self.SetSelection(n)
        if trigger:
            self.post_select()
        return self


class ListBox(ControlWithItems):
    """列表框"""
    wxtype = wx.ListBox
    wxevent = wx.EVT_LISTBOX

    def __init__(self, choices=None, **kwargs):
        if choices is not None:
            kwargs['wxparams'] = {'choices': choices}
        super().__init__(**kwargs)


class CheckListBox(ListBox):
    """带复选列表框"""
    wxtype = wx.CheckListBox


class RearrangeList(CheckListBox):
    """可排序复选列表框"""
    wxtype = wx.RearrangeList

    def __init__(self, order=None, **kwargs):
        super().__init__(wxparams={'order': order}, **kwargs)


class Choice(ControlWithItems):
    """简易下拉框"""
    wxtype = wx.Choice
    wxevent = wx.EVT_CHOICE

    def __init__(self, choices=None, **kwargs):
        if choices is not None:
            kwargs['wxparams'] = {'choices': choices}
        super().__init__(**kwargs)


class ComboBox(ControlWithItems):
    """下拉框"""
    wxtype = wx.ComboBox
    wxevent = wx.EVT_COMBOBOX

    def __init__(self, choices=None, value="", **kwargs):
        wxparams = {'value': value}
        if choices is not None:
            wxparams['choices'] = choices
        kwargs['wxparams'] = wxparams
        super().__init__(**kwargs)

    set_onenter = event_binder(wx.EVT_TEXT_ENTER)
    value = value_property


class RadioBox(ControlWithItems):
    """选择框"""
    wxtype = wx.RadioBox
    wxevent = wx.EVT_RADIOBOX

    def __init__(self, title="", choices=None, **kwargs):
        wxparams = {'title': title}
        if choices:
            wxparams['choices'] = choices
        kwargs['wxparams'] = wxparams
        super().__init__(**kwargs)

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
        super().__init__(**kwargs)


class FilePickerCtrl(Control):
    """文件选择器"""
    wxtype = wx.FilePickerCtrl

    def __init__(self, path="", message="", wildcard="", **kwargs):
        kwargs['wxparams'] = dict(path=path, message=message, wildcard=wildcard)
        super().__init__(**kwargs)

    set_onchange = event_binder(wx.EVT_FILEPICKER_CHANGED)


class DirPickerCtrl(Control):
    """目录选择器"""
    wxtype = wx.DirPickerCtrl

    def __init__(self, path="", message="", **kwargs):
        kwargs['wxparams'] = dict(path=path, message=message)
        super().__init__(**kwargs)

    set_onchange = event_binder(wx.EVT_DIRPICKER_CHANGED)


class TreeCtrl(Control):
    """树控件"""
    wxtype = wx.TreeCtrl

    def __init__(self, wxstyle=wx.TR_HAS_BUTTONS | wx.TR_SINGLE, **kwargs):
        super().__init__(wxstyle=wxstyle, **kwargs)

    set_on_item_activated = event_binder(wx.EVT_TREE_ITEM_ACTIVATED, pass_event=True)


class StatusBar(Control):
    wxtype = wx.StatusBar

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.GetParent().SetStatusBar(self.wxwindow)

    def render(self, parent):
        self.wxparams.pop('pos')
        self.wxparams.pop('size')
        super().render(parent)


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
