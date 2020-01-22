from . import wx


class MenuHolder:
    """菜单管理"""
    MENUS = []

    def __init__(self, handlers=None):
        self.children = []
        self.handlers = handlers

    def __del__(self):
        if self.handlers:
            self.handlers.clear()
        self.children.clear()

    @classmethod
    def active_menu(cls):
        return cls.MENUS[-1] if cls.MENUS else None

    def __enter__(self):
        self.MENUS.append(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.MENUS.pop()

    def getmenu(self, itemid):
        return self.handlers.get(itemid, None)

    def setmenu(self, itemid, menu):
        self.handlers[itemid] = menu

    def onselect(self, owner, itemid):
        menu = self.getmenu(itemid)
        if menu:
            # Call MenuItem.onselect
            return menu.onselect(owner)
        return False


class Menu(MenuHolder):
    """基本菜单"""
    def __init__(self, text=None, help="", handlers=None):
        super().__init__(handlers)
        self.wxmenu = wx.Menu()
        if text is not None:
            parent = self.active_menu()
            if parent:
                self.wxmenuitem = parent.AppendSubMenu(self.wxmenu, text, help)
                parent.children.append(self)
                self.handlers = parent.handlers

    def __getattr__(self, name):
        return getattr(self.wxmenu, name)


class ContextMenu(Menu):
    """右键菜单"""
    def __init__(self, onselect=None):
        super().__init__(handlers={})
        self._onselect = onselect

    def onselect(self, view, id):
        if Menu.onselect(self, view, id):
            return True
        elif self._onselect is not None:
            self._onselect(view, self.getmenu(id))
            return True


class MenuBar(MenuHolder):
    """菜单栏"""
    def __init__(self, onselect=None):
        super().__init__(handlers={})
        self._onselect = onselect
        self.wxwindow = wx.MenuBar(0)
        self.wxwindow.SetHost(self)

    def AppendSubMenu(self, menu, text, help=None):
        self.Append(menu, text)

    def remove(self, menu):
        for i in range(self.GetMenuCount()):
            if self.GetMenu(i) == menu.wxmemu:
                self.Remove(i)
                break

    def onselect(self, id):
        if Menu.onselect(self, None, id):
            return True
        elif self._onselect is not None:
            self._onselect(self, self.getmenu(id))
            return True

    def __getattr__(self, name):
        return getattr(self.wxwindow, name)


class MenuItem:
    """菜单项"""
    def __init__(self, text="", help="", kind=wx.ITEM_NORMAL, id=-1, separator=False, onselect=None):
        parent = MenuHolder.active_menu()
        if parent:
            if separator:
                parent.AppendSeparator()
            self.wxmenuitem = parent.Append(id, text, help, kind)
            parent.setmenu(self.GetId(), self)
        self._onselect = onselect

    def onselect(self, owner):
        if self._onselect:
            if owner:
                # contextmenu
                return self._onselect(owner, self)
            return self._onselect(self)
        return False

    @property
    def checked(self):
        return self.IsChecked()

    @checked.setter
    def checked(self, checked):
        self.Check(checked)

    def __getattr__(self, name):
        return getattr(self.wxmenuitem, name)
