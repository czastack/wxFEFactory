from . import wx


class MenuHolder:
    """菜单管理"""
    MENUS = []

    def __init__(self, handlers=None):
        self.children = []
        self.handlers = handlers

    def __del__(self):
        self.handlers.clear()

    @classmethod
    def active_menu(cls):
        return cls.MENUS[-1] if cls.MENUS else None

    def __enter__(self):
        self.MENUS.append(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.MENUS.pop()

    def getmenu(self, menuid):
        return self.handlers.get(menuid, None)

    def setmenu(self, menuid, menu):
        self.handlers[menuid] = menu

    def onselect(self, menuid, owner):
        menu = self.getmenu(menuid)
        if menu:
            menu.onselect(owner)


class Menu(MenuHolder):
    """基本菜单"""
    def __init__(self, handlers=None, text=None, help=None):
        MenuHolder.__init__(handlers)
        self.wxmenu = wx.Menu()
        if text is not None and help is not None:
            parent = self.active_menu()
            if parent:
                parent.AppendSubMenu(menu, text, help)


class ContextMenu(Menu):
    """右键菜单"""
    def __init__(self, onselect=None):
        Menu.__init__(self, {})
        self.m_onselect = onselect

    def onselect_view(self, view, id):
        if Menu.onselect(self, id, view):
            return True
        elif self.m_onselect is not None:
            self.m_onselect(view, self.getmenu(id))
            return True


class MenuBar(MenuHolder):
    """菜单栏"""
    def __init__(self, onselect=None):
        MenuHolder.__init__(self, {})
        self.m_onselect = onselect
        self.wxwindow = wx.MenuBar(0)
        self.wxwindow.SetClientData(self)

    def remove(self, menu):
        pass

    def onselect_view(self, view, id):
        if Menu.onselect(self, id, view):
            return True
        elif self.m_onselect is not None:
            self.m_onselect(view, self.getmenu(id))
            return True


class MenuItem:
    """菜单项"""
    def __init__(self, text=None, help=None, kind=None, id=-1, separator=False, onselect=None):
        parent = MenuHolder.active_menu()
        if parent:
            if separator:
                parent.AppendSeparator()
            self.ptr = parent.Append(id, text, help, kind)
