from functools import partial
from lib.hack.forms import (
    Group, StaticGroup, ProxyInput, ListFooterButtons
)
from lib.hack.handlers import MemHandler
from lib.hack.utils import Descriptor
from lib.win32.keys import VK
from tools.base.assembly_hacktool import AssemblyItem, AssemblyItems, VariableType
from tools.base.mono_hacktool import MonoHacktool, call_arg
from tools.base.assembly_code import AssemblyGroup, MemRead, Variable, ORIGIN
from fefactory_api import ui
from . import models, datasets


class Main(MonoHacktool):
    CLASS_NAME = 'UnityWndClass'
    WINDOW_NAME = 'Wizard of Legend'

    def __init__(self):
        super().__init__()
        self.controller = None

    def onattach(self):
        super().onattach()
        self.register_classes((
            models.NumVarStat,
            models.Health,
            models.Wallet,
            models.Player,
            models.GameController,
            models.Cooldown,
            models.CooldownEntry,
        ))

        self.controller = models.GameController(None, self)

    def render_main(self):
        with Group("player", "全局", None):
            self.render_global()
        self.lazy_group(StaticGroup("技能"), self.render_skills)
        self.lazy_group(StaticGroup("符文"), self.render_items)
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_functions)
        self.lazy_group(StaticGroup("快捷键"), self.render_hotkeys)

    def render_global(self):
        ui.Hr()
        ui.Text('游戏版本: v1.1')
        ProxyInput("CurrentHealthValue", "生命",
            *Descriptor(lambda: self.activePlayer.health, "CurrentHealthValue"))
        ProxyInput("CurrentHealthValue", "生命上限",
            *Descriptor(lambda: self.activePlayer.health.healthStat, "ModifiedValue"))
        ProxyInput("CurrentShieldValue", "护盾",
            *Descriptor(lambda: self.activePlayer.health, "CurrentShieldValue"))
        ProxyInput("CurrentShieldValue", "护盾上限",
            *Descriptor(lambda: self.activePlayer.health.shieldStat, "ModifiedValue"))
        ProxyInput("CurrentGuardCountValue", "防御次数",
            *Descriptor(lambda: self.activePlayer.health, "CurrentGuardCountValue"))
        ProxyInput("CurrentGuardCountValue", "防御次数上限",
            *Descriptor(lambda: self.activePlayer.health.guardCountStat, "ModifiedValue"))
        ProxyInput("balance", "宝石", *Descriptor(lambda: self.activePlayer.platWallet, "balance"))
        ProxyInput("balance", "金币", *Descriptor(lambda: self.activePlayer.goldWallet, "balance"))

    def render_skills(self):
        """渲染技能列表"""
        li = self.skill_listview = ui.ListView(className="fill")
        li.enableCheckboxes()
        li.appendColumns(("名称", "授权", "描述"), (260, 400, 800))
        li.insertItems((item[1:] for item in datasets.skills_info))

        with ui.Horizontal(className="expand padding_top"):
            ListFooterButtons(li)
            ui.Button(label="解锁所选", className="button", onclick=self.unlock_checked_skills)
            ui.Button(label="捡起当前", className="button", onclick=self.pickup_selected_skill)

    def render_items(self):
        """渲染符文列表"""
        li = self.item_listview = ui.ListView(className="fill")
        li.enableCheckboxes()
        li.appendColumns(("名称", "描述"), (260, 1000))
        li.insertItems((item[1:] for item in datasets.items_info))

        with ui.Horizontal(className="expand padding_top"):
            ListFooterButtons(li)
            ui.Button(label="给予所选", className="button", onclick=self.give_checked_items)

    def render_assembly_functions(self):
        Cooldown = models.Cooldown
        if not Cooldown.get_ChargesMissing.mono_compile:
            print('需要先加载游戏')
            return False

        super().render_assembly_functions((
            AssemblyItems('无冷却',
                AssemblyItem('no_cooldown', None, b'\x48???\x2B\xC1',
                    Cooldown.get_ChargesMissing.mono_compile,
                    Cooldown.get_ChargesMissing.mono_compile + 0x2d,
                    b'', AssemblyGroup(b'\x89\x46', MemRead(offset=3, size=1), ORIGIN),
                    inserted=True, find_base=False, fuzzy=True),
                AssemblyItem('no_cooldown2', None, b'\x40\x0F\x94\xC0\x48\x0F\xB6\xC0',
                    Cooldown.get_IsCharging.mono_compile,
                    Cooldown.get_IsCharging.mono_compile + 0x58,
                    b'\x90\x90\x30', find_base=False, replace_len=3)),
            AssemblyItem('enhanced_magic_4', '技能连发', b'\x48\x83\xEC\x20\x48\x8B??????????\x48\x83\xC4\x20\x4C\x8B\xC0',
                models.CooldownEntry.EntryUpdate.mono_compile,
                models.CooldownEntry.EntryUpdate.mono_compile + 0x141,
                b'', AssemblyGroup(
                    b'\x53\x50',
                    MemRead(offset=4, size=3),
                    b'\x48\x8B\x80',
                    MemRead(offset=0xC, size=4),
                    b'\x48\xBB',
                    Variable('cSkillStateGetIsEmpowered'),
                    b'\x48\x8B\x1B\x48\x85\xDB\x75\x39\x80\x38\xE8\x74\x65\x80\x38\x55\x75\x60\x48\xBB',
                    Variable('cSkillStateGetIsEmpowered'),
                    b'\x48\x89\x03\xFF\x30\x8F\x43\x08\xFF\x70\x08\x8F\x43\x10\x48\xBB\x48\xB8\x01\x00\x00\x00\x00\x00'
                    b'\x48\x89\x18\xBB\x00\x00\xC3\x90\x89\x58\x08\xEB\x31\x48\xBB',
                    Variable('bEnhancedMagicScriptState'),
                    b'\x80\x3B\x01\x7C\x22\x48\xBB',
                    Variable('cSkillStateGetIsEmpowered'),
                    b'\xFF\x73\x08\x8F\x00\xFF\x73\x10\x8F\x40\x08\x48\xBB',
                    Variable('bEnhancedMagicScriptState'),
                    b'\xC6\x03\x02\x58\x5B',
                    ORIGIN,
                ),
                inserted=True, find_base=False, fuzzy=True, replace_len=7,
                args=(
                    VariableType('cSkillStateGetIsEmpowered', size=0x28),
                    VariableType('bEnhancedMagicScriptState', size=8),
                )),
        ))

    def render_hotkeys(self):
        ui.Text("Capslock: 大招槽满\n"
            "h: 血量满\n")

    def get_hotkeys(self):
        return (
            (0, VK.CAPSLOCK, self.overdrive),
            (0, VK.H, self.recovery),
        )

    @property
    def activePlayer(self):
        return self.controller and self.controller.activePlayers[0]

    def recovery(self):
        """恢复健康"""
        player = self.activePlayer
        if player:
            health = player.health
            health.CurrentHealthValue = health.healthStat.ModifiedValue

    def overdrive(self):
        """大招槽满"""
        player = self.activePlayer
        if player:
            player.OverdriveProgress = 100.0

    def GetSkill(self, skill):
        """获取技能"""
        return self.activePlayer.GetSkill(self.call_mono_string_new(skill))

    def HandleSkillUnlock(self, skill):
        """技能解锁"""
        self.activePlayer.HandleSkillUnlock(self.call_mono_string_new(skill), True)

    def HandleSkillsUnlock(self, skills):
        """解锁多个技能"""
        player = self.activePlayer
        args = tuple(
            player.__class__.HandleSkillUnlock.op_runtime_invoke(player, (self.call_mono_string_new(skill), True))
            for skill in skills
        )
        self.mono_security_call_reuse(args)

    def PickUpSkill(self, skill):
        """捡起技能，原有技能会掉出"""
        self.activePlayer.PickUpSkill(self.call_mono_string_new(skill), True, True)

    def GiveItem(self, item):
        """给予物品"""
        self.activePlayer.GiveDesignatedItem(self.call_mono_string_new(item))

    def GiveItems(self, items):
        """给予物品"""
        player = self.activePlayer
        args = tuple(
            player.__class__.GiveDesignatedItem.op_runtime_invoke(player, (self.call_mono_string_new(item),))
            for item in items
        )
        self.mono_security_call_reuse(args)

    def unlock_checked_skills(self, _):
        """解锁所选技能"""
        skills = (datasets.skills_info[i][0] for i in self.skill_listview.getCheckedList())
        self.HandleSkillsUnlock(skills)

    def pickup_selected_skill(self, _):
        """捡起当前第一个高亮选中的技能"""
        indexs = self.skill_listview.getSelectedList()
        if indexs:
            index = indexs[0]
            self.PickUpSkill(datasets.skills_info[index][0])
            if len(indexs) > 1:
                print('选中了多个技能，但只生效第一个')

    def give_checked_items(self, _):
        """给予所选物品"""
        items = (datasets.items_info[i][0] for i in self.item_listview.getCheckedList())
        self.GiveItems(items)
