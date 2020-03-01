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
        self.StarBox = None

    def onattach(self):
        super().onattach()
        self.register_classes((
            models.GirlData,
            models.GameTool,
            models.Role,
            models.Enemy,
            models.Player,
            models.StarBox,
        ))

        self.GameTool = models.GameTool(0, self)
        self.StarBox = models.StarBox(0, self)

    def render_main(self):
        roleData = (self._roleData, models.GirlData)

        with Group(None, "全局", roleData):
            self.render_global()
        self.lazy_group(Group(None, "玩家", (self._player, models.Player)), self.render_player)
        self.lazy_group(Group(None, "敌人", (self._enemy, models.Enemy)), self.render_enemy)

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

    def render_role(self):
        ModelInput('CurHP')
        ModelInput('MaxHP')
        ModelInput('OrgPhysicAtk')
        ModelInput('OrgMagicAtk')
        ModelInput('OrgPhysicDef')
        ModelInput('OrgMagicDef')
        ModelInput('PhysicAtk')
        ModelInput('MagicAtk')
        ModelInput('PhysicDef')
        ModelInput('MagicDef')
        ModelInput('CureRate')
        ModelInput('VampireRate')

    def render_player(self):
        self.render_role()
        ModelInput('CurRage')
        ModelInput('MaxRage')
        ModelInput('CureAtk')
        ModelInput('RageAtk')
        ModelInput('RageRate')
        ModelInput('RageLocked')

    def render_enemy(self):
        self.render_role()
        ModelInput('BrokeClothLevel')

    def _roleData(self):
        return self.GameTool.roleData

    roleData = property(_roleData)

    def _player(self):
        return self.StarBox.Instance.Player

    player = property(_player)

    def _enemy(self):
        return self.StarBox.Instance.Enemy

    enemy = property(_enemy)
