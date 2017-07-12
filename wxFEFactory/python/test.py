# from modules.character import form

# from ctypes import addressof, sizeof

# string_at(addressof(r),sizeof(r))


from fefactory_api.layout import *

winstyle = {
    'width': 600,
    'height': 320,
}

btnstyle = {
    # 'flex': 1,
    # 'expand': True,
    'padding': 10,
    'showPadding': '1',
    'fontSize': 20,
    'verticalAlign': 'center',
}

styles = {
    'type': {
        'Button': btnstyle,
        'Text': btnstyle,
        'CheckBox': btnstyle,
        'RadioBox': {'flexDirection': 'row', 'expand': True, 'flex': 1},
        'ListBox': {
            'expand': True,
        },
        'ComboBox': {
            'expand': True,
        },
    },
    'class': {
        'input': [btnstyle, {'flex': 1, 'color': '#f00', 'textAlign': 'center'}]
    }
}

def onclick(btn):
    print(btn, 123)

def onselect(*args):
    print(args)

def onchange(cb):
    print(cb.checked)

def onselect_item(menu):
    print(menu, 123)

def closeWindow(m):
    win.close()

with MenuBar(onselect=onselect) as m:
    with Menu("文件"):
        MenuItem("打开\tCtrl+O")
        MenuItem("关闭", onselect=onselect_item)
    with Menu("窗口"):
        MenuItem("关闭\tCtrl+W", onselect=closeWindow)


with Window("测试窗口", style=winstyle, styles=styles, menuBar=m) as win:
    # with ScrollView(style=winstyle, key="sc", horizontal=True):
    #     with Vertical(key='lp', style={'expand': True}) as lp:
    #         ListBox(options=['选项1', '选项2'], values=[11,22], onselect=onselect, style={'width': 800})

    # with SplitterWindow(False, 160):
    #     Text(label="标签", key="label")
    #     TextInput(value="123", className="input", key="input")

        # with AuiManager():
        #     AuiItem(PropertyGrid(key="pg"), direction="left", maximizeButton=True, closeButton=False)
        #     AuiItem(ListView(key="li"), direction="right", caption="右")
        #     with AuiNotebook(key="book") as book:
        #         AuiItem(ListBox(options=['选项1', '选项2'], values=[11,22], onselect=onselect), caption="Page")
        #     AuiItem(book, direction="center", caption="中间")

    # with Vertical(key='vp'):
    #     with Horizontal(key='lp', style={'expand': True}) as lp:
    #         Text(label="标签", key="label")
    #         TextInput(value="123", className="input", key="input")
    #         Button(label="按钮", onclick=onclick, key="btn")
    #         CheckBox(label="Check me", onchange=onchange, alignRight=True)
    #     ListBox(options=['选项1', '选项2'], values=[11,22], onselect=onselect)
    #     RadioBox(label="Radios", options=['选项1', '选项2'], values=[11,22], onselect=onselect, key="select")

    with GridLayout(cols=2, key="gl"):
        CheckBox(label="Check me", onchange=onchange, alignRight=True, key="cb")
        Button(label="按钮", onclick=onclick, key="btn")
        Text(label="标签", key="label")
        TextInput(value="123", className="input", key="input")

