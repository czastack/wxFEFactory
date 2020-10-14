import abc
import traceback
import __main__
from lib import lazy, ui
from lib.scene import BaseScene
from styles import styles, dialog_style


class BaseTool(BaseScene, metaclass=abc.ABCMeta):
    # 窗口嵌套
    nested = False

    # def __del__(self):
    #     print(self.module_name, '析构')

    def attach(self, frame):
        try:
            if self.nested:
                with frame.book:
                    win = self.render()
            else:
                with frame.win:
                    win = self.render()
            if win:
                win.set_onclose(ui.EventFunctor(self.onclose, pass_event=True))
                self.win = win
        except Exception:
            traceback.print_exc()

    @abc.abstractmethod
    def render(self):
        """ 渲染视图，供attach调用
        :return: 返回根元素
        """
        pass

    def render_float_win(self):
        """浮动的窗口"""
        return ui.HotkeyFrame(title=self.title, styles=styles, style=dialog_style, menubar=self.render_menu(),
            wxstyle=ui.wx.FRAME_BASE | ui.wx.FRAME_FLOAT_ON_PARENT)

    def render_menu(self):
        """ 渲染基本菜单
        :return: menubar
        """
        with ui.MenuBar() as menubar:
            with ui.Menu("窗口"):
                ui.MenuItem("关闭\tCtrl+W", onselect=self.weak.close_window)
                ui.MenuItem("重载\tCtrl+R", onselect=self.weak.reload)
                ui.MenuItem("切换置顶", onselect=self.weak.switch_keeptop, kind=ui.wx.ITEM_CHECK)

        return menubar

    def add_close_callback(self, callback):
        close_callbacks = getattr(self, '_close_callbacks', None)
        if not close_callbacks:
            close_callbacks = self._close_callbacks = []
        close_callbacks.append(callback)

    @lazy.classlazy
    def title(self):
        """获取原始标题，显示在标签页标题和菜单栏"""
        module = self.__module__
        return __import__(module[:module.rfind('.')], fromlist='__init__').name

    @lazy.classlazy
    def module_name(self):
        """模块名称，即模块文件夹名"""
        module = self.__module__
        return module[module.find('.') + 1: module.rfind('.')]

    def reload(self, _=None):

        def close_callback():
            __main__.frame.restart(extra_option={'open_tool': self.module_name})

        if self.nested:
            # 主窗口的onclose里会先关闭所有未关闭子窗口
            close_callback()
        else:
            self.close_window()
            close_callback()

    def close_window(self, _=None):
        if self.nested:
            try:
                # close_page会自动调用onclose
                self.win.parent.close_page()
            except Exception:
                traceback.print_exc()
                self.win.Close()
        else:
            # win应该设置close回调为self.onclose
            self.win.Close()

    def onclose(self, view=None, event=None):
        """
        有三种情况进入这里
        1. nested且有关闭按钮，点关闭按钮触发，可以直接调用parent.close_page
        2. 手动调用self.close_window(菜单)，由parent.close_page内调用window的onclose触发
        3. parent(AuiNotebook)点Tab的关闭按钮触发(类似情况2)
        """
        if self.nested:
            if event and event.GetId() != 0:
                # 情况1
                self.win.parent.close_page()
                return False
        elif self.win.parent:
            self.win.parent.children.remove(self.win)

        close_callbacks = getattr(self, '_close_callbacks', None)
        if close_callbacks:
            for callback in close_callbacks:
                callback(self)
            close_callbacks.clear()

        super().onclose()
        self.win.Destroy()
        self.__dict__.clear()
        return True

    def switch_keeptop(self, view):
        self.win.keeptop = view.checked


class NestedTool(BaseTool):
    nested = True
    key_hook = True
    key_hook_ll = False  # low level

    def render_win(self):
        menubar = self.render_menu()
        Frame = ui.KeyHookFrame if self.key_hook else ui.HotkeyFrame
        self.win = Frame(title=self.title, styles=styles, menubar=menubar, pos=ui.wx.Point(70, 4), wxstyle=0x80804,
                         extra=dict(caption=self.unique_title))
        return self.win
