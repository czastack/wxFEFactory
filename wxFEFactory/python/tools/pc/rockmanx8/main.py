from functools import partial
from lib.hack.forms import Group, ModelCheckBox, ModelInput, ModelSelect
from lib.hack.handlers import MemHandler
from lib.win32.keys import VK
from tools.hacktool import BaseHackTool
from fefactory_api import ui
from . import models


class Main(BaseHackTool):
    CLASS_NAME = 'D3D Window'
    WINDOW_NAME = 'ROCKMANX8'

    def __init__(self):
        super().__init__()
        self.handler = MemHandler()
        self._global = models.Global(0, self.handler)

    def render_main(self):

        with Group("player", "角色", self._global, handler=self.handler):
            ModelCheckBox("x_invincible", "X无敌", enableData=0xFF, disableData=0)
            ModelCheckBox("zero_invincible", "ZEOR无敌", enableData=0xFF, disableData=0)
            ModelCheckBox("axl_invincible", "AXL无敌", enableData=0xFF, disableData=0)
            ModelInput("hp_axl", "AXL HP")
            ModelInput("hpmax_axl", "AXL最大HP")
            ModelInput("hp_x", "X HP")
            ModelInput("hpmax_x", "X最大HP")
            ModelInput("hp_zero", "ZERO HP")
            ModelInput("hpmax_zero", "ZERO最大HP")

        with Group("player", "全局", self._global, handler=self.handler):
            ModelInput("metal", "金属")
            ModelInput("resurgence", "复活晶片")
            ModelInput("joint_attack", "双人合击气槽")
            ModelCheckBox("zero_jump", "ZERO无限跳", enableData=0x02, disableData=0)
            ModelCheckBox("all_weapon", "解锁全部武器", enableData=0xFF, disableData=0)
            ModelCheckBox("super_x", "超级装甲X", enableData=0xFF, disableData=0)
            ModelCheckBox("back_zero_white_axl", "暗黑ZERO和坠天使AXL", enableData=0xFF, disableData=0)
            ModelCheckBox("ultimate_x", "终极装甲X", enableData=0xFF, disableData=0)

    def get_hotkeys(self):
        this = self.weak
        return (
            (VK.MOD_ALT, VK.H, this.pull_through),
        )

    def pull_through(self, _=None):
        _global = self._global
        _global.hp_axl = _global.hpmax_axl
        _global.hp_x = _global.hpmax_x
        _global.hp_zero = _global.hpmax_zero
