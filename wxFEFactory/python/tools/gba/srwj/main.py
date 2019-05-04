from lib.hack.forms import (
    Group, StaticGroup, ModelInput, ModelArrayInput, ModelSelect, ModelArraySelect,
    ModelFlagWidget, ModelCheckBox, Choice
)
from lib.win32.keys import VK
from lib.exui.components import Pagination
from fefactory_api import ui
from ..base import BaseGbaHack
from . import models, datasets


class Main(BaseGbaHack):

    def __init__(self):
        super().__init__()
        self._global = models.Global(0, self.handler)
        self.robot = models.Robot(models.Robot.START, self.handler)
        self.pilot = models.Pilot(models.Pilot.START, self.handler)

    def render_main(self):
        with Group("global", "全局", self._global):
            ModelInput("money")
            ModelInput("turn")
            ModelInput("after_money")
            ModelInput("after_exp")
            ModelSelect("chapter", choices=datasets.CHAPTERS)

        with Group("robot", "机体", self.robot, cols=4):
            self.render_robot()

        with Group("pilot", "机师", self.pilot, cols=4):
            self.render_pilot()

        with StaticGroup("功能"):
            self.render_functions(('all_intensified_parts', 'all_mini_games', 'all_skill_chip', 'all_move_10'))

    def render_robot(self):
        Choice("机体", datasets.ROBOT_CHOICES, self.on_robot_change)
        ModelInput("hp")
        ModelInput("en")
        ModelSelect("body", choices=datasets.ROBOTS)
        ModelSelect("pilot", choices=datasets.ROBOT_CHARACTERS)
        ModelArrayInput("body_remould")
        ModelArrayInput("ammo")
        ModelInput("weapon_remould")

    def render_pilot(self):
        Choice("角色", datasets.ROBOT_CHARACTERS, self.on_pilot_change)
        ModelSelect("pilot", choices=datasets.PILOT_CHARACTERS)
        ModelInput("exp")
        ModelInput("sp")
        ModelInput("killed")
        ui.Hr()
        ui.Hr()
        ModelFlagWidget("skill_1", labels=datasets.SKILLS_1, cols=2)
        ModelFlagWidget("skill_2", labels=datasets.SKILLS_2, cols=2)
        ModelCheckBox("skill_1_status")
        ModelCheckBox("skill_2_status")
        ModelInput("help_atk")
        ModelInput("help_def")
        ModelInput("energy")
        ModelInput("points")
        ModelArrayInput("develop")
        ModelArraySelect("skill_chip", choices=datasets.SHILL_CHIPS)

    def get_hotkeys(self):
        this = self.weak
        return (
            (VK.MOD_ALT, VK.R, this.move_again),
        )

    def on_robot_change(self, lb):
        self.robot.addr = models.Robot.START + models.Robot.SIZE * lb.index

    def on_pilot_change(self, lb):
        self.pilot.addr = models.Pilot.START + models.Pilot.SIZE * lb.index

    def all_intensified_parts(self, _):
        """全强化部件"""
        self._global.intensified_parts.fill(99)

    def all_mini_games(self, _):
        """全小游戏"""
        self._global.mini_games.fill(1)

    def all_skill_chip(self, _):
        """全技能芯片"""
        self._global.skill_chip.fill(99)

    def all_move_10(self, _):
        """全员十次移动次数"""
        addr = 0x0203424F
        for i in range(60):
            self.handler.write8(addr, 10)
            addr += 0x84

    def move_again(self):
        self.handler.write32(0x02034E2B, 10)
