from lib.hack.forms import Group, DialogGroup, StaticGroup, ModelInput, ModelSelect, Choice
from lib.win32.keys import VK
from lib import ui, utils
from ..base import BaseNesHack
from . import models, datasets


class Main(BaseNesHack):

    def __init__(self):
        super().__init__()
        self._global = models.Global(0, self.handler)
        self.character = models.Character(0, self.handler)
        self.itemholder = models.ItemHolder(0, self.handler)

    def render_main(self):
        with Group("global", "全局", self._global):
            ModelInput("money_1p", "1p金钱")
            ModelInput("money_2p", "2p金钱")
            ModelSelect("scene", "场景", choices=datasets.SCENES)

        with Group("player", "我方角色", self.character, cols=4) as group:
            Choice("角色", ("1P", "2P"), self.on_character_change)

            for addr, name in models.PERSON_ATTRS:
                ModelInput(name)

        with group.footer:
            dialog_style = {'width': 1200, 'height': 900}
            with DialogGroup("items", "道具", self.itemholder, dialog_style=dialog_style) as dialog_group:
                with ModelSelect.choices_cache:
                    for i in range(8):
                        ModelSelect("items.%d" % i, "道具%02d" % (i + 1), choices=datasets.ITEMS)

        with StaticGroup("快捷键"):
            ui.Text("恢复HP: alt+h")

    def get_hotkeys(self):
        this = self.weak
        return (
            (VK.MOD_ALT, VK.H, this.pull_through),
        )

    def on_character_change(self, lb):
        index = lb.index
        self.character.addr = index
        self.itemholder.addr = index * models.ItemHolder.SIZE

    def characters(self):
        character = models.Character(0, self.handler)
        for i in range(2):
            character.addr = i
            yield character

    def pull_through(self):
        for character in self.characters():
            character.set_with("生命上限", "生命")
