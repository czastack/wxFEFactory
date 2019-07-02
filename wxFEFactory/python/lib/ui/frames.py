import fefactory_api
from .view import Layout
from . import wx


class BaseTopLevelWindow(Layout):
    _onclose = None

    def onready(self):
        super().onready()
        self.Show()

    def onclose(self, event):
        if self._onclose:
            if self._onclose(event) is False:
                event.Veto()
                return False
            event.Skip()
        return True

    def set_onclose(self, fn):
        self._onclose = fn

    @property
    def keeptop(self):
        return self.has_wxstyle(wx.STAY_ON_TOP)

    @keeptop.setter
    def keeptop(self, value):
        self.toggle_wxstyle(wx.STAY_ON_TOP, value)


class BaseFrame(BaseTopLevelWindow):
    def onready(self):
        self.bind_event_e(wx.EVT_CLOSE_WINDOW, self.onclose)
        if self.menubar:
            self.set_menu(self.menubar)

        super().onready()

    def set_menu(self, menubar):
        self.menubar = menubar
        self.SetMenuBar(menubar.wxwindow)
        if not self.has_event_type(wx.EVT_MENU):
            self.Bind(wx.EVT_MENU, self.on_menu)

    def on_menu(self, event):
        """菜单选中事件"""
        self.menubar.onselect(event.GetId())


class Window(BaseFrame):
    wxtype = wx.Frame

    def __init__(self, title, menubar=None, **kwargs):
        BaseFrame.__init__(self, **kwargs)
        self.wxparams['title'] = title
        self.menubar = menubar


class MDIParentFrame(BaseFrame):
    wxtype = wx.MDIParentFrame

    def __init__(self, title, menubar=None, **kwargs):
        BaseFrame.__init__(self, **kwargs)
        self.wxparams['title'] = title
        self.menubar = menubar


class MDIChildFrame(BaseFrame):
    wxtype = wx.MDIChildFrame

    def __init__(self, title, menubar=None, **kwargs):
        BaseFrame.__init__(self, **kwargs)
        self.wxparams['title'] = title
        self.menubar = menubar


class HotkeyWindow(Window):
    def __init__(self, **kwargs):
        Window.__init__(self, **kwargs)
        self.hotkey_map = {}

    def prepare_hotkey(self, hotkey):
        if isinstance(hotkey, str):
            return fefactory_api.GlobalAddAtom(hotkey)
        else:
            return hotkey

    def RegisterHotKeys(self, hotkeys):
        # TODO
        pass


class KeyHookWindow(Window):
    pass


class Dialog(BaseTopLevelWindow):
    wxtype = wx.Dialog
    default_style = wx.DEFAULT_DIALOG_STYLE | wx.MINIMIZE_BOX | wx.RESIZE_BORDER | wx.CLIP_CHILDREN

    def __init__(self, title, wxstyle=default_style, **kwargs):
        BaseTopLevelWindow.__init__(self, **kwargs)
        self.wxparams['title'] = title

    def dismiss(self, ok=True):
        if self.IsModal():
            self.EndModal(ok)
        else:
            self.Hide()
