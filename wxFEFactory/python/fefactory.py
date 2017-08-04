from modules import modules
from functools import partial
import sys
import os
import fefactory_api
import traceback

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

    def confirm_yes(msg, defdefaultButton=fefactory_api.YES):
        return fefactory_api.confirm('确认', msg, defdefaultButton) == fefactory_api.YES

    __builtins__['input'] = partial(fefactory_api.input, '输入')
    fefactory_api.alert = staticmethod(alert)
    fefactory_api.confirm_yes = staticmethod(confirm_yes)
    fefactory_api.fefactory_inited = True


def reload():
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

    __import__(__name__)


import mainframe