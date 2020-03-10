from functools import partial
from lib import ui
from lib.hack.forms import (
    Group, StaticGroup, ModelInput, ModelAddrInput, ProxyInput, Title
)
from lib.hack.handlers import MemHandler
from lib.win32.keys import VK
from tools.base.assembly_code import AssemblyGroup, MemRead, Variable, Cmp, ORIGIN
from tools.base.assembly_hacktool import (
    AssemblyHacktool, AssemblyItem, AssemblyItems, AssemblySwitch, VariableType, Delta
)
from . import models


class Main(AssemblyHacktool):
    CLASS_NAME = 'HL_WIN'
    WINDOW_NAME = None
    key_hook = False

    def __init__(self):
        super().__init__()
        self.handler = MemHandler()
        # self.player = models.Player(self.variable_getter('player_ptr'), self.handler)
        self.hlhandle = models.HlHandle(0, self.handler)

    def onattach(self):
        super().onattach()
        self._libhl = self.handler.get_module('libhl.dll')
        self._hl_base = self.handler.ptrs_read(self._libhl + 0x00049184, (0x560, 4))
        self.hlhandle.addr = self._hl_base

    def render_main(self):
        hlhandle = self.hlhandle
        with Group(None, "全局"):
            self.render_global()
        self.lazy_group(Group("game", "游戏数据", (lambda: hlhandle.game, models.Game)), self.render_game)
        self.lazy_group(Group("progress", "统计", (lambda: hlhandle.progress, models.Progress)), self.render_progress)
        self.lazy_group(Group("player", "玩家", (lambda: hlhandle.player, models.Player)), self.render_player)
        self.lazy_group(Group("weapon", "武器", None), self.render_weapon)
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_buttons_own)
        self.lazy_group(StaticGroup("快捷键"), self.render_hotkeys)

    def render_global(self):
        Title('游戏版本: 1.7')
        ProxyInput('red_tier', '暴虐等级+', *self.assambly_patcher('red_tier', 2, 1, is_memory=True))
        ProxyInput('purple_tier', '战术等级+', *self.assambly_patcher('purple_tier', 2, 1, is_memory=True))
        ProxyInput('green_tier', '生存等级+', *self.assambly_patcher('green_tier', 2, 1, is_memory=True))

    def render_game(self):
        for name in models.Game.field_names:
            ModelInput(name)

    def render_progress(self):
        for name in models.Progress.field_names:
            ModelInput(name)

    def render_player(self):
        ModelAddrInput()
        for name in models.Player.form_fields:
            ModelInput(name)

    def render_weapon(self):
        hlhandle = self.hlhandle
        primary_weapon = (lambda: hlhandle.player.primary_weapon, models.Weapon)
        secondary_weapon = (lambda: hlhandle.player.secondary_weapon, models.Weapon)
        for label, instance in (('主武器', primary_weapon), ('副武器', secondary_weapon)):
            Title(label)
            ModelAddrInput(instance=instance)
            for name in models.Weapon.field_names:
                ModelInput(name, instance=instance)

        left_skill = (lambda: hlhandle.player.left_skill, models.Skill)
        right_skill = (lambda: hlhandle.player.right_skill, models.Skill)
        for label, instance in (('左技能', left_skill), ('右技能', right_skill)):
            Title(label)
            ModelAddrInput(instance=instance)
            for name in models.Skill.field_names:
                ModelInput(name, instance=instance)

    def render_assembly_buttons_own(self):
        find_start = 0x0C000000
        find_end = 0x1FFF0000

        tier_item = AssemblyItem(
            None, None, '89 45 F8 01 45 FC FF',
            find_start, find_end, b'', AssemblyGroup('83 C0 08', ORIGIN),
            inserted=True, replace_len=7, replace_offset=-7)

        self.render_assembly_buttons((
            # 1.7
            AssemblyItem('three_health', '三倍血', 'F2 0F 11 45 E8 B8 64 00 00 00 89 45 BC',
                         find_start, find_end, '2C 01', replace_offset=6, replace_len=2),
            AssemblyItem('double_money', '两倍钱', '89 45 F8 03 45 0C 89 45 F8 89 42 2C',
                         find_start, find_end, '03 45 0C', replace_len=3),
            AssemblyItem('quadruple_cell', '四倍细胞', '03 CA 89 4D F8 89 88 40 03 00 00',
                         find_start, find_end, b'', 'C1 E2 02 03 CA 89 4D F8',
                         replace_len=5, inserted=True),
            AssemblyItem('curse_quick', '诅咒快消', '89 88 C4 02 00 00 8B 90 C4 02 00 00',
                         find_start, find_end, b'', '83 E8 04 89 88 C4 02 00 00',
                         replace_len=6, inserted=True, help='五倍速度'),
            AssemblyItem('curse_clear', '诅咒消除', '89 88 C4 02 00 00 8B 90 C4 02 00 00',
                         find_start, find_end, b'', '31 C0 89 88 C4 02 00 00',
                         replace_len=6, inserted=True, help='至少击杀一名敌人(与诅咒快消互斥)'),
            AssemblyItem('player_ptr', '玩家地址', '8B 90 E8 00 00 00 89 55 F4 F2',
                         find_start, find_end, b'',
                         AssemblyGroup(
                             'A3',
                             Variable('player_ptr'),
                             Cmp('quick_health', 1),
                             '0F 85 0C 00 00 00 8B 88 EC 00 00 00 89 88 E8 00 00 00 8B 90 E8 00 00 00'
                         ),
                         args=('player_ptr', 'quick_health'), replace_len=6, inserted=True),
            AssemblySwitch('quick_health', '生命快速恢复'),
            AssemblyItem('inf_medicine', '无限药水', '89 88 10 03 00 00 33 D2',
                         find_start, find_end, b'', 'BA 10 00 00 00 89 90 10 03 00 00',
                         replace_len=6, inserted=True),
            AssemblyItem('inf_arrow', '无限弓箭', '89 48 18 8B 55 08 8B 42 08',
                         find_start, find_end, '8B 48 18 8B 55 08', replace_len=6),
            AssemblyItem('no_cd', '技能无冷却', 'F2 0F 11 6A 78 F2 0F 10 7A',
                         find_start, find_end, '0F 57 ED 90', replace_offset=-9, replace_len=4),
            AssemblyItem('no_injured', '敌人无伤害', '2B 85 6C FF FF FF 89 85 70 FF FF FF 8B 4D 08 * * * * * * 8B',
                         find_start, find_end, b'', AssemblyGroup(
                             '83 BD 6C FF FF FF 00 7E 1F 52 8B 55 08 3B 15', Variable(
                                 'player_ptr'),
                             '75 0E C7 85 6C FF FF FF 00 00 00 00 5A 2B 85 6C FF FF FF'),
                         replace_len=6, inserted=True, depends='player_ptr'),
            AssemblyItem('one_kill', '一击必杀', '89 81 E8 00 00 00 8B 55 08',
                         find_start, find_end, b'', AssemblyGroup(
                             '3B 0D', Variable('player_ptr'), '74 02 31 C0 89 82 E8 00 00 00'),
                         replace_len=6, inserted=True, depends='player_ptr'),
            AssemblyItem('inf_jump', '无限跳跃', '89 88 B0 02 00 00 33 D2',
                         find_start, find_end, '33 D2 89 90 B0 02 00 00'),
            AssemblyItem('time_reset', '时间重记', 'F2 0F 58 CB F2 0F 11 4D * F2 0F 11 4A 20',
                         find_start, find_end, '0F 57 C9 90', replace_len=4),
            AssemblyItem('time_pause', '时间暂停', 'F2 0F 58 CB F2 0F 11 4D * F2 0F 11 4A 20',
                         find_start, find_end, '90 90 90 90', replace_len=4),
            AssemblyItem('kill_keep', '无伤击杀数保持', '89 48 50 8B 55 08 8B 42 5C',
                         find_start, find_end, '90 90 90', replace_len=3),
            AssemblyItem('boss_kill', 'BOSS快速杀死', '8B 4D 08 89 81 E8 00 00 00 E9',
                         find_start, find_end, b'', '8B 4D 08 B8 00 00 00 00 89 81 E8 00 00 00',
                         inserted=True, replace_len=9),
            AssemblyItem('yellow_count', '金币数量', '03 45 0C 89 45 F8 89 42 2C',
                         find_start, find_end, b'', '89 45 F8 B8 3F 42 0F 00 89 42 2C',
                         replace_offset=3, replace_len=6, inserted=True, help='获得1次细胞后开启'),
            AssemblyItem('blue_count', '细胞数量', '89 4D F8 89 88 40 03 00 00',
                         find_start, find_end, b'', '89 4D F8 B9 7F 96 98 00 89 88 40 03 00 00',
                         replace_len=6, inserted=True, fuzzy=True, help='投资1次细胞后开启'),

            # 1.1:
            # AssemblyItem('three_health', '三倍血', 'F2 0F 11 45 E8 B8 64 00 00 00 89 45 BC',
            #              find_start, find_end, '2C 01', replace_offset=6, replace_len=2),
            # AssemblyItem('double_money', '两倍钱', '89 45 F8 03 45 0C 89 45 F8 89 42 34',
            #              find_start, find_end, '03 45 0C', replace_len=3),
            # AssemblyItem('quadruple_cell', '四倍细胞', '03 CA 89 4D F8 89 88 3C 03 00 00',
            #              find_start, find_end, b'', 'C1 E2 02 03 CA 89 4D F8',
            #              replace_len=5, inserted=True),
            # AssemblyItem('curse_quick', '诅咒快消', '89 82 C4 02 00 00 8B 8A C4 02 00 00',
            #              find_start, find_end, b'', '83 E8 04 89 82 C4 02 00 00',
            #              replace_len=6, inserted=True, help='五倍速度'),
            # AssemblyItem('curse_clear', '诅咒消除', '89 82 C4 02 00 00 8B 8A C4 02 00 00',
            #              find_start, find_end, b'', '31 C0 89 82 C4 02 00 00',
            #              replace_len=6, inserted=True, help='至少击杀一名敌人(与诅咒快消互斥)'),
            # AssemblyItem('player_ptr', '玩家地址', '8B 90 E8 00 00 00 89 55 F4 F2',
            #              find_start, find_end, b'',
            #              AssemblyGroup(
            #                  'A3',
            #                  Variable('player_ptr'),
            #                  Cmp('quick_health', 1),
            #                  '0F 85 0C 00 00 00 8B 88 EC 00 00 00 89 88 E8 00 00 00 8B 90 E8 00 00 00'
            #              ),
            #              args=('player_ptr', 'quick_health'), replace_len=6, inserted=True),
            # AssemblySwitch('quick_health', '生命快速恢复'),
            # AssemblyItem('inf_medicine', '无限药水', '89 88 10 03 00 00 33 C9',
            #              find_start, find_end, b'', 'B9 10 00 00 00 89 88 10 03 00 00',
            #              replace_len=6, inserted=True),
            # AssemblyItem('inf_arrow', '无限弓箭', '89 48 18 8B 55 08 8B 42 04',
            #              find_start, find_end, b'', 'B9 0A 00 00 00 89 48 18 8B 55 08',
            #              replace_len=6, inserted=True),
            # AssemblyItem('no_cd', '技能无冷却', 'F2 0F 11 59 78 F2 0F 10 69',
            #              find_start, find_end, '0F 57 DB 90', replace_offset=-9, replace_len=4),
            # AssemblyItem('no_injured', '敌人无伤害', '2B 8D 4C FF FF FF 89 8D 50',
            #              find_start, find_end, b'', AssemblyGroup(
            #                  '83 BD 4C FF FF FF 00 7E 17 52 8B 55 08 3B 15', Variable(
            #                      'player_ptr'),
            #                  '75 0A C7 85 4C FF FF FF 00 00 00 00 5A 2B 8D 4C FF FF FF'),
            #              replace_len=6, inserted=True, depends='player_ptr'),
            # AssemblyItem('one_kill', '一击必杀', '89 8A E8 00 00 00 8B 45 08',
            #              find_start, find_end, b'', AssemblyGroup(
            #                  '3B 15', Variable('player_ptr'), '74 02 31 C9 89 8A E8 00 00 00'),
            #              replace_len=6, inserted=True, depends='player_ptr'),
            # AssemblyItem('inf_jump', '无限跳跃', '89 88 B0 02 00 00 33 D2',
            #              find_start, find_end, '33 D2 89 90 B0 02 00 00'),
            # AssemblyItem('time_reset', '时间重记', '8B 4D E8 F2 0F 11 49 28',
            #              find_start, find_end, b'', '8B 4D E8 0F 57 C9 F2 0F 11 49 28', inserted=True),
            # AssemblyItem('time_pause', '时间暂停', 'F2 0F 11 49 28 8B 15',
            #              find_start, find_end, '90 90 90 90 90', replace_len=5),
            # AssemblyItem('kill_keep', '无伤击杀数保持', '89 48 50 8B 55 08 8B 42 48',
            #              find_start, find_end, '90 90 90', replace_len=3),
            # AssemblyItem('boss_kill', 'BOSS快速杀死', '8B 4D 08 89 81 E8 00 00 00 E9',
            #              find_start, find_end, b'', '8B 4D 08 B8 00 00 00 00 89 81 E8 00 00 00',
            #              inserted=True, replace_len=9),
            # AssemblyItem('yellow_count', '金币数量', '03 45 0C 89 45 F8 89 42 34',
            #              find_start, find_end, b'', '89 45 F8 B8 3F 42 0F 00 89 42 34',
            #              replace_offset=3, replace_len=6, inserted=True, help='获得1次细胞后开启 '),
            # AssemblyItem('blue_count', '细胞数量', '8B 91 3C 03 00 00 89 55 F4 B8**** 89',
            #              find_start, find_end, b'', 'C7 81 3C 03 00 00 36 42 0F 00 8B 91 3C 03 00 00',
            #              replace_len=6, inserted=True, fuzzy=True, help='投资1次细胞后开启'),
            tier_item.clone().set_data('red_tier', '暴虐等级+8', ordinal=3),
            tier_item.clone().set_data('purple_tier', '战术等级+8', ordinal=1),
            tier_item.clone().set_data('green_tier', '生存等级+8', ordinal=2),
        ))

    def render_hotkeys(self):
        ui.Text("h: 血量满\n")

    def get_hotkeys(self):
        return (
            (VK.MOD_ALT, VK.B, self.quick_health),
            (VK.MOD_ALT, VK.LEFT, self.move_left),
            (VK.MOD_ALT, VK.RIGHT, self.move_right),
            (VK.MOD_ALT, VK.UP, self.move_up),
            (VK.MOD_ALT, VK.DOWN, self.move_down),
        )

    def move_left(self):
        self.hlhandle.player.coord_x -= 5

    def move_right(self):
        self.hlhandle.player.coord_x += 5

    def move_up(self):
        self.hlhandle.player.coord_y -= 5

    def move_down(self):
        self.hlhandle.player.coord_y += 5

    def quick_health(self):
        self.toggle_assembly_button('quick_health')
