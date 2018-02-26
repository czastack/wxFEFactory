from ..base import BaseDolphinHack
from . import models
from lib.hack.form import Group, StaticGroup, InputWidget, CheckBoxWidget, ModelInputWidget


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
