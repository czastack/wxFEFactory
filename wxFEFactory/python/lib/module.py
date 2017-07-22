from mainframe import win
from application import app
from lib.lazy import lazyclassmethod
import os
import json

DUMP_INDENT = app.getConfig('json_indent', 4)

class BaseModule:
    menu = None
    INS = None

    from fefactory_api import alert, confirm, YES, NO, CANCEL, longtext_dialog

    def __init__(self):
        ins = __class__.INS
        if ins is None:
            ins = __class__.INS = []
        
        try:
            self.index = ins.index(None)
            ins[self.index] = self
        except ValueError:
            self.index = len(ins)
            ins.append(self)

        with win.book:
            self.view = self.render()
        with win.menubar:
            self.menu = self.getMenu()

    def onclose(self):
        if self.menu:
            win.menubar.remove(self.menu)
        __class__.INS[__class__.INS.index(self)] = None
        return True

    def readFrom(self, reader):
        pass

    def render(self):
        pass

    def getMenu(self, menubar):
        pass

    def getFirstOtherInstance(self):
        for it in __class__.INS:
            if it is not None and it is not self:
                return it

    def getTitle(self):
        title = self.form.title
        if self.index is not 0:
            title += str(self.index + 1)
        return title

    @lazyclassmethod
    def getName(cls):
        return cls.__module__.split('.')[1]

    @classmethod
    def getDir(cls):
        return os.path.join(app.project.path, cls.getName())

    @classmethod
    def loadJson(cls, name, defval={}):
        try:
            with open(os.path.join(cls.getDir(), name + '.json')) as file:
                ret = json.load(file)
        except Exception: #FileNotFoundError, json.decoder.JSONDecodeError
            ret = defval
        return ret

    @classmethod
    def dumpJson(cls, name, data, indent=DUMP_INDENT):
        dir_ = cls.getDir()
        if not os.path.exists(dir_):
            os.mkdir(dir_)
        with open(os.path.join(dir_, name + '.json'), 'w') as file:
            json.dump(data, file, indent=indent)
        print("保存成功: " + file.name)
