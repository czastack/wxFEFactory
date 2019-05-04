from lib.hack.forms import (
    Group, StaticGroup
)
from lib.hack.handlers import MemHandler
from tools.base.assembly_hacktool import AssemblyItem
from tools.base.mono_hacktool import MonoHacktool, call_arg, call_arg_int64
from fefactory_api import ui
# from . import models, datasets


class Main(MonoHacktool):
    CLASS_NAME = 'UnityWndClass'
    WINDOW_NAME = 'ICEY'

    def onattach(self):
        super().onattach()

        context_array = self.context_array
        PlayerAttribute, UIDataBind = self.native_call_n((
            call_arg_int64(*self.mono_class_from_name, self.image, "", "PlayerAttribute"),
            call_arg_int64(*self.mono_class_from_name, self.image, "", "UIDataBind"),
        ), context_array)

        set_currentEnergy, set_currentHP, UpdateCharInfo = self.native_call_n((
            call_arg_int64(*self.mono_class_get_method_from_name, PlayerAttribute, "set_currentEnergy", 1),
            call_arg_int64(*self.mono_class_get_method_from_name, PlayerAttribute, "set_currentHP", 1),
            call_arg_int64(*self.mono_class_get_method_from_name, UIDataBind, "UpdateCharInfo", 0),
        ), context_array)

        (
            _, _,
            self.set_currentEnergy_native,
            self.set_currentHP_native,
            self.UpdateCharInfo_native,
        ) = self.native_call_n((
            call_arg(*self.mono_thread_attach, self.root_domain),
            call_arg(*self.mono_security_set_mode, 0),
            call_arg_int64(*self.mono_compile_method, set_currentEnergy),
            call_arg_int64(*self.mono_compile_method, set_currentHP),
            call_arg_int64(*self.mono_compile_method, UpdateCharInfo),
        ), context_array)

    def render_main(self):
        Group("player", "全局", None)
        self.lazy_group(StaticGroup("代码插入"), self.render_assembly_functions)

    def render_assembly_functions(self):
        functions = (
            AssemblyItem('unlimited_health', '无限生命', b'\x89\x47\x20\x48\x8B\x7D\xF8',
                self.set_currentHP_native, self.set_currentHP_native + 0x100,
                b'', b'\x8B\x47\x1C\x89\x47\x20\x48\x8B\x7D\xF8',
                inserted=True, find_base=False),
            AssemblyItem('unlimited_energy', '无限能量', b'\x89\x47\x28\x48\x8B\x7D\xF8',
                self.set_currentEnergy_native, self.set_currentEnergy_native + 0x100,
                b'', b'\x8B\x47\x24\x89\x47\x28\x48\x8B\x7D\xF8',
                inserted=True, find_base=False),
            AssemblyItem('unlimited_money', '无限金钱', b'\x48\x63\x49\x10\x3B\xC1',
                self.UpdateCharInfo_native + 0x200, self.UpdateCharInfo_native + 0x400,
                b'', b'\xC7\x41\x10\x9F\x86\x01\x00\x48\x63\x49\x10\x39\xC8',
                replace_len=6, inserted=True, find_base=False),
        )
        super().render_assembly_functions(functions)
