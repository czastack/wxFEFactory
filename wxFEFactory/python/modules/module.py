from application import app
from lib.lazy import lazyclassmethod
from lib.basescene import BaseScene
from commonstyle import styles
from . import modules
import os
import json
import types
import __main__
import fefactory_api
ui = fefactory_api.ui

DUMP_INDENT = app.getConfig('json_indent', 4)

class BaseModule(BaseScene):
    menu = None

    def attach(self, frame):
        """模块加载完毕后调用，用于添加视图到主窗口"""
        with frame.book:
            self.view = self.render()
        with frame.win.menubar:
            self.menu = self.getMenu()

    def onClose(self):
        """标签页关闭回调，返回False会取消关闭"""
        super().onClose()

        if self.menu:
            __main__.win.menubar.remove(self.menu)

        return True

    def render(self):
        """
        渲染视图，供attach调用
        :return: 返回根元素
        """
        pass

    def getMenu(self):
        """
        渲染菜单，供attach调用
        :return: 返回Menu对象
        """
        pass

    @lazyclassmethod
    def doGetTitle(class_):
        """获取原始标题，显示在标签页标题和菜单栏"""
        name = class_.getName()
        for item in modules:
            if item[1] == name:
                return item[0]
        return name

    @lazyclassmethod
    def getName(class_):
        """模块名称，即模块文件夹名"""
        return class_.__module__.split('.')[1]

    @classmethod
    def getDir(class_):
        """根据当前项目获取模块数据存放目录，即模块工作目录"""
        return os.path.join(app.project.path, class_.getName())

    @classmethod
    def loadJson(class_, name, defval={}):
        """从模块工作目录读取一个json文件"""
        try:
            with open(os.path.join(class_.getDir(), name + '.json'), encoding="utf-8") as file:
                ret = json.load(file)
        except Exception: #FileNotFoundError, json.decoder.JSONDecodeError
            ret = defval
        return ret

    @classmethod
    def dumpJson(class_, name, data, indent=DUMP_INDENT):
        """在模块工作目录写入一个json文件"""
        dir_ = class_.getDir()
        if not os.path.exists(dir_):
            os.mkdir(dir_)
        with open(os.path.join(dir_, name + '.json'), 'w', encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=indent)
        print("保存成功: " + file.name)

    def readFrom(self, reader):
        """从rom等数据源读取数据"""
        pass


class BaseListBoxModuel(BaseModule):
    """
    列表模块基类
    左侧显示一个ListBox，右侧显示主视图（重载 render_right 方法 ）
    """
    def render(self):
        with ui.SplitterWindow(False, 220, styles=styles) as panel:
            with ui.Vertical():
                self.listbox = ui.RearrangeList(className="fill", onselect=self.onListSelect)
                with ui.Horizontal(className="expand"):
                    ui.Text("Ctrl+↑↓ 上移/下移当前项")
                with ui.Horizontal(className="expand"):
                    ui.Button(label="添加", className="button", onclick=self.onAdd)
                    ui.Button(label="删除", className="button", onclick=self.onDel)
            with ui.Vertical():
                self.render_right()
        ui.AuiItem(panel, caption=self.getTitle(), onclose=self.onClose)

        with ui.ContextMenu() as listmenu:
            ui.MenuItem("重命名", onselect=self.onRename)

        self.listbox.setOnKeyDown(self.onListBoxKey)

        contextmenu = self.render_contextmenu()
        if contextmenu:
            self.listbox.setContextMenu(contextmenu)
        return panel

    def render_right(self):
        """渲染右侧主视图"""
        pass

    def render_contextmenu(self):
        """ListBox右键菜单"""
        with ui.ContextMenu() as contextmenu:
            ui.MenuItem("重命名", onselect=self.onRename)

        return contextmenu

    def getMenu(self):
        with ui.Menu(self.getTitle()) as menu:
            ui.MenuItem("清空", onselect=self.onClear)
        return menu

    def onClear(self, m):
        """清空列表"""
        if self.confirm('提示', '确认清空所有列表项？', self.NO) is self.YES:
            self.listbox.clear()
            return True

    def onRename(self, m):
        """重命名列表项"""
        name = self.listbox.text
        if name:
            newname = input("新名称", name)
            self.listbox.setText(newname)
            return name, newname

    def onDel(self, btn):
        """删除一项"""
        pos = self.listbox.index
        if pos is not -1:
            if self.confirm('提示', '确认删除该项？', self.NO) is self.YES:
                text = self.listbox[pos]
                self.listbox.pop(pos)
                return pos, text
        return -1, None

    def moveUp(self):
        """上移一项"""
        self.listbox.moveUp()

    def moveDown(self):
        """下移一项"""
        self.listbox.moveDown()

    def onListBoxKey(self, lb, event):
        """按键监听"""
        mod = event.GetModifiers()
        if mod == event.CTRL:
            code = event.GetKeyCode()
            if code == event.UP:
                self.moveUp()
            elif code == event.DOWN:
                self.moveDown()
        event.Skip()

    def doAdd(self, text):
        """添加列表项"""
        if isinstance(text, types.GeneratorType):
            text = tuple(text)
        elif not isinstance(text, (list, tuple)):
            text = (text,)
        self.listbox.appendItems(text)