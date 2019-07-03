from . import wx


class View:
    """视图元素"""
    LAYOUTS = []
    wxtype = None

    def __init__(self, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, wxstyle=0,
                 class_=None, style=None, extra=None):
        # style: None | [{}] | {}
        self.style = style
        self.wxparams = {
            'id': id,
            'pos': pos,
            'size': size,
        }
        if wxstyle is not 0:
            self.wxparams['style'] = wxstyle
        if class_ is not None:
            class_ = class_.split()
        self.class_ = class_
        self.extra = extra
        self.event_table = {}
        self.wxwindow = None
        self.contextmenu = None

        parent = self.active_layout()
        if parent is not None:
            parent.append(self)
            styles = parent.get_styles()
            if styles is not None:
                for style in styles:
                    self.try_styles(style)

    def __del__(self):
        print('del', self)

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

    def bind_wx(self, wxwindow):
        self.wxwindow = wxwindow
        wxwindow.SetHost(self)

    def _render(self, parent):
        self.render(parent)
        self.onready()
        del self.wxparams

    def render(self, parent):
        """渲染"""
        self.bind_wx(self.wxtype(parent and parent.wxwindow, **self.wxparams))

    def onready(self):
        """渲染后的操作"""
        pass

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

    def apply_style(self):
        """应用样式"""
        # computed_style
        style = {}
        for item in self.iter_style():
            style.update(item)

        if not style:
            return style

        backgroud = style.get('backgroud', None)
        if backgroud is not None:
            if isinstance(backgroud, str):
                # parseColor
                pass
            else:
                self.SetBackgroundColour(backgroud)

        color = style.get('color', None)
        if color is not None:
            if isinstance(color, str):
                # parseColor
                pass
            else:
                self.SetForegroundColour(color)

        fontsize = style.get('font-size', None)
        if fontsize is not None:
            # TODO
            font = self.GetFont()
            font.SetPointSize(fontsize)
            self.SetFont(font)

        fontDict = style.get('font', None)
        if fontDict is not None:
            # TODO
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
        width = style.get('width', None)
        height = style.get('height', None)
        if width or height:
            size = self.GetSize()
            if width:
                size.x = width
            if height:
                size.y = height
            self.SetSize(size)

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

        self.apply_style_own(style)
        return style

    def apply_style_own(self, style):
        """应用独有样式"""
        pass

    def set_context_menu(self, contextmenu):
        """设置右键菜单"""
        # m_elem->Bind(wx.EVT_CONTEXT_MENU, &View::onPopMenu, this);
        # m_elem->Bind(wx.EVT_MENU, &View::onContextMenu, this);
        self.contextmenu = contextmenu

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

    def has_wxstyle(self, flag):
        """是否有wxWidgets样式flag"""
        return self.GetWindowStyle() & flag != 0

    def toggle_wxstyle(self, flag, toggle=None):
        """切换wxWidgets样式flag
        :param toggle: None 切换, True 设置, False 取消
        """
        style = self.GetWindowStyle()
        if toggle is None:
            toggle = style & flag == 0
        if toggle:
            style |= flag
        else:
            style &= ~flag
        self.SetWindowStyle(style)

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
        self.AddPendingEvent(wx.Event(event_type, self.GetId()))

    def __getattr__(self, name):
        return getattr(self.wxwindow, name)

    def set_on_keydown(fn):
        self.bind_event(wx.EVT_KEY_DOWN, fn, false, true)

    # void setOnFileDrop(pycref ondrop);

    # void setOnTextDrop(pycref ondrop);

    # void startTextDrag(wxcstr text, pycref callback);

    def set_on_destroy(fn):
        bind_event(wx.EVT_DESTROY, fn)


class Layout(View):
    """容器元素"""
    def __init__(self, *args, styles=None, **kwargs):
        View.__init__(self, *args, **kwargs)
        self.styles = styles
        self.children = []
        self.pendding_children = []
        self.tmp_styles_list = None

    def __del__(self):
        self.children.clear()

    def __enter__(self):
        if self.tmp_styles_list is None:
            self.tmp_styles_list = tmp_styles_list = []

        parent = self.active_layout()
        if parent is None:
            # 判断是否是AuiManager
            if type(parent).__name__ == 'AuiManager':
                parent = parent.GetHost()

        only_self = False
        # 父元素的临时列表还没释放，本次只要检查自己的
        if parent and parent.tmp_styles_list is not None:
            tmp_styles_list.extend(parent.tmp_styles_list)
            only_self = True

        self.LAYOUTS.append(self)
        i = len(self.LAYOUTS) - 1

        # 加上父控件的样式列表
        while i is not -1:
            styles = self.LAYOUTS[i].styles
            if styles is not None:
                if isinstance(styles, list):
                    tmp_styles_list.extend(styles)
                else:
                    tmp_styles_list.append(styles)
            if only_self:
                break
            i -= 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 根节点，开始渲染
        __class__.LAYOUTS.pop()
        if not __class__.LAYOUTS:
            self._render(None)
            self.apply_style()
        # 释放临时样式表
        self.tmp_styles_list = None

    def append(self, child):
        self.children.append(child)
        self.pendding_children.append(child)

    def onready(self):
        self.Freeze()
        for child in self.pendding_children:
            child._render(self)
            style = child.apply_style()
            self.layout_child(child, style)
        self.pendding_children.clear()
        self.layout()
        self.Thaw()

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
            return child.GetClientData()


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
        self.fn(*args)
