from lib.hack.forms import (
    Group, StaticGroup
)
from lib.hack.handlers import MemHandler
from tools.base.assembly_hacktool import AssemblyItem, AssemblyItems
from tools.base.mono_hacktool import MonoHacktool, call_arg
from tools.base.mono_models import MonoClass, MonoField, MonoStaticField, MonoArrayT, MonoMethod
from tools.base.assembly_code import AssemblyGroup, ORIGIN
from fefactory_api import ui
# from . import models, datasets


class Player(MonoClass):
    pass


class GameController(MonoClass):
    need_vtable = True
    activePlayers = MonoStaticField(type=MonoArrayT(Player))


class Cooldown(MonoClass):
    get_ChargesMissing = MonoMethod(compile=True)
    get_IsCharging = MonoMethod(compile=True)


class Main(MonoHacktool):
    CLASS_NAME = 'UnityWndClass'
    WINDOW_NAME = 'Wizard of Legend'

    def onattach(self):
        super().onattach()
        self.register_classes((GameController, Player, Cooldown))

        # controller = GameController(None, self)
        # activePlayers = controller.activePlayers.value[0]
        # print('activePlayers', hex(activePlayers.mono_object))
        print(hex(Cooldown.get_IsCharging.mono_compile))

    def render_main(self):
        Group("player", "全局", None)
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_functions)

    def render_assembly_functions(self):
        functions = (
            AssemblyItems('无冷却',
                AssemblyItem('no_cooldown', None, b'\x48???\x2B\xC1',
                    Cooldown.get_ChargesMissing.mono_compile, Cooldown.get_ChargesMissing.mono_compile + 0x2d,
                    b'', AssemblyGroup(b'\x89\x46\x38', ORIGIN),
                    inserted=True, find_base=False, fuzzy=True),
                AssemblyItem('no_cooldown2', None, b'\x40\x0F\x94\xC0\x48\x0F\xB6\xC0',
                    Cooldown.get_IsCharging.mono_compile, Cooldown.get_IsCharging.mono_compile + 0x58,
                    b'\x90\x90\x30', find_base=False, replace_len=3)),
        )
        super().render_assembly_functions(functions)
