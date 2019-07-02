from .containers import Layout
from .frames import BaseFrame, BaseTopLevelWindow
from . import wx


class AuiManager(Layout):
    """自动布局器"""
    def __init__(self, **kwargs):
        Layout.__init__(self, **kwargs)
        self.mgr = None
        self.close_listeners = {}

    def __del__(self):
        self.mgr.UnInit()
        self.close_listeners.clear()

    def on_owner_close(self, event):
        event.Skip()
        self.UnInit()
        del self

    def render(self, parent):
        self.wxwindow = parent.wxwindow
        self.mgr = wx.AuiManager(parent.wxwindow)
        self.bind_event_e(wx.EVT_CLOSE_WINDOW, self.on_owner_close)

    def layout(self):
        self.mgr.Update()

    def layout_child(self, child, style):
        data = child.extra
        info = wx.AuiPaneInfo()

        if data is None:
            print(child)

        if 'name' in data:
            info.Name(data['name'])

        if 'caption' in data:
            info.Caption(data['caption'])

        direction = data.get('direction', None)
        if direction is not None:
            info.dock_direction = wx.AUI_DOCK_MAP[direction]

        closeButton = data.get('closeButton', None)
        if closeButton is not None:
            info.CloseButton(closeButton)

        maximizeButton = data.get('maximizeButton', None)
        if maximizeButton is not None:
            info.MaximizeButton(maximizeButton)

        minimizeButton = data.get('minimizeButton', None)
        if minimizeButton is not None:
            info.MinimizeButton(minimizeButton)

        captionVisible = data.get('captionVisible', None)
        if captionVisible is not None:
            info.CaptionVisible(captionVisible)

        row = data.get('row', None)
        if row is not None:
            info.Row(row)

        if data.get('hide', False):
            info.Show(False)

        self.mgr.AddPane(child.wxwindow, info)

    def show_pane(self, name, show=True):
        """显示面板"""
        self.mgr.GetPane(name).Show(show)
        self.layout()


class AuiNotebook(Layout):
    wxtype = wx.AuiNotebook

    def __init__(self, **kwagrs):
        Layout.__init__(self, **kwagrs)
        self.close_listeners = {}

    def __del__(self):
        self.close_listeners.clear()

    def onready(self):
        self.Bind(wx.EVT_AUINOTEBOOK_PAGE_CLOSE, self.on_page_close)

    def on_page_close(self, event):
        """页面关闭事件"""
        selection = event.GetSelection()
        if not self.can_page_close(selection):
            event.Veto()
        else:
            self.remove_page(selection)

    def remove_page(self, n):
        """移除page引用"""
        page = self.GetPage(n)
        self.children.remove(page.GetHost())

    def close_page(self, n=None):
        """关闭指定页面"""
        if n is None:
            n = self.SetSelection()

        if self.can_page_close(n):
            self.remove_page(n)
            self.DeletePage(n)
        return False

    def close_all_page(self):
        """关闭全部页面"""
        for i in range(self.GetPageCount()):
            if not self.close_page(i):
                return False
        return True

    def can_page_close(self, n=None):
        """检查页面能否删除"""
        if self.GetPageCount() is 0:
            return False
        if n is None:
            n = self.GetSelection()
        succeed = True
        page = self.GetPage(n)
        onclose = self.close_listeners.get(page, None)
        if onclose is not None:
            if onclose():
                succeed = True
                self.close_listeners.pop(page)
        if succeed:
            # 手动调用子窗口的onClose
            if isinstance(page, BaseTopLevelWindow):
                # TODO
                page.onclose(wx.CloseEvent(wx.EVT_CLOSE_WINDOW))

    def set_on_page_changed(self, fn):
        """设置页面切换事件"""
        self.bind_event(wx.EVT_AUINOTEBOOK_PAGE_CHANGED, fn)


class AuiMDIParentFrame(BaseFrame):
    wxtype = wx.AuiMDIParentFrame

    def __init__(self, title, **kwagrs):
        Layout.__init__(self, **kwagrs)
        self.wxparams['title'] = title


class AuiMDIChildFrame(BaseTopLevelWindow):
    wxtype = wx.AuiMDIParentFrame

    def __init__(self, title, **kwagrs):
        Layout.__init__(self, **kwagrs)
        self.wxparams['title'] = title
