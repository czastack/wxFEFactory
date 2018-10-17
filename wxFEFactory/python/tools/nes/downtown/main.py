from ..base import BaseNesHack
from lib.hack.forms import Group, DialogGroup, StaticGroup, ModelInput, ModelSelect, Choice
from lib.win32.keys import VK
from lib import utils
from fefactory_api import ui
from . import models, datasets


class Main(BaseNesHack):

    def __init__(self):
        super().__init__()
        self._global = models.Global(0, self.handler)
        self.person = models.Person(0, self.handler)
        self.itemholder = models.ItemHolder(0, self.handler)

    def render_main(self):
        with Group("global", "全局", self._global):
            ModelInput("money_1p", "1p金钱")
            ModelInput("money_2p", "2p金钱")
            ModelSelect("scene", "场景", choices=datasets.SCENES)

        with Group("player", "我方角色", self.person, cols=4) as group:
            Choice("角色", ("1P", "2P"), self.on_person_change)

            for addr, name in models.PERSON_ATTRS:
                ModelInput(name)

        with group.footer:
            dialog_style = {'width': 1200, 'height': 900}
            with DialogGroup("items", "道具", self.itemholder, dialog_style=dialog_style) as dialog_group:
                for i in range(8):
                    ModelSelect("items.%d" % i, "道具%02d" % (i + 1), choices=datasets.ITEMS)

        with StaticGroup("快捷键"):
            ui.Text("恢复HP: alt+h")

    def get_hotkeys(self):
        this = self.weak
        return (
            (VK.MOD_ALT, VK.H, this.pull_through),
        )

    def on_person_change(self, lb):
        index = lb.index
        self.person.addr = index
        self.itemholder.addr = index * models.ItemHolder.SIZE

    def persons(self):
        person = models.Person(0, self.handler)
        for i in range(2):
            person.addr = i
            yield person

    def pull_through(self):
        for person in self.persons():
            person.set_with("生命上限", "生命")
