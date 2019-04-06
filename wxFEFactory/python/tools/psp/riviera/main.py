from ..base import BasePspHack
from lib.hack.forms import Group, StaticGroup, ModelInput, ModelSelect, ModelFlagWidget, Choice
from lib.win32.keys import VK
from fefactory_api import ui
from . import models, datasets


class Main(BasePspHack):
    def __init__(self):
        super().__init__()
        self._global = models.Global(0, self.handler)
        # self.person = models.Person(0, self.handler)

    def render_main(self):
        # person = self.person
        with Group("global", "全局", self._global):
            ModelInput("tp", "TP")
