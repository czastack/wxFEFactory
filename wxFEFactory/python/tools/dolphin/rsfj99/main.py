from ..base import BaseDolphinHack
from . import models
from lib.hack.form import Group, StaticGroup, InputWidget, CheckBoxWidget, ModelInputWidget
import fefactory_api
ui = fefactory_api.ui


class Tool(BaseDolphinHack):

    def __init__(self):
        super().__init__()
        self._ram = models.Ram(0, self.handler)

    def check_attach(self, _=None):
        if super().check_attach():
            self._ram.addr = self.ramaddr
            return True
        return False
    
    def render_main(self):
        with Group("player", "角色", self._ram, handler=self.handler):
            ModelInputWidget("level", "等级(1+)")
            ModelInputWidget("hp", "生命")
            ModelInputWidget("max_hp", "最大生命")
            ModelInputWidget("money", "金钱")
            ModelInputWidget("power", "力")
            ModelInputWidget("stamina", "体力")
            ModelInputWidget("energy", "气力")
            ModelInputWidget("soul", "魂")
            ModelInputWidget("exp", "经验")

        with StaticGroup("刀"):
            li = ui.ListView(className="fill")
            li.enableCheckboxes()
            li.appendColumns(('姓名', '编号', 'R键说明'), (300, 150, 200))
            li.insertItems([('艾希', '01', '少女'), ('赛思', 12, '圣骑士'), ('赛思', 12, '圣骑士')])
            # li.insertItems([('艾希', '01', '少女')], 1, False)
            li.setOnItemSelected({'arg_event': True, 'callback': self.onListSelect})


    def onListSelect(self, view, event):
        index = event.index
        view.checkItem(index, not view.isItemChecked(index))