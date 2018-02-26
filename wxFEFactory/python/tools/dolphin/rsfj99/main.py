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
            self.hp_view = ModelInputWidget("hp", "生命")
            self.max_hp_view = ModelInputWidget("max_hp", "最大生命")
