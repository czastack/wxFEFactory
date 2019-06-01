from lib.hack.forms import (
    Group, StaticGroup
)
from lib.hack.handlers import MemHandler
from lib.win32.keys import VK
from tools.base.assembly_hacktool import AssemblyItem, AssemblyItems, VariableType
from tools.base.mono_hacktool import MonoHacktool, call_arg
from tools.base.mono_models import MonoClass, MonoField, MonoStaticField, MonoArrayT, MonoProperty, MonoMethod
from tools.base.assembly_code import AssemblyGroup, MemRead, Variable, ORIGIN
from fefactory_api import ui
# from . import models, datasets


class Player(MonoClass):
    OverdriveProgress = MonoProperty(type=float)


class GameController(MonoClass):
    need_vtable = True
    activePlayers = MonoStaticField(type=MonoArrayT(Player))


class Cooldown(MonoClass):
    get_ChargesMissing = MonoMethod(compile=True)
    get_IsCharging = MonoMethod(compile=True)


class CooldownEntry(MonoClass):
    EntryUpdate = MonoMethod(compile=True)


class Main(MonoHacktool):
    CLASS_NAME = 'UnityWndClass'
    WINDOW_NAME = 'Wizard of Legend'

    def __init__(self):
        super().__init__()
        self.activePlayers = None

    def onattach(self):
        super().onattach()
        self.register_classes((GameController, Player, Cooldown, CooldownEntry))

        controller = GameController(None, self)
        self.activePlayers = controller.activePlayers.value
        # print(hex(Cooldown.get_IsCharging.mono_compile))

    def render_main(self):
        Group("player", "全局", None)
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_functions)

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

    def get_hotkeys(self):
        return (
            (0, VK.CAPSLOCK, self.overdrive),
        )

    @property
    def activePlayer(self):
        return self.activePlayers and self.activePlayers[0]

    def overdrive(self):
        player = self.activePlayer
        if player:
            player.OverdriveProgress.value = 100.0
