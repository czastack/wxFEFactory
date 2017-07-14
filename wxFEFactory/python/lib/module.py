from mainframe import win


class BaseModule:
    menu = None
    INS = None

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

    def readFrom(self):
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
