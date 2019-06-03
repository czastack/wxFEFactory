from lib.hack.forms import (
    Group, StaticGroup, ProxyInput
)
from lib.hack.handlers import MemHandler
from lib.hack.utils import Descriptor
from lib.win32.keys import VK
from tools.base.assembly_hacktool import AssemblyItem, AssemblyItems, VariableType
from tools.base.mono_hacktool import MonoHacktool, call_arg
from tools.base.mono_models import MonoClass, MonoField, MonoStaticField, MonoArrayT, MonoProperty, MonoMethod
from tools.base.assembly_code import AssemblyGroup, MemRead, Variable, ORIGIN
from fefactory_api import ui
# from . import models, datasets


class NumVarStat(MonoClass):
    """数值"""
    CurrentValue = MonoProperty(type=float)  # 当前值
    ModifiedValue = MonoProperty(type=float)  # 最大值


class Health(MonoClass):
    # 生命值相关
    CurrentHealthValue = MonoProperty()  # 生命
    CurrentShieldValue = MonoProperty()  # 护盾
    CurrentGuardCountValue = MonoProperty()  # 防御次数

    healthStat = MonoField(type=NumVarStat)
    shieldStat = MonoField(type=NumVarStat)
    guardCountStat = MonoField(type=NumVarStat)


class Wallet(MonoClass):
    """钱包"""
    balance = MonoField(label="余额")
    maxBalance = MonoField(label="最大值")
    # 存入
    Deposit = MonoMethod(param_count=1, compile=True)


class Player(MonoClass):
    # 玩家
    need_vtable = True
    OverdriveProgress = MonoProperty(type=float)
    health = MonoField(type=Health)
    goldWallet = MonoStaticField(type=Wallet)
    platWallet = MonoStaticField(type=Wallet)

    # void AssignSkillSlot(int skillSlotNum, string skillID, bool setSignature = false, bool signatureStatus = false)
    # AssignSkillSlot = MonoMethod(param_count=4, signature='iP2B')
    # Player.SkillState GetSkill(string ID)
    GetSkill = MonoMethod(param_count=1, signature='P', type=MonoClass)
    # void PickUpSkill(string givenID, bool isSignature = false, bool isEmpowered = false)
    PickUpSkill = MonoMethod(param_count=3, signature='P2B')
    # void GiveDesignatedItem(string givenID = "")
    GiveDesignatedItem = MonoMethod(param_count=1, signature='P')

    # # void RequestTeleportMoveToLocation(Vector2 givenLocation, bool useCheck = false)
    # RequestTeleportMoveToLocation = MonoMethod(param_count=2, signature='PB')
    # # Vector2 GetInputVector(bool faceInputVector = true, bool useAimVector = true, bool ignoreZero = true)
    # GetInputVector = MonoMethod(param_count=3, signature='3B')


class GameController(MonoClass):
    # 获取玩家实例
    need_vtable = True
    activePlayers = MonoStaticField(type=MonoArrayT(Player))


class Cooldown(MonoClass):
    # 技能冷却相关
    get_ChargesMissing = MonoMethod(compile=True)
    get_IsCharging = MonoMethod(compile=True)


class CooldownEntry(MonoClass):
    EntryUpdate = MonoMethod(compile=True)


class Main(MonoHacktool):
    CLASS_NAME = 'UnityWndClass'
    WINDOW_NAME = 'Wizard of Legend'

    def __init__(self):
        super().__init__()
        self.controller = None

    def onattach(self):
        super().onattach()
        self.register_classes((NumVarStat, Health, Wallet, Player, GameController, Cooldown, CooldownEntry))

        self.controller = GameController(None, self)
        # self.activePlayers = controller.activePlayers
        # print(hex(Cooldown.get_IsCharging.mono_compile))
        # string = self.call_mono_string_new('ShockTouchBasic')
        # result = self.mono_security_call_1(call_arg(*self.mono_string_length, string, ret_type=int))
        # print(hex(string))

    def render_main(self):
        with Group("player", "全局", None):
            self.render_global()
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

    def render_assembly_functions(self):
        if not Cooldown.get_ChargesMissing.mono_compile:
            print('需要先加载游戏')
            return False

        super().render_assembly_functions((
            AssemblyItems('无冷却',
                AssemblyItem('no_cooldown', None, b'\x48???\x2B\xC1',
                    Cooldown.get_ChargesMissing.mono_compile, Cooldown.get_ChargesMissing.mono_compile + 0x2d,
                    b'', AssemblyGroup(b'\x89\x46', MemRead(offset=3, size=1), ORIGIN),
                    inserted=True, find_base=False, fuzzy=True),
                AssemblyItem('no_cooldown2', None, b'\x40\x0F\x94\xC0\x48\x0F\xB6\xC0',
                    Cooldown.get_IsCharging.mono_compile, Cooldown.get_IsCharging.mono_compile + 0x58,
                    b'\x90\x90\x30', find_base=False, replace_len=3)),
            AssemblyItem('enhanced_magic_4', '技能连发', b'\x48\x83\xEC\x20\x48\x8B??????????\x48\x83\xC4\x20\x4C\x8B\xC0',
                CooldownEntry.EntryUpdate.mono_compile, CooldownEntry.EntryUpdate.mono_compile + 0x141,
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
        # 存在BUG
        return self.activePlayer.GetSkill(self.call_mono_string_new(skill))

    def PickUpSkill(self, skill):
        """给予技能"""
        self.activePlayer.PickUpSkill(self.call_mono_string_new(skill), True, True)

    def GiveItem(self, item):
        """给予物品"""
        self.activePlayer.GiveDesignatedItem(self.call_mono_string_new(item))
