from lib.basescene import BaseScene
from lib.lazy import lazyclassmethod
from . import tools

class BaseTool(BaseScene):

    def render(self):
        """
        渲染视图，供attach调用
        :return: 返回根元素
        """
        pass

    @lazyclassmethod
    def doGetTitle(class_):
        """获取原始标题，显示在标签页标题和菜单栏"""
        name = class_.getName()
        for item in tools:
            if item[1] == name:
                return item[0]
        return name

    @lazyclassmethod
    def getName(class_):
        """模块名称，即模块文件夹名"""
        return class_.__module__.split('.')[1]