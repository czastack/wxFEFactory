from ..base import BaseNesHack
from lib.hack.forms import Group, StaticGroup, ModelInput, ModelSelect, Choice
from lib.win32.keys import VK
from fefactory_api import ui
from . import models, datasets


class Main(BaseNesHack):

    def __init__(self):
        super().__init__()
        self._global = models.Global(0, self.handler)
        self.person = models.Person(0, self.handler)
        self.equip_holder = models.EquipHolder(0, self.handler)

    def render_main(self):
        with Group("global", "全局", self._global):
            ModelInput("turn").set_help('0~1,下面会一直累加(慎用)')
            ModelInput("minutes")
            ModelInput("seconds_1")
            ModelInput("seconds_0")
            ModelInput("our_points")
            ModelInput("enemy_points")
            ModelInput("basketry_left_top")
            ModelInput("basketry_left_middle")
            ModelInput("basketry_left_bottom")
            ModelInput("basketry_right_top")
            ModelInput("basketry_right_middle")
            ModelInput("basketry_right_bottom")
            ModelInput("ball_owner").set_help('球在人手里(0~3),地上或空中(6)')

        with Group("player", "我方角色", self.person) as group:
            Choice("角色", ("1P", "2P", "3P", "4P"), self.on_person_change)

            # ModelInput("jump")
            # ModelInput("power")
            ModelInput("character").set_help('0~3')
            with ModelSelect.choices_cache:
                ModelSelect("equip_1", instance=self.equip_holder, choices=datasets.ITEMS)
                ModelSelect("equip_2", instance=self.equip_holder, choices=datasets.ITEMS)
                ModelSelect("equip_3", instance=self.equip_holder, choices=datasets.ITEMS)

        with StaticGroup("快捷键"):
            ui.Text("B: 获得球")
            ui.Text("N: 左边耐久置0")
            ui.Text("M: 球筐耐久恢复")

    def get_hotkeys(self):
        this = self.weak
        return (
            (0, VK.B, this.get_ball),
            (0, VK.N, this.basketry_zero),
            (0, VK.M, this.basketry_reset),
        )

    def on_person_change(self, lb):
        index = lb.index
        self.person.addr = index
        self.equip_holder.set_addr_by_index(index)

    def get_ball(self):
        self._global.ball_owner = 0

    def basketry_zero(self):
        self._global.basketry = 0x050006000800

    def basketry_reset(self):
        self._global.basketry = 0x050506060808
