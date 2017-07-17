from modules import modules
from project import Project
from application import app
import fefactory_api
import fefactory
import __main__
import traceback
import os
Path = os.path

ui = fefactory_api.layout

if __name__ == 'mainframe':
    winstyle = {
        'width': 1200,
        'height': 960,
    }

    styles = {
        'type': {

        },
        'class': {
            
        }
    }

    consoleStyle = {
        'height': 150,
    }
    consoleInputStyle = {
        'expand': True,
        'showPadding': '1 0 0 0',
    }
    consoleOutputStyle = {
        'expand': True,
        'flex': 1,
    }

    def onNav(listbox):
        """左边导航切换模块"""
        name = listbox.getValue()
        try:
            module = __import__('modules.' + name, fromlist=['main']).main
            module.Module()
            __main__.M = module.Module

        except Exception as e:
            print('加载模块%s失败' % name)
            traceback.print_exc()

    def closeWindow(m=None):
        win.close()

    def restart(m):
        closeWindow()
        fefactory.reload()

    def toggleConsole(m):
        """显示/隐藏控制台"""
        win.aui.togglePane("console")

    def onselect(*args):
        print(args)

    def newProject(m):
        path = fefactory_api.choose_dir("选择工程文件夹")
        if path:
            project = Project(path)
            if project.exists():
                fefactory_api.confirm_dialog("提示", "此工程已存在，是否覆盖", fefactory.NO)
            else:
                # TODO
                project.title = fefactory_api.input_dialog("工程名称", "请输入工程名称", Path.basename(path))
            app.onChangeProject(project)
            onOpenProject(project)

    def openProject(m):
        path = fefactory_api.choose_dir("选择工程文件夹")
        if path:
            project = Project(path)
            if project.exists():
                app.onChangeProject(project)
            else:
                fefactory_api.alert("提示", "该目录下没有project.json")

    def doOpenProject(m):
        path = m.getText()
        print(path)
        if path != app.project.path:
            project = Project(path)
            app.onChangeProject(project)
            onOpenProject(project)

    def onOpenProject(project):
        win.title = "%s - %s" % (win.title, project.title)

    def clearRecentProject(m):
        pass

    with ui.MenuBar() as m:
        with ui.Menu("文件"):
            with ui.Menu("新建"):
                ui.MenuItem("新建工程\tCtrl+Shift+N", onselect=newProject)
            with ui.Menu("打开"):
                ui.MenuItem("打开工程\tCtrl+Shift+O", onselect=openProject)
            with ui.Menu("最近的工程"):
                for path in app.config['recent_project']:
                    ui.MenuItem(path, onselect=doOpenProject)
                if app.config['recent_project']:
                   ui.MenuItem("清除列表", onselect=clearRecentProject, sep=True) 
            ui.MenuItem("重启\tCtrl+R", onselect=restart)
            ui.MenuItem("退出\tCtrl+Q", onselect=closeWindow)
        with ui.Menu("视图"):
            ui.MenuItem("切换控制台\tCtrl+`", onselect=toggleConsole)
        with ui.Menu("窗口"):
            pass

    with ui.Window("火纹工厂", style=winstyle, styles=styles, menuBar=m) as win:
        with ui.AuiManager(key="aui"):
            ui.AuiItem(ui.ToolBar().addTool("123", "1234", "", onselect).realize(), direction="top", captionVisible=False)
            ui.AuiItem(ui.ListBox(options=modules, values=lambda x: x, onselect=onNav), captionVisible=False)
            ui.AuiItem(ui.AuiNotebook(key="book"), direction="center", maximizeButton=True, captionVisible=False)
            with ui.Vertical(style=consoleStyle) as console:
                consol_output = ui.TextInput(readonly=True, multiline=True, style=consoleOutputStyle)
                consol_input = ui.TextInput(extStyle=0x0400, style=consoleInputStyle)
            ui.AuiItem(console, name="console", direction="bottom", caption="控制台", maximizeButton=True)
        ui.StatusBar()

    with ui.ContextMenu(onselect=onselect) as cm:
        ui.MenuItem("测试")
    
    win.book.setContextMenu(cm)
    fefactory_api.setConsoleElem(consol_input, consol_output)

    if hasattr(app, 'project'):
        onOpenProject(app.project)

    __main__.app = app
    __main__.win = win
