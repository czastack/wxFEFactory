import os
import traceback
import types
import __main__
import fefactory_api
import fefactory
import tools
from application import app
from project import Project
from modules import modules
from fe.ferom import FeRomRW
from lib import exui, extypes, wxconst
from lib.win32.keys import WXK
Path = os.path
ui = fefactory_api.ui


"""
:param name: 工具文件夹名
:param label: 工具名称
:param packae: 是否是工具集(有子工具)
:param children: 子工具元组
"""
ToolTreeItem = extypes.DataClass("ToolTreeItem", ("module", "label", "package", "children", "id"))


class MainFrame:
    def __init__(self, start_option=None):
        self.weak = extypes.WeakBinder(self)
        self.opened_tools = []
        self.opened_tools_map = {}
        self.render()

        if start_option:
            size = start_option.get('size', None)
            if size:
                self.win.size = size
            position = start_option.get('position', None)
            if position:
                self.win.position = position

        if getattr(app, 'project', None):
            self.on_open_project(app.project)

    def render(self):
        with ui.MenuBar() as menubar:
            with ui.Menu("文件"):
                with ui.Menu("新建"):
                    ui.MenuItem("新建工程\tCtrl+Shift+N", onselect=self.new_project)
                with ui.Menu("打开"):
                    ui.MenuItem("打开工程\tCtrl+Shift+O", onselect=self.open_project)
                with ui.Menu("最近的工程"):
                    for path in app.config['recent_project']:
                        ui.MenuItem(path, onselect=self.do_open_project)
                    if app.config['recent_project']:
                        ui.MenuItem("清除列表", onselect=self.clear_recent_project, sep=True)
                ui.MenuItem("打开工程所在文件夹", onselect=self.open_project_dir)
                ui.MenuItem("从ROM中读取内容\tCtrl+Shift+R", "打开火纹的rom读取对应的资源", onselect=self.read_from_rom)
                ui.MenuItem("重启\tCtrl+R", onselect=self.restart)
                ui.MenuItem("退出\tCtrl+Q", onselect=self.closeWindow)
            with ui.Menu("视图"):
                ui.MenuItem("切换控制台\tCtrl+`", onselect=self.toggle_console)
                ui.MenuItem("切换控制台长文本输入\tCtrl+Shift+`", onselect=self.toggle_consol_input_multi)
            with ui.Menu("工具"):
                ui.MenuItem("打开工具\tCtrl+Shift+P", onselect=self.open_tool)
            with ui.Menu("窗口"):
                ui.MenuItem("保存窗口位置和大小", onselect=self.save_win_option)

        with ui.Window("火纹工厂", style=window_style, styles=styles, menubar=menubar) as win:
            with ui.AuiManager() as aui:
                toolbar = self.render_toolbar()
                ui.AuiItem(toolbar, direction="top", captionVisible=False)
                # ui.AuiItem(ui.ListBox(choices=self.module_names, onselect=self.onNav), captionVisible=False)
                self.book = ui.AuiNotebook()
                ui.AuiItem(self.book, direction="center", maximizeButton=True, captionVisible=False)
                with ui.Vertical(className="console-bar") as console:
                    self.console_output = ui.TextInput(readonly=True, multiline=True, className="console-output")
                    with ui.Horizontal(className="expand console-input-bar"):
                        self.console_input = ui.ComboBox(wxstyle=wxconst.CB_DROPDOWN | wxconst.TE_PROCESS_ENTER,
                            className="expand console-input")
                        ui.Button("∧", className="btn-sm", onclick=self.toggle_consol_input_multi)
                with ui.Horizontal(className="console-input-multi").show(False) as multiline_console:
                    self.console_input_multi = ui.TextInput(className="console-input", multiline=True)
                    with ui.Vertical(className="expand"):
                        ui.Button("∨", className="btn-sm", onclick=self.toggle_consol_input_multi)
                        ui.Button(">>", className="btn-sm fill", onclick=self.consol_input_multi_run).setToolTip(
                            "执行输入框中代码 Ctrl+Enter")
                ui.AuiItem(console, name="console", direction="bottom", row=1, caption="控制台", maximizeButton=True)
                ui.AuiItem(multiline_console, name="multiline_console", direction="bottom",
                    captionVisible=False, hide=True)
            ui.StatusBar()
            # 尝试加载图标
            icon_name = fefactory.executable_name() + '.ico'
            if Path.exists(icon_name):
                win.setIcon(icon_name)

        win.setOnClose(self.onClose)
        self.book.setOnPageChanged(self.on_tool_change)

        self.win = win
        self.aui = aui
        self.console = console
        fefactory_api.console.bind_elem(self.console_input, self.console_output)
        self.console.setOnFileDrop(self.onConsoleFileDrop)
        self.console_input_multi.setOnKeyDown(self.on_console_input_multi_key)

    def on_enter(self, _):
        print(_)

    @property
    def module_names(self):
        return (module[0] for module in modules)

    @property
    def tool_names(self):
        return (f'{t[1]}: {t[0]}' for t in tools.tools)

    def get_module(self, name):
        module = __import__('modules.' + name, fromlist=['main']).main
        return module.Module

    def get_tool(self, name):
        name = name.__name__ if isinstance(name, types.ModuleType) else 'tools.' + name
        module = __import__(name, fromlist=['main']).main
        return module.Main

    def onNav(self, listbox):
        """左边导航切换模块"""
        name = modules[listbox.index][1]
        try:
            Module = self.get_module(name)
            module = Module()
            module.attach(self)
            __main__.module = module
        except Exception:
            print('加载模块%s失败' % name)
            traceback.print_exc()

    def onClose(self, _=None):
        if self.book.closeAllPage():
            del self.book
            self.opened_tools.clear()
            self.opened_tools_map.clear()
            return True
        return False

    def closeWindow(self, _=None):
        self.win.close()

    def restart(self, _=None, callback=None):
        self.closeWindow()
        fefactory.reload({"size": self.win.size, "position": self.win.position}, callback)

    def render_toolbar(self):
        bitmap = ui.Bitmap()
        toolbar = ui.AuiToolBar()
        for item in tools.toolbar_tools:
            bitmap.loadIcon('python/tools/%s/icon.ico' % item[1].replace('.', '/'))
            toolbar.addTool(item[0], "", bitmap, self.on_toolbar_tool_click)

        return toolbar.realize()

    def on_toolbar_tool_click(self, toolbar, toolid):
        self.open_tool_by_name(tools.toolbar_tools[toolbar.getToolPos(toolid)][1])

    def toggle_console(self, menu):
        """显示/隐藏控制台"""
        self.aui.togglePane("console")

    def onselect(self, *args):
        print(args)

    def new_project(self, menu):
        path = fefactory_api.choose_dir("选择工程文件夹")
        if path:
            project = Project(path)
            if project.exists():
                # TODO
                fefactory_api.confirm_yes("此工程已存在，是否覆盖", fefactory_api.NO)
            else:
                # TODO
                project.title = input("请输入工程名称", Path.basename(path))
            app.onChangeProject(project)
            self.on_open_project(project)

    def open_project(self, menu):
        path = fefactory_api.choose_dir("选择工程文件夹")
        if path:
            project = Project(path)
            if project.exists():
                app.onChangeProject(project)
            else:
                fefactory_api.alert("提示", "该目录下没有project.json")

    def do_open_project(self, menu):
        path = menu.getText()
        print(path)
        if path != app.project.path:
            project = Project(path)
            app.onChangeProject(project)
            self.on_open_project(project)

    def on_open_project(self, project):
        if project:
            self.win.title = "%s - %s" % (self.win.title, project.title)

    def open_project_dir(self, menu):
        if app.project_confirm():
            os.startfile(app.project.path)

    def clear_recent_project(self, menu):
        pass

    def toggle_consol_input_multi(self, _=None):
        p1 = self.console_input.parent
        isShow = not p1.isShow()
        p1.show(isShow)
        self.aui.showPane("multiline_console", not isShow)
        self.console.relayout()

    def consol_input_multi_run(self, _=None):
        try:
            exec(self.console_input_multi.value, vars(__main__))
        except Exception as e:
            if isinstance(e, SystemExit):
                raise
            else:
                traceback.print_exc()

    def onConsoleFileDrop(self, files):
        # scope = __main__.__dict__
        scope = {'__builtins__': __main__.__builtins__}
        for file in files:
            if file.endswith('.py'):
                print('执行脚本: ' + file)
                fefactory_api.exec_file(file, scope)

        if scope != __main__.__dict__:
            __main__.last_scope = scope

    def on_console_input_multi_key(self, text_input, event):
        """控制台多行输入框按键事件"""
        mod = event.GetModifiers()
        code = event.GetKeyCode()
        if code == WXK.TAB:
            text_input.writeText('    ')
            return True
        if mod == WXK.MOD_CONTROL:
            if code == WXK.RETURN:
                self.consol_input_multi_run()
                return True
            elif code == WXK.A:
                text_input.selectAll()
                return True
            elif code == WXK.L:
                self.console_output.clear()
                return True

    def read_from_rom(self, menu):
        rom = fefactory_api.choose_file("选择火纹的Rom", wildcard='*.gba|*.gba')
        if not rom:
            return
        reader = FeRomRW(rom)
        if not reader.closed:
            print(reader.getRomTitle())
            dialog = exui.ListDialog("选择执行导入的模块", listbox={'choices': self.module_names})
            if dialog.showModal():
                for i in dialog.listbox.getCheckedItems():
                    name = modules[i][1]
                    try:
                        Module = self.get_module(name)
                        module = Module()
                        module.attach()
                        module.readFrom(reader)

                    except Exception:
                        print('加载模块%s失败' % name)
                        traceback.print_exc()

    def open_tool(self, menu):
        dialog = getattr(self, 'tool_dialog', None)
        if dialog is None:
            with exui.StdDialog("选择工具", style={'width': 640, 'height': 900}) as dialog:
                # wxTR_HIDE_ROOT|wxTR_NO_LINES|wxTR_FULL_ROW_HIGHLIGHT|wxTR_ROW_LINES|wxTR_HAS_BUTTONS|wxTR_SINGLE
                tree = ui.TreeCtrl(className="fill", wxstyle=0x2C05)
                root = tree.AddRoot("")
                self.root_tools = self.get_sub_tools(tools)

                for item in self.root_tools:
                    item.id = tree.InsertItem(root, item.label, data=item)

                tree.setOnItemActivated(self.weak.on_tool_select)
            self.tool_dialog = dialog
        dialog.showModal()

    def get_sub_tools(self, parent):
        dir_path = Path.dirname(parent.__file__)
        files = os.listdir(dir_path)
        result = []
        for file in files:
            if not file.startswith('__') and file.find('.') is -1 and Path.isdir(Path.join(dir_path, file)):
                module = __import__(parent.__name__ + '.' + file, fromlist=file)
                name = getattr(module, 'name', None)
                if name is not None:
                    result.append(ToolTreeItem(module, name, getattr(module, 'package', False), None, None))
        return result

    def open_tool_by_name(self, name):
        Tool = self.get_tool(name)
        tool = Tool()
        tool.attach(self)
        tool.add_close_callback(self.weak.on_tool_close)
        self.opened_tools.append(tool)
        self.opened_tools_map[id(tool.win)] = tool
        self.book.index = self.book.count - 1

        __main__.tool = tool

    def on_tool_select(self, tree, event):
        """打开工具选项框项选中"""
        item = tree.GetItemData(event.item)
        if item.package:
            if not item.children:
                item.children = self.get_sub_tools(item.module)
                for child in item.children:
                    child.id = tree.InsertItem(item.id, child.label, data=child)
        else:
            self.open_tool_by_name(item.module)
            self.tool_dialog.endModal()

    def on_tool_change(self, book):
        __main__.tool = self.opened_tools_map.get(id(book.getPage()), None)

    def on_tool_close(self, tool):
        self.opened_tools.remove(tool)
        self.opened_tools_map.pop(id(tool.win), None)

        if getattr(__main__, 'tool', None) == tool:
            del __main__.tool

    def save_win_option(self, menu):
        app.setconfig('start_option', {
            'position': self.win.position,
            'size': self.win.size,
        })


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

if __name__ == 'main':
    frame = MainFrame(app.start_option)

    __main__.app = app
    __main__.frame = frame
    __main__.win = win = frame.win
    __main__.fefactory_api = fefactory_api
    __main__.copy = fefactory_api.set_clipboard
