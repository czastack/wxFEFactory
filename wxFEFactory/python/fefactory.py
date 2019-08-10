import json
import os
import sys
import traceback
import __main__
import pyapi
from application import Application
from functools import partial
from lib.ui import wx


def restart(start_option=None):
    """重新加载程序"""
    __main__.app.save_temp_start_option(start_option)
    pyapi.restart()


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
    path = pyapi.choose_file("选择保存文件", file=lastfile, wildcard='*.json')
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
    path = pyapi.choose_file("选择要读取的文件", file=lastfile, wildcard='*.json')
    if path:
        if owner:
            owner.lastfile = path
        with open(path, encoding="utf-8") as file:
            return json.load(file)


class Screen:
    size = pyapi.ui.GetDisplaySize()
    width, height = size.x, size.y
    dpi = pyapi.ui.GetDisplaySize()


def main():
    # 重定向标准输出
    class LogWriter:
        def flush(self):
            pass

        def write(self, s):
            pyapi.log_message(s)

    sys.stdout = sys.stderr = LogWriter()

    if not hasattr(pyapi, '_alert'):
        pyapi._alert = pyapi.alert

    def alert(title, msg=None):
        if not msg:
            msg = title
            title = '提示'
        pyapi._alert(title, msg)

    def confirm_yes(msg, defdefaultButton=wx.YES):
        return pyapi.confirm('确认', msg, defdefaultButton) == wx.YES

    pyapi.alert = alert
    pyapi.confirm_yes = confirm_yes
    __builtins__['input'] = partial(pyapi.input, '输入')

    __main__.app = Application()
    pyapi.set_on_exit(__main__.app.on_exit)

    import main
    main.main()


if __name__ == 'fefactory':
    main()
