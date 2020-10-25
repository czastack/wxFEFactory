import os
import sys
import wx
import wx.aui
import wx.py

from widgets.buttonpanel import ButtonPanel


class MainFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title='主窗口', style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSize(self.FromDIP(wx.Size(640, 960)))
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.mgr = wx.aui.AuiManager()
        self.mgr.SetManagedWindow(self)
        self.mgr.SetFlags(wx.aui.AUI_MGR_DEFAULT)

        self.Freeze()
        self.menubar = wx.MenuBar(0)
        self.SetMenuBar(self.menubar)

        self.statusBar = self.CreateStatusBar(1, wx.STB_SIZEGRIP, wx.ID_ANY)

        self.auiToolBar = wx.aui.AuiToolBar(self, size=self.FromDIP(wx.Size(-1, 50)), style=wx.aui.AUI_TB_HORZ_LAYOUT)
        # self.auiToolBar.Realize()
        self.mgr.AddPane(self.auiToolBar, wx.aui.AuiPaneInfo().Top().CaptionVisible(
            False).CloseButton(False))

        self.notebook = wx.aui.AuiNotebook(self)
        self.mgr.AddPane(self.notebook, wx.aui.AuiPaneInfo().Center().CaptionVisible(
            False).CloseButton(False))

        self.bottomPanel = ButtonPanel(self, size=self.FromDIP(wx.Size(-1, 150)))
        self.mgr.AddPane(self.bottomPanel, wx.aui.AuiPaneInfo().Bottom().CloseButton(
            False).MaximizeButton(True))

        self.mgr.Update()
        self.Centre(wx.BOTH)
        self.Thaw()

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.LoadSettings()

    def LoadSettings(self):
        """
        加载配置
        """
        confDir = os.path.join(os.path.dirname(sys.executable), 'config')
        if not os.path.exists(confDir):
            os.mkdir(confDir)
        fileName = os.path.join(confDir, 'config.ini')
        self.config = wx.FileConfig(localFilename=fileName)
        self.config.SetRecordDefaults(True)

        self.bottomPanel.LoadSettings(self.config)

    def OnClose(self, event):
        """Event handler for closing."""
        if self.bottomPanel.shell.waiting:
            if event.CanVeto():
                event.Veto(True)
        else:
            self.bottomPanel.shell.destroy()
            self.mgr.UnInit()
            event.Skip()


if __name__ == "__main__":
    app = wx.App()
    frm = MainFrame(None)
    frm.Show()
    app.MainLoop()
