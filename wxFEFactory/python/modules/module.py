import os
import json
import types
import __main__
from application import app
from lib import extypes, lazy, wxconst
from lib.scene import BaseScene
from styles import styles
from fefactory_api import ui
from . import modules

DUMP_INDENT = app.getconfig('json_indent', 4)


class BaseModule(BaseScene):
    menu = None

    # def __del__(self):
    #     print(self.module_name, '析构')

    def attach(self, frame):
        """模块加载完毕后调用，用于添加视图到主窗口"""
        with frame.book:
            self.view = self.render()
        with frame.win.menubar:
            self.menu = self.get_menu()

    def onclose(self, _=None):
        """标签页关闭回调，返回False会取消关闭"""
        if self.menu:
            __main__.win.menubar.remove(self.menu)

        if getattr(__main__, 'module', None) == self:
            del __main__.module

        super().onclose()

        return True

    def render(self):
        """
        渲染视图，供attach调用
        :return: 返回根元素
        """
        pass

    def get_menu(self):
        """
        渲染菜单，供attach调用
        :return: 返回Menu对象
        """
        pass

    @lazy.classlazy
    def title(cls):
        """获取原始标题，显示在标签页标题和菜单栏"""
        name = cls.module_name
        for item in modules:
            if item[1] == name:
                return item[0]
        return name

    @lazy.classlazy
    def module_name(cls):
        """模块名称，即模块文件夹名"""
        return cls.__module__.split('.')[1]

    @classmethod
    def get_dir(cls):
        """根据当前项目获取模块数据存放目录，即模块工作目录"""
        return os.path.join(app.project.path, cls.module_name)

    @classmethod
    def load_json(cls, name, defval={}):
        """从模块工作目录读取一个json文件"""
        try:
            with open(os.path.join(cls.get_dir(), name + '.json'), encoding="utf-8") as file:
                ret = json.load(file)
        except Exception:  # FileNotFoundError, json.decoder.JSONDecodeError
            ret = defval
        return ret

    @classmethod
    def dump_json(cls, name, data, indent=DUMP_INDENT):
        """在模块工作目录写入一个json文件"""
        dir_ = cls.get_dir()
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
    左侧显示一个ListBox，右侧显示主视图（重载 render_main 方法 ）
    """
    def render(self):
        this = self.weak
        with ui.SplitterWindow(False, 220, styles=styles, extra=dict(
                caption=self.unique_title, onclose=self.onclose)) as panel:
            with ui.Vertical():
                self.listbox = ui.RearrangeList(class_="fill", onselect=this.onListSelect)
                with ui.Horizontal(class_="expand"):
                    ui.Text("Ctrl+↑↓ 上移/下移当前项")
                with ui.Horizontal(class_="expand"):
                    ui.Button(label="添加", class_="button", onclick=this.onAdd)
                    ui.Button(label="删除", class_="button", onclick=this.onDel)
            with ui.Vertical():
                self.render_main()

        self.listbox.setOnKeyDown(this.onListBoxKey)

        contextmenu = self.render_contextmenu()
        if contextmenu:
            self.listbox.setContextMenu(contextmenu)
        return panel

    def render_main(self):
        """渲染右侧主视图"""
        pass

    def render_contextmenu(self):
        """ListBox右键菜单"""
        with ui.ContextMenu() as contextmenu:
            ui.MenuItem("重命名", onselect=self.weak.onRename)

        return contextmenu

    def get_menu(self):
        with ui.Menu(self.unique_title) as menu:
            ui.MenuItem("清空", onselect=self.weak.onClear)
        return menu

    def onClear(self, menu):
        """清空列表"""
        if self.confirm('提示', '确认清空所有列表项？', wxconst.NO) is wxconst.YES:
            self.listbox.clear()
            return True

    def onRename(self, view, menu):
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
            if self.confirm('提示', '确认删除该项？', wxconst.NO) is wxconst.YES:
                text = self.listbox[pos]
                self.listbox.pop(pos)
                return pos, text
        return -1, None

    def move_up(self):
        """上移一项"""
        self.listbox.MoveCurrentUp()

    def move_down(self):
        """下移一项"""
        self.listbox.MoveCurrentDown()

    def onListBoxKey(self, lb, event):
        """按键监听"""
        mod = event.GetModifiers()
        if mod == WXK.MOD_CONTROL:
            code = event.GetKeyCode()
            if code == WXK.UP:
                self.move_up()
            elif code == WXK.DOWN:
                self.move_down()
        event.Skip()

    def doAdd(self, text):
        """添加列表项"""
        if isinstance(text, types.GeneratorType):
            text = tuple(text)
        elif not extypes.is_list_tuple(text):
            text = (text,)
        self.listbox.appendItems(text)
