from lib.hack.forms import (
    Group, StaticGroup, ModelInput, ModelAddrInput
)
from lib.hack.handlers import MemHandler
from lib.win32.keys import VK
from tools.base.assembly_code import AssemblyGroup, Variable, Offset, Cmp
from tools.base.assembly_hacktool import (
    AssemblyHacktool, AssemblyItem, AssemblyItems, AssemblySwitch, VariableType, Delta
)
from . import models


class Main(AssemblyHacktool):
    CLASS_NAME = 'UnrealWindow'
    WINDOW_NAME = 'Bloodstained: Ritual of the Night '
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
        ModelInput('money')
        ModelInput('exp')
        ModelInput('exp_mult', '多倍经验', instance=self.variable_model)

    def render_game(self):
        pass

    def render_player(self):
        ModelAddrInput()
        for name in models.Player.form_fields:
            ModelInput(name)

    def render_weapon(self):
        pass

    def render_assembly_buttons_own(self):
        delta = Delta(0x1000)
        self.render_assembly_buttons((
            AssemblyItem('inf_health_mp', '无限生命/MP依赖',
                '48 8B 49 28 48 85 C9 74 * 48 8B 89 E8 09 00 00', 0x874000, delta, b'',
                AssemblyGroup(
                    '48 89 0D', Offset('player_addr'),
                    Cmp('b_inf_health', 1),
                    '01 75 07 C7 41 38 0F 27 00 00',
                    Cmp('b_inf_mp', 1),
                    '01 75 07 C7 41 3C 0F 27 00 00 48 8B 49 28 48 85 C9'),
                args=(VariableType('player_addr', size=8), 'b_inf_health', 'b_inf_mp'),
                inserted=True, fuzzy=True, replace_len=7),
            AssemblySwitch('b_inf_health', '无限生命', depends=('inf_health_mp',)),
            AssemblySwitch('b_inf_mp', '无限MP', depends=('inf_health_mp',)),
            AssemblyItem('inf_item', '无限物品/子弹', '8B 43 48 3B C6 0F', 0x84D000, delta,
                b'', '8B 43 4C 83 F8 01 7E 0C 8B 43 48 39 F0 7E 05 8B 43 4C 31 F6 39 F0',
                inserted=True, replace_len=5),
            AssemblyItem('super_lucky', '超级幸运/掉宝率',
                'FF C8 66 0F 6E D0 0F 5B D2 F3 0F 59 D6 0F 28 74 24 20 F3 0F 58 96 E4 00 00 00',
                0x86d000, delta, b'', 'B8 9F 86 01 00 66 0F 6E D0', inserted=True, replace_len=6),
            AssemblyItem('money_exp_depends', '金钱/经验依赖', '44 8B C2 48 8B D9 48 85 C0', 0x88f000, delta, b'',
                AssemblyGroup(
                    Cmp('b_inf_money', 1),
                    '75 07 BA 7F 96 98 00 EB 15',
                    Cmp('exp_mult', 0),
                    '74 0C 83 FA 00 7E 07',
                    '0F AF 15', Offset('exp_mult', 7),
                    '44 8B C2 48 8B D9'),
                args=('b_inf_money', 'exp_mult'),
                inserted=True, replace_len=6),
            AssemblySwitch('b_inf_money', '无限金钱', depends=('money_exp_depends',)),
            AssemblyItems('无限二段跳',
                AssemblyItem('inf_jump_twice1', None, '48 89 54 24 10 53 48 83 EC 20 48 8B 99 18 02 00 00',
                    0x0083D000, 0x00E89000, 'B0 01 C3 90 90', replace_len=5),

                AssemblyItem('inf_jump_twice2', None, 'FF C8 89 81 E4 13 00 00',
                    0x007F4000, 0x00E87D00, '90 90', replace_len=2)),
            AssemblyItem('max_kill_count', '最高杀敌数', '8D 04 2B 89 87 DC 03 00 00', 0x8a6000, delta,
                b'', 'C7 87 DC 03 00 00 7F 96 98 00',
                inserted=True),
            AssemblyItem('one_hit_kill', '一击必杀', '8B 7B 38 8B CF', 0x866000, delta,
                b'', AssemblyGroup(
                    '83 FE 00 7E 14 48 BF',
                    Variable('player_addr'),
                    '48 39 1F 74 05 BE 3F 42 0F 00 8B 7B 38 8B CF'
                ),
                inserted=True, replace_len=5, depends=('inf_health_mp',)),
            AssemblyItems('重置游戏时间',
                AssemblyItem('reset_time1', None, 'F3 0F 58 87 68 02 00 00 F3 0F 11 87 68 02 00 00',
                    0x897357, 0x00E89000, '0F 57 C0 90 90 90 90 90', replace_len=8),

                AssemblyItem('reset_time2', None, '0F 2F C1 F3 0F 11 81 EC 05 00 00',
                    0x7ddfa6, 0x00E87D00, '0F 57 C0', replace_len=3)),
            AssemblyItem('show_whole_map', '显示全地图', '40 38 6C 18 58', 0x8fb000, delta,
                '0C 01 90 90 90'),
        ))

    def render_hotkeys(self):
        # ui.Text("h: 血量满\n")
        pass

    def get_hotkeys(self):
        return (
            # (VK.MOD_ALT, VK.B, self.quick_health),
        )
