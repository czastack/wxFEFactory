from lib.basescene import BaseScene
from lib.lazy import lazyclassmethod_indict
from . import tools
import traceback
import fefactory_api
ui = fefactory_api.ui
import __main__


class BaseTool(BaseScene):
    # 窗口嵌套
    nested = False

    # def __del__(self):
    #     print(self.getName(), '析构')

    def attach(self, frame):
        try:
            if self.nested:
                with frame.book:
                    win = self.render()
                    if win:
                        ui.AuiItem(win, caption=self.getTitle())
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

        return menubar

    def add_close_callback(self, callback):
        close_callbacks = getattr(self, '_close_callbacks', None)
        if not close_callbacks:
            close_callbacks = self._close_callbacks = []
        close_callbacks.append(callback)

    @lazyclassmethod_indict
    def doGetTitle(class_):
        """获取原始标题，显示在标签页标题和菜单栏"""
        name = class_.getName()
        for item in tools:
            if item[1] == name:
                return item[0]
        return name

    @lazyclassmethod_indict
    def getName(class_):
        """模块名称，即模块文件夹名"""
        module = class_.__module__
        return module[module.find('.') + 1: module.rfind('.')]

    def reload(self, _=None):
        from mainframe import frame
        name = self.getName()

        def close_callback():
            def callback():
                from mainframe import frame
                frame.openToolByName(name)
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
            except:
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
            fefactory_api.alert('请通过菜单过Tab上的关闭按钮关闭')
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