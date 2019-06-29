from .view import Layout, Control
from . import wx


class ToolBarBase(Layout):
    def __init__(self, **kwargs):
        Layout.__init__(**kwargs)
        self.listeners = {}

    def onready(self):
        super().onready()
        # Bind(wx.EVT_COMMAND_TOOL_CLICKED, &ToolBarBase::onClick, this)

    def onclick(self, event):
        pass

    def layout_child(self, child, styles):
        self.AddControl(child, "", None)


class ToolBar(ToolBarBase):
    wxtype = wx.ToolBar


class AuiToolBar(ToolBarBase):
    wxtype = wx.AuiToolBar
