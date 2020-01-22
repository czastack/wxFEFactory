from .view import Layout, Control
from . import wx


class ToolBarBase(Layout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listeners = {}
        self.Bind(wx.EVT_COMMAND_TOOL_CLICKED, self.onclick)

    def set_onclick(self, toolid, listener):
        self.listeners[toolid] = listener

    def onclick(self, event):
        toolid = event.GetId()
        listener = self.listeners.get(toolid, None)
        if listener is not None:
            listener(self, toolid)

    def layout_child(self, child, styles):
        self.AddControl(child.wxwindow, "", None)


class ToolBar(ToolBarBase):
    wxtype = wx.ToolBar


class AuiToolBar(ToolBarBase):
    wxtype = wx.AuiToolBar
