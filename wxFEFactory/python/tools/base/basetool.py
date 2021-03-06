import traceback
import __main__
from lib import wxconst, lazy
from lib.scene import BaseScene
from styles import styles, dialog_style
from fefactory_api import ui, alert


class BaseTool(BaseScene):
    # 窗口嵌套
    nested = False

    # def __del__(self):
    #     print(self.module_name, '析构')

    def attach(self, frame):
        try:
            if self.nested:
                with frame.book:
                    win = self.render()
                    if win:
                        ui.AuiItem(win, caption=self.unique_title)
            else:
                with frame.win:
                    win = self.render()
            if win:
                win.setOnClose({'callback': self.onClose, 'arg_event': True})
                self.win = win
        except Exception:
            traceback.print_exc()

    def render(self):
        """ 渲染视图，供attach调用
        :return: 返回根元素
        """
        pass

    def render_float_win(self):
        """浮动的窗口"""
        return ui.HotkeyWindow(self.title, styles=styles, style=dialog_style, menubar=self.render_menu(),
            wxstyle=wxconst.FRAME_BASE | wxconst.FRAME_FLOAT_ON_PARENT)

    def render_menu(self):
        """ 渲染基本菜单
        :return: menubar
        """
        with ui.MenuBar() as menubar:
            with ui.Menu("窗口"):
                ui.MenuItem("关闭\tCtrl+W", onselect=self.closeWindow)
                ui.MenuItem("重载\tCtrl+R", onselect=self.reload)
                ui.MenuItem("切换置顶", onselect=self.swith_keeptop)

        return menubar

    def add_close_callback(self, callback):
        close_callbacks = getattr(self, '_close_callbacks', None)
        if not close_callbacks:
            close_callbacks = self._close_callbacks = []
        close_callbacks.append(callback)

    @lazy.classlazy
    def title(cls):
        """获取原始标题，显示在标签页标题和菜单栏"""
        module = cls.__module__
        return __import__(module[:module.rfind('.')], fromlist='__init__').name

    @lazy.classlazy
    def module_name(cls):
        """模块名称，即模块文件夹名"""
        module = cls.__module__
        return module[module.find('.') + 1: module.rfind('.')]

    def reload(self, _=None):
        name = self.module_name

        def close_callback():
            def callback():
                __main__.frame.open_tool_by_name(name)
            __main__.frame.restart(callback=callback)

        if self.nested:
            # 现在改成了主窗口的onClose里会先关闭所有未关闭子窗口
            close_callback()
        else:
            self.closeWindow()
            close_callback()

    def closeWindow(self, _=None):
        if self.nested:
            try:
                # closePage会自动调用onClose
                self.win.parent.closePage()
            except Exception:
                traceback.print_exc()
                self.win.close()
        else:
            # win应该设置close回调为self.onClose
            self.win.close()

    def onClose(self, view=None, event=None):
        """
        有三种情况进入这里
        1. nested且有关闭按钮，点关闭按钮触发
        2. 手动调用self.closeWindow(菜单)，由parent.closePage内调用window的onClose触发
        3. parent(AuiNotebook)点Tab的关闭按钮触发(类似情况2)
        """
        if self.nested:
            if event and event.id is not 0:
                # 第一种情况阻止关闭
                alert('请通过菜单过Tab上的关闭按钮关闭')
                return False
        elif self.win.parent:
            self.win.parent.children.remove(self.win)

        close_callbacks = getattr(self, '_close_callbacks', None)
        if close_callbacks:
            for callback in close_callbacks:
                callback(self)
            close_callbacks.clear()

        super().onClose()

        callback = getattr(self, 'close_callback', None)
        if callback:
            callback()

        self.__dict__.clear()
        return True

    def swith_keeptop(self, _):
        self.win.keeptop = not self.win.keeptop


class NestedTool(BaseTool):
    nested = True
    key_hook = True

    def render_win(self):
        menubar = self.render_menu()
        Window = ui.KeyHookWindow if self.key_hook else ui.HotkeyWindow
        self.win = Window(self.title, styles=styles, menubar=menubar, wxstyle=0x80804)
        self.win.position = (70, 4)
        return self.win
