from lib.hack.forms import Group, StaticGroup, ModelInput, ModelAddrInput, ModelSelect, Choice, ModelCheckBox
from lib.ui.components import Pagination
from lib.win32.keys import VK
from tools.base.assembly_code import AssemblyGroup, Variable, Offset, Cmp
from tools.base.assembly_hacktool import (
    AssemblyHacktool, AssemblyItem, AssemblyItems, AssemblySwitch, VariableType, Delta
)
from . import assembly, datasets, models


class Main(AssemblyHacktool):
    CLASS_NAME = 'UnrealWindow'
    WINDOW_NAME = 'OCTOPATH TRAVELER '

    ITEMS_PAGE_LENGTH = 10
    ITEMS_PAGE_TOTAL = 20

    def __init__(self):
        super().__init__()
        self.base = models.Base(0, self.handler)
        self.battle_result = models.BattleResult(0, self.handler)
        self.base.main.items_offset = 0
        self.char_index = 0
        self.battle_character_index = 0
        self.battle_enemy_index = 0
        self.items_group = None

    def onattach(self):
        super().onattach()
        self.base.addr = self.handler.base_addr

    def render_main(self):
        character = (self._character, models.Character)
        battle_character = (self._battle_character, models.BattleCharacter)
        battle_enemy = (self._battle_enemy, models.BattleEnemy)
        battle_result = (self._battle_result, models.BattleResult)
        with Group(None, "全局", self.base):
            self.render_global()
        self.lazy_group(Group("character", "角色", character), self.render_character)
        self.lazy_group(Group("battle_character", "战斗中角色", battle_character), self.render_battle_character)
        self.lazy_group(Group("battle_enemy", "战斗中敌人", battle_enemy), self.render_battle_enemy)
        self.lazy_group(Group("battle_result", "战斗结果", battle_result), self.render_battle_result)
        self.items_group = Group("items", "物品", self.base)
        self.lazy_group(self.items_group, self.render_items)
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_buttons_own)
        self.lazy_group(StaticGroup("快捷键"), self.render_hotkeys)

    def render_global(self):
        ModelInput('main.money', '金钱')
        ModelInput('encounter')
        ModelCheckBox('no_encounter')

    def render_character(self):
        Choice("角色", datasets.CHARACTERS, self.on_character_change)
        ModelAddrInput()
        for name in models.Character.field_names:
            ModelInput(name)

    def render_battle_character(self):
        Choice("序号", range(5), self.on_battle_character_change)
        ModelAddrInput()
        for name in models.BattleCharacter.field_names:
            ModelInput(name)

    def render_battle_enemy(self):
        Choice("序号", range(5), self.on_battle_enemy)
        ModelAddrInput()
        for name in models.BattleEnemy.field_names:
            ModelInput(name)

    def render_battle_result(self):
        ModelAddrInput()
        for name in models.BattleResult.field_names:
            ModelInput(name)
        ModelInput('money_multi', '金钱倍数', instance=self.variable_model)
        ModelInput('exp_multi', '经验倍数', instance=self.variable_model)
        ModelInput('jp_multi', '技能点数倍数', instance=self.variable_model)

    def render_items(self):
        with ModelSelect.choices_cache:
            for i in range(10):
                ModelSelect("main.items.%d+items_offset.item" % i, "", choices=datasets.ITEMS)
                ModelInput("main.items.%d+items_offset.count" % i, "数量")
        with Group.active_group().footer:
            Pagination(self.on_items_page, self.ITEMS_PAGE_TOTAL)

    def render_assembly_buttons_own(self):
        self.render_assembly_buttons(assembly.ASSEMBLY_ITEMS)

    def render_hotkeys(self):
        # ui.Text("h: 血量满\n")
        pass

    def get_hotkeys(self):
        return (
            # (VK.MOD_ALT, VK.B, self.quick_health),
            (VK.MOD_ALT, VK.E, self.instant_encounter),
        )

    def _character(self):
        if self.handler.active:
            chars = self.base.main.chars
            return chars[self.char_index]

    def _battle_character(self):
        if self.handler.active:
            chars = self.base.battle.chars
            return chars[self.battle_character_index]

    def _battle_enemy(self):
        if self.handler.active:
            enemys = self.base.battle.enemys
            return enemys[self.battle_enemy_index].target

    def _battle_result(self):
        if self.handler.active:
            self.battle_result.addr = self.get_variable_value('br_ptr')
            return self.battle_result

    def on_character_change(self, lb):
        self.char_index = lb.index

    def on_battle_character_change(self, lb):
        self.battle_character_index = lb.index

    def on_battle_enemy(self, lb):
        self.battle_enemy_index = lb.index

    def on_items_page(self, page):
        self.base.main.items_offset = (page - 1) * self.ITEMS_PAGE_LENGTH
        self.items_group.read()

    def instant_encounter(self):
        """立即遇敌"""
        self.base.encounter = 1
