from .tool import NestedTool
from lib.config import Config
from lib.hack.form import Widget, BaseGroup
import traceback
import fefactory_api
ui = fefactory_api.ui


class BaseHackTool(NestedTool):
    def __init__(self):
        super().__init__()
        self.config = Config(self.getName() + '_config.json')

    def attach(self, frame):
        super().attach(frame)
        return self.check_attach()

    def render(self):
        with self.render_win() as win:
            with ui.Vertical():
                with ui.Horizontal(className="expand container"):
                    ui.Button("检测", className="vcenter", onclick=self.check_attach)
                    self.attach_status_view = ui.Text("", className="vcenter grow left_padding")
                    ui.CheckBox("保持最前", className="vcenter", onchange=self.swith_keeptop)
                with ui.Notebook(className="fill") as book:
                    book.setOnPageChange(self.onNotePageChange)
                    self.begin_group()
                    try:
                        self.render_main()
                    except:
                        win.close()
                        raise
                    self.end_group()

        return win

    def check_attach(self, _=None):
        """检查运行目标程序状态"""
        if self.handler.active:
            self.ondetach()

        if self.handler.attachByWindowName(self.CLASS_NAME, self.WINDOW_NAME):
            self.attach_status_view.label = self.WINDOW_NAME + ' 正在运行'

            if not self.win.hotkeys:
                hotkeys = self.get_hotkeys()
                if hotkeys:
                    self.win.RegisterHotKeys(hotkeys)
            self.onattach()
            return True
        else:
            self.attach_status_view.label = '没有检测到 ' + self.WINDOW_NAME
            return False

    def get_hotkeys(self):
        """重写这个函数，返回要注册的热键列表"""
        return ()

    def onClose(self, *args):
        if self.handler.active:
            self.ondetach()
        self.config.write()
        return super().onClose(*args)

    def lazy_group(self, group, fn):
        groups = getattr(self, 'lazy_groups', None)
        if groups is None:
            self.lazy_groups = groups = {}

        groups[group.root] = group, fn

    def onNotePageChange(self, book):
        groups = getattr(self, 'lazy_groups', None)
        if groups:
            root = book.getPage()
            item = groups.get(root, None)
            if item:
                group, fn = item
                with group:
                    fn()
                group.after_lazy()
                del groups[root]

    def begin_group(self):
        Widget.GROUPS.append(self)
        self.groups = []

    def appendChild(self, child):
        if isinstance(child, BaseGroup):
            self.groups.append(child)
        else:
            raise ValueError("Group层级校验失败")

    def end_group(self):
        while Widget.GROUPS.pop() is not self:
            pass

    def discard_config(self, _=None):
        self.config.cancel_change()

    def swith_keeptop(self, cb):
        if self.nested:
            from __main__ import win
        else:
            win = self.win
        win.keeptop = cb.checked

    def read_vector(self, addr):
        """ 在addr读三个float类型
        :return: (x, y, z)
        """
        r = self.handler.readFloat
        return (r(addr), r(addr + 4), r(addr + 8))

    def onattach(self):
        pass

    def ondetach(self):
        pass

    def custom_hotkey(self, _=None):
        """用于自定义的临时热键功能"""
        fn = getattr(self, 'cfn', None)
        if fn:
            fn()

    def toggle_setting(self, name, default=False):
        """切换设置"""
        toggle = not getattr(self, name, default)
        setattr(self, name, toggle)
        return toggle

    def get_cache(self, name, key, fn):
        """ 获取缓存的内容
        :param fn: 缓存不存在时通过fn(key)获取
        """
        cache_name = '_cache_' + name
        cache = getattr(self, cache_name, None)
        if cache is None:
            cache = {}
            setattr(self, cache_name, cache)

        value = cache.get(key, None)
        if value is None:
            value = cache[key] = fn(key)
        return value

    def set_cfn(self, btn, m=None):
        self.cfn = btn.click

    def set_buttons_contextmenu(self):
        parent = ui.View.get_active_layout()
        with ui.ContextMenu(onselect=self.set_cfn) as contextmenu:
            ui.MenuItem("设为alt+c快捷键(&C)")
        for btn in parent.children:
            btn.setContextMenu(contextmenu)

    def render_functions(self, names):
        with ui.GridLayout(cols=4, vgap=10, className="expand"):
            for name in names:
                func = getattr(self.weak, name)
                ui.Button(func.__doc__, onclick=func)