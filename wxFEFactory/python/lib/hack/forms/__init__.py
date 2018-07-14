from .widgets import *


LAZY = {
    'ModelCoordWidget': ('.coordwidget', 'ModelCoordWidget'),
}


def __getattr__(name):
    if name in LAZY:
        module, fromlist = LAZY[name]
        if isinstance(fromlist, str):
            fromlist = (fromlist,)
        if module[0] == '.':
            module = __package__ + module
        result = __import__(module, fromlist=fromlist)
        if len(fromlist) == 1:
            result = getattr(result, fromlist[0])
        globals()[name] = result
        return result
    raise AttributeError