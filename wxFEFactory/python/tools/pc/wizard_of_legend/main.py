from lib.hack.forms import (
    Group, StaticGroup
)
from lib.hack.handlers import MemHandler
from tools.base.assembly_hacktool import AssemblyItem
from tools.base.mono_hacktool import MonoHacktool, call_arg
from fefactory_api import ui
# from . import models, datasets


class Main(MonoHacktool):
    CLASS_NAME = 'UnityWndClass'
    WINDOW_NAME = 'Wizard of Legend'

    def onattach(self):
        super().onattach()
        GameController, Player = self.get_global_mono_classes((
            "GameController",
            "Player",
        ))

        # activePlayers, enemies, bosses, totalGold

        (
            GameController_vtable,
            activePlayers,
        ) = self.native_call_n((
            self.call_arg_int(*self.mono_class_vtable, self.root_domain, GameController),
            self.call_arg_int(*self.mono_class_get_field_from_name, GameController, "activePlayers"),
        ), self.context_array)

        self.native_call_n((
            call_arg(*self.mono_field_static_get_value, GameController_vtable, activePlayers,
                self.native_context.get_temp_addr()),
        ), self.context_array)

        print('activePlayers', hex(self.native_context.get_temp_addr()))

    def render_main(self):
        Group("player", "全局", None)
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_functions)

    def render_assembly_functions(self):
        functions = (

        )
        super().render_assembly_functions(functions)
