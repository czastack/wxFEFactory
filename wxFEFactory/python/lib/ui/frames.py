import traceback
import fefactory_api
from .view import Layout
from . import wx


class BaseTopLevelWindow(Layout):
    _onclose = None

    def onclose(self, event):
        if self._onclose:
            if self._onclose(self, event) is False:
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


class Frame(BaseFrame):
    wxtype = wx.Frame

    def __init__(self, title, menubar=None, **kwargs):
        self.menubar = menubar
        BaseFrame.__init__(self, wxparams={'title': title}, **kwargs)


class MDIParentFrame(BaseFrame):
    wxtype = wx.MDIParentFrame

    def __init__(self, title, menubar=None, **kwargs):
        self.menubar = menubar
        BaseFrame.__init__(self, wxparams={'title': title}, **kwargs)


class MDIChildFrame(BaseFrame):
    wxtype = wx.MDIChildFrame

    def __init__(self, title, menubar=None, **kwargs):
        self.menubar = menubar
        BaseFrame.__init__(self, wxparams={'title': title}, **kwargs)


class HotkeyFrame(Frame):
    def __init__(self, **kwargs):
        self.hotkey_map = {}
        Frame.__init__(self, **kwargs)

    def __del__(self):
        self.hotkey_map.clear()

    def onready(self):
        self.Bind(wx.EVT_HOTKEY, self.onhotkey)

    def prepare_hotkey(self, hotkey):
        """获取全局唯一的id"""
        if isinstance(hotkey, str):
            return fefactory_api.GlobalAddAtom(hotkey)
        else:
            return hotkey

    def register_hotkey(self, hotkey_id, modifiers, vk, onhotkey):
        """注册热键"""
        hotkey_int = self.prepare_hotkey(hotkey_id)
        if hotkey_int in self.hotkey_map:
            print(hotkey_id, '已经在使用了')
        else:
            if self.RegisterHotKey(hotkey_int, modifiers, vk):
                self.hotkey_map[hotkey_int] = onhotkey
            else:
                print(hotkey_id, "热键注册失败")

    def unregister_hotkey(self, hotkey_id, force=False):
        """卸载热键"""
        hotkey_int = self.prepare_hotkey(hotkey_id)
        if force or hotkey_int in self.hotkey_map:
            if self.UnregisterHotKey(hotkey_int):
                self.hotkey_map.pop(hotkey_int, None)
                return True
        return False

    def register_hotkeys(self, hotkeys):
        """批量注册热键"""
        for modifiers, vk, onhotkey, *hotkey_id in hotkeys:
            if hotkey_id:
                hotkey_id = hotkey_id[0]
            else:
                hotkey_id = onhotkey.__name__
            self.register_hotkey(hotkey_id, modifiers, vk, onhotkey)

    def stop_hotkey(self):
        for hotkey_int in self.hotkey_map:
            if fefactory_api.GlobalDeleteAtom(hotkey_int) is 0:
                self.unregister_hotkey(hotkey_int)

    def onhotkey(self, event):
        hokey_int = event.GetId()
        ret = self.hotkey_map[hokey_int]()
        if ret is not True:
            event.Skip()


class KeyHookFrame(Frame):
    def __init__(self, **kwargs):
        self.hotkey_map = {}
        Frame.__init__(self, **kwargs)

    def __del__(self):
        self.hotkey_map.clear()

    def onready(self):
        self.mgr = wx.KeyHookManager(self.wxwindow)
        self.setHook = self.mgr.setHook
        self.unsetHook = self.mgr.unsetHook
        self.Bind(wx.EVT_KEYHOOK, self.onhotkey)

    def register_hotkeys(self, hotkeys):
        """批量注册热键"""
        for modifiers, vk, onhotkey in hotkeys:
            key = (modifiers << 16) | vk
            if key in self.hotkey_map:
                print('已经在使用了')
            else:
                self.hotkey_map[key] = onhotkey

    def onhotkey(self, event):
        modifiers = 0
        if (event.lParam & 0x20000000) != 0:
            modifiers |= MOD_ALT
        if wx.GetKeyState(wx.VK_CONTROL) < 0:
            modifiers |= MOD_CONTROL
        if wx.GetKeyState(wx.VK_SHIFT) < 0:
            modifiers |= MOD_SHIFT
        key = modifiers << 16 | event.wParam
        fn = self.hotkey_map.get(key, None)
        if fn is not None:
            fn()

    def _uninited(self, *args, **kwargs):
        raise ValueError('mgr未初始化')

    setHook = _uninited
    unsetHook = _uninited


class Dialog(BaseTopLevelWindow):
    wxtype = wx.Dialog
    default_style = wx.DEFAULT_DIALOG_STYLE | wx.MINIMIZE_BOX | wx.RESIZE_BORDER | wx.CLIP_CHILDREN

    def __init__(self, title, wxstyle=default_style, **kwargs):
        BaseTopLevelWindow.__init__(self, wxparams={'title': title}, wxstyle=wxstyle, **kwargs)

    def dismiss(self, ok=True):
        if self.IsModal():
            self.EndModal(ok)
        else:
            self.Hide()
