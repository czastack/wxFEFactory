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

    def render(self, parent):
        self.wxwindow = parent.wxwindow
        self.mgr = wx.AuiManager(parent.wxwindow)
        # Bind(wx.EVT_CLOSE_WINDOW, &AuiManager::onOwnerClose, this)

    def relayout(self):
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
            info.Hide()

    def show_pane(self, name, show=True):
        """显示面板"""
        self.GetPane(name).Show(show)
        self.layout()


class AuiNotebook(Layout):
    wxtype = wx.AuiNotebook

    def __init__(self, **kwagrs):
        Layout.__init__(self, **kwagrs)
        self.close_listeners = {}

    def __del__(self):
        self.close_listeners.clear()

    def onready(self):
        # Bind(wx.EVT_AUINOTEBOOK_PAGE_CLOSE, &AuiNotebook::OnPageClose, this)
        pass

    def on_page_close(self, event):
        selection = event.GetSelection()
        if not self.can_page_close(selection):
            event.Veto()
        else:
            self._remove_page(selection)

    def _remove_page(self, n):
        page = self.GetPage(n)
        self.children.remove(page)

    def can_page_close(self, n=None):
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
                page.onClose(wx.CloseEvent(wx.EVT_CLOSE_WINDOW))


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
