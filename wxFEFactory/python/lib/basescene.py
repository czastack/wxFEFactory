from lib.extypes import WeakBinder


class BaseScene:
    # 这些方法可以在实例中用self访问
    from fefactory_api import alert, confirm, confirm_yes, YES, NO, CANCEL, longtext_dialog
    alert = staticmethod(alert)
    confirm = staticmethod(confirm)
    confirm_yes = staticmethod(confirm_yes)
    longtext_dialog = staticmethod(longtext_dialog)

    def __init__(self):
        # 同一类实例列表
        ins = self.__class__.__dict__.get('INS', None)
        if ins is None:
            ins = self.__class__.INS = []
        
        try:
            self.index = ins.index(None)
            ins[self.index] = self
        except ValueError:
            self.index = len(ins)
            ins.append(self)
        self.weak = WeakBinder(self)

    def onClose(self, _=None):
        ins = self.__class__.INS
        ins[ins.index(self)] = None

        i = len(ins)
        while i:
            i -= 1
            if ins[i] is None:
                ins.pop()
            else:
                break

    def getTitle(self):
        """
        获取标题，显示在标签页标题和菜单栏
        如果打开了多个实例，会在标题后添加序号
        """
        title = self.doGetTitle()
        if self.index is not 0:
            title += str(self.index + 1)
        return title