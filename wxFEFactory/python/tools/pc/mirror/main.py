from lib import ui
from lib.hack.forms import (
    Group, StaticGroup, ModelInput, ModelAddrInput, ProxyInput, Title
)
from lib.hack.utils import Descriptor
from lib.win32.keys import VK
from tools.base.assembly_code import AssemblyGroup, MemRead, ORIGIN
from tools.base.assembly_hacktool import AssemblyItem, AssemblyItems, Delta
from tools.base.mono_hacktool import MonoHacktool
from . import models, datasets


class Main(MonoHacktool):
    CLASS_NAME = 'UnityWndClass'
    WINDOW_NAME = 'Mirror'

    def __init__(self):
        super().__init__()
        self.GameTool = None

    def onattach(self):
        super().onattach()
        self.register_classes((
            models.GirlData,
            models.GameTool,
        ))

        self.GameTool = models.GameTool(0, self)

    def render_main(self):
        roleData = (self._roleData, models.GirlData)

        with Group(None, "全局", roleData):
            self.render_global()

    def render_global(self):
        ModelInput('Money')
        ModelInput('Hp')
        ModelInput('PhysicAtk')
        ModelInput('MagicAtk')
        ModelInput('CureAtk')
        ModelInput('RageAtk')
        ModelInput('curAbyssLevel')
        ModelInput('curAbyssIndex')
        ModelInput('abyssScore')
        ModelInput('totalAbyssGold')
        ModelInput('playerAbyssScore')
        ModelInput('saveRage')

    def _roleData(self):
        return self.GameTool.roleData

    roleData = property(_roleData)
