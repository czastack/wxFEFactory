from fefactory_api.layout import *
from modules import modules
import fefactory_api
import fefactory
import traceback
import imp

if __name__ == 'mainframe':
    winstyle = {
        'width': 800,
        'height': 640,
    }

    styles = {
        'type': {

        },
        'class': {
            
        }
    }

    consoleStyle = {
        'height': 300,
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
            module = getattr(__import__('modules.' + name), name) # , fromlist=['main']
            module.run()
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

    with MenuBar() as m:
        with Menu("文件"):
            MenuItem("打开\tCtrl+O")
            MenuItem("重启\tCtrl+R", onselect=restart)
            MenuItem("关闭")
        with Menu("窗口"):
            MenuItem("关闭\tCtrl+W", onselect=closeWindow)

    with Window("火纹工厂", style=winstyle, styles=styles, menuBar=m) as win:
        with AuiManager():
            AuiItem(ListBox(options=modules, values=lambda x: x, onselect=onNav))
            AuiItem(AuiNotebook(key="book"), direction="center", maximizeButton=True)
            with Vertical(style=consoleStyle) as console:
                consol_output = TextInput(readonly=True, multiline=True, style=consoleOutputStyle)
                consol_input = TextInput(extStyle=0x0400, style=consoleInputStyle)
            AuiItem(console, direction="bottom", caption="控制台", maximizeButton=True)

    def onselect(*args):
        print(args)

    with ContextMenu(onselect=onselect) as cm:
        MenuItem("测试")
    win.book.setContextMenu(cm)
    fefactory_api.setConsoleElem(consol_input, consol_output)
