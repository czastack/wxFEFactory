from .view import View, Layout
from . import wx


class SizerLayout(Layout):

    def layout_child(self, child, style):
        flag = self.get_box_flag(style)
        weight = style.get('weight', 0)
        padding = style.get('padding', 5)
        self.GetSizer().Add(child, weight, flag, padding)

    def layout(self):
        self.GetSizer().Layout()

    def relayout(self):
        self.layout()

    def __exit__(self, *args):
        Layout.__exit__(self, *args)
        self.layout()

    def get_box_flag(self, style):
        """获取布局参数"""
        flag = 0
        if child.get('expand', False):
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
        self.SetSizer(wx.BoxSizer(wx.VERTICAL))


class Horizontal(SizerPanel):
    """水平布局"""
    def onready(self):
        self.SetSizer(wx.BoxSizer(wx.HORIZONTAL))


class GridLayout(SizerPanel):
    """网格布局"""
    def __init__(self, rows=0, cols=2, vgap=0, hgap=0, **kwargs):
        super().__init__(**kwargs)
        self.rows = rows
        self.cols = cols
        self.vgap = vgap
        self.hgap = hgap

    def onready(self):
        self.SetSizer(wx.GridSizer(self.rows, self.cols, self.vgap, self.hgap))


class FlexGridLayout(SizerPanel):
    """网格布局"""
    def __init__(self, rows=0, cols=2, vgap=0, hgap=0, **kwargs):
        super().__init__(**kwargs)
        self.rows = rows
        self.cols = cols
        self.vgap = vgap
        self.hgap = hgap

    def onready(self):
        sizer = wx.FlexGridSizer(self.rows, self.cols, self.vgap, self.hgap)
        sizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        self.SetSizer(sizer)


class ScrollView(SizerLayout):
    def __init__(self, horizontal=False, wxstyle=wx.HSCROLL | wx.VSCROLL, **kwargs):
        super().__init__(wxstyle=wxstyle, **kwargs)
        self.horizontal = horizontal

    def onready(self):
        self.SetScrollRate(5, 5)
        self.SetSizer(wx.BoxSizer(wx.HORIZONTAL if self.horizontal else wx.VERTICAL))

    def layout(self):
        self.GetSizer().FitInside(self.wxwindow)
        self.Layout()


class SplitterWindow(Layout):
    """分割窗口"""
    wxtype = wx.SplitterWindow

    def __init__(self, horizontal=False, sashpos=0, **kwargs):
        Layout.__init__(self, **kwargs)
        self.horizontal = horizontal
        self.sashpos = sashpos

    def onready(self):
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
        super().__init__(**kwargs)
        self.wxparams['label'] = label

    def onready(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.InsertSpacer(0, 15)
        self.SetSizer(sizer)


class BookCtrlBase(Layout):
    def layout_child(self, child, style):
        caption = child.extra['caption']
        self.AddPage(child, caption)

    def getpage(self, n=None):
        if n is None:
            n = self.GetSelection()
        else:
            count = self.GetPageCount()
            if n < 0:
                n += count
            if not 0 <= n < count:
                raise IndexError('list index out of range')

        return self.GetPage(n).GetClientData()

    def set_onchange(self, onchange, reset=True):
        self.bind_event(self.wxevent, onchange, reset)


class Notebook(BookCtrlBase):
    wxtype = wx.Notebook
    wxevent = wx.EVT_NOTEBOOK_PAGE_CHANGED


class Listbook(BookCtrlBase):
    wxtype = wx.Listbook
    wxevent = wx.EVT_LISTBOOK_PAGE_CHANGED
