from functools import partial
from lib.hack.forms import (
    Group, StaticGroup, ProxyInput, ListFooterButtons
)
from lib.hack.handlers import MemHandler
from lib.hack.utils import Descriptor
from lib.win32.keys import VK
from tools.base.assembly_hacktool import AssemblyItem, AssemblyItems, VariableType, Delta
from tools.base.mono_hacktool import MonoHacktool, call_arg
from tools.base.assembly_code import AssemblyGroup, MemRead, Variable, ORIGIN
from fefactory_api import ui
from . import models, datasets


class Main(MonoHacktool):
    CLASS_NAME = 'UnityWndClass'
    WINDOW_NAME = 'Wizard of Legend'

    def __init__(self):
        super().__init__()
        self.GameController = None

    def onattach(self):
        super().onattach()
        self.register_classes((
            models.NumVarStat,
            models.Health,
            models.Wallet,
            models.PlatWallet,
            models.GoldWallet,
            models.Player,
            models.GameController,
            models.Cooldown,
            models.CooldownEntry,
            models.Item,
            models.SkillState,
            models.MeleeAttackState,
        ))

        self.GameController = models.GameController(0, self)
        self.Item = models.Item(0, self)

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
        ProxyInput("overdriveMinValue", "必杀槽最小值", *Descriptor(lambda: self.activePlayer, "overdriveMinValue"))
        ProxyInput("overdriveBuildDecayRate", "必杀槽未满衰减",
            *Descriptor(lambda: self.activePlayer.overdriveBuildDecayRate, "ModifiedValue"))
        ProxyInput("overdriveActiveDecayRate", "必杀槽满后衰减",
            *Descriptor(lambda: self.activePlayer.overdriveActiveDecayRate, "ModifiedValue"))

    def render_skills(self):
        """渲染技能列表"""
        li = self.skill_listview = ui.ListView(class_="fill")
        li.enableCheckboxes()
        li.appendColumns(("名称", "加强", "描述"), (260, 400, 800))
        li.insertItems((item[1:] for item in datasets.skills_info))

        with ui.Horizontal(class_="expand padding_top"):
            ListFooterButtons(li)
            ui.Button(label="解锁所选", class_="button", onclick=self.unlock_checked_skills)
            ui.Button(label="捡起高亮", class_="button", onclick=self.pickup_selected_skill)

    def render_items(self):
        """渲染符文列表"""
        li = self.item_listview = ui.ListView(class_="fill")
        li.enableCheckboxes()
        li.appendColumns(("名称", "描述"), (260, 1000))
        li.insertItems((item[1:] for item in datasets.items_info))

        with ui.Horizontal(class_="expand padding_top"):
            ListFooterButtons(li)
            ui.Button(label="给予所选", class_="button", onclick=self.give_checked_items)
            ui.Button(label="给予高亮", class_="button", onclick=self.give_selected_items)

    def render_assembly_functions(self):
        Cooldown = models.Cooldown
        if not Cooldown.get_ChargesMissing.mono_compile:
            print('需要先加载游戏')
            return False

        super().render_assembly_functions((
            AssemblyItems('无冷却',
                AssemblyItem('no_cooldown', None, b'\x48???\x2B\xC1',
                    Cooldown.get_ChargesMissing.mono_compile, Delta(0x2d), b'',
                    AssemblyGroup(b'\x89\x46', MemRead(offset=3, size=1), ORIGIN),
                    inserted=True, find_base=False, fuzzy=True),
                AssemblyItem('no_cooldown2', None, b'\x40\x0F\x94\xC0\x48\x0F\xB6\xC0',
                    Cooldown.get_IsCharging.mono_compile, Delta(0x58),
                    b'\x90\x90\x30', find_base=False, replace_len=3)),
            AssemblyItem('basic_continue', '连续平A', b'\x40\x0F\x94\xC0\x48\x0F\xB6\xC0',
                models.MeleeAttackState.HandleSelfTransition.mono_compile, Delta(0xf0),
                b'\x48\x31\xC0\x48\xFF\xC0', find_base=False),
            AssemblyItem('double_plat', '双倍宝石', b'\xBA\x07\x00\x00\x00',
                models.PlatWallet.Deposit.mono_compile, Delta(0x5d), b'',
                AssemblyGroup(b'\x48\x01\xf6', ORIGIN),
                inserted=True, find_base=False),
            AssemblyItem('double_gold', '双倍金币', b'\xBA\x01\x00\x00\x00',
                models.GoldWallet.Deposit.mono_compile, Delta(0x5d), b'',
                AssemblyGroup(b'\x48\x01\xf6', ORIGIN),
                inserted=True, find_base=False),
            AssemblyItem('skill_empowered', '技能增强', b'\xFF\x90\xE0\x00\x00\x00',
                models.SkillState.get_IsEmpowered.mono_compile, Delta(0x2b),
                b'\x48\x31\xC0\x48\xFF\xC0', find_base=False),
        ))

    def render_hotkeys(self):
        ui.Text("Capslock: 必杀槽满\n"
            "h: 血量满\n")

    def get_hotkeys(self):
        return (
            (0, VK.CAPSLOCK, self.overdrive),
            (0, VK.H, self.recovery),
        )

    @property
    def activePlayer(self):
        """当前玩家"""
        return self.GameController and self.GameController.activePlayers[0]

    def recovery(self):
        """恢复健康"""
        player = self.activePlayer
        if player:
            health = player.health
            health.CurrentHealthValue = health.healthStat.ModifiedValue

    def overdrive(self):
        """必杀槽满"""
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

    def ItemIsUnlocked(self, item, set=True):
        """设置或查询符文解锁情况"""
        return self.Item.IsUnlocked(self.call_mono_string_new(item), set)

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

    def give_selected_items(self, _):
        """给予高亮选中物品"""
        items = (datasets.items_info[i][0] for i in self.item_listview.getSelectedList())
        self.GiveItems(items)
