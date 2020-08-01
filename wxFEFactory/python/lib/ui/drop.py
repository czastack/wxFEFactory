from . import wx


class FileDropListener(wx.FileDropTarget):
    def __init__(self, listener):
        wx.FileDropTarget.__init__(self)
        self.listener = listener

    def OnDropFiles(self, x, y, filenames):
        return self.listener(x, y, filenames) == False


class TextDropListener(wx.TextDropTarget):
    def __init__(self, listener):
        wx.TextDropTarget.__init__(self)
        self.listener = listener

    def OnDropText(self, x, y, text):
        return self.listener(x, y, text) == False
