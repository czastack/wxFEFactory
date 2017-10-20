from lib.basescene import BaseScene
from lib.lazy import lazyclassmethod
from . import tools
import fefactory_api
ui = fefactory_api.ui
import __main__


class BaseTool(BaseScene):
    # 窗口嵌套
    nested = False

    def attach(self, frame):
        if self.nested:
            with frame.book:
                win = self.render()
                if win:
                    ui.AuiItem(win, caption=self.getTitle())
        else:
            win = self.render()
        
        if win:
            win.setOnClose(self.onClose)
            self.win = win

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

    @lazyclassmethod
    def doGetTitle(class_):
        """获取原始标题，显示在标签页标题和菜单栏"""
        name = class_.getName()
        for item in tools:
            if item[1] == name:
                return item[0]
        return name

    @lazyclassmethod
    def getName(class_):
        """模块名称，即模块文件夹名"""
        return class_.__module__.split('.')[1]

    def reload(self, _=None):
        from mainframe import frame
        name = self.getName()

        def close_callback():
            def callback():
                from mainframe import frame
                frame.openToolByName(name)
            frame.restart(callback=callback)

        if self.nested:
            # 因为nested模式下，onClose在book的closePage后调用onClose（异步）
            # 故使用回调的方式
            self.close_callback = close_callback
            self.closeWindow()
        else:
            self.closeWindow()
            close_callback()

    def closeWindow(self, _=None):
        if self.nested:
            self.win.parent.closePage()
            # closePage会自动调用onClose
        else:
            # win应该设置close回调为self.onClose
            self.win.close()

    def onClose(self, _=None):
        super().onClose()
        
        if getattr(__main__, 'tool', None) == self:
            del __main__.tool

        callback = getattr(self, 'close_callback', None)
        if callback:
            callback()
        
        return True