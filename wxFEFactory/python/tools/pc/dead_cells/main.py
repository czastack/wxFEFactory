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
        Title('游戏版本: 1.1')
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
        for label, instance in (
            ('主武器', primary_weapon),
            ('副武器', secondary_weapon)
        ):
            Title(label)
            ModelAddrInput(instance=instance)
            for name in models.Weapon.field_names:
                ModelInput(name, instance=instance)

        left_skill = (lambda: hlhandle.player.left_skill, models.Skill)
        right_skill = (lambda: hlhandle.player.right_skill, models.Skill)
        for label, instance in (
            ('左技能', left_skill),
            ('右技能', right_skill)
        ):
            Title(label)
            ModelAddrInput(instance=instance)
            for name in models.Skill.field_names:
                ModelInput(name, instance=instance)

    def render_assembly_buttons_own(self):
        tier_item = AssemblyItem(
            None, None, b'\x89\x45\xF8\x01\x45\xFC\xFF',
            0x0C000000, 0x0FFF0000, b'', AssemblyGroup(b'\x83\xC0\x08', ORIGIN),
            inserted=True, replace_len=7, replace_offset=-7)

        self.render_assembly_buttons((
            AssemblyItem('three_health', '三倍血', b'\xF2\x0F\x11\x45\xE8\xB8\x64\x00\x00\x00\x89\x45\xBC',
                0x0C000000, 0x0FFF0000, b'\x2C\x01', replace_offset=6, replace_len=2),
            AssemblyItem('double_money', '两倍钱', b'\x89\x45\xF8\x03\x45\x0C\x89\x45\xF8\x89\x42\x34',
                0x0C000000, 0x0FFF0000, b'\x03\x45\x0C', replace_len=3),
            AssemblyItem('quadruple_cell', '四倍细胞', b'\x03\xCA\x89\x4D\xF8\x89\x88\x3C\x03\x00\x00',
                0x0C000000, 0x0FFF0000, b'', b'\xC1\xE2\x02\x03\xCA\x89\x4D\xF8',
                replace_len=5, inserted=True),
            AssemblyItem('curse_quick', '诅咒快消', b'\x89\x82\xC4\x02\x00\x00\x8B\x8A\xC4\x02\x00\x00',
                0x0C000000, 0x0FFF0000, b'', b'\x83\xE8\x04\x89\x82\xC4\x02\x00\x00',
                replace_len=6, inserted=True, help='五倍速度'),
            AssemblyItem('curse_clear', '诅咒消除', b'\x89\x82\xC4\x02\x00\x00\x8B',
                0x0C000000, 0x0FFF0000, b'', b'\x31\xC0\x89\x82\xC4\x02\x00\x00',
                replace_len=6, inserted=True, help='至少击杀一名敌人(与诅咒快消互斥)'),
            AssemblyItem('player_ptr', '玩家地址', b'\x8B\x90\xE8\x00\x00\x00\x89\x55\xF4\xF2',
                0x0C000000, 0x0FFF0000, b'',
                AssemblyGroup(
                    b'\xA3',
                    Variable('player_ptr'),
                    Cmp('quick_health', 1),
                    b'\x0F\x85\x0C\x00\x00\x00\x8B\x88\xEC\x00\x00\x00\x89\x88\xE8\x00\x00\x00\x8B\x90\xE8\x00\x00\x00'
                ),
                args=('player_ptr', 'quick_health'), replace_len=6, inserted=True),
            AssemblySwitch('quick_health', '生命快速恢复'),
            AssemblyItem('inf_medicine', '无限药水', b'\x89\x88\x10\x03\x00\x00\x33\xC9',
                0x0C000000, 0x0FFF0000, b'', b'\xB9\x10\x00\x00\x00\x89\x88\x10\x03\x00\x00',
                replace_len=6, inserted=True),
            AssemblyItem('inf_arrow', '无限弓箭', b'\x89\x48\x18\x8B\x55\x08\x8B\x42\x04',
                0x0C000000, 0x0FFF0000, b'', b'\xB9\x0A\x00\x00\x00\x89\x48\x18\x8B\x55\x08',
                replace_len=6, inserted=True),
            AssemblyItem('no_cd', '技能无冷却', b'\xF2\x0F\x11\x59\x78\xF2\x0F\x10\x69',
                0x0C000000, 0x0FFF0000, b'\x0F\x57\xDB\x90', replace_offset=-9, replace_len=4),
            AssemblyItem('no_injured', '敌人无伤害', b'\x2B\x8D\x4C\xFF\xFF\xFF\x89\x8D\x50',
                0x0C000000, 0x0FFF0000, b'', AssemblyGroup(
                    b'\x83\xBD\x4C\xFF\xFF\xFF\x00\x7E\x17\x52\x8B\x55\x08\x3B\x15', Variable('player_ptr'),
                    b'\x75\x0A\xC7\x85\x4C\xFF\xFF\xFF\x00\x00\x00\x00\x5A\x2B\x8D\x4C\xFF\xFF\xFF'),
                replace_len=6, inserted=True, depends='player_ptr'),
            AssemblyItem('one_kill', '一击必杀', b'\x89\x8A\xE8\x00\x00\x00\x8B\x45\x08',
                0x0C000000, 0x0FFF0000, b'', AssemblyGroup(
                    b'\x3B\x15', Variable('player_ptr'), b'\x74\x02\x31\xC9\x89\x8A\xE8\x00\x00\x00'),
                replace_len=6, inserted=True, depends='player_ptr'),
            AssemblyItem('inf_jump', '无限跳跃', b'\x89\x88\xB0\x02\x00\x00\x33\xD2',
                0x0C000000, 0x0FFF0000, b'\x33\xD2\x89\x90\xB0\x02\x00\x00'),
            AssemblyItem('time_reset', '时间重记', b'\x8B\x4D\xE8\xF2\x0F\x11\x49\x28',
                0x0C000000, 0x0FFF0000, b'', b'\x8B\x4D\xE8\x0F\x57\xC9\xF2\x0F\x11\x49\x28', inserted=True),
            AssemblyItem('time_pause', '时间暂停', b'\xF2\x0F\x11\x49\x28\x8B\x15',
                0x0C000000, 0x0FFF0000, b'\x90\x90\x90\x90\x90', replace_len=5),
            AssemblyItem('kill_keep', '无伤击杀数保持', b'\x89\x48\x50\x8B\x55\x08\x8B\x42\x48',
                0x0C000000, 0x0FFF0000, b'\x90\x90\x90', replace_len=3),
            AssemblyItem('boss_kill', 'BOSS快速杀死', b'\x8B\x4D\x08\x89\x81\xE8\x00\x00\x00\xE9',
                0x0C000FF0, 0x0FFF0000, b'', b'\x8B\x4D\x08\xB8\x00\x00\x00\x00\x89\x81\xE8\x00\x00\x00',
                inserted=True, replace_len=9),
            AssemblyItem('yellow_count', '金币数量', b'\x03\x45\x0C\x89\x45\xF8\x89\x42\x34',
                0x0C000000, 0x0FFF0000, b'', b'\x89\x45\xF8\xB8\x3F\x42\x0F\x00\x89\x42\x34',
                replace_offset=3, replace_len=6, inserted=True, help='获得1次细胞后开启 '),
            AssemblyItem('blue_count', '细胞数量', b'\x8B\x91\x3C\x03\x00\x00\x89\x55\xF4\xB8????\x89',
                0x0D000000, 0x0FFF0000, b'', b'\xC7\x81\x3C\x03\x00\x00\x36\x42\x0F\x00\x8B\x91\x3C\x03\x00\x00',
                replace_len=6, inserted=True, fuzzy=True, help='投资1次细胞后开启'),
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
