from lib.hack.forms import (
    Group, StaticGroup
)
from lib.hack.handlers import MemHandler
from tools.base.assembly_hacktool import AssemblyItem
from tools.base.mono_hacktool import MonoHacktool, call_arg
from tools.base.mono_models import MonoClass, MonoField, MonoStaticField, MonoArrayT
from fefactory_api import ui
# from . import models, datasets


class Player(MonoClass):
    pass


class GameController(MonoClass):
    need_vtable = True
    activePlayers = MonoStaticField(type=MonoArrayT(Player))


class Main(MonoHacktool):
    CLASS_NAME = 'UnityWndClass'
    WINDOW_NAME = 'Wizard of Legend'

    def onattach(self):
        super().onattach()
        self.register_classes((GameController, Player))

        controller = GameController(None, self)
        activePlayers = controller.activePlayers.value[0]
        print('activePlayers', hex(activePlayers.mono_object))

    def render_main(self):
        Group("player", "全局", None)
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_functions)

    def render_assembly_functions(self):
        functions = (

        )
        super().render_assembly_functions(functions)
