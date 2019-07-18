from .view import View, Layout
from . import wx
from lib.exctypes import int32


class SizerLayout(Layout):
    def layout_child(self, child, style):
        flag = self.get_box_flag(style)
        weight = style.get('weight', 0)
        padding = style.get('padding', 5)
        self.sizer.Add(child.wxwindow, weight, flag, padding)

    def layout(self):
        self.sizer.Layout()

    def set_sizer(self, sizer):
        self.sizer = sizer
        self.SetSizer(sizer)

    def get_box_flag(self, style):
        """获取布局参数"""
        flag = 0
        if style.get('expand', False):
            flag |= wx.EXPAND

        padding_flag = style.get('padding-flag', 0)
        if padding_flag is not 0:
            if padding_flag is 1:
                flag |= wx.ALL
            else:
                if padding_flag & 0b1000:
                    flag |= wx.TOP
                if padding_flag & 0b0100:
                    flag |= wx.RIGHT
                if padding_flag & 0b0010:
                    flag |= wx.BOTTOM
                if padding_flag & 0b0001:
                    flag |= wx.LEFT

        vertical = style.get('vertical-align', None)
        if vertical is not None:
            if vertical == 'top':
                flag |= wx.ALIGN_TOP
            elif vertical == 'bottom':
                flag |= wx.ALIGN_BOTTOM
            elif vertical == 'middle':
                flag |= wx.ALIGN_CENTER_VERTICAL
            else:
                print("%s: %s not available" % ('vertical-align', vertical))

        align = style.get('align', None)
        if align is not None:
            if align == 'left':
                flag |= wx.ALIGN_LEFT
            elif align == 'right':
                flag |= wx.ALIGN_RIGHT
            elif align == 'center':
                flag |= wx.ALIGN_CENTER_HORIZONTAL
            else:
                print("%s: %s not available" % ('align', align))

        return flag


class SizerPanel(SizerLayout):
    wxtype = wx.Panel


class Vertical(SizerPanel):
    """垂直布局"""
    def onready(self):
        self.set_sizer(wx.BoxSizer(wx.VERTICAL))
        super().onready()


class Horizontal(SizerPanel):
    """水平布局"""
    def onready(self):
        self.set_sizer(wx.BoxSizer(wx.HORIZONTAL))
        super().onready()


class GridLayout(SizerPanel):
    """网格布局"""
    def __init__(self, rows=0, cols=2, vgap=0, hgap=0, **kwargs):
        self.rows = rows
        self.cols = cols
        self.vgap = vgap
        self.hgap = hgap
        super().__init__(**kwargs)

    def onready(self):
        self.set_sizer(wx.GridSizer(self.rows, self.cols, self.vgap, self.hgap))
        super().onready()


class FlexGridLayout(SizerPanel):
    """网格布局"""
    def __init__(self, rows=0, cols=2, vgap=0, hgap=0, **kwargs):
        self.rows = rows
        self.cols = cols
        self.vgap = vgap
        self.hgap = hgap
        super().__init__(**kwargs)

    def onready(self):
        sizer = wx.FlexGridSizer(self.rows, self.cols, self.vgap, self.hgap)
        sizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        self.set_sizer(sizer)
        super().onready()


class ScrollView(SizerLayout):
    wxtype = wx.ScrolledWindow

    def __init__(self, horizontal=False, wxstyle=int32(wx.HSCROLL | wx.VSCROLL).value, **kwargs):
        self.horizontal = horizontal
        super().__init__(wxstyle=wxstyle, **kwargs)

    def onready(self):
        self.SetScrollRate(5, 5)
        self.set_sizer(wx.BoxSizer(wx.HORIZONTAL if self.horizontal else wx.VERTICAL))
        super().onready()

    def layout(self):
        self.sizer.FitInside(self.wxwindow)
        self.Layout()


class SplitterWindow(Layout):
    """分割窗口"""
    wxtype = wx.SplitterWindow

    def __init__(self, horizontal=False, sashpos=0, **kwargs):
        self.horizontal = horizontal
        self.sashpos = sashpos
        Layout.__init__(self, **kwargs)

    def onready(self):
        super().onready()
        length = len(self.children)
        if length > 2:
            print('SplitterWindow不支持大于两个子元素')
            return
        if length is 1:
            self.Initialize(self.children[0])
        elif length is 2:
            child1 = self.children[0]
            child2 = self.children[1]
            if self.horizontal:
                self.SplitHorizontally(child1, child2, self.sashpos)
            else:
                self.SplitVertically(child1, child2, self.sashpos)


class StaticBox(SizerLayout):
    """静态框"""
    wxtype = wx.StaticBox

    def __init__(self, label, **kwargs):
        super().__init__(wxparams={'label': label}, **kwargs)

    def onready(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.InsertSpacer(0, 15)
        self.set_sizer(sizer)
        super().onready()


class BookCtrlBase(Layout):
    def layout_child(self, child, style):
        caption = child.extra['caption']
        self.AddPage(child.wxwindow, caption)

    def get_page(self, n=None):
        if n is None:
            n = self.GetSelection()
        else:
            count = self.GetPageCount()
            if n < 0:
                n += count
            if not 0 <= n < count:
                raise IndexError('list index out of range')

        return self.GetPage(n).GetHost()

    def set_onchange(self, onchange, reset=True):
        self.bind_event(self.wxevent, onchange, reset)

    @property
    def index(self):
        return self.GetSelection()

    @index.setter
    def index(self, n):
        self.SetSelection(n)


class Notebook(BookCtrlBase):
    wxtype = wx.Notebook
    wxevent = wx.EVT_NOTEBOOK_PAGE_CHANGED


class Listbook(BookCtrlBase):
    wxtype = wx.Listbook
    wxevent = wx.EVT_LISTBOOK_PAGE_CHANGED
