from modules import modules
from project import Project
from application import app
from fe.ferom import FeRomRW
import os
import traceback
import __main__
import fefactory_api
import fefactory
Path = os.path

ui = fefactory_api.layout

class MainFrame:
    def __init__(self):
        self.render()
        if hasattr(app, 'project'):
            self.onOpenProject(app.project)

    def render(self):
        with ui.MenuBar() as menubar:
            with ui.Menu("文件"):
                with ui.Menu("新建"):
                    ui.MenuItem("新建工程\tCtrl+Shift+N", onselect=self.newProject)
                with ui.Menu("打开"):
                    ui.MenuItem("打开工程\tCtrl+Shift+O", onselect=self.openProject)
                with ui.Menu("最近的工程"):
                    for path in app.config['recent_project']:
                        ui.MenuItem(path, onselect=self.doOpenProject)
                    if app.config['recent_project']:
                       ui.MenuItem("清除列表", onselect=self.clearRecentProject, sep=True) 
                ui.MenuItem("打开工程所在文件夹", onselect=self.openProjectDir)
                ui.MenuItem("从ROM中读取内容", onselect=self.readFromRom)
                ui.MenuItem("重启\tCtrl+R", onselect=self.restart)
                ui.MenuItem("退出\tCtrl+Q", onselect=self.closeWindow)
            with ui.Menu("视图"):
                ui.MenuItem("切换控制台\tCtrl+`", onselect=self.toggleConsole)
            with ui.Menu("窗口"):
                pass

        with ui.Window("火纹工厂", style=winstyle, styles=styles, menuBar=menubar) as win:
            with ui.AuiManager(key="aui"):
                ui.AuiItem(ui.ToolBar().addTool("123", "1234", "", self.onselect).realize(), direction="top", captionVisible=False)
                ui.AuiItem(ui.ListBox(options=modules, values=lambda x: x, onselect=self.onNav), captionVisible=False)
                ui.AuiItem(ui.AuiNotebook(key="book"), direction="center", maximizeButton=True, captionVisible=False)
                with ui.Vertical(style=consoleStyle) as console:
                    self.consol_output = ui.TextInput(readonly=True, multiline=True, style=consoleOutputStyle)
                    with ui.Horizontal(className="expand"):
                        self.consol_input = ui.TextInput(extStyle=0x0400, className="expand console-input")
                        ui.Button(label="∧", className="btn-sm", onclick=self.toggleConsolInputMulti)
                    with ui.Horizontal(className="expand").show(False):
                        self.consol_input_multi = ui.TextInput(className="console-input console-input-multi", multiline=True)
                        with ui.Vertical(className="expand"):
                            ui.Button(label="∨", className="btn-sm", onclick=self.toggleConsolInputMulti)
                            ui.Button(label=">>", className="btn-sm fill", onclick=self.consolInputMultiRun).setToolTip("执行输入框中代码")
                ui.AuiItem(console, name="console", direction="bottom", caption="控制台", maximizeButton=True)
            ui.StatusBar()

        with ui.ContextMenu(onselect=self.onselect) as cm:
            ui.MenuItem("测试")
        
        self.win = win
        self.console = console
        win.book.setContextMenu(cm)
        fefactory_api.setConsoleElem(self.consol_input, self.consol_output)
        
    def onNav(self, listbox):
        """左边导航切换模块"""
        name = listbox.getValue()
        try:
            module = __import__('modules.' + name, fromlist=['main']).main
            __main__.m = module.Module()

        except Exception as e:
            print('加载模块%s失败' % name)
            traceback.print_exc()

    def closeWindow(self, m=None):
        self.win.close()

    def restart(self, m):
        self.closeWindow()
        fefactory.reload()

    def toggleConsole(self, m):
        """显示/隐藏控制台"""
        self.win.aui.togglePane("console")

    def onselect(self, *args):
        print(args)

    def newProject(self, m):
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
            self.onOpenProject(project)

    def openProject(self, m):
        path = fefactory_api.choose_dir("选择工程文件夹")
        if path:
            project = Project(path)
            if project.exists():
                app.onChangeProject(project)
            else:
                fefactory_api.alert("提示", "该目录下没有project.json")

    def doOpenProject(self, m):
        path = m.getText()
        print(path)
        if path != app.project.path:
            project = Project(path)
            app.onChangeProject(project)
            self.onOpenProject(project)

    def onOpenProject(self, project):
        self.win.title = "%s - %s" % (self.win.title, project.title)

    def openProjectDir(self, m):
        if app.project_confirm():
            os.startfile(app.project.path)

    def clearRecentProject(self, m):
        pass

    def toggleConsolInputMulti(self, btn):
        p1 = self.consol_input.parent
        p2 = self.consol_input_multi.parent
        p1.show(not p1.isShow())
        p2.show(not p2.isShow())
        self.console.reLayout()

    def consolInputMultiRun(self, btn):
        exec(self.consol_input_multi.value, vars(__main__))

    def readFromRom(self, m):
        rom = fefactory_api.choose_file("选择火纹的Rom", wildcard='*.gba|*.gba|*.zip|*.zip')
        reader = FeRomRW(rom)
        if not reader.closed:
            print(reader.getRomTitle())

winstyle = {
    'width': 1200,
    'height': 960,
}

styles = {
    'type': {

    },
    'class': {
        'fill': {'flex': 1},
        'expand': {'expand': True},
        'console-input': {
            'expand': True,
            'flex': 1,
        },
        'console-input-multi': {'height': 70},
        'btn-sm': {'width': 30,}
    }
}

consoleStyle = {
    'height': 150,
}
consoleOutputStyle = {
    'expand': True,
    'flex': 1,
    'showPadding': '0 0 1 0',
}

if __name__ == 'mainframe':
    frame = MainFrame()

    __main__.app = app
    __main__.win = win = frame.win
