import os
import sys
import wx
import wx.aui
import wx.py
from wx.py.pseudo import PseudoFileOut, PseudoFileErr


class ButtonPanel(wx.aui.AuiNotebook):
    """
    底部面板
    """
    def __init__(self, parent, *args, **kwargs):
        kwargs.setdefault('style', wx.aui.AUI_NB_DEFAULT_STYLE & ~wx.aui.AUI_NB_CLOSE_ON_ACTIVE_TAB)
        wx.aui.AuiNotebook.__init__(self, parent, *args, **kwargs)
        self.outputWindow = wx.TextCtrl(self, style=wx.TE_READONLY | wx.TE_MULTILINE | wx.TE_RICH2 | wx.TE_WORDWRAP)
        self.AddPage(self.outputWindow, '输出')

        self.shell = wx.py.shell.Shell(self, execStartupScript=False)
        self.AddPage(self.shell, '控制台')

        self.stdout = sys.stdout
        self.stderr = sys.stderr

        self.redirectStdout()
        self.redirectStderr()

    def LoadSettings(self, config):
        """
        加载配置
        """
        self.config = config
        self.shell.LoadSettings(self.config)

    def redirectStdout(self, redirect=True):
        """重定向标准输出"""
        if redirect:
            sys.stdout = PseudoFileOut(self.outputAppendText)
        else:
            sys.stdout = self.stdout

    def redirectStderr(self, redirect=True):
        """重定向标准错误"""
        if redirect:
            sys.stderr = PseudoFileErr(self.outputAppendText)
        else:
            sys.stderr = self.stderr

    def outputAppendText(self, text):
        self.outputWindow.AppendText(text)
