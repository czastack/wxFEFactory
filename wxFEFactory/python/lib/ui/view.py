from . import wx


class BinderHelper:
    def __init__(self, fn):
        self.fn = fn

    def __set_name__(self, owner, name):
        self.fn.__qualname__ = name
        setattr(owner, name, self.fn)


def event_binder(event_type, name=None, **args):
    def binder(self, fn, reset=True):
        self.bind_event(event_type, EventFunctor(fn, **args), reset)
    if name is not None:
        binder.__qualname__ = name
    else:
        binder = BinderHelper(binder)
    return binder


@property
def value_property(self):
    return self.GetValue()


@value_property.setter
def value_property(self, value):
    self.SetValue(value)


class View:
    """视图元素"""
    LAYOUTS = []
    wxtype = None
    _here = False

    def __init__(self, parent=None, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, wxstyle=0,
                 class_=None, style=None, wxparams=None, extra=None):
        # style: None | [{}] | {}
        self.style = style
        if wxparams is None:
            wxparams = {}
        wxparams.update(id=id, pos=pos, size=size)
        if wxstyle is not 0:
            wxparams['style'] = wxstyle
        if class_ is not None:
            class_ = class_.split()
        self.computed_style = None
        self.class_ = class_
        self.wxparams = wxparams
        self.extra = extra
        self.event_table = {}
        self.wxwindow = None
        self.contextmenu = None

        parent = parent or self.active_layout()
        if parent is not None:
            parent.append(self)
            styles = parent.get_styles()
            if styles is not None:
                for style in styles:
                    self.try_styles(style)

        if View._here:
            # 立即渲染
            self._render(parent)

    @classmethod
    def active_layout(cls):
        return cls.LAYOUTS[-1] if __class__.LAYOUTS else None

    @classmethod
    def active_wxwindow(cls):
        layout = cls.active_layout()
        return layout and layout.wxwindow

    @classmethod
    def safe_active_wxwindow(cls):
        return self.active_wxwindow() or wx.GetApp().GetTopWindow()

    @property
    def parent(self):
        parent = self.GetParent()
        if parent is not None:
            parent = parent.GetHost()
        return parent

    @property
    def wxstyle(self):
        return self.GetWindowStyle()

    @wxstyle.setter
    def wxstyle(self, value):
        self.SetWindowStyle(value)

    @property
    def size(self):
        size = self.GetSize()
        return size.x, size.y

    @size.setter
    def size(self, value):
        self.SetSize(*value)

    @property
    def position(self):
        position = self.GetPosition()
        return position.x, position.y

    @position.setter
    def position(self, value):
        self.Move(*value)

    @property
    def label(self):
        return self.GetLabel()

    @label.setter
    def label(self, value):
        self.SetLabel(value)

    def has_wxstyle(self, flag):
        """是否有wxWidgets样式flag"""
        return self.GetWindowStyle() & flag != 0

    def toggle_wxstyle(self, flag, toggle=None):
        """切换wxWidgets样式flag
        :param toggle: None 切换, True 设置, False 取消
        """
        style = self.GetWindowStyle()
        if toggle is None:
            toggle = style & flag != 0
        if toggle:
            style |= flag
        else:
            style &= ~flag
        self.SetWindowStyle(style)

    def bind_wx(self, wxwindow):
        self.wxwindow = wxwindow
        wxwindow.SetHost(self)

    def __getattr__(self, name):
        return getattr(self.wxwindow, name)

    def _render(self, parent):
        self.compute_style()
        self.render(parent)
        self.apply_style()
        self.onready()
        parent.layout_child(self, self.computed_style)
        del self.wxparams
        del self.computed_style

    def render(self, parent):
        """渲染"""
        self.bind_wx(self.wxtype(parent and parent.wxwindow, **self.wxparams))

    def onready(self):
        """渲染后的操作"""
        if self.extra:
            tooltip = self.extra.get('tooltip', None)
            if tooltip is not None:
                self.SetToolTip(tooltip)

    def add_style(self, target):
        """添加样式
        :param target: 样式 {} | [{}]
        """
        style = self.style
        if isinstance(style, list):
            temp = style
        else:
            temp = []
            if style is not None:
                temp.append(style)
        if isinstance(target, list):
            temp.extend(target)
        else:
            temp.append(target)
        self.style = temp

    def get_style(self, name):
        """获取某个样式"""
        style = self.style
        if style is not None:
            if isinstance(style, list):
                for item in reversed(style):
                    result = item.get(name, None)
                    if result is not None:
                        return result
            else:
                return style.get(name, None)

    def has_style(self, name):
        """判断是否有该样式"""
        for style in self.iter_style():
            if name in style:
                return True
        return False

    def iter_style(self):
        """遍历样式"""
        style = self.style
        if style is not None:
            if isinstance(style, list):
                for item in style:
                    yield item
            else:
                yield style

    def try_styles(self, styles):
        """尝试应用样式表"""
        typecase = styles.get('type', None)
        classcase = styles.get('class', None)
        if typecase is not None:
            style = typecase.get(self.__class__.__name__, None)
            if style is not None:
                self.add_style(style)

        if classcase is not None and isinstance(self.class_, list):
            for item in self.class_:
                style = classcase.get(item, None)
                if style is not None:
                    self.add_style(style)

    def compute_style(self):
        style = {}
        for item in self.iter_style():
            style.update(item)
        self.computed_style = style
        # 尺寸
        width = style.get('width', -1)
        height = style.get('height', -1)
        if width is not -1 or height is not -1:
            self.wxparams['size'] = wx.Size(width, height)
        return style

    def apply_style(self):
        """应用样式"""
        style = self.computed_style

        if not style:
            return style

        background = style.get('background', None)
        if background is not None:
            if isinstance(background, str):
                background = self.parsecolor(background)
            self.SetBackgroundColour(background)

        color = style.get('color', None)
        if color is not None:
            if isinstance(color, str):
                color = self.parsecolor(color)
            self.SetForegroundColour(color)

        fontsize = style.get('font-size', None)
        if fontsize is not None:
            font = self.GetFont()
            font.SetPointSize(fontsize)
            self.SetFont(font)

        fontDict = style.get('font', None)
        if fontDict is not None:
            font = self.GetFont()
            # 字重
            weight = fontDict.get('weight', None)
            if weight is not None:
                # wx.FONTWEIGHT_NORMAL: 400 | wx.FONTWEIGHT_LIGHT: 300 | wx.FONTWEIGHT_BOLD: 700
                font.SetWeight(weight)
            font_style = fontDict.get('style', None)
            if font_style is not None:
                # wx.FONTSTYLE_NORMAL: 90 | wx.FONTSTYLE_ITALIC: 93 | wx.FONTSTYLE_SLANT: 94
                font.SetStyle(font_style)
            underline = fontDict.get('underline', None)
            if underline is not None:
                font.SetUnderlined(underline)
            face = fontDict.get('face', None)
            if face is not None:
                font.SetFaceName(face)
            self.SetFont(font)

        # 尺寸
        # width = style.get('width', None)
        # height = style.get('height', None)
        # if width or height:
        #     size = self.GetSize()
        #     if width:
        #         size.x = width
        #     if height:
        #         size.y = height
        #     self.SetSize(size)

        # 最大/最小尺寸
        min_width = style.get('min-width', None)
        min_height = style.get('min-height', None)
        max_width = style.get('max-width', None)
        max_height = style.get('max-height', None)

        if min_width or min_height:
            size = self.GetMinSize()
            if min_width:
                size.x = min_width
            if min_height:
                size.y = min_height
            self.SetMinSize(size)

        if max_width or max_height:
            size = self.GetMaxSize()
            if max_width:
                size.x = max_width
            if max_height:
                size.y = max_height
            self.SetMaxSize(size)

    def set_context_menu(self, contextmenu):
        """设置右键菜单"""
        self.Bind(wx.EVT_CONTEXT_MENU, self.on_pop_menu)
        self.Bind(wx.EVT_MENU, self.on_context_menu)
        self.contextmenu = contextmenu

    def bind_event(self, event_type, func, reset=True, pass_event=False, pass_view=True):
        """添加事件监听器"""
        wxbind = False
        if func is not None:
            if event_type in self.event_table:
                event_list = self.event_table[event_type]
                if reset:
                    event_list.clear()
            else:
                self.event_table[event_type] = event_list = []
                wxbind = True

            if not isinstance(func, EventFunctor):
                func = EventFunctor(func, pass_event, pass_view)
            event_list.append(func)

        if wxbind:
            self.Bind(event_type, self.handle_event)

    def bind_event_e(self, event_type, func, reset=True):
        self.bind_event(event_type, func, reset, pass_event=True, pass_view=False)

    def has_event(self, event):
        """是否已注册该类事件"""
        return event.GetEventType() in self.event_table

    def has_event_type(self, event_type):
        """是否已注册该类事件"""
        return event_type in self.event_table

    def handle_event(self, event):
        """处理事件"""
        event_list = self.event_table.get(event.GetEventType(), None)
        res = None
        if event_list is not None:
            for handler in event_list:
                res = handler(self, event)
                if res is not True:
                    if res is False:
                        return False
                    event.Skip()
        return True

    def post_event(self, event_type):
        """手动添加事件"""
        self.AddPendingEvent(wx.CommandEvent(event_type, self.GetId()))

    set_on_keydown = event_binder(wx.EVT_KEY_DOWN, pass_event=True)
    set_on_left_down = event_binder(wx.EVT_LEFT_DOWN, pass_event=True)
    set_on_left_up = event_binder(wx.EVT_LEFT_UP, pass_event=True)
    set_on_right_down = event_binder(wx.EVT_RIGHT_DOWN, pass_event=True)
    set_on_right_up = event_binder(wx.EVT_RIGHT_UP, pass_event=True)

    def on_pop_menu(self, event):
        if self.contextmenu:
            self.PopupMenu(self.contextmenu.wxmenu)

    def on_context_menu(self, event):
        if self.contextmenu:
            self.contextmenu.onselect(self, event.GetId())

    def set_on_file_drop(self, fn):
        self.SetDropTarget(FileDropListener(fn))

    def set_on_text_drop(self, fn):
        self.SetDropTarget(TextDropListener(fn))

    def start_text_drop(fn):
        pass

    def set_on_destroy(fn):
        bind_event(wx.EVT_DESTROY, fn)

    class Here:
        """立即渲染"""
        def __enter__(self):
            View._here = True

        def __exit__(self, exc_type, exc_val, exc_tb):
            View._here = False

    HERE = Here()


class Layout(View):
    """容器元素"""
    def __init__(self, *args, keep_styles=False, styles=None, **kwargs):
        View.__init__(self, *args, **kwargs)
        self.styles = styles
        self.children = []
        self.pendding_children = []
        self.keep_styles = keep_styles

        # 合并父元素持有的样式表
        self.tmp_styles_list = tmp_styles_list = []
        parent = kwargs.get('parent', None) or self.active_layout()
        # 父元素的临时列表还没释放，本次只要检查自己的
        if parent and parent.tmp_styles_list is not None:
            tmp_styles_list.extend(parent.tmp_styles_list)
        else:
            i = len(self.LAYOUTS) - 1
            # 加上父控件的样式列表
            while i is not -1:
                styles = self.LAYOUTS[i].styles
                if styles is not None:
                    if isinstance(styles, list):
                        tmp_styles_list.extend(styles)
                    else:
                        tmp_styles_list.append(styles)
                i -= 1

        styles = self.styles
        if styles is not None:
            if isinstance(styles, list):
                tmp_styles_list.extend(styles)
            else:
                tmp_styles_list.append(styles)

    def __del__(self):
        self.children.clear()

    def __enter__(self):
        self.LAYOUTS.append(self)
        if View._here:
            self.Freeze()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        __class__.LAYOUTS.pop()
        if View._here:
            self.layout()
            self.Thaw()
        elif self.wxwindow is None and not __class__.LAYOUTS:
            # 根节点，开始渲染
            self.render_as_root(None)
        # 释放临时样式表
        if not self.keep_styles:
            self.tmp_styles_list = None

    def append(self, child):
        self.children.append(child)
        if not View._here:
            self.pendding_children.append(child)

    def render_as_root(self, parent=None):
        """作为根节点渲染，通常是另外添加的元素"""
        self.compute_style()
        self.render(parent)
        self.Freeze()
        self.apply_style()
        self.onready()
        self.Thaw()
        del self.wxparams
        del self.computed_style

    def onready(self):
        if not View._here:
            for child in self.pendding_children:
                child._render(self)
            self.pendding_children.clear()
        self.layout()
        super().onready()

    def layout_child(self, child, style):
        """布局子元素"""
        pass

    def layout(self):
        """可选布局"""
        pass

    def relayout(self):
        """子元素改变后重新布局"""
        self.layout()

    def get_styles(self):
        return self.tmp_styles_list

    def set_styles(self, styles):
        """设置样式表"""
        self.styles = styles
        if styles is not None:
            for child in self.children:
                child.try_styles(styles)
        self.relayout()

    def remove_child(self, child):
        """移除子元素"""
        self.RemoveChild(child.wx.Window)
        self.children.remove(child)

    def clear_children(self):
        """清空子元素"""
        for child in self.children:
            self.RemoveChild(child)
        self.children.clear()

    def find_focus(self):
        """当前获取焦点的元素"""
        child = self.FindFocus()
        if child is not None:
            return child.GetHost()

    @staticmethod
    def parsecolor(color):
        def shl(n):
            return (n << 4) | n
        if color.startswith('#'):
            color = color[1:]
        value = int(color, 16)
        if len(color) == 3:
            value = (shl(value & 0xF00) << 8) | (shl(value & 0xF0) << 4) | shl(value & 0xF)
        return value


class Control(View):
    __slots__ = ()


class EventFunctor:
    def __init__(self, fn, pass_event=False, pass_view=True):
        self.fn = fn
        self.pass_event = pass_event
        self.pass_view = pass_view

    def __call__(self, view, event):
        args = []
        if self.pass_view:
            args.append(view)
        if self.pass_event:
            args.append(event)
        return self.fn(*args)
