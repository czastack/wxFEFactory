from modules import modules
from project import Project
import fefactory_api
import fefactory
import traceback
import imp
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

    def onNav(name, index):
        try:
            module = __import__('modules.' + name, fromlist=['main']).main
            module.Module()

        except Exception as e:
            print('加载模块%s失败' % name)
            traceback.print_exc()

    def closeWindow(m=None):
        win.close()

    def restart(m):
        closeWindow()
        fefactory.reload()
        import mainframe
        imp.reload(mainframe)

    def toggleConsole(m):
        win.aui.togglePane("console")

    def onselect(*args):
        print(args)

    def newProject(self):
        path = fefactory_api.choose_dir("选择新工程文件夹")
        if path:
            name = fefactory_api.input_dialog("工程名称", "请输入工程名称", Path.basename(path))
            project = Project(path, name)
            win.title = "%s - %s" % (win.title, project.title)

    with ui.MenuBar() as m:
        with ui.Menu("文件"):
            ui.MenuItem("打开\tCtrl+O")
            with ui.Menu("新建"):
                ui.MenuItem("新建工程\tCtrl+Shift+N", onselect=newProject)
            ui.MenuItem("重启\tCtrl+R", onselect=restart)
            ui.MenuItem("退出\tCtrl+Q", onselect=closeWindow)
        with ui.Menu("视图"):
            ui.MenuItem("切换控制台\tCtrl+`", onselect=toggleConsole)
        with ui.Menu("窗口"):
            pass

    with ui.Window("火纹工厂", style=winstyle, styles=styles, menuBar=m) as win:
        with ui.AuiManager(key="aui"):
            ui.AuiItem(ui.ListBox(options=modules, values=lambda x: x, onselect=onNav))
            ui.AuiItem(ui.AuiNotebook(key="book"), direction="center", maximizeButton=True)
            with ui.Vertical(style=consoleStyle) as console:
                consol_output = ui.TextInput(readonly=True, multiline=True, style=consoleOutputStyle)
                consol_input = ui.TextInput(extStyle=0x0400, style=consoleInputStyle)
            ui.AuiItem(console, name="console", direction="bottom", caption="控制台", maximizeButton=True)

    with ui.ContextMenu(onselect=onselect) as cm:
        ui.MenuItem("测试")
    win.book.setContextMenu(cm)
    fefactory_api.setConsoleElem(consol_input, consol_output)
