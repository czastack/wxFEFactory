import fefactory_api
import json
import os
import sys
import traceback
import application
import __main__
from modules import modules
from functools import partial
from lib.ui import wx


def reload(start_option=None, callback=None):
    """重新加载相关模块"""
    pydir = os.path.dirname(__file__)
    for name in list(sys.modules):
        file = getattr(sys.modules[name], '__file__', None)
        if file is None:
            file = getattr(sys.modules[name], '__path__', None)
            if file is not None:
                file = file._path[0]
            else:
                continue
        if file.startswith(pydir):
            del sys.modules[name]

    for name in list(__main__.__dict__):
        if not name.startswith('__'):
            del __main__.__dict__[name]

    try:
        del __builtins__['fpy']
    except Exception:
        pass

    if start_option:
        application.app.start_option = start_option

    __import__(__name__)

    if callback:
        callback()


def executable_file():
    return sys.argv[0]


def executable_name():
    path = executable_file()
    return os.path.splitext(os.path.basename(path))[0]


def execfile(path, encoding="utf-8"):
    with open(path, encoding=encoding) as f:
        exec(f.read())


def json_dump_file(owner, data, dumper=None):
    """选择json文件导出"""
    lastfile = owner and getattr(owner, 'lastfile', None)
    path = fefactory_api.choose_file("选择保存文件", file=lastfile, wildcard='*.json')
    if path:
        if owner:
            owner.lastfile = path
        with open(path, 'w', encoding="utf-8") as file:
            if dumper is None:
                json.dump(data, file)
            else:
                dumper(data, file)


def json_load_file(owner):
    """选择json文件导入"""
    lastfile = owner and getattr(owner, 'lastfile', None)
    path = fefactory_api.choose_file("选择要读取的文件", file=lastfile, wildcard='*.json')
    if path:
        if owner:
            owner.lastfile = path
        with open(path, encoding="utf-8") as file:
            return json.load(file)


class Screen:
    size = fefactory_api.ui.GetDisplaySize()
    width, height = size.x, size.y
    dpi = fefactory_api.ui.GetDisplaySize()


if getattr(fefactory_api, 'fefactory_inited', False) is not True:
    # 重定向标准输出
    class _LogWriter:
        def flush(self):
            pass

        def write(self, s):
            fefactory_api.log_message(s)

    sys.stdout = sys.stderr = _LogWriter()
    _alert = fefactory_api.alert

    def alert(title, msg=None):
        if not msg:
            msg = title
            title = '提示'
        _alert(title, msg)

    def confirm_yes(msg, defdefaultButton=wx.YES):
        return fefactory_api.confirm('确认', msg, defdefaultButton) == wx.YES

    fefactory_api.alert = alert
    fefactory_api.confirm_yes = confirm_yes
    fefactory_api.fefactory_inited = True
    __builtins__['input'] = partial(fefactory_api.input, '输入')


if __name__ == 'fefactory':
    __builtins__['fpy'] = sys.modules[__name__]
    import main
