from lib import ui
from lib.hack.forms import (
    Group, StaticGroup, ModelInput, ModelAddrInput, Title
)
from lib.hack.handlers import MemHandler
from tools.base.assembly_hacktool import AssemblyHacktool
from . import assembly, models


class Main(AssemblyHacktool):
    CLASS_NAME = 'NieR:Automata_MainWindow'
    WINDOW_NAME = 'NieR:Automata'
    key_hook = False

    def __init__(self):
        super().__init__()
        self.handler = MemHandler()
        self.game = models.Game(0, self.handler)

    def onattach(self):
        super().onattach()
        self.game.addr = self.handler.base_addr

    def render_main(self):
        with Group(None, "全局", self.game):
            self.render_global()
        # self.lazy_group(Group("player", "玩家", None), self.render_player)
        # self.lazy_group(Group("weapon", "武器", None), self.render_weapon)
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_buttons_own)
        self.lazy_group(StaticGroup("快捷键"), self.render_hotkeys)

    def render_global(self):
        Title('游戏版本: 1.1')
        ModelInput('money')
        ModelInput('exp')
        ModelInput('exp_mult', '多倍经验', instance=self.variable_model)

    # def render_game(self):
    #     for name in models.Game.field_names:
    #         ModelInput(name)

    # def render_player(self):
    #     ModelAddrInput()
    #     for name in models.Player.field_names:
    #         ModelInput(name)

    def render_weapon(self):
        pass

    def render_assembly_buttons_own(self):
        self.render_assembly_buttons(assembly.ASSEMBLY_ITEMS)

    def render_hotkeys(self):
        ui.Text("h: 血量满\n")

    def get_hotkeys(self):
        return (
            # (VK.MOD_ALT, VK.B, self.quick_health),
        )

    def quick_health(self):
        self.toggle_assembly_function('quick_health')
