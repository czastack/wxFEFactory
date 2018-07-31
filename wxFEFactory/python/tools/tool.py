from lib.scene import BaseScene
from lib.lazy import ClassLazy
from styles import styles
from fefactory_api import ui, alert
import traceback
import __main__


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

    @ClassLazy
    def title(cls):
        """获取原始标题，显示在标签页标题和菜单栏"""
        module = cls.__module__
        return __import__(module[:module.rfind('.')], fromlist='__init__').name

    @ClassLazy
    def module_name(cls):
        """模块名称，即模块文件夹名"""
        module = cls.__module__
        return module[module.find('.') + 1: module.rfind('.')]

    def reload(self, _=None):
        from mainframe import frame
        name = self.module_name

        def close_callback():
            def callback():
                from mainframe import frame
                frame.open_tool_by_name(name)
            frame.restart(callback=callback)

        if self.nested:
            # 现在改成了mainframe的onClose里会先关闭所有未关闭子窗口
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
        if self.nested and event and event.id is not 0:
            # 第一种情况阻止关闭
            alert('请通过菜单过Tab上的关闭按钮关闭')
            return False

        close_callbacks = getattr(self, '_close_callbacks', None)
        if close_callbacks:
            for callback in close_callbacks:
                callback()
            close_callbacks.clear()

        super().onClose()

        if getattr(__main__, 'tool', None) == self:
            del __main__.tool

        callback = getattr(self, 'close_callback', None)
        if callback:
            callback()

        self.__dict__.clear()
        return True

    def swith_keeptop(self, _):
        self.win.keeptop = not self.win.keeptop


class NestedTool(BaseTool):
    nested = True

    def render_win(self):
        menubar = self.render_menu()
        self.win = ui.HotkeyWindow(self.title, styles=styles, menubar=menubar, wxstyle=0x80804)
        self.win.position = (70, 4)
        return self.win
