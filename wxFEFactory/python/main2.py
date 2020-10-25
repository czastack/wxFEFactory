import os
import sys
import wx
import wx.aui
import wx.py


class MainFrame (wx.Frame):

    def __init__(self, parent):
        width, height = wx.GetDisplaySize()
        if width <= 1366:
            size = (480, 640)
        elif width <= 1920:
            size = (640, 960)
        elif width <= 2560:
            size = (720, 1080)
        else:  # elif width <= 3840:
            size = (1366, 1800)

        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition, size=size,
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.mgr = wx.aui.AuiManager()
        self.mgr.SetManagedWindow(self)
        self.mgr.SetFlags(wx.aui.AUI_MGR_DEFAULT)

        self.menubar = wx.MenuBar(0)
        self.SetMenuBar(self.menubar)

        self.statusBar = self.CreateStatusBar(1, wx.STB_SIZEGRIP, wx.ID_ANY)

        self.auiToolBar = wx.aui.AuiToolBar(
            self, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, 100), wx.aui.AUI_TB_HORZ_LAYOUT)
        self.auiToolBar.Realize()
        self.mgr.AddPane(self.auiToolBar, wx.aui.AuiPaneInfo().Top().CaptionVisible(
            False).CloseButton(False))

        self.notebook = wx.aui.AuiNotebook(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.aui.AUI_NB_DEFAULT_STYLE)
        self.mgr.AddPane(self.notebook, wx.aui.AuiPaneInfo().Center().CaptionVisible(
            False).CloseButton(False))

        self.bottomPanel = wx.aui.AuiNotebook(
            self, wx.ID_ANY, wx.DefaultPosition, (-1, 300), wx.aui.AUI_NB_DEFAULT_STYLE)
        self.mgr.AddPane(self.bottomPanel, wx.aui.AuiPaneInfo().Bottom().CloseButton(
            False).MaximizeButton(True))

        self.outputWindow = wx.py.editwindow.EditWindow(parent=self)
        self.bottomPanel.AddPage(self.outputWindow, '输出')

        self.shell = wx.py.shell.Shell(parent=self)
        self.bottomPanel.AddPage(self.shell, '控制台')

        self.mgr.Update()
        self.Centre(wx.BOTH)

        self.shell.redirectStdout()
        self.shell.redirectStderr()

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.LoadSettings()

        print(111)

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
        self.shell.LoadSettings(self.config)

        self.outputWindow.SetReadOnly(True)
        self.outputWindow.setDisplayLineNumbers(True)
        self.outputWindow.SetWrapMode(True)

    def OnClose(self, event):
        """Event handler for closing."""
        # This isn't working the way I want, but I'll leave it for now.
        if self.shell.waiting:
            if event.CanVeto():
                event.Veto(True)
        else:
            self.shell.destroy()
            self.mgr.UnInit()
            event.Skip()


if __name__ == "__main__":
    app = wx.App()
    frm = MainFrame(None)
    frm.Show()
    app.MainLoop()
