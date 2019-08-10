import os
import sys
import traceback
import types
import __main__
import pyapi
import fefactory
import tools
from project import Project
# from modules import modules
from lib import ui, extypes
from lib.win32.keys import WXK


"""
:param name: 工具文件夹名
:param label: 工具名称
:param packae: 是否是工具集(有子工具)
:param children: 子工具元组
"""
ToolTreeItem = extypes.DataClass("ToolTreeItem", ("module", "label", "package", "children", "id"))


class MainFrame:
    def __init__(self):
        self.weak = extypes.WeakBinder(self)
        self.opened_tools = []
        self.opened_tools_map = {}
        self.toolbar_items = __main__.app.getconfig('toolbar_items') or []
        self.render()

        start_option = __main__.app.start_option
        if start_option:
            size = start_option.get('size', None)
            if size:
                self.win.SetSize(*size)
            position = start_option.get('position', None)
            if position:
                self.win.Move(*position)
            toolname = start_option.get('open_tool')
            if toolname:
                self.open_tool_by_name(toolname)

        if getattr(__main__.app, 'project', None):
            self.on_open_project(__main__.app.project)

    def render(self):
        weak = self.weak
        with ui.MenuBar() as menubar:
            with ui.Menu("文件"):
                with ui.Menu("新建"):
                    ui.MenuItem("新建工程\tCtrl+Shift+N", onselect=weak.new_project)
                with ui.Menu("打开"):
                    ui.MenuItem("打开工程\tCtrl+Shift+O", onselect=weak.open_project)
                with ui.Menu("最近的工程"):
                    for path in __main__.app.config['recent_project']:
                        ui.MenuItem(path, onselect=weak.do_open_project)
                    if __main__.app.config['recent_project']:
                        ui.MenuItem("清除列表", onselect=weak.clear_recent_project, sep=True)
                ui.MenuItem("打开工程所在文件夹", onselect=weak.open_project_dir)
                ui.MenuItem("重启\tCtrl+R", onselect=weak.restart)
                ui.MenuItem("退出\tCtrl+Q", onselect=weak.close_window)
            with ui.Menu("视图"):
                ui.MenuItem("切换控制台\tCtrl+`", onselect=weak.toggle_console)
                ui.MenuItem("切换控制台长文本输入\tCtrl+Shift+`", onselect=weak.toggle_console_input_multi)
            with ui.Menu("工具"):
                ui.MenuItem("打开工具\tCtrl+Shift+P", onselect=weak.open_tool)
            with ui.Menu("窗口"):
                ui.MenuItem("保存窗口位置和大小", onselect=weak.save_win_option)

        with ui.Frame("火纹工厂", style=window_style, styles=styles, menubar=menubar) as win:
            with ui.AuiManager() as aui:
                toolbar = ui.AuiToolBar(style={'height': 100}, extra=dict(direction="top", captionVisible=False))
                # ui.ListBox(choices=self.module_names, onselect=self.on_nav, extra=dict(captionVisible=False))
                self.book = ui.AuiNotebook(extra=dict(direction="center", maximizeButton=True, captionVisible=False))
                with ui.Vertical(class_="console-bar", extra=dict(
                    name="console", direction="bottom", row=1, caption="控制台", closeButton=False, maximizeButton=True
                )) as console:
                    self.console_output = ui.TextInput(readonly=True, multiline=True, class_="console-output")
                    with ui.Horizontal(class_="expand console-input-bar"):
                        self.console_input = ui.ComboBox(
                            wxstyle=ui.wx.CB_DROPDOWN | ui.wx.TE_PROCESS_ENTER, class_="expand console-input")
                        ui.Button("∧", class_="btn-sm", onclick=weak.toggle_console_input_multi)
                with ui.Horizontal(
                    class_="console-input-multi",
                    extra=dict(name="multiline_console", direction="bottom", captionVisible=False, hide=True)
                ) as multiline_console:
                    self.console_input_multi = ui.TextInput(class_="console-input", multiline=True)
                    with ui.Vertical(class_="expand"):
                        ui.Button("∨", class_="btn-sm fill", onclick=weak.toggle_console_input_multi)
                        ui.Button(">>", class_="btn-sm fill", onclick=weak.console_input_multi_run,
                                  extra={"tooltip": "执行输入框中代码 Ctrl+Enter"})
            # ui.StatusBar()

        self.win = win
        self.aui = aui
        self.console = console

        # 绑定控制台控件
        pyapi.console.bind_elem(self.console_input.wxwindow, self.console_output.wxwindow)
        win.set_onclose(self.weak.onclose)
        # 尝试加载图标
        icon_path = fefactory.executable_name() + '.ico'
        if os.path.exists(icon_path):
            icon = ui.wx.Icon(icon_path, ui.wx.BITMAP_TYPE_ICO)
            win.SetIcon(icon)
        self.render_toolbar(toolbar)
        self.book.set_on_page_changed(self.weak.on_tool_change)

        win.Show()
        # self.console.set_on_file_drop(self.weak.on_console_file_drop)
        self.console_input_multi.set_on_keydown(self.weak.on_console_input_multi_key)

    # @property
    # def module_names(self):
    #     return (module[0] for module in modules)

    @property
    def tool_names(self):
        return (f'{t[1]}: {t[0]}' for t in tools.tools)

    # def get_module(self, name):
    #     module = __import__('modules.' + name, fromlist=['main']).main
    #     return module.Module

    def get_tool(self, name):
        name = name.__name__ if isinstance(name, types.ModuleType) else 'tools.' + name
        module = __import__(name, fromlist=['main']).main
        return module.Main

    # def on_nav(self, listbox):
    #     """左边导航切换模块"""
    #     name = modules[listbox.index][1]
    #     try:
    #         Module = self.get_module(name)
    #         module = Module()
    #         module.attach(self)
    #         __main__.module = module
    #     except Exception:
    #         print('加载模块%s失败' % name)
    #         traceback.print_exc()

    def onclose(self, *args):
        if self.book.close_all_page():
            self.opened_tools.clear()
            self.opened_tools_map.clear()
            del self.book
            del self.win
        else:
            return False

    def close_window(self, _=None):
        self.win.Close()

    def restart(self, _=None, extra_option=None):
        """重启"""
        size = self.win.size
        position = self.win.position
        start_option = {"size": size, "position": position}
        if extra_option:
            start_option.update(extra_option)
        fefactory.restart(start_option)
        self.close_window()

    def render_toolbar(self, toolbar):
        """渲染快捷工具栏"""
        bitmap = ui.wx.Bitmap()
        listener = self.weak.on_toolbar_tool_click
        for name, module in self.toolbar_items:
            icon = ui.wx.Icon('python/tools/%s/icon.ico' % module.replace('.', '/'), ui.wx.BITMAP_TYPE_ICO)
            bitmap.CopyFromIcon(icon)
            toolitem = toolbar.AddTool(ui.wx.ID_ANY, name, bitmap, name)
            toolbar.set_onclick(toolitem.GetId(), listener)

        return toolbar.Realize()

    def on_toolbar_tool_click(self, toolbar, toolid):
        """快捷工具栏点击处理"""
        self.open_tool_by_name(self.toolbar_items[toolbar.GetToolPos(toolid)][1])

    def toggle_console(self, menu):
        """显示/隐藏控制台"""
        self.aui.toggle_pane("console")

    def new_project(self, menu):
        """新建工程"""
        path = pyapi.choose_dir("选择工程文件夹")
        if path:
            project = Project(path)
            if project.exists():
                # TODO
                pyapi.confirm_yes("此工程已存在，是否覆盖", pyapi.NO)
            else:
                # TODO
                project.title = input("请输入工程名称", os.path.basename(path))
            __main__.app.on_change_project(project)
            self.on_open_project(project)

    def open_project(self, menu):
        """打开工程"""
        path = pyapi.choose_dir("选择工程文件夹")
        if path:
            project = Project(path)
            if project.exists():
                __main__.app.on_change_project(project)
            else:
                pyapi.alert("提示", "该目录下没有project.json")

    def do_open_project(self, menu):
        """处理打开工程"""
        path = menu.GetText()
        print(path)
        if path != __main__.app.project.path:
            project = Project(path)
            __main__.app.on_change_project(project)
            self.on_open_project(project)

    def on_open_project(self, project):
        """打开工程回调"""
        if project:
            self.win.title = "%s - %s" % (self.win.title, project.title)

    def open_project_dir(self, menu):
        """打开工程目录"""
        if __main__.app.project_confirm():
            os.startfile(__main__.app.project.path)

    def clear_recent_project(self, menu):
        # 清除最近的工程
        pass

    def toggle_console_input_multi(self, _=None):
        """触发控制台多行输入框"""
        p1 = self.console_input.parent
        show = not p1.IsShown()
        p1.Show(show)
        self.aui.show_pane("multiline_console", not show)
        self.console.relayout()

    def console_input_multi_run(self, _=None):
        """控制台多行输入框执行"""
        try:
            exec(self.console_input_multi.GetValue(), vars(__main__))
        except Exception as e:
            if isinstance(e, SystemExit):
                raise
            else:
                traceback.print_exc()

    def on_console_file_drop(self, files):
        """控制台文件拖动事件"""
        # scope = __main__.__dict__
        scope = {'__builtins__': __main__.__builtins__}
        for file in files:
            if file.endswith('.py'):
                print('执行脚本: ' + file)
                pyapi.exec_file(file, scope)

        if scope != __main__.__dict__:
            __main__.last_scope = scope

    def on_console_input_multi_key(self, text_input, event):
        """控制台多行输入框按键事件"""
        mod = event.GetModifiers()
        code = event.GetKeyCode()
        if code == WXK.TAB:
            text_input.WriteText('    ')
            return True
        if mod == WXK.MOD_CONTROL:
            if code == WXK.RETURN:
                self.console_input_multi_run()
                return True
            elif code == WXK.A:
                text_input.SelectAll()
                return True
            elif code == WXK.L:
                self.console_output.Clear()
                return True

    def open_tool(self, menu):
        """打开工具菜单"""
        dialog = getattr(self, 'tool_dialog', None)
        if dialog is None:
            with ui.View.HERE, ui.dialog.StdDialog(
                    "选择工具", parent=self.win, style={'width': 640, 'height': 900}) as dialog:
                # wxTR_HIDE_ROOT|wxTR_NO_LINES|wxTR_FULL_ROW_HIGHLIGHT|wxTR_ROW_LINES|wxTR_HAS_BUTTONS|wxTR_SINGLE
                tree = ui.TreeCtrl(class_="fill", wxstyle=0x2C05)
                root = tree.AddRoot("")
                self.root_tools = self.get_sub_tools(tools)

                for item in self.root_tools:
                    item.id = tree.InsertItem(root, text=item.label, data=ui.wx.PyTreeItemData(item))

                tree.set_on_item_activated(self.weak.on_tool_select)
                # with dialog.footer:
                #     ui.Button(label="收藏")
                dialog.view.keep_styles = False
            self.tool_dialog = dialog
        dialog.ShowModal()

    def get_sub_tools(self, parent):
        """获取子目录工具"""
        dir_path = os.path.dirname(parent.__file__)
        files = os.listdir(dir_path)
        result = []
        for file in files:
            if not file.startswith('__') and file.find('.') is -1 and os.path.isdir(os.path.join(dir_path, file)):
                module = __import__(parent.__name__ + '.' + file, fromlist=file)
                name = getattr(module, 'name', None)
                if name is not None:
                    result.append(ToolTreeItem(module, name, getattr(module, 'package', False), None, None))
        return result

    def open_tool_by_name(self, name):
        """根据名称打开工具"""
        Tool = self.get_tool(name)
        tool = Tool()
        tool.attach(self)
        tool.add_close_callback(self.weak.on_tool_close)
        self.opened_tools.append(tool)
        self.opened_tools_map[id(tool.win)] = tool
        if tool.nested:
            self.book.index = self.book.GetPageCount() - 1
        else:
            tool.win.Show()

        __main__.tool = tool

    def on_tool_select(self, tree, event):
        """打开工具选项框项选中"""
        item = tree.GetItemData(event.GetItem()).data
        if item.package:
            if not item.children:
                item.children = self.get_sub_tools(item.module)
                for child in item.children:
                    child.id = tree.InsertItem(item.id, text=child.label, data=ui.wx.PyTreeItemData(child))
        else:
            self.open_tool_by_name(item.module)
            self.tool_dialog.EndModal()

    def on_tool_change(self, book):
        """切换工具"""
        __main__.tool = self.opened_tools_map.get(id(book.get_page()), None)

    def on_tool_close(self, tool):
        """工具窗口关闭回调，移除引用"""
        self.opened_tools.remove(tool)
        self.opened_tools_map.pop(id(tool.win), None)

        if getattr(__main__, 'tool', None) == tool:
            del __main__.tool

    def save_win_option(self, menu):
        """保存窗口参数(大小和位置等)"""
        __main__.app.setconfig('start_option', {
            'position': self.win.position,
            'size': self.win.size,
        })


# 自适应默认窗口大小
screen_width = fefactory.Screen.width
if screen_width <= 1366:
    window_size = (900, 1200)
elif screen_width <= 1920:
    window_size = (1200, 960)
elif screen_width <= 2560:
    window_size = (1200, 960)
else:  # elif screen_width <= 3840:
    window_size = (1366, 1800)

window_style = {'width': window_size[0], 'height': window_size[1]}

styles = {
    'class': {
        'fill': {'weight': 1},
        'expand': {'expand': True},
        'console-bar': {'height': 160},
        'console-output': {'expand': True, 'weight': 1},
        'console-input': {'expand': True, 'weight': 1},
        'console-input-bar': {'padding-flag': 0b1000},
        'console-input-multi': {'height': 100},
        'btn-sm': {'width': 34},
    }
}


def main():
    frame = MainFrame()
    __main__.frame = frame
    __main__.win = frame.win
    __main__.pyapi = pyapi
    __main__.copy = pyapi.set_clipboard
